import hashlib
import json
import locale
import platform


class BaseConnection:
    """All connection specific data like tokens,ids, urls
    etc are stored here"""

    # the homematic ip cloud tends to time out. retry the call X times.
    _restCallRequestCounter = 3
    _restCallTimeout = 5

    def __init__(self, auth_token, access_point_id):
        self._auth_token = auth_token
        self._access_point_id = access_point_id

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

        self._clientauth_token = hashlib.sha512(
            str(access_point_id + "jiLpVitHvWnIGD1yo7MA").encode(
                'utf-8')).hexdigest().upper()
        self._urlREST = ""
        self._urlWebSocket = ""
        self.socket_connection = None  # ClientWebSocketResponse

        self._headers = {'content-type': 'application/json',
                         'accept': 'application/json', 'VERSION': '10',
                         'AUTHTOKEN': self._auth_token,
                         'CLIENTAUTH': self._clientauth_token}

    def _full_url(self, partial_url):
        return '{}/hmip/{}'.format(self._urlREST, partial_url)

    @property
    def client_characteristics(self):
        # todo: is this property still in use ?
        return self._clientCharacteristics

    def _init_connection(self):
        """Gets the init connection data"""
        return ("https://lookup.homematic.com:48335/getHost",
                self._clientCharacteristics)

    def init_connection(self, lookup=True):
        """Initializes the hmip connection.

        - get the _init_connection_data
        - do an api call
        - do the _do_lookup
        """
        pass

    async def _rest_call(self, path: str, body: dict = None, full_url=False):
        """Make a call to the Hmip server.

        All calls pass through here."""
        pass

    def _do_lookup(self, lookup, js):
        """Lookup the addresses of the hmip server based on server response
        data
        """
        if lookup:
            self._urlREST = js["urlREST"]
            self._urlWebSocket = js["urlWebSocket"]
        else:
            self._urlREST = "https://ps1.homematic.com:6969"
            self._urlWebSocket = "wss://ps1.homematic.com:8888"
