import json
import logging
from asyncio.futures import CancelledError
from json.decoder import JSONDecodeError

import aiohttp
from aiohttp import ClientError
from aiohttp.http_exceptions import HttpProcessingError
import async_timeout
import asyncio

from homematicip.base.base_connection import BaseConnection, HmipWrongHttpStatusError, \
    ATTR_AUTH_TOKEN, ATTR_CLIENT_AUTH, HmipConnectionError, HmipServerCloseError

logger = logging.getLogger(__name__)


class AsyncConnection(BaseConnection):
    """Handles async http and websocket traffic."""
    reconnect_timeout = 120
    heartbeat = 2

    def __init__(self, loop, session=None):
        super().__init__()
        self._loop = loop
        if session is None:
            self._websession = aiohttp.ClientSession(loop=loop)
        else:
            self._websession = session
        self.socket_connection = None  # ClientWebSocketResponse
        self.ws_reader_task = None

    @property
    def ws_connected(self):
        """Websocket is connected."""
        return self.socket_connection is not None

    async def init(self, accesspoint_id, lookup=True, **kwargs):
        self.set_token_and_characteristics(accesspoint_id)

        if lookup:
            result = await self.api_call("https://lookup.homematic.com:48335/getHost",
                                         json.dumps(self.clientCharacteristics), full_url=True)

            self._urlREST = result["urlREST"]
            self._urlWebSocket = result["urlWebSocket"]
        else:
            self._urlREST = "https://ps1.homematic.com:6969"
            self._urlWebSocket = "wss://ps1.homematic.com:8888"

    def _restCall(self, path, body=None):
        """Shadows the original restCalls"""
        return path, body

    def full_url(self, partial_url):
        return '{}/hmip/{}'.format(self._urlREST, partial_url)

    async def api_call(self, path, body=None, full_url=False):
        """Make the actual call to the HMIP server.

        Throws `HmipWrongHttpStatusError` or `HmipConnectionError` if connection has failed or
        response is not correct."""
        result = None
        if not full_url:
            path = self.full_url(path)
        for i in range(self._restCallRequestCounter):
            try:
                with async_timeout.timeout(self._restCallTimout,
                                           loop=self._loop):
                    result = await self._websession.post(path, data=body, headers=self.headers)
                    if result.status == 200:
                        if result.content_type == 'application/json':
                            ret = await result.json()
                        else:
                            ret = True
                        return ret
                    else:
                        raise HmipWrongHttpStatusError
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

    # def listen_for_websocket_data(self, incoming_parser):
    #     self._socket_task = self._loop.create_task(
    #         self._listen_for_incoming_websocket_data(incoming_parser))

    async def _connect_to_websocket(self):
        try:
            with async_timeout.timeout(self._restCallTimout, loop=self._loop):
                self.socket_connection = await self._websession.ws_connect(
                    self._urlWebSocket,
                    headers={
                        ATTR_AUTH_TOKEN: self._auth_token,
                        ATTR_CLIENT_AUTH: self._clientauth_token},
                    heartbeat=self.heartbeat
                )
        except (asyncio.TimeoutError, aiohttp.ClientConnectionError)as err:
            raise HmipConnectionError(err)

    async def ws_connect(self, incoming_parser):
        await self._connect_to_websocket()
        self.ws_reader_task = self._loop.create_task(self._ws_loop(incoming_parser))
        return self.ws_reader_task

    # async def close_websocket_connection(self):
    #     if not self.ws_connected:
    #         return
    #     #with asyncio.wait_for()
    #     val = await self.socket_connection.close()
    #     logger.debug("Socket close message sent.")
    #     self.socket_connection = None

    @asyncio.coroutine
    def close_websocket_connection(self):
        if not self.ws_connected:
            return
        self.ws_reader_task.cancel()
        yield from self.socket_connection.close()
        self.socket_connection = None

    # async def _ws_connect(self, incoming_parser):
    #     """Creates a websocket connection, listens for incoming data and
    #     uses the incoming parser to parse the incoming data.
    #     """
    #             try:
    #                 await self._connect_to_websocket()
    #                 break
    #             except (asyncio.TimeoutError,
    #                     aiohttp.ClientConnectionError):
    #                 logger.warning(
    #                     'websocket connection timed-out. or other connection error occurred.')
    #                 await asyncio.sleep(self._restCallTimout)
    #         else:
    #             # exit while loop without break. Raising error which
    #             # should be handled by user.
    #             raise HmipConnectionError("Problem connecting to hmip websocket connection")
    #
    #         logger.info('Connected to HMIP websocket.')

    async def _ws_loop(self, incoming_parser):
        try:
            while True:
                async for msg in self.socket_connection:
                    logger.debug(msg)
                    if msg.tp == aiohttp.WSMsgType.BINARY:
                        message = str(msg.data, 'utf-8')
                        incoming_parser(None, message)
                    elif msg.tp in [aiohttp.WSMsgType.CLOSE,
                                    aiohttp.WSMsgType.CLOSED,
                                    aiohttp.WSMsgType.ERROR]:
                        raise HmipServerCloseError("Server closed. close code: %s", self.socket_connection.close_code)
        except (ClientError, HttpProcessingError) as err:
            raise HmipConnectionError(err)
        except CancelledError:
            return
        finally:
            await self.close_websocket_connection()
