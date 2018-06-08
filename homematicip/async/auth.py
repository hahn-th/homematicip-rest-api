import asyncio
import json
import uuid
import logging

from homematicip.async.connection import AsyncConnection
from homematicip.auth import Auth
from homematicip.base.base_connection import BaseConnection, HmipWrongHttpStatusError, \
    ATTR_AUTH_TOKEN, ATTR_CLIENT_AUTH, HmipConnectionError

LOGGER = logging.getLogger(__name__)

class AsyncAuthConnection(AsyncConnection):
    def __init__(self, loop, session=None):
        super().__init__(loop, session)
        self.headers = {'content-type': 'application/json', 'accept': 'application/json', 'VERSION': '12', 'CLIENTAUTH' : self.clientauth_token }


class AsyncAuth(Auth):
    """this class represents the 'Async Auth' of the homematic ip"""

    def __init__(self, loop, websession=None):
        self.uuid = str(uuid.uuid4())
        self._connection=AsyncAuthConnection(loop, websession)

    async def init(self, access_point_id, lookup=True):
        await self._connection.init(access_point_id, lookup)

# not yet touched

    def connectionRequest(self, access_point, devicename = "homematicip-python"):
        data = {"deviceId": self.uuid, "deviceName": devicename, "sgtin": access_point}
        headers = self.headers
        if self.pin != None:
            headers["PIN"] = self.pin
        response = requests.post("{}/hmip/auth/connectionRequest".format(self.url_rest), json=data,
                                 headers=headers)
        return response

    def isRequestAcknowledged(self):
        data = {"deviceId": self.uuid}
        response = requests.post("{}/hmip/auth/isRequestAcknowledged".format(self.url_rest), json=data,
                                 headers=self.headers)
        return response.status_code == 200

    def requestAuthToken(self):
        data = {"deviceId": self.uuid}
        response = requests.post("{}/hmip/auth/requestAuthToken".format(self.url_rest), json=data,
                                 headers=self.headers)
        return json.loads(response.text)["authToken"]

    def confirmAuthToken(self, authToken):
        data = {"deviceId": self.uuid, "authToken": authToken}
        response = requests.post("{}/hmip/auth/confirmAuthToken".format(self.url_rest), json=data,
                                 headers=self.headers)
        return json.loads(response.text)["clientId"]
