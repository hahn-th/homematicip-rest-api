
import logging
import uuid
from dataclasses import dataclass

from homematicip.connection.rest_connection import RestConnection, RestResult
from homematicip.exceptions.connection_exceptions import HmipConnectionError

LOGGER = logging.getLogger(__name__)


def _read_field(result: RestResult, field: str, action: str) -> str:
    """Read a field from an auth response, or raise.
    @param result: The result of the auth request
    @param field: The name of the field to read
    @param action: What was attempted, for the error message
    @return: The value of the field
    @raises HmipConnectionError: If the request failed or carried no such field
    """
    # async_post reports a failed call as a RestResult instead of raising, so an
    # unchecked read turns a rejected token step into a TypeError on json being None
    if not result.success:
        raise HmipConnectionError(
            f"{action} failed with status {result.status} ({result.status_text})"
        )

    if not isinstance(result.json, dict) or field not in result.json:
        raise HmipConnectionError(f"{action} returned no {field}")

    return result.json[field]


@dataclass
class Auth:
    """This class generates the auth token for the homematic ip access point."""

    client_id: str = str(uuid.uuid4())
    header: dict = None
    accesspoint_id: str = None
    pin: str = None
    connection: RestConnection = None

    def __init__(self, connection: RestConnection, client_auth_token: str, accesspoint_id: str):
        """Initialize the auth object.
        @param connection: The connection object
        @param client_auth_token: The client auth token
        @param accesspoint_id: The access point id
        """
        LOGGER.debug("Initialize new Auth")
        self.accesspoint_id = accesspoint_id
        self.connection = connection
        self.headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "VERSION": "12",
            "CLIENTAUTH": client_auth_token,
            "ACCESSPOINT-ID": self.accesspoint_id,
        }

    def set_pin(self, pin: str):
        """Set the pin for the auth object.
        @param pin: The pin"""
        self.pin = pin

    async def connection_request(self, access_point: str, device_name="homematicip-python") -> RestResult:
        LOGGER.debug("Requesting connection for access point [REDACTED]")
        headers = self.headers.copy()
        if self.pin is not None:
            headers["PIN"] = self.pin

        data = {
            "deviceId": self.client_id,
            "deviceName": device_name,
            "sgtin": access_point
        }

        return await self.connection.async_post("auth/connectionRequest", data, headers)

    async def is_request_acknowledged(self) -> bool:
        LOGGER.debug("Checking if request is acknowledged")
        data = {
            "deviceId": self.client_id,
            "accessPointId": self.accesspoint_id
        }

        result = await self.connection.async_post("auth/isRequestAcknowledged", data, self.headers)

        LOGGER.debug("Request acknowledged check finished with status %s", result.status)
        return result.status == 200

    async def request_auth_token(self) -> str:
        """Request an auth token from the access point.
        @return: The auth token"""
        LOGGER.debug("Requesting auth token")
        data = {"deviceId": self.client_id}
        result = await self.connection.async_post("auth/requestAuthToken", data, self.headers)
        LOGGER.debug("Auth token request finished with status %s", result.status)

        return _read_field(result, "authToken", "Requesting the auth token")

    async def confirm_auth_token(self, auth_token: str) -> str:
        """Confirm the auth token and get the client id.
        @param auth_token: The auth token
        @return: The client id"""

        LOGGER.debug("Confirming auth token")
        data = {"deviceId": self.client_id, "authToken": auth_token}
        result = await self.connection.async_post("auth/confirmAuthToken", data, self.headers)
        LOGGER.debug("Auth token confirmation finished with status %s", result.status)

        return _read_field(result, "clientId", "Confirming the auth token")

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
