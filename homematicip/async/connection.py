# coding=utf-8
import platform
import locale
import logging
import hashlib
import aiohttp
import asyncio

_LOGGER = logging.getLogger(__name__)


class Connection:
    def __init__(self, loop, auth_token):
        self._loop = loop
        self._websession = aiohttp.ClientSession(loop=loop)
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
            "id": None
        }
        self._auth_token = auth_token
        self._clientauth_token = ""
        self._urlREST = ""
        self._urlWebSocket = ""

    @property
    def urlWebSocket(self):
        return self._urlWebSocket

    @property
    def urlREST(self):
        return self._urlREST

    @property
    def websession(self):
        return self._websession

    @property
    def clientauth_token(self):
        return self._clientauth_token

    @clientauth_token.setter
    def clientauth_token(self, value):
        self._clientauth_token = value

    @property
    def auth_token(self):
        return self._auth_token

    @property
    def client_characteristics(self):
        return self._clientCharacteristics

    @asyncio.coroutine
    def init(self, accesspoint_id, lookup=True):
        accesspoint_id = accesspoint_id.replace('-', '').upper()
        self._clientCharacteristics["id"] = accesspoint_id

        self._clientauth_token = hashlib.sha512(
            str(accesspoint_id + "jiLpVitHvWnIGD1yo7MA").encode(
                'utf-8')).hexdigest().upper()

        if lookup:
            # todo: while True might be dangerous. Rewrite this ?
            while True:
                try:
                    result = yield from self._websession.post(
                        "https://lookup.homematic.com:48335/getHost",
                        json=self._clientCharacteristics, timeout=3)
                    js = yield from result.json()
                    self._urlREST = js["urlREST"]
                    self._urlWebSocket = js["urlWebSocket"]
                    break
                except Exception as e:
                    _LOGGER.exception(e)
        else:
            self._urlREST = "https://ps1.homematic.com:6969"
            self._urlWebSocket = "wss://ps1.homematic.com:8888"

