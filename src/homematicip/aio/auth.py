import json
import logging
import uuid

from homematicip.aio.connection import AsyncConnection
from homematicip.auth import Auth
from homematicip.base.base_connection import HmipWrongHttpStatusError

LOGGER = logging.getLogger(__name__)


class AsyncAuthConnection(AsyncConnection):
    def __init__(self, loop, session=None):
        super().__init__(loop, session)
        self.headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "VERSION": "12",
            "CLIENTAUTH": self.clientauth_token,
        }


# todo: make the overridden methods match signature and return types of the overridden class.


class AsyncAuth(Auth):
    """this class represents the 'Async Auth' of the homematic ip"""

    def __init__(self, loop, websession=None):
        self.uuid = str(uuid.uuid4())
        self.pin = None
        self._connection = AsyncAuthConnection(loop, websession)

    async def init(self, access_point_id, lookup=True, lookup_url=None):
        self.accesspoint = access_point_id
        if lookup_url:
            await self._connection.init(access_point_id, lookup, lookup_url)
        else:
            await self._connection.init(access_point_id, lookup)

    async def connectionRequest(self, devicename="homematicip-async"):
        data = {
            "deviceId": self.uuid,
            "deviceName": devicename,
            "sgtin": self.accesspoint,
        }
        if self.pin is not None:
            self._connection.headers["PIN"] = self.pin
        json_state = await self._connection.api_call(
            "auth/connectionRequest", json.dumps(data)
        )
        return json_state

    async def isRequestAcknowledged(self):
        data = {"deviceId": self.uuid}
        try:
            await self._connection.api_call(
                "auth/isRequestAcknowledged", json.dumps(data)
            )
            return True
        except HmipWrongHttpStatusError:
            return False

    async def requestAuthToken(self):
        data = {"deviceId": self.uuid}
        json_state = await self._connection.api_call(
            "auth/requestAuthToken", json.dumps(data)
        )
        return json_state["authToken"]

    async def confirmAuthToken(self, authToken):
        data = {"deviceId": self.uuid, "authToken": authToken}
        json_state = await self._connection.api_call(
            "auth/confirmAuthToken", json.dumps(data)
        )
        return json_state["clientId"]
