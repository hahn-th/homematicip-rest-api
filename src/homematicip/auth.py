import logging
import uuid
from dataclasses import dataclass

from homematicip.connection.rest_connection import ConnectionContext, RestResult, RestConnection

LOGGER = logging.getLogger(__name__)


@dataclass
class Auth:

    client_id: str = str(uuid.uuid4())
    header: dict = None
    pin: str = None
    connection: RestConnection = None

    def __init__(self, context: ConnectionContext):
        LOGGER.debug("Initialize new Auth")
        self.connection = RestConnection(context)
        self.headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "VERSION": "12"
        }

    async def connection_request(self, access_point: str, device_name="homematicip-python", pin=None) -> RestResult:
        LOGGER.debug(f"Requesting connection for access point {access_point}")
        headers = self.headers
        if pin is not None:
            headers["PIN"] = pin

        data = {
            "deviceId": self.client_id,
            "deviceName": device_name,
            "sgtin": access_point
        }

        return await self.connection.async_post("auth/connectionRequest", data, headers)

    async def is_request_acknowledged(self) -> bool:
        LOGGER.debug("Checking if request is acknowledged")
        data = {
            "deviceId": self.client_id
        }

        result = await self.connection.async_post("auth/isRequestAcknowledged", data, self.headers)

        LOGGER.debug(f"Request acknowledged result: {result}")
        return result.status == 200

    async def request_auth_token(self) -> str:
        """Request an auth token from the access point.
        @return: The auth token"""
        LOGGER.debug("Requesting auth token")
        data = {"deviceId": self.client_id}
        result = await self.connection.async_post("auth/requestAuthToken", data, self.headers)
        LOGGER.debug(f"Request auth token result: {result}")

        return result.json["authToken"]

    async def confirm_auth_token(self, auth_token: str) -> str:
        """Confirm the auth token and get the client id.
        @param auth_token: The auth token
        @return: The client id"""

        LOGGER.debug("Confirming auth token")
        data = {"deviceId": self.client_id, "authToken": auth_token}
        result = await self.connection.async_post("auth/confirmAuthToken", data, self.headers)
        LOGGER.debug(f"Confirm auth token result: {result}")

        return result.json["clientId"]
