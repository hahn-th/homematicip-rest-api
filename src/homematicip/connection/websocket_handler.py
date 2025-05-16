import asyncio
import logging
from typing import Callable, List

import aiohttp

from homematicip.connection import ATTR_AUTH_TOKEN, ATTR_CLIENT_AUTH, ATTR_ACCESSPOINT_ID
from homematicip.connection.connection_context import ConnectionContext

LOGGER = logging.getLogger(__name__)


class WebsocketHandler:
    """
    This class manages a WebSocket connection to Homematic IP and provides methods for starting, stopping, and processing messages.
    It supports automatic reconnect, adding message handlers, and checking the connection status.
    """

    def __init__(self):
        """
        Initialize the WebsocketHandler with default values and empty handler lists.
        """
        self.url = None
        self._session = None
        self._ws = None
        self._stop_event = asyncio.Event()
        self._reconnect_task = None
        self._task_lock = asyncio.Lock()
        self._on_message_handlers: List[Callable] = []

    def add_on_message_handler(self, handler: Callable):
        """
        Add a handler that will be called for incoming messages.
        The handler must be a function or coroutine accepting one argument (the message).
        """
        self._on_message_handlers.append(handler)

    async def _connect(self, context: ConnectionContext):
        """
        Establish the WebSocket connection and automatically try to reconnect on connection loss.
        Uses connection data from the provided ConnectionContext.
        """
        backoff = 1
        max_backoff = 900

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
                    ssl=context.ssl_ctx if hasattr(context, 'ssl_ctx') else True,
                    heartbeat=30,
                    timeout=aiohttp.ClientTimeout(total=60)
                )

                LOGGER.info(f"WebSocket connection established to {context.websocket_url}.")
                backoff = 1

                await self._listen()

            except Exception as e:
                LOGGER.error(f"[Error] Websocket lost connection: {e}. Retry in {backoff:.1f}s.")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, max_backoff)

            finally:
                await self._cleanup()

    async def _listen(self):
        """
        Listen for incoming messages and call all registered handlers asynchronously.
        Terminates on WebSocket errors.
        """
        async for msg in self._ws:
            if msg.type == aiohttp.WSMsgType.TEXT or msg.type == aiohttp.WSMsgType.BINARY:
                LOGGER.debug(f"Received message {msg.data}")
                for handler in self._on_message_handlers:
                    try:
                        await handler(msg.data)
                    except Exception as e:
                        LOGGER.error(f"Error while handling message: {e}")
            elif msg.type == aiohttp.WSMsgType.ERROR:
                LOGGER.error(f"Error in websocket: {msg}")
                break

    async def _cleanup(self):
        """
        Close WebSocket and session, set internal references to None.
        """
        if self._ws:
            await self._ws.close()
            self._ws = None
        if self._session:
            await self._session.close()
            self._session = None

    async def start(self, context: ConnectionContext):
        """
        Start the connection in the background if not already connected.
        """
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
        """
        Stop the WebSocket connection and wait for the background task to finish.
        """
        LOGGER.info("Stop websocket client...")
        self._stop_event.set()

        async with self._task_lock:
            if self._reconnect_task:
                await self._reconnect_task
                self._reconnect_task = None

        await self._cleanup()
        LOGGER.info("[Stop] WebSocket client stopped.")

    def _handle_task_result(self, task: asyncio.Task):
        """
        Callback for error handling of the background task. Logs errors or cancellations.
        """
        try:
            task.result()
        except asyncio.CancelledError:
            LOGGER.info("[Task] Reconnect task was cancelled.")
        except Exception as e:
            LOGGER.error(f"[Task] Error in reconnect task: {e}")

    def is_connected(self):
        """
        Returns True if the WebSocket connection is active and not closed.
        """
        return self._ws is not None and not self._ws.closed
