import httpx

from homematicip.connection import RATE_LIMITER_FILL_RATE, RATE_LIMITER_TOKENS
from homematicip.connection.buckets import Buckets
from homematicip.connection.connection_context import ConnectionContext
from homematicip.connection.rest_connection import RestConnection, RestResult


class RateLimitedRestConnection(RestConnection):

    def __init__(self,
                 context: ConnectionContext,
                 tokens: int = RATE_LIMITER_TOKENS,
                 fill_rate: int = RATE_LIMITER_FILL_RATE,
                 httpx_client_session: httpx.AsyncClient | None = None):
        """Initialize the RateLimitedRestConnection with a token bucket algorithm.

        :param context: The connection context.
        :param tokens: The number of tokens in the bucket. Default is 10.
        :param fill_rate: The fill rate of the bucket in tokens per second. Default is 8.
        :param httpx_client_session: The httpx client session if you want to use a custom one.
        """
        super().__init__(context, httpx_client_session=httpx_client_session)
        self._buckets = Buckets(tokens=tokens, fill_rate=fill_rate)

    async def async_post(self, url: str, data: dict | None = None, custom_header: dict | None = None) -> RestResult:
        """Post data to the HomematicIP Cloud API."""
        await self._buckets.wait_and_take()
        return await super().async_post(url, data, custom_header)
