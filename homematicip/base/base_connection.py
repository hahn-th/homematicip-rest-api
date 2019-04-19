import hashlib
import locale
import platform
import re

ATTR_AUTH_TOKEN = "AUTHTOKEN"
ATTR_CLIENT_AUTH = "CLIENTAUTH"


class HmipConnectionError(Exception):
    pass


class HmipWrongHttpStatusError(HmipConnectionError):
    pass


class HmipServerCloseError(HmipConnectionError):
    pass


class BaseConnection:
    """Base connection class.

    Threaded and Async connection class must inherit from this."""

    _auth_token = ""
    _clientauth_token = ""
    _urlREST = ""
    _urlWebSocket = ""
    # the homematic ip cloud tends to time out. retry the call X times.
    _restCallRequestCounter = 3
    _restCallTimout = 6

    def __init__(self):
        self.headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "VERSION": "12",
            ATTR_AUTH_TOKEN: None,
            ATTR_CLIENT_AUTH: None,
        }
        lang = "en_US"
        def_locale = locale.getdefaultlocale()
        if def_locale != None and def_locale[0] != None:
            lang = def_locale[0]

        self._clientCharacteristics = {
            "clientCharacteristics": {
                "apiVersion": "10",
                "applicationIdentifier": "homematicip-python",
                "applicationVersion": "1.0",
                "deviceManufacturer": "none",
                "deviceType": "Computer",
                "language": lang,
                "osType": platform.system(),
                "osVersion": platform.release(),
            },
            "id": None,
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

    def set_token_and_characteristics(self, accesspoint_id):
        accesspoint_id = re.sub(r"[^a-fA-F0-9 ]", "", accesspoint_id).upper()
        self._clientCharacteristics["id"] = accesspoint_id
        self._clientauth_token = (
            hashlib.sha512(str(accesspoint_id + "jiLpVitHvWnIGD1yo7MA").encode("utf-8"))
            .hexdigest()
            .upper()
        )
        self.headers[ATTR_CLIENT_AUTH] = self._clientauth_token

    def set_auth_token(self, auth_token):
        self._auth_token = auth_token
        self.headers[ATTR_AUTH_TOKEN] = auth_token

    def init(self, accesspoint_id, lookup=True, **kwargs):
        raise NotImplementedError

    def _restCall(self, path, body=None):
        raise NotImplementedError
