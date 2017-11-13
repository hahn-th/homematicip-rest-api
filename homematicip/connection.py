import hashlib
import json
import locale
import platform
import logging
import requests
import re

logger = logging.getLogger(__name__)

AUTH_TOKEN = 'AUTHTOKEN'
CLIENT_AUTH = 'CLIENTAUTH'


class Connection:
    _auth_token = ""
    _clientauth_token = ""
    _urlREST = ""
    _urlWebSocket = ""
    # the homematic ip cloud tends to time out. retry the call X times.
    _restCallRequestCounter = 3
    _restCallTimout = 6

    def __init__(self):
        self.headers = {'content-type': 'application/json',
                        'accept': 'application/json', 'VERSION': '12',
                        AUTH_TOKEN: None, CLIENT_AUTH: None}

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

    @property
    def clientCharacteristics(self):
        return self._clientCharacteristics

    @property
    def urlWebSocket(self):
        return self._urlWebSocket

    @property
    def urlREST(self):
        return self._urlREST

    @property
    def auth_token(self):
        return self._auth_token

    @property
    def clientauth_token(self):
        return self._clientauth_token

    def init(self, accesspoint_id, lookup=True, **kwargs):
        accesspoint_id = re.sub('\W+','', accesspoint_id).upper()
        self.clientCharacteristics["id"] = accesspoint_id
        self._clientauth_token = hashlib.sha512(
            str(accesspoint_id + "jiLpVitHvWnIGD1yo7MA").encode(
                'utf-8')).hexdigest().upper()
        self.headers[CLIENT_AUTH] = self._clientauth_token

        if lookup:
            while True:
                try:
                    result = requests.post(
                        "https://lookup.homematic.com:48335/getHost",
                        json=self.clientCharacteristics, timeout=3)
                    js = json.loads(result.text)
                    self._urlREST = js["urlREST"]
                    self._urlWebSocket = js["urlWebSocket"]
                    break
                except:
                    pass
        else:
            self._urlREST = "https://ps1.homematic.com:6969"
            self._urlWebSocket = "wss://ps1.homematic.com:8888"

    def set_auth_token(self, auth_token):
        self._auth_token = auth_token
        self.headers[AUTH_TOKEN] = auth_token

    def _restCall(self, path, body=None):
        result = None
        requestPath = '{}/hmip/{}'.format(self._urlREST, path)
        logger.debug("_restcall path({}) body({})".format(requestPath, body))
        for i in range(0, self._restCallRequestCounter):
            try:
                result = requests.post(requestPath, data=body,
                                       headers=self.headers,
                                       timeout=self._restCallTimout)
                ret = (result.json() if len(result.content) != 0 else "")
                logger.debug(
                    "_restcall result: Errorcode={} content({})".format(
                        result.status_code, ret))
                return ret
            except requests.Timeout:
                logger.error(
                    "call to '{}' failed due Timeout".format(requestPath))
                pass
        return {"errorCode": "TIMEOUT"}
