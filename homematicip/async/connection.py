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

from homematicip.base.base_connection import BaseConnection

_LOGGER = logging.getLogger(__name__)

INIT_RETRIES = 3
WEBSOCKET_RETRIES = 3


class HmipConnectionException(Exception):
    pass


class HmipBadResponseCodeException(HmipConnectionException):
    pass


class Connection(BaseConnection):
    """Async connection class implementation."""

    def __init__(self, loop, auth_token, access_point_id):
        super().__init__(auth_token, access_point_id)
        self._loop = loop
        self._websession = aiohttp.ClientSession(loop=loop)

        self._socket_task = None

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
            # self._loop.create_task(self.socket_connection.close())

    async def _call(self, full_path, body: dict = None):
        result = None
        try:
            with async_timeout.timeout(self._restCallTimeout,
                                       loop=self._loop):
                result = await self._websession.post(
                    full_path,
                    json=body,
                    headers=self._headers
                )
                if result.status in [200, 201]:
                    if result.content_type == 'application/json':
                        ret = await result.json()
                    else:
                        ret = True
                    return ret
                else:
                    _LOGGER.error("Error %s on %s", result.status, full_path)
                    raise HmipBadResponseCodeException("status: %s path: %s",
                                                       result.status,
                                                       full_path)
        finally:
            if result is not None:
                await result.release()

    async def _rest_call(self, path: str, body: dict = None, full_url=False):
        """Make the API call.
        returns a dict with results if content type == 'application/json'
        returns true if not, but status is still 200 or 201
        raises an exception when any error occurs or status is not 200 or 201


        :param path:
        :param body:
        :param full_url:
        :return:
        """
        if not full_url:
            path = self._full_url(path)
        for i in range(self._restCallRequestCounter):
            try:
                return await self._call(path, body=body)
            except (asyncio.TimeoutError, ConnectionError):
                _LOGGER.error(
                    "Error connecting to: %s. Retries left: %s",
                    path,
                    self._restCallRequestCounter - i)
        raise HmipConnectionException(
            "Problem connecting to hmip server %s", path)

    async def init_connection(self, lookup=True):
        url, body = self._init_connection()
        js = await self._rest_call(url, body=body, full_url=True)
        self._do_lookup(lookup, js)
