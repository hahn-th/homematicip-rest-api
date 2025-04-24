from ssl import SSLContext

import aiohttp


class ConnectionUrlResolver:
    """Lookup rest and websocket urls."""

    @staticmethod
    async def lookup_urls_async(
            client_characteristics: dict,
            lookup_url: str,
            enforce_ssl: bool = True,
            ssl_context: SSLContext | None= None,
            client_session: aiohttp.ClientSession | None = None,
    ) -> tuple[str, str]:
        """Lookup urls async.

        :param client_characteristics: The client characteristics
        :param lookup_url: The lookup url
        :param enforce_ssl: Disable ssl verification by setting enforce_ssl to False
        :param ssl_context: The ssl context
        :param client_session: The httpx client session if you want to use a custom one

        :return: The rest and websocket url as tuple
        """
        verify = ConnectionUrlResolver._get_verify(enforce_ssl, ssl_context)

        if client_session is None:
            async with aiohttp.ClientSession() as client:
                async with client.post(lookup_url, ssl=verify, json=client_characteristics) as result:
                    result = await result.json()
        else:
            async with client_session.post(lookup_url, ssl=verify, json=client_characteristics) as result:
                result = await result.json()

        result.raise_for_status()

        js = result.json()

        rest_url = js["urlREST"]
        websocket_url = js["urlWebSocket"]

        return rest_url, websocket_url

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
        result = aiohttp.post(lookup_url, json=client_characteristics, verify=verify)
        result.raise_for_status()

        js = result.json()

        rest_url = js["urlREST"]
        websocket_url = js["urlWebSocket"]

        return rest_url, websocket_url

    @staticmethod
    def _get_verify(enforce_ssl: bool, ssl_context):
        if ssl_context is not None:
            return ssl_context
        if enforce_ssl:
            return enforce_ssl

        return True
