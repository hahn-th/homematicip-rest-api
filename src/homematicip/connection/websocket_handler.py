import asyncio
import logging
from typing import Any, Callable, List
from urllib.parse import urlparse

import websockets
from websockets.legacy.client import WebSocketClientProtocol

from homematicip.connection import (
    ATTR_AUTH_TOKEN,
    ATTR_CLIENT_AUTH,
    ATTR_ACCESSPOINT_ID,
)
from homematicip.connection.connection_context import ConnectionContext

LOGGER = logging.getLogger(__name__)


class WebsocketHandler:
    """Manages a WebSocket connection to Homematic IP.

    Provides methods for starting, stopping, and processing messages.
    Supports automatic reconnect, adding handlers, and status queries.
    """

    def __init__(self) -> None:
        self.INITIAL_BACKOFF = 8
        self.url = None
        self._stop_event = asyncio.Event()
        self._websocket_connected = asyncio.Event()
        self._reconnect_task: asyncio.Task | None = None
        self._task_lock = asyncio.Lock()
        self._on_message_handlers: List[Callable] = []
        self._on_connected_handler: List[Callable] = []
        self._on_disconnected_handler: List[Callable] = []
        self._on_reconnect_handler: List[Callable] = []

    def add_on_connected_handler(self, handler: Callable) -> None:
        """Add a handler that is called when the connection is established."""
        self._on_connected_handler.append(handler)

    def add_on_disconnected_handler(self, handler: Callable) -> None:
        """Add a handler that is called when the connection is closed."""
        self._on_disconnected_handler.append(handler)

    def add_on_reconnect_handler(self, handler: Callable) -> None:
        """Add a handler that is called when the connection is re-established."""
        self._on_reconnect_handler.append(handler)

    def add_on_message_handler(self, handler: Callable) -> None:
        """Add a handler for incoming messages."""
        self._on_message_handlers.append(handler)

    async def _call_handlers(self, handlers: List[Callable], *args: Any) -> None:
        """Helper function to call handlers (sync and async)."""
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(*args)
                else:
                    handler(*args)
            except Exception as exc:  # pragma: no cover - defensive logging
                handler_name = getattr(handler, "__name__", repr(handler))
                LOGGER.error(
                    "Error in handler '%s': %s",
                    handler_name,
                    exc,
                    exc_info=True,
                )

    async def _connect(self, context: ConnectionContext) -> None:
        """Establish the WebSocket connection and handle automatic reconnects."""
        backoff = self.INITIAL_BACKOFF
        max_backoff = 900

        headers = {
            ATTR_AUTH_TOKEN: context.auth_token,
            ATTR_CLIENT_AUTH: context.client_auth_token,
            ATTR_ACCESSPOINT_ID: context.accesspoint_id,
        }

        # Normalize SSL handling for websockets:
        # - For wss:// without explicit ssl_ctx: use True (system defaults)
        # - For ws:// without explicit ssl_ctx: use None (no TLS)
        # - If context.ssl_ctx is provided, always pass it through.
        parsed = urlparse(context.websocket_url)
        if context.ssl_ctx is not None:
            ssl_ctx = context.ssl_ctx
        else:
            if parsed.scheme == "wss":
                # Respect enforce_ssl flag: if it is False, we deliberately
                # disable certificate verification by passing False here.
                ssl_ctx = True if context.enforce_ssl else False
            else:
                # Plain WS has no TLS; websockets expects ssl=None in this case.
                ssl_ctx = None

        while not self._stop_event.is_set():
            try:
                LOGGER.info("Connect to %s", context.websocket_url)

                async with websockets.connect(
                    context.websocket_url,
                    additional_headers=headers,
                    ping_interval=30,
                    ssl=ssl_ctx,
                ) as ws:  # type: WebSocketClientProtocol
                    backoff = self.INITIAL_BACKOFF
                    self.url = context.websocket_url
                    LOGGER.info(
                        "WebSocket connection established to %s.",
                        context.websocket_url,
                    )
                    self._websocket_connected.set()
                    await self._call_handlers(self._on_connected_handler)
                    await self._listen(ws)

            except asyncio.CancelledError:
                LOGGER.info("WebSocket connect task cancelled.")
                break
            except Exception as exc:  # pragma: no cover - network failure
                self._websocket_connected.clear()
                reason = (
                    f"Websocket lost connection: {exc}. Retry in {backoff}s."
                )
                LOGGER.warning("%s", reason)

                try:
                    await self._call_handlers(self._on_reconnect_handler, reason)
                except Exception as handler_error:  # pragma: no cover
                    LOGGER.error(
                        "Error in reconnect handler: %s",
                        handler_error,
                        exc_info=True,
                    )

                if self._stop_event.is_set():
                    break

                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, max_backoff)
            finally:
                await self._cleanup()

    async def _listen(self, ws: WebSocketClientProtocol) -> None:
        """Listen for incoming WebSocket messages and dispatch them."""
        try:
            async for msg in ws:
                # websockets yields ``str`` for text frames and ``bytes`` for binary
                await self._handle_ws_message(msg)
        except asyncio.CancelledError:
            LOGGER.info("WebSocket listener cancelled.")
            raise
        except websockets.ConnectionClosed as exc:  # pragma: no cover
            LOGGER.info(
                "WebSocket connection closed: code=%s reason=%s",
                getattr(exc.rcvd, "code", None),
                getattr(exc.rcvd, "reason", None),
            )
        except Exception as exc:  # pragma: no cover - defensive
            LOGGER.error("Error in websocket listener: %s", exc, exc_info=True)

    async def _handle_ws_message(self, message: Any) -> None:
        """Dispatch a single WebSocket message to registered handlers."""
        try:
            await self._call_handlers(self._on_message_handlers, message)
        except Exception as exc:  # pragma: no cover - defensive
            LOGGER.error("Error handling message: %s", exc, exc_info=True)

    async def _cleanup(self) -> None:
        self._websocket_connected.clear()
        await self._call_handlers(self._on_disconnected_handler)

    async def start(self, context: ConnectionContext) -> None:
        async with self._task_lock:
            LOGGER.info("Start websocket client...")
            if self._reconnect_task and not self._reconnect_task.done():
                LOGGER.info("Already connected.")
                return
            self._stop_event.clear()
            self._reconnect_task = asyncio.create_task(self._connect(context))
            self._reconnect_task.add_done_callback(self._handle_task_result)
            LOGGER.info("Connect task started.")

    async def stop(self) -> None:
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

    def _handle_task_result(self, task: asyncio.Task) -> None:
        try:
            task.result()
        except asyncio.CancelledError:
            LOGGER.info("[Task] Reconnect task was cancelled.")
        except Exception as exc:  # pragma: no cover - defensive logging
            LOGGER.error("[Task] Error in reconnect task: %s", exc)

    def is_connected(self) -> bool:
        """Returns True if the WebSocket connection is active."""
        return self._websocket_connected.is_set()
