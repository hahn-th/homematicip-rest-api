import json

from homematicip.connection_v2 import RATE_LIMITER_FILL_RATE, RATE_LIMITER_TOKENS
from homematicip.connection_v2.buckets import Buckets
from homematicip.connection_v2.rest_connection import RestConnection, RestResult
from homematicip.connection_v2.connection_context import ConnectionContext


class RateLimitedRestConnection(RestConnection):

    def __init__(self,
                 context: ConnectionContext,
                 tokens: int = RATE_LIMITER_TOKENS,
                 fill_rate: int = RATE_LIMITER_FILL_RATE):
        """Initialize the RateLimitedRestConnection with a token bucket algorithm.

        :param context: The connection_v2 context.
        :param tokens: The number of tokens in the bucket. Default is 10.
        :param fill_rate: The fill rate of the bucket in tokens per second. Default is 8."""
        super().__init__(context)
        self._buckets = Buckets(tokens=tokens, fill_rate=fill_rate)

    async def async_post(self, url: str, data: json = None, custom_header: dict = None) -> RestResult:
        """Post data to the HomematicIP Cloud API."""
        await self._buckets.wait_and_take()
        return await super().async_post(url, data, custom_header)