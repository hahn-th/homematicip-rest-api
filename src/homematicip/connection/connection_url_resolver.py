from ssl import SSLContext

import httpx2

from homematicip.connection import get_ssl_verify
from homematicip.exceptions.connection_exceptions import HmipConnectionError


class ConnectionUrlResolver:
    """Lookup rest and websocket urls."""

    @staticmethod
    async def lookup_urls_async(
            client_characteristics: dict,
            lookup_url: str,
            enforce_ssl: bool = True,
            ssl_context: SSLContext | None= None,
            httpx_client_session: httpx2.AsyncClient | None = None,
    ) -> tuple[str, str]:
        """Lookup urls async.

        :param client_characteristics: The client characteristics
        :param lookup_url: The lookup url
        :param enforce_ssl: Disable ssl verification by setting enforce_ssl to False
        :param ssl_context: The ssl context
        :param httpx_client_session: The httpx2 client session if you want to use a custom one

        :return: The rest and websocket url as tuple
        """
        verify = ConnectionUrlResolver._get_verify(enforce_ssl, ssl_context)

        try:
            if httpx_client_session is None:
                async with httpx2.AsyncClient(verify=verify) as client:
                    result = await client.post(lookup_url, json=client_characteristics)
            else:
                result = await httpx_client_session.post(lookup_url, json=client_characteristics)
            return ConnectionUrlResolver._urls_from_response(result)
        except httpx2.HTTPError as err:
            raise HmipConnectionError(f"Lookup of the cloud hosts failed: {err}") from err

    @staticmethod
    def _urls_from_response(result: httpx2.Response) -> tuple[str, str]:
        # callers only know HmipConnectionError, a raw httpx2 or parsing error ends a Home Assistant
        # setup for good instead of being retried
        result.raise_for_status()
        try:
            js = result.json()
            return js["urlREST"], js["urlWebSocket"]
        except (ValueError, KeyError, TypeError) as err:
            raise HmipConnectionError(f"Lookup of the cloud hosts returned an unexpected answer: {err!r}") from err

    @staticmethod
    def lookup_urls(
            client_characteristics: dict,
            lookup_url: str,
            enforce_ssl: bool = True,
            ssl_context=None,
    ) -> tuple[str, str]:
        """Lookup urls.

        :param client_characteristics: The client characteristics
        :param lookup_url: The lookup url
        :param enforce_ssl: Disable ssl verification by setting enforce_ssl to False
        :param ssl_context: The ssl context

        :return: The rest and websocket url as tuple
        """
        verify = ConnectionUrlResolver._get_verify(enforce_ssl, ssl_context)
        try:
            result = httpx2.post(lookup_url, json=client_characteristics, verify=verify)
            return ConnectionUrlResolver._urls_from_response(result)
        except httpx2.HTTPError as err:
            raise HmipConnectionError(f"Lookup of the cloud hosts failed: {err}") from err

    @staticmethod
    def _get_verify(enforce_ssl: bool, ssl_context):
        return get_ssl_verify(enforce_ssl, ssl_context)
