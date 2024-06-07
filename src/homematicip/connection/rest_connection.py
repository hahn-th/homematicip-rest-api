from dataclasses import dataclass
import json
import logging
from typing import Optional

import httpx

from homematicip.connection.client_characteristics_builder import ClientCharacteristicsBuilder
from homematicip.connection.client_token_builder import ClientTokenBuilder
from homematicip.exceptions.connection_exceptions import HmipThrottlingError

ATTR_AUTH_TOKEN = "AUTHTOKEN"
ATTR_CLIENT_AUTH = "CLIENTAUTH"

THROTTLE_STATUS_CODE = 429

LOGGER = logging.getLogger(__name__)


@dataclass
class RestResult:
    status: int = -1
    status_text: str = ""
    json: Optional[dict] = None
    exception: Optional[Exception] = None

    def __post_init__(self):
        self.status_text = httpx.codes.get_reason_phrase(self.status)
        if self.status_text == "":
            self.status_text = "No status code"


@dataclass
class ConnectionContext:
    auth_token: str = None
    client_auth_token: str = None

    websocket_url: str = "ws://localhost:8765"
    rest_url: str = None

    accesspoint_id: str = None

    @classmethod
    def create(cls, access_point_id: str, lookup_url: str, auth_token: str = None):
        """
        Create a new connection context.

        :param access_point_id: Access point id
        :param lookup_url: Url to lookup the connection urls
        :param auth_token: The Auth Token if exists. If no one is provided None will be used
        :return: a new ConnectionContext
        """
        ctx = ConnectionContext()
        ctx.accesspoint_id = access_point_id
        ctx.client_auth_token = ClientTokenBuilder.build_client_token(access_point_id)

        cc = ClientCharacteristicsBuilder.get(access_point_id)
        ctx.rest_url, ctx.websocket_url = ConnectionUrlResolver().lookup_urls(cc, lookup_url)

        if auth_token is not None:
            ctx.auth_token = auth_token

        return ctx


@dataclass
class RestConnection:
    _context: ConnectionContext = None
    _headers: dict[str, str] = None

    def __init__(self, context: ConnectionContext):
        LOGGER.debug("Initialize new RestConnection")
        self._context: ConnectionContext = context
        self._headers = self._get_header(self._context)

    def update_connection_context(self, context: ConnectionContext) -> None:
        self._context = context
        self._headers = self._get_header(self._context)

    @staticmethod
    def _get_header(context: ConnectionContext) -> dict[str, str]:
        """Create a json header"""
        return {
            "content-type": "application/json",
            "accept": "application/json",
            "VERSION": "12",
            ATTR_AUTH_TOKEN: context.auth_token,
            ATTR_CLIENT_AUTH: context.client_auth_token
        }

    async def async_post(self, url: str, data: json = None, custom_header: dict = None) -> RestResult:
        """Send an async post request to cloud with json data. Returns a json result."""
        full_url = self._build_url(self._context.rest_url, url)
        async with httpx.AsyncClient() as client:
            try:
                header = self._headers
                if custom_header is not None:
                    header = custom_header

                LOGGER.debug(f"Sending post request to url {full_url}. Data is: {data}")
                r = await client.post(full_url, json=data, headers=header)
                LOGGER.debug(f"Got response {r.status_code}.")

                if r.status_code == THROTTLE_STATUS_CODE:
                    LOGGER.error("Got error 429 (Throttling active)")
                    raise HmipThrottlingError

                r.raise_for_status()

                result = RestResult(status=r.status_code)
                try:
                    result.json = r.json()
                except json.JSONDecodeError:
                    pass

                return result
            except httpx.RequestError as exc:
                LOGGER.error(f"An error occurred while requesting {exc.request.url!r}.")
                return RestResult(status=-1, exception=exc)
            except httpx.HTTPStatusError as exc:
                LOGGER.error(
                    f"Error response {exc.response.status_code} while requesting {exc.request.url!r} with data {data if data is not None else "<no-data>"}."
                )
                LOGGER.error(f"Response: {repr(exc.response)}")
                return RestResult(status=-1, exception=exc)

    def _build_url(self, base_url: str, path: str) -> str:
        """Build full qualified url."""
        return f"{base_url}/hmip/{path}"


class ConnectionUrlResolver:
    """Lookup rest and websocket urls."""

    @staticmethod
    def lookup_urls(
            client_characteristics: dict,
            lookup_url: str,
    ) -> tuple[str, str]:
        """Lookup urls.

        :param client_characteristics: The client characteristics
        :param lookup_url: The lookup url

        :return: The rest and websocket url as tuple
        """
        result = httpx.post(lookup_url, json=client_characteristics)
        result.raise_for_status()

        js = result.json()

        rest_url = js["urlREST"]
        websocket_url = js["urlWebSocket"]

        return rest_url, websocket_url
