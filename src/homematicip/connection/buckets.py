import asyncio
import time


class Buckets:
    """Class to manage the rate limiting of the HomematicIP Cloud API.
    The implementation is based on the token bucket algorithm."""

    def __init__(self, tokens, fill_rate):
        """Initialize the Buckets with a token bucket algorithm.

        :param tokens: The number of tokens in the bucket.
        :param fill_rate: The fill rate of the bucket in tokens every x seconds."""
        self.capacity = tokens
        self._tokens = tokens
        self.fill_rate = fill_rate
        self.timestamp = time.time()
        self.lock = asyncio.Lock()

    async def take(self, tokens=1) -> bool:
        """Get a single token from the bucket. Return True if successful, False otherwise.

        :param tokens: The number of tokens to take from the bucket. Default is 1.
        :return: True if successful, False otherwise.
        """
        async with self.lock:
            if tokens <= await self.tokens():
                self._tokens -= tokens
                return True
        return False

    async def wait_and_take(self, timeout=120, tokens=1) -> bool:
        """Wait until a token is available and then take it. Return True if successful, False otherwise.

        :param timeout: The maximum time to wait for a token in seconds. Default is 120 seconds.
        :param tokens: The number of tokens to take from the bucket. Default is 1.
        :return: True if successful, False otherwise.
        """
        start_time = time.time()
        while True:
            if tokens <= await self.tokens():
                self._tokens -= tokens
                return True

            if time.time() - start_time > timeout:
                raise asyncio.TimeoutError("Timeout while waiting for token.")

            await asyncio.sleep(1)  # Wait for a second before checking again

    async def tokens(self):
        """Get the number of tokens in the bucket. Refill the bucket if necessary."""
        if self._tokens < self.capacity:
            now = time.time()
            delta = int((now - self.timestamp) / self.fill_rate)
            if delta > 0:
                self._tokens = min(self.capacity, self._tokens + delta)
                self.timestamp = now
        return self._tokens
