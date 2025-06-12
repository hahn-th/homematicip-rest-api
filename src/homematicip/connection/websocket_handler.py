import asyncio
import logging
from typing import Callable, List

import aiohttp

from homematicip.connection import ATTR_AUTH_TOKEN, ATTR_CLIENT_AUTH, ATTR_ACCESSPOINT_ID
from homematicip.connection.connection_context import ConnectionContext

LOGGER = logging.getLogger(__name__)


class WebsocketHandler:
    """
    Manages a WebSocket connection to Homematic IP and provides methods for starting, stopping, and processing messages.
    Supports automatic reconnect, adding handlers, and status queries.
    """

    def __init__(self):
        self.INITIAL_BACKOFF = 8
        self.url = None
        self._session = None
        self._ws = None
        self._stop_event = asyncio.Event()
        self._reconnect_task = None
        self._task_lock = asyncio.Lock()
        self._on_message_handlers: List[Callable] = []
        self._on_connected_handler: List[Callable] = []
        self._on_disconnected_handler: List[Callable] = []

    def add_on_connected_handler(self, handler: Callable):
        """Adds a handler that is called when the connection is established."""
        self._on_connected_handler.append(handler)

    def add_on_disconnected_handler(self, handler: Callable):
        """Adds a handler that is called when the connection is closed."""
        self._on_disconnected_handler.append(handler)

    def add_on_message_handler(self, handler: Callable):
        """Adds a handler for incoming messages."""
        self._on_message_handlers.append(handler)

    async def _call_handlers(self, handlers, *args):
        """Helper function to call handlers (sync and async)."""
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(*args)
                else:
                    handler(*args)
            except Exception as e:
                handler_name = getattr(handler, "__name__", repr(handler))
                LOGGER.error(f"Error in handler '{handler_name}': {e}", exc_info=True)

    async def _connect(self, context: ConnectionContext):
        backoff = self.INITIAL_BACKOFF
        max_backoff = 1800
        while not self._stop_event.is_set():
            try:
                LOGGER.info(f"Connect to {context.websocket_url}")
                self._session = aiohttp.ClientSession()
                self._ws = await self._session.ws_connect(
                    context.websocket_url,
                    headers={
                        ATTR_AUTH_TOKEN: context.auth_token,
                        ATTR_CLIENT_AUTH: context.client_auth_token,
                        ATTR_ACCESSPOINT_ID: context.accesspoint_id
                    },
                    ssl=getattr(context, 'ssl_ctx', True),
                    heartbeat=30,
                    timeout=aiohttp.ClientTimeout(total=30)
                )
                LOGGER.info(f"WebSocket connection established to {context.websocket_url}.")
                await self._call_handlers(self._on_connected_handler)
                backoff = self.INITIAL_BACKOFF
                await self._listen()
            except Exception as e:
                await self._call_handlers(self._on_disconnected_handler)
                LOGGER.warning(f"Websocket lost connection: {e}. Retry in {backoff:.1f}s.")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, max_backoff)
            finally:
                await self._cleanup()

    async def _listen(self):
        async for msg in self._ws:
            if msg.type in (aiohttp.WSMsgType.TEXT, aiohttp.WSMsgType.BINARY):
                LOGGER.debug(f"Received message {msg.data}")
                await self._call_handlers(self._on_message_handlers, msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                LOGGER.error(f"Error in websocket: {msg}")
                break

    async def _cleanup(self):
        if self._ws:
            if not self._ws.closed:
                await self._ws.close()
            self._ws = None
        if self._session:
            if not self._session.closed:
                await self._session.close()
            self._session = None

        await self._call_handlers(self._on_disconnected_handler)

    async def start(self, context: ConnectionContext):
        async with self._task_lock:
            LOGGER.info("Start websocket client...")
            if self._reconnect_task and not self._reconnect_task.done():
                LOGGER.info("Already connected.")
                return
            self._stop_event.clear()
            self._reconnect_task = asyncio.create_task(self._connect(context))
            self._reconnect_task.add_done_callback(self._handle_task_result)
            LOGGER.info("Connect task started.")

    async def stop(self):
        LOGGER.info("Stop websocket client...")
        self._stop_event.set()
        async with self._task_lock:
            if self._reconnect_task:
                await self._reconnect_task
                self._reconnect_task = None
        await self._cleanup()
        LOGGER.info("[Stop] WebSocket client stopped.")

    def _handle_task_result(self, task: asyncio.Task):
        try:
            task.result()
        except asyncio.CancelledError:
            LOGGER.info("[Task] Reconnect task was cancelled.")
        except Exception as e:
            LOGGER.error(f"[Task] Error in reconnect task: {e}")

    def is_connected(self):
        """Returns True if the WebSocket connection is active."""
        return self._ws is not None and not self._ws.closed
