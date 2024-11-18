import asyncio
import logging
import signal
import ssl
import sys
from typing import Callable

import certifi
from websockets import connect
from websockets.exceptions import ConnectionClosed

from homematicip.connection_v2 import ATTR_AUTH_TOKEN, ATTR_CLIENT_AUTH
from homematicip.connection_v2.connection_context import ConnectionContext
from homematicip.exceptions.connection_exceptions import HmipServerCloseError

LOGGER = logging.getLogger(__name__)


class WebSocketHandler:

    def __init__(self):
        self._on_message_handler = []
        self._stop_event = asyncio.Event()
        self._is_connected: bool = False
        self._websocket = None

    def add_on_message_handler(self, handler: Callable):
        self._on_message_handler.append(handler)

    def _set_connection_state(self, connected):
        self._is_connected = connected

    async def listen(self, context: ConnectionContext,
                     reconnect_on_error: bool = True):
        uri = context.websocket_url
        ssl_context = self._get_ssl_context()

        self._reset_stop_event()

        async with connect(
                uri,
                additional_headers={
                    ATTR_AUTH_TOKEN: context.auth_token,
                    ATTR_CLIENT_AUTH: context.client_auth_token,
                },
                ssl=ssl_context,
        ) as websocket:
            LOGGER.info("Connected to WebSocket server.")
            # Close the connection when receiving SIGTERM.
            self._websocket = websocket
            loop = asyncio.get_running_loop()
            loop.add_signal_handler(signal.SIGTERM, loop.create_task, websocket.close())

            # Process messages received on the connection.
            async for message in websocket:
                LOGGER.debug(f"Received message: {message}")
                if self._stop_event.is_set():
                    break
                try:
                    logging.getLogger("websockets").info(message)
                    self._set_connection_state(True)

                    for handler in self._on_message_handler:
                        await handler(message)

                except ConnectionClosed:
                    self._set_connection_state(False)
                    LOGGER.warning(
                        f"Got ConnectionClosed Exception. Should reconnect is set to {reconnect_on_error}"
                    )
                    if not reconnect_on_error:
                        raise HmipServerCloseError()

                    await asyncio.sleep(5)

                    continue

        # If we reach this point, the connection is closed.
        self._set_connection_state(False)
        self._websocket = None

    def stop_listening(self):
        LOGGER.info("Stopping WebSocket connection.")
        if self._websocket:
            self._websocket.close()
        self._stop_event.set()

    def _reset_stop_event(self):
        self._stop_event.clear()

    def is_connected(self):
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
