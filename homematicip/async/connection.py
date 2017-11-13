import json
import logging
from asyncio.futures import CancelledError
from json.decoder import JSONDecodeError

import aiohttp
import async_timeout
import asyncio

from homematicip.base.base_connection import BaseConnection, \
    HmipWrongHttpStatusError, ATTR_AUTH_TOKEN, ATTR_CLIENT_AUTH, \
    HmipConnectionError

logger = logging.getLogger(__name__)


class AsyncConnection(BaseConnection):
    def __init__(self, loop,session=None):
        super().__init__()
        self._loop = loop
        if session is None:
            self._websession = aiohttp.ClientSession(loop=loop)
        else:
            self._websession=session
        self.socket_connection = None  # ClientWebSocketResponse
        self._socket_task = None

    async def init(self, accesspoint_id, lookup=True, **kwargs):
        self.set_token_and_characteristics(accesspoint_id)

        if lookup:
            result = await self.api_call(
                "https://lookup.homematic.com:48335/getHost",
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
        result = None
        if not full_url:
            path = self.full_url(path)
        for i in range(self._restCallRequestCounter):
            try:
                with async_timeout.timeout(self._restCallTimout,
                                           loop=self._loop):
                    result = await self._websession.post(
                        path,
                        data=body,
                        headers=self.headers
                    )
                    if result.status == 200:
                        if result.content_type == 'application/json':
                            ret = await result.json()
                        else:
                            ret = True
                        return ret
                    else:
                        raise HmipWrongHttpStatusError
            except (asyncio.TimeoutError, ConnectionError):
                logger.debug(
                    "Connection timed out or another error occurred %s" % path)
            except JSONDecodeError as err:
                logger.exception(err)
                break
            finally:
                if result is not None:
                    await result.release()
        raise HmipConnectionError("Failed to connect to HomeMaticIp server")

    def listen_for_websocket_data(self, incoming_parser):
        self._socket_task = self._loop.create_task(
            self._listen_for_incoming_websocket_data(incoming_parser))

    async def _connect_to_websocket(self):
        self.socket_connection = await self._websession.ws_connect(
            self._urlWebSocket,
            headers={ATTR_AUTH_TOKEN: self._auth_token,
                     ATTR_CLIENT_AUTH: self._clientauth_token},
            heartbeat=120,
            timeout=3
        )

    def close_websocket_connection(self):
        self._socket_task.cancel()

    async def _listen_for_incoming_websocket_data(self, incoming_parser):
        """Creates a websocket connection, listens for incoming data and
        uses the incoming parser to parse the incoming data.
        """

        try:
            while True:
                for i in range(self._restCallRequestCounter):
                    try:
                        await self._connect_to_websocket()
                        break
                    except TimeoutError:
                        logger.info('websocket connection timed-out.')

                        await asyncio.sleep(i ** 2)
                else:
                    # exit while loop without break. Raising error.
                    raise ConnectionError(
                        "Problem connecting to hmip websocket connection")

                logger.info('Connected to HMIP websocket.')
                try:
                    while not self.socket_connection.closed:
                        msg = await self.socket_connection.receive()
                        if msg.tp == aiohttp.WSMsgType.BINARY:
                            message = str(msg.data,'utf-8')
                            incoming_parser(None,message)
                except Exception as e:
                    logger.exception(e)
                    await asyncio.sleep(3)
        except CancelledError:
            logger.debug('stopping websocket incoming listener')
            self._loop.create_task(self.socket_connection.close())