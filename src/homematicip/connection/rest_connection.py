import json
import logging
from dataclasses import dataclass
from ssl import SSLContext
from typing import Optional

import httpx

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
        self.status_text = httpx.codes.get_reason_phrase(self.status)
        if self.status_text == "":
            self.status_text = "No status code"

        self.success = 200 <= self.status < 300


@dataclass
class RestConnection:
    _context: ConnectionContext | None = None
    _headers: dict[str, str] = None
    _verify = None
    _log_status_exceptions = True
    _httpx_client_session: httpx.AsyncClient | None = None

    def __init__(self, context: ConnectionContext, httpx_client_session: httpx.AsyncClient | None = None,
                 log_status_exceptions: bool = True):
        """Initialize the RestConnection object.

        @param context: The connection context
        @param httpx_client_session: The httpx client session if you want to use a custom one
        @param log_status_exceptions: If status exceptions should be logged
        """
        LOGGER.debug("Initialize new RestConnection")
        self.update_connection_context(context)
        self._log_status_exceptions = log_status_exceptions
        self._httpx_client_session = httpx_client_session

    def update_connection_context(self, context: ConnectionContext) -> None:
        self._context: ConnectionContext = context
        self._headers: dict = self._get_header(context)
        self._verify:  SSLContext | str | bool = self._get_verify(context.enforce_ssl, context.ssl_ctx)

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
        @raises HmipThrottlingError: If the cloud returns a 429 status code (throttling active)
        """
        full_url = self._build_url(self._context.rest_url, url)
        try:
            header = self._headers
            if custom_header is not None:
                header = custom_header

            LOGGER.debug(f"Sending post request to url {full_url}. Data is: {data}")
            r = await self._execute_request_async(full_url, data, header)
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
            if self._log_status_exceptions:
                LOGGER.error(
                    f"Error response {exc.response.status_code} ({exc.response.text}) while requesting {exc.request.url!r} with data {data if data is not None else "<no-data>"}."
                )
            return RestResult(status=exc.response.status_code, exception=exc, text=exc.response.text)

    async def _execute_request_async(self, url: str, data: dict | None = None, header: dict | None = None):
        """Execute a request async. Uses the httpx client session if available.
        @param url: The path of the url to send the request to
        @param data: The data to send as json
        @param custom_header: A custom header to send. Replaces the default header
        @return: The result as a RestResult object
        """
        if self._httpx_client_session is None:
            async with httpx.AsyncClient(verify=self._verify) as client:
                result = await client.post(url, json=data, headers=header)
        else:
            result = await self._httpx_client_session.post(url, json=data, headers=header)

        return result

    @staticmethod
    def _build_url(base_url: str, path: str) -> str:
        """Build full qualified url."""
        return f"{base_url}/hmip/{path}"

    @staticmethod
    def _get_verify(enforce_ssl: bool, ssl_context) -> SSLContext | str | bool:
        if ssl_context is not None:
            return ssl_context
        if enforce_ssl:
            return enforce_ssl

        return True
