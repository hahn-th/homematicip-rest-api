# coding=utf-8
import json
import platform
import locale
import logging
import hashlib
from json.decoder import JSONDecodeError

import aiohttp
import asyncio
from asyncio.futures import CancelledError

import async_timeout
from aiohttp.client_exceptions import ClientResponseError
from aiohttp.client_ws import ClientWebSocketResponse

_LOGGER = logging.getLogger(__name__)

INIT_RETRIES = 3
WEBSOCKET_RETRIES = 3


class Connection:
    _restCallRequestCounter = 3  # the homematic ip cloud tends to time out. retry the call X times.
    _restCallTimout = 5

    def __init__(self, loop, auth_token, access_point_id):
        self._loop = loop
        self._websession = aiohttp.ClientSession(loop=loop)

        # accesspoint_id = accesspoint_id.replace('-', '').upper()

        self._clientCharacteristics = {"clientCharacteristics":
            {
                "apiVersion": "10",
                "applicationIdentifier": "homematicip-python",
                "applicationVersion": "1.0",
                "deviceManufacturer": "none",
                "deviceType": "Computer",
                "language": locale.getdefaultlocale()[0],
                "osType": platform.system(),
                "osVersion": platform.release(),
            },
            "id": access_point_id.replace('-', '').upper()
        }

        self._auth_token = auth_token
        self._clientauth_token = hashlib.sha512(
            str(access_point_id + "jiLpVitHvWnIGD1yo7MA").encode(
                'utf-8')).hexdigest().upper()
        self._urlREST = ""
        self._urlWebSocket = ""
        self.socket_connection = None  # ClientWebSocketResponse
        self._socket_task = None

        self._headers = {'content-type': 'application/json',
                         'accept': 'application/json', 'VERSION': '10',
                         'AUTHTOKEN': self._auth_token,
                         'CLIENTAUTH': self._clientauth_token}

    @property
    def client_characteristics(self):
        return self._clientCharacteristics

    def listen_for_websocket_data(self, incoming_parser):
        self._socket_task = self._loop.create_task(
            self._listen_for_incoming_websocket_data(incoming_parser))

    @asyncio.coroutine
    def _connect_to_websocket(self):
        self.socket_connection = yield from self._websession.ws_connect(
            self._urlWebSocket,
            headers={'AUTHTOKEN': self._auth_token,
                     'CLIENTAUTH': self._clientauth_token},
            heartbeat=120,
            timeout=3
        )

    def close_websocket_connection(self):
        self._socket_task.cancel()

    @asyncio.coroutine
    def _listen_for_incoming_websocket_data(self, incoming_parser):
        """Creates a websocket connection, listens for incoming data and
        uses the incoming parser to parse the incoming data.
        """

        try:
            while True:
                _connection_try = 0
                while _connection_try < WEBSOCKET_RETRIES:
                    try:
                        yield from self._connect_to_websocket()
                        break
                    except TimeoutError:
                        _LOGGER.info(
                            'websocket connection timed-out. retry %s'
                            % _connection_try)
                    _connection_try += 1
                    yield from asyncio.sleep(_connection_try ** 2)
                else:
                    # exit while loop without break. Raising error.
                    raise ConnectionError(
                        "Problem connecting to hmip websocket connection")

                _LOGGER.info('Connected to HMIP websocket.')
                try:
                    while not self.socket_connection.closed:
                        msg = yield from self.socket_connection.receive()
                        if msg.tp == aiohttp.WSMsgType.BINARY:
                            js = json.loads(str(msg.data, 'utf-8'))
                            _LOGGER.debug("incoming: {}".format(js))
                            incoming_parser(js)
                        elif msg.tp == aiohttp.WSMsgType.CLOSE:
                            break
                except KeyError as e:
                    _LOGGER.exception(e)
                _LOGGER.info("Socket connection closed. Retry in 5 seconds.")
                yield from asyncio.sleep(5)
        except CancelledError:
            _LOGGER.debug('stopping websocket incoming listener')
        finally:
            self._websession.close()
            #self._loop.create_task(self.socket_connection.close())

    def full_url(self, partial_url):
        return '{}/hmip/{}'.format(self._urlREST, partial_url)

    async def _apiCall(self, path, body=None, full_url=False):
        result = None
        if not full_url:
            path = self.full_url(path)
        # requestPath = '{}/hmip/{}'.format(self._urlREST, path)
        for i in range(self._restCallRequestCounter):
            try:
                with async_timeout.timeout(self._restCallTimout,
                                           loop=self._loop):
                    result = await self._websession.post(
                        path,
                        data=body,
                        headers=self._headers
                    )
                    if result.status == 200:

                        try:
                            if result.content_type == 'application/json':
                                ret = await result.json()
                            else:
                                ret = True
                            return ret
                        except Exception as e:
                            _LOGGER.exception(e)
            except (
                    asyncio.TimeoutError, ConnectionError,
                    ClientResponseError):
                _LOGGER.error(
                    "Error connecting to: %s" % path)
            except JSONDecodeError:
                _LOGGER.error('Unable to decode response to json')
            finally:
                if result is not None:
                    await result.release()
        raise ConnectionError(
            "Problem connecting to hmip server %s" % path)

    async def init(self, lookup=True):

        if lookup:
            js = await self._apiCall(
                "https://lookup.homematic.com:48335/getHost",
                body=json.dumps(self._clientCharacteristics), full_url=True)

            self._urlREST = js["urlREST"]
            self._urlWebSocket = js["urlWebSocket"]
        else:
            self._urlREST = "https://ps1.homematic.com:6969"
            self._urlWebSocket = "wss://ps1.homematic.com:8888"
        return True
