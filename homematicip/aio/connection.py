import asyncio
import json
import logging
from asyncio import CancelledError
from json.decoder import JSONDecodeError

import aiohttp
import async_timeout
import websockets
from websockets import ConnectionClosed

from homematicip.base.base_connection import (
    ATTR_AUTH_TOKEN,
    ATTR_CLIENT_AUTH,
    BaseConnection,
    HmipConnectionError,
    HmipWrongHttpStatusError,
)

logger = logging.getLogger(__name__)


class AsyncConnection(BaseConnection):
    """Handles async http and websocket traffic."""

    connect_timeout = 20
    ping_timeout = 3
    ping_loop = 60

    def __init__(self, loop, session=None):
        super().__init__()
        self._loop = loop
        if session is None:
            self._websession = aiohttp.ClientSession()
        else:
            self._websession = session
        self.socket_connection = None  # ClientWebSocketResponse
        self.ws_reader_task = None
        self.ping_pong_task = None
        # self.ws_close_lock = Lock()
        self._closing_task = None

    @property
    def ws_connected(self):
        """Websocket is connected."""
        return self.socket_connection is not None

    async def init(
        self,
        accesspoint_id,
        lookup=True,
        lookup_url="https://lookup.homematic.com:48335/getHost",
        **kwargs
    ):
        self.set_token_and_characteristics(accesspoint_id)
        self._lookup_url = lookup_url  # needed for testcases

        if lookup:
            result = await self.api_call(
                lookup_url, json.dumps(self.clientCharacteristics), full_url=True
            )

            self._urlREST = result["urlREST"]
            self._urlWebSocket = result["urlWebSocket"]
        else:  # pragma: no cover
            self._urlREST = "https://ps1.homematic.com:6969"
            self._urlWebSocket = "wss://ps1.homematic.com:8888"

    def _restCall(self, path, body=None):
        """Shadows the original restCalls"""
        return path, body

    def full_url(self, partial_url):
        return "{}/hmip/{}".format(self._urlREST, partial_url)

    async def api_call(self, path, body=None, full_url=False):
        """Make the actual call to the HMIP server.

        Throws `HmipWrongHttpStatusError` or `HmipConnectionError` if connection has failed or
        response is not correct."""
        result = None
        if not full_url:
            path = self.full_url(path)
        for i in range(self._restCallRequestCounter):
            try:
                with async_timeout.timeout(self._restCallTimout):
                    result = await self._websession.post(
                        path, data=body, headers=self.headers
                    )
                    if result.status == 200:
                        if result.content_type == "application/json":
                            ret = await result.json()
                        else:
                            ret = True
                        return ret
                    else:
                        raise HmipWrongHttpStatusError(result.status)
            except (asyncio.TimeoutError, aiohttp.ClientConnectionError):
                # Both exceptions occur when connecting to the server does
                # somehow not work.
                logger.debug("Connection timed out or another error occurred %s" % path)
            except JSONDecodeError as err:
                logger.exception(err)
            finally:
                if result is not None:
                    await result.release()
        raise HmipConnectionError("Failed to connect to HomeMaticIp server")

    async def _connect_to_websocket(self):
        try:
            self.socket_connection = await asyncio.wait_for(
                websockets.connect(
                    self._urlWebSocket,
                    extra_headers={
                        ATTR_AUTH_TOKEN: self._auth_token,
                        ATTR_CLIENT_AUTH: self._clientauth_token,
                    },
                ),
                timeout=self.connect_timeout,
            )
        except asyncio.TimeoutError:
            raise HmipConnectionError("Connecting to hmip ws socket timed out.")
        except Exception as err:
            logger.exception(err)
            raise HmipConnectionError()

    async def ws_connect(self, *, on_message, on_error):
        await self._connect_to_websocket()
        self.ping_pong_task = self._loop.create_task(self._ws_ping_loop())
        self.ws_reader_task = self._loop.create_task(
            self._ws_loop(on_message, on_error)
        )
        return self.ws_reader_task

    async def close_websocket_connection(self, source_is_reading_loop=False):
        if self._closing_task is None or self._closing_task.done():
            self._closing_task = self._loop.create_task(
                self._shut_down(source_is_reading_loop)
            )

    async def _shut_down(self, source_is_reading_loop=False):
        logger.debug("Closing connection")

        if self.ws_reader_task and not source_is_reading_loop:
            self.ws_reader_task.cancel()

        if self.ping_pong_task:
            self.ping_pong_task.cancel()

        if self.ws_connected:
            try:
                await self.socket_connection.close()
            except Exception as err:
                logger.exception(err)
        self.socket_connection = None

    async def _ws_ping_loop(self):
        try:
            while True:
                logger.debug("Sending out ping request.")
                pong_waiter = await self.socket_connection.ping()
                await asyncio.wait_for(pong_waiter, timeout=self.ping_timeout)
                logger.debug("Pong received.")
                await asyncio.sleep(self.ping_loop)
        except CancelledError:
            logger.debug("WS Ping pong task cancelled.")
        except (asyncio.TimeoutError, ConnectionClosed):
            logger.error("No Pong received from server.")
        except Exception as err:
            logger.debug("WS Ping pong task close.")
            logger.exception(err)
        finally:
            await self.close_websocket_connection()

    async def _ws_loop(self, on_message, on_error):
        try:
            while True:
                msg = await self.socket_connection.recv()
                logger.debug("incoming hmip message")
                on_message(None, msg.decode())
        except TypeError:
            logger.error("Problem converting incoming bytes %s", msg)
        except ConnectionClosed:
            logger.debug("Connection closed by server")
        except CancelledError:
            logger.info("Reading task is cancelled.")
        except Exception as err:
            logger.debug("WS Reader task stop.")
            logger.exception(err)
        finally:
            await self.close_websocket_connection(source_is_reading_loop=True)
            await self._closing_task

            raise HmipConnectionError()
