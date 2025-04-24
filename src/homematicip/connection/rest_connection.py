import json
import logging
from dataclasses import dataclass
from ssl import SSLContext
from typing import Optional

import aiohttp

from homematicip.connection import ATTR_AUTH_TOKEN, ATTR_CLIENT_AUTH, THROTTLE_STATUS_CODE, ATTR_ACCESSPOINT_ID
from homematicip.connection.connection_context import ConnectionContext
from homematicip.exceptions.connection_exceptions import HmipThrottlingError

LOGGER = logging.getLogger(__name__)


@dataclass
class RestResult:
    status: int = -1
    status_text: str = ""
    json: Optional[dict] = None
    exception: Optional[Exception] = None
    success: bool = False
    text: str = ""

    def __post_init__(self):
        self.status_text = "No status code" if self.status == -1 else str(self.status)
        self.success = 200 <= self.status < 300


@dataclass
class RestConnection:
    _context: ConnectionContext | None = None
    _headers: dict[str, str] = None
    _verify = None
    _log_status_exceptions = True
    _client_session: aiohttp.ClientSession | None = None
    _owns_session: bool = False

    def __init__(self, context: ConnectionContext, client_session: aiohttp.ClientSession | None = None,
                 log_status_exceptions: bool = True):
        """Initialize the RestConnection object.

        @param context: The connection context
        @param client_session: The aiohttp client session if you want to use a custom one
        @param log_status_exceptions: If status exceptions should be logged
        """
        LOGGER.debug("Initialize new RestConnection")
        self.update_connection_context(context)
        self._log_status_exceptions = log_status_exceptions
        self._client_session = client_session
        self._owns_session = client_session is None

    def update_connection_context(self, context: ConnectionContext) -> None:
        self._context: ConnectionContext = context
        self._headers: dict = self._get_header(context)
        self._verify = self._get_verify(context.enforce_ssl, context.ssl_ctx)

    @staticmethod
    def _get_header(context: ConnectionContext) -> dict[str, str]:
        """Create a json header"""
        return {
            "content-type": "application/json",
            # "accept": "application/json",
            "VERSION": "12",
            ATTR_AUTH_TOKEN: context.auth_token,
            ATTR_CLIENT_AUTH: context.client_auth_token,
            ATTR_ACCESSPOINT_ID: context.accesspoint_id
        }

    def get_header(self) -> dict[str, str]:
        """If headers must be manipulated use this method to get the current headers."""
        return self._headers

    async def async_post(self, url: str, data: dict | None = None, custom_header: dict | None = None) -> RestResult:
        """Send an async post request to cloud with json data. Returns a json result.
        @param url: The path of the url to send the request to
        @param data: The data to send as json
        @param custom_header: A custom header to send. Replaces the default header
        @return: The result as a RestResult object
        """
        full_url = self._build_url(self._context.rest_url, url)
        try:
            header = self._headers
            if custom_header is not None:
                header = custom_header

            LOGGER.debug(f"Sending post request to url {full_url}. Data is: {data}")
            async with await self._get_session() as session:
                async with session.post(full_url, json=data, headers=header,
                                        ssl=self._verify) as response:
                    LOGGER.debug(f"Got response {response.status}.")

                    if response.status == THROTTLE_STATUS_CODE:
                        LOGGER.error("Got error 429 (Throttling active)")
                        raise HmipThrottlingError

                    result = RestResult(status=response.status)
                    try:
                        result.json = await response.json()
                    except aiohttp.ContentTypeError:
                        result.text = await response.text()

                    response.raise_for_status()
                    return result

        # except aiohttp.ClientError as exc:
        #     LOGGER.error(f"An error occurred while requesting {full_url!r}.")
        #     return RestResult(status=-1, exception=exc)
        except aiohttp.ClientResponseError as exc:
            if self._log_status_exceptions:
                LOGGER.error(
                    f"Error response {exc.status} while requesting {full_url!r} with data {data if data is not None else '<no-data>'}."
                )
                LOGGER.error(f"Response: {repr(exc)}")
            return RestResult(status=exc.status, exception=exc, text=str(exc))

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create a client session."""
        if self._client_session is None:
            self._client_session = aiohttp.ClientSession()
            self._owns_session = True
        return self._client_session

    async def close(self):
        """Close the session if we own it."""
        if self._owns_session and self._client_session is not None:
            await self._client_session.close()
            self._client_session = None

    @staticmethod
    def _build_url(base_url: str, path: str) -> str:
        """Build full qualified url."""
        return f"{base_url}/hmip/{path}"

    @staticmethod
    def _get_verify(enforce_ssl: bool, ssl_context) -> SSLContext | bool:
        if ssl_context is not None:
            return ssl_context
        return enforce_ssl