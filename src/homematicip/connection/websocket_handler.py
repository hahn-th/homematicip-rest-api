import ssl
from typing import Callable

import certifi
import websockets

from homematicip.connection.rest_connection import ConnectionContext, ATTR_AUTH_TOKEN, ATTR_CLIENT_AUTH, LOGGER
from homematicip.exceptions.connection_exceptions import HmipServerCloseError


class WebSocketHandler:
    async def listen(self, context: ConnectionContext, connection_state_callback: Callable, reconnect_on_error: bool = True):
        uri = context.websocket_url
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())
        async with websockets.connect(
                uri,
                extra_headers={
                    ATTR_AUTH_TOKEN: context.auth_token,
                    ATTR_CLIENT_AUTH: context.client_auth_token,
                },
                ssl=ssl_context,
        ) as websocket:
            # Process messages received on the connection.
            async for message in websocket:
                try:
                    if connection_state_callback is not None:
                        connection_state_callback(True)
                    yield message

                except websockets.ConnectionClosed:
                    if connection_state_callback is not None:
                        connection_state_callback(False)
                    LOGGER.warn(
                        f"Got ConnectionClosed Exception. Should reconnect is set to {reconnect_on_error}"
                    )
                    if not reconnect_on_error:
                        raise HmipServerCloseError()

                    continue

        # If we reach this point, the connection is closed.
        connection_state_callback(False)
