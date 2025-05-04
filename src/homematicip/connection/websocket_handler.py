import asyncio
import logging
import platform
import signal
import ssl
import sys
from typing import Callable, List

import certifi
from websockets.asyncio.client import connect, ClientConnection
from websockets.exceptions import ConnectionClosed, ConnectionClosedError, InvalidHandshake

from homematicip.connection import ATTR_AUTH_TOKEN, ATTR_CLIENT_AUTH, ATTR_ACCESSPOINT_ID
from homematicip.connection.connection_context import ConnectionContext
from homematicip.exceptions.connection_exceptions import HmipServerCloseError, HmipConnectionError

LOGGER = logging.getLogger(__name__)


class WebSocketHandler:

    def __init__(self):
        self._on_message_handler: List[Callable] = []
        self._stop_event: asyncio.Event = asyncio.Event()
        self._is_connected: bool = False
        self._websocket: ClientConnection | None = None

    def add_on_message_handler(self, handler: Callable):
        self._on_message_handler.append(handler)

    def _set_connection_state(self, connected: bool):
        """Set the connection state."""
        self._is_connected = connected

    async def listen(self, context: ConnectionContext,
                     reconnect_on_error: bool = True):
        try:
            await self._listen_internal(context, reconnect_on_error)
        except (ConnectionClosedError, InvalidHandshake) as e:
            LOGGER.error(f"Connection error while connecting to WebSocket server: {e}")
            raise HmipConnectionError(f"Connection error while connecting to WebSocket server: {e}") from e
        finally:
            # If we reach this point, the connection is closed.
            self._set_connection_state(False)
            self._websocket = None

    async def _listen_internal(self, context: ConnectionContext,
                     reconnect_on_error: bool = True):
        uri = context.websocket_url
        ssl_context = self._get_ssl_context(context)

        self._reset_stop_event()

        LOGGER.info(f"Connecting to WebSocket server at {uri}")
        async with connect(
                uri,
                additional_headers={
                    ATTR_AUTH_TOKEN: context.auth_token,
                    ATTR_CLIENT_AUTH: context.client_auth_token,
                    ATTR_ACCESSPOINT_ID: context.accesspoint_id
                },
                ssl=ssl_context,
                open_timeout=10,
                ping_interval=60,
                ping_timeout=10,
        ) as websocket:
            LOGGER.info("Connected to WebSocket server.")
            self._websocket = websocket
            self._set_connection_state(True)

            if platform.system() != "Windows":
                loop = asyncio.get_running_loop()
                loop.add_signal_handler(signal.SIGINT, lambda x: asyncio.create_task(self._handle_signal(x)),
                                        websocket)

            # Process messages received on the connection.
            async for message in websocket:
                LOGGER.debug(f"Received message: {message}")
                if self._stop_event.is_set():
                    LOGGER.debug("Found stop event.")
                    break
                try:
                    logging.getLogger("websockets").info(message)
                    self._set_connection_state(True)

                    for handler in self._on_message_handler:
                        await handler(message)

                except ConnectionClosed:
                    self._set_connection_state(False)
                    LOGGER.warning(
                        f"Got ConnectionClosed. Should reconnect is set to {reconnect_on_error}"
                    )
                    if not reconnect_on_error:
                        raise HmipServerCloseError()

                    await asyncio.sleep(5)
                    continue

    @staticmethod
    async def _handle_signal(websocket):
        logging.info("Signal received, closing websocket.")
        await websocket.close()

    async def stop_listening_async(self, timeout: int = 5):
        LOGGER.info("Stopping WebSocket connection.")
        self._stop_event.set()
        if self._websocket:
            try:
                await asyncio.wait_for(self._websocket.close(), timeout=timeout)
                LOGGER.debug("WebSocket connection closed successfully.")
            except asyncio.TimeoutError:
                LOGGER.warning(f"Timeout while closing WebSocket connection after {timeout} seconds.")
                self._set_connection_state(False)
                self._websocket = None
            except ConnectionClosedError as e:
                LOGGER.error(f"Connection error while closing WebSocket connection: {e}")
                self._set_connection_state(False)
                self._websocket = None

    def _reset_stop_event(self):
        self._stop_event.clear()

    def is_connected(self):
        """Return the connection state."""
        return self._is_connected

    @staticmethod
    def _get_ssl_context(context: ConnectionContext = None):
        if context.ssl_ctx:
            return context.ssl_ctx

        if hasattr(sys, "_called_from_test"):  # disable ssl during a test run
            return None

        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())
        return ssl_context
