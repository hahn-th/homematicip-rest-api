import asyncio
import json
import uuid
import logging

from homematicip.aio.connection import AsyncConnection
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
        self.pin = None
        self._connection=AsyncAuthConnection(loop, websession)

    async def init(self, access_point_id, lookup=True, lookup_url = None):
        self.accesspoint = access_point_id
        if lookup_url:
            await self._connection.init(access_point_id, lookup, lookup_url)
        else:
            await self._connection.init(access_point_id, lookup)

    async def connectionRequest(self, devicename = "homematicip-async"):
        data = {"deviceId": self.uuid, "deviceName": devicename, "sgtin": self.accesspoint}
        if self.pin != None:
            self._connection.headers["PIN"] = self.pin
        json_state =  await self._connection.api_call('auth/connectionRequest', json.dumps(data))
        return json_state

    async def isRequestAcknowledged(self):
        data = {"deviceId": self.uuid}
        return await self._connection.api_call('auth/isRequestAcknowledged', json.dumps(data))

    async def requestAuthToken(self):
        data = {"deviceId": self.uuid}
        json_state = await self._connection.api_call('auth/requestAuthToken', json.dumps(data))
        return json_state["authToken"]

    async def confirmAuthToken(self, authToken):
        data = {"deviceId": self.uuid, "authToken": authToken}
        json_state = await self._connection.api_call('auth/confirmAuthToken', json.dumps(data))
        return json_state["clientId"]
