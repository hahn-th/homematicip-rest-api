import asyncio
import inspect
import logging
import time
from collections.abc import Callable

import aiohttp
from aiohttp import WSMessage

from homematicip.connection import (
    ATTR_ACCESSPOINT_ID,
    ATTR_AUTH_TOKEN,
    ATTR_CLIENT_AUTH,
)
from homematicip.connection.connection_context import ConnectionContext

LOGGER = logging.getLogger(__name__)


class WebsocketHandler:
    """
    Manages a WebSocket connection to Homematic IP and provides methods for starting, stopping, and processing messages.
    Supports automatic reconnect, adding handlers, and status queries.
    """

    def __init__(self):
        self.INITIAL_BACKOFF = 8
        self.MAX_BACKOFF = 900
        self.HEARTBEAT_INTERVAL = 30
        self.CONNECT_TIMEOUT = 30
        self.MESSAGE_STALE_TIMEOUT = 28800
        self.url = None
        self._stop_event = asyncio.Event()
        self._websocket_connected = asyncio.Event()
        self._reconnect_task = None
        self._task_lock = asyncio.Lock()
        self._last_message_time: float | None = None
        self._message_count = 0
        self._disconnect_notified = True
        self._reconnect_attempt_count = 0
        self._last_disconnect_reason: str | None = None
        self._on_message_handlers: list[Callable] = []
        self._on_connected_handler: list[Callable] = []
        self._on_disconnected_handler: list[Callable] = []
        self._on_reconnect_handler: list[Callable] = []

    def add_on_connected_handler(self, handler: Callable):
        """Adds a handler that is called when the connection is established."""
        self._on_connected_handler.append(handler)

    def add_on_disconnected_handler(self, handler: Callable):
        """Adds a handler that is called when the connection is closed."""
        self._on_disconnected_handler.append(handler)

    def add_on_reconnect_handler(self, handler: Callable):
        """Adds a handler that is called when the connection is re-established."""
        self._on_reconnect_handler.append(handler)

    def add_on_message_handler(self, handler: Callable):
        """Adds a handler for incoming messages."""
        self._on_message_handlers.append(handler)

    async def _call_handlers(self, handlers, *args):
        """Helper function to call handlers (sync and async)."""
        for handler in handlers:
            try:
                if inspect.iscoroutinefunction(handler):
                    await handler(*args)
                else:
                    handler(*args)
            except Exception as e:
                handler_name = getattr(handler, "__name__", repr(handler))
                LOGGER.error(f"Error in handler '{handler_name}': {e}", exc_info=True)

    async def _connect(self, context: ConnectionContext):
        backoff = self.INITIAL_BACKOFF
        while not self._stop_event.is_set():
            try:
                LOGGER.info(f"Connect to {context.websocket_url}")

                async with aiohttp.ClientSession() as session:
                    ws = await asyncio.wait_for(
                        session.ws_connect(
                            context.websocket_url,
                            headers={
                                ATTR_AUTH_TOKEN: context.auth_token,
                                ATTR_CLIENT_AUTH: context.client_auth_token,
                                ATTR_ACCESSPOINT_ID: context.accesspoint_id
                            },
                            heartbeat=self.HEARTBEAT_INTERVAL,
                            ssl=getattr(context, 'ssl_ctx', True),
                        ),
                        timeout=self.CONNECT_TIMEOUT,
                    )
                    async with ws:
                        backoff = self.INITIAL_BACKOFF
                        self._reconnect_attempt_count = 0
                        LOGGER.info(f"WebSocket connection established to {context.websocket_url}.")
                        self._websocket_connected.set()
                        self._disconnect_notified = False
                        await self._call_handlers(self._on_connected_handler)
                        await self._listen(ws)

            except TimeoutError:
                reason = (
                    f"Websocket connect timed out after {self.CONNECT_TIMEOUT}s. "
                    f"Retry in {backoff}s."
                )
                await self._handle_reconnect(reason)
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, self.MAX_BACKOFF)
            except Exception as e:
                reason = f"Websocket lost connection: {e}. Retry in {backoff}s."
                await self._handle_reconnect(reason)
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, self.MAX_BACKOFF)
            finally:
                await self._cleanup()


    async def _listen(self, ws):
        while not self._stop_event.is_set():
            try:
                msg = await asyncio.wait_for(
                    ws.receive(),
                    timeout=self.MESSAGE_STALE_TIMEOUT,
                )
            except TimeoutError:
                reason = (
                    "No HomematicIP websocket events received for "
                    f"{self.MESSAGE_STALE_TIMEOUT} seconds despite an open connection. "
                    "Forcing reconnect as a stale-connection safety net."
                )
                LOGGER.warning(reason)
                await ws.close(
                    code=aiohttp.WSCloseCode.GOING_AWAY,
                    message=b"Stale connection safety net",
                )
                self._last_disconnect_reason = reason
                break

            if msg.type in (aiohttp.WSMsgType.TEXT, aiohttp.WSMsgType.BINARY):
                self._last_message_time = time.monotonic()
                self._message_count += 1
                await self._handle_ws_message(msg)
            elif msg.type in (aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSED):
                LOGGER.info("WebSocket closed by server.")
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                LOGGER.error("Error in websocket: %s", msg)
                break

    async def _handle_ws_message(self, message: WSMessage):
        try:
            await self._call_handlers(self._on_message_handlers, message.data)
        except Exception as e:
            LOGGER.error(f"Error handling message: {e}", exc_info=True)

    async def _cleanup(self):
        if self._disconnect_notified:
            return
        self._disconnect_notified = True
        self._websocket_connected.clear()
        await self._call_handlers(self._on_disconnected_handler)

    async def _handle_reconnect(self, reason: str):
        self._websocket_connected.clear()
        self._reconnect_attempt_count += 1
        self._last_disconnect_reason = reason
        LOGGER.warning(reason)

        try:
            await self._call_handlers(self._on_reconnect_handler, reason)
        except Exception as handler_error:
            LOGGER.error(f"Error in reconnect handler: {handler_error}", exc_info=True)

    def _apply_context_settings(self, context: ConnectionContext):
        self.HEARTBEAT_INTERVAL = context.websocket_heartbeat_interval
        self.CONNECT_TIMEOUT = context.websocket_connect_timeout
        self.MESSAGE_STALE_TIMEOUT = context.websocket_message_stale_timeout
        self.INITIAL_BACKOFF = context.websocket_initial_backoff
        self.MAX_BACKOFF = context.websocket_max_backoff

    async def start(self, context: ConnectionContext):
        async with self._task_lock:
            LOGGER.info("Start websocket client...")
            if self.is_running():
                LOGGER.info("WebSocket client is already running.")
                return
            self._apply_context_settings(context)
            self._stop_event.clear()
            self._reconnect_task = asyncio.create_task(self._connect(context))
            self._reconnect_task.add_done_callback(self._handle_task_result)
            LOGGER.info("Connect task started.")

    async def stop(self):
        LOGGER.info("Stop websocket client...")
        self._stop_event.set()
        async with self._task_lock:
            if self._reconnect_task and not self._reconnect_task.done():
                self._reconnect_task.cancel()
                try:
                    await self._reconnect_task
                except asyncio.CancelledError:
                    pass

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
        return self._websocket_connected.is_set()

    def is_running(self) -> bool:
        """Returns True if the reconnect loop is currently running."""
        return self._reconnect_task is not None and not self._reconnect_task.done()

    def last_message_time(self) -> float | None:
        """Returns the loop timestamp of the last received WebSocket message."""
        return self._last_message_time

    def message_count(self) -> int:
        """Returns the number of WebSocket messages received in this session."""
        return self._message_count

    def seconds_since_last_message(self) -> float | None:
        """Returns the seconds since the last WebSocket message was received."""
        if self._last_message_time is None:
            return None
        return time.monotonic() - self._last_message_time

    def reconnect_attempt_count(self) -> int:
        """Returns the number of reconnect attempts in the current outage."""
        return self._reconnect_attempt_count

    def last_disconnect_reason(self) -> str | None:
        """Returns the last recorded disconnect or reconnect reason."""
        return self._last_disconnect_reason
