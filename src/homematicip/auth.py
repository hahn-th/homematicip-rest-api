# coding=utf-8

import logging
import uuid
from dataclasses import dataclass

from homematicip.connection_v2.connection_context import ConnectionContext
from homematicip.connection_v2.rest_connection import RestResult, RestConnection

LOGGER = logging.getLogger(__name__)


@dataclass
class Auth:
    """This class generates the auth token for the homematic ip access point."""

    client_id: str = str(uuid.uuid4())
    header: dict = None
    pin: str = None
    connection: RestConnection = None

    def __init__(self, connection: RestConnection, client_auth_token: str):
        """Initialize the auth object.
        @param connection: The connection object
        @param client_auth_token: The client auth token
        """
        LOGGER.debug("Initialize new Auth")
        self.connection = connection
        self.headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "VERSION": "12",
            "CLIENTAUTH": client_auth_token
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

#
# class Auth(object):
#     def __init__(self, home: Home):
#         self.uuid = str(uuid.uuid4())
#         self.headers = {
#             "content-type": "application/json",
#             "accept": "application/json",
#             "VERSION": "12",
#             "CLIENTAUTH": home._connection.clientauth_token,
#         }
#         self.url_rest = home._connection.urlREST
#         self.pin = None
#
#     def connectionRequest(
#         self, access_point, devicename="homematicip-python"
#     ) -> requests.Response:
#         data = {"deviceId": self.uuid, "deviceName": devicename, "sgtin": access_point}
#         headers = self.headers
#         if self.pin != None:
#             headers["PIN"] = self.pin
#         response = requests.post(
#             "{}/hmip/auth/connectionRequest".format(self.url_rest),
#             json=data,
#             headers=headers,
#         )
#         return response
#
#     def isRequestAcknowledged(self):
#         data = {"deviceId": self.uuid}
#         response = requests.post(
#             "{}/hmip/auth/isRequestAcknowledged".format(self.url_rest),
#             json=data,
#             headers=self.headers,
#         )
#         return response.status_code == 200
#
#     def requestAuthToken(self):
#         data = {"deviceId": self.uuid}
#         response = requests.post(
#             "{}/hmip/auth/requestAuthToken".format(self.url_rest),
#             json=data,
#             headers=self.headers,
#         )
#         return json.loads(response.text)["authToken"]
#
#     def confirmAuthToken(self, authToken):
#         data = {"deviceId": self.uuid, "authToken": authToken}
#         response = requests.post(
#             "{}/hmip/auth/confirmAuthToken".format(self.url_rest),
#             json=data,
#             headers=self.headers,
#         )
#         return json.loads(response.text)["clientId"]
