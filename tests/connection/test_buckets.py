import asyncio

import pytest

from homematicip.connection.buckets import Buckets


@pytest.mark.asyncio
async def test_get_bucket():
    """Testing the get bucket method."""
    bucket = Buckets(2, 10)

    got_1st_token = await bucket.take()
    got_2nd_token = await bucket.take()
    got_3rd_token = await bucket.take()

    assert got_1st_token is True
    assert got_2nd_token is True
    assert got_3rd_token is False


async def test_get_bucket_with_timeout():
    """Testing the get bucket method with timeout."""
    bucket = Buckets(1, 100)

    await bucket.take()
    with pytest.raises(asyncio.TimeoutError):
        await bucket.wait_and_take(timeout=1)


async def test_get_bucket_and_wait_for_new():
    """Testing the get bucket method and waiting for new tokens."""
    bucket = Buckets(1, 1)

    got_1st_token = await bucket.take()
    got_2nd_token = await bucket.wait_and_take()

    assert got_1st_token is True
    assert got_2nd_token is True

def test_initial_tokens():
    """Testing the initial tokens of the bucket."""
    bucket = Buckets(2, 10)
    assert bucket._tokens == 2
    assert bucket.capacity == 2
    assert bucket.fill_rate == 10


@pytest.mark.asyncio
async def test_wait_and_take_no_oversubscription_under_concurrency():
    """More callers than tokens must not oversubscribe.

    Without the lock around the check + decrement, two callers can observe
    the same token count and both decrement, taking the bucket negative.
    The yield injected into ``tokens()`` deterministically opens that race
    window: every caller awaits ``tokens()`` before deciding to take, so
    without the lock they all observe the same starting value.
    """
    bucket = Buckets(tokens=5, fill_rate=3600)
    real_tokens = bucket.tokens

    async def yielding_tokens():
        result = await real_tokens()
        await asyncio.sleep(0)  # force a scheduling yield between read and decrement
        return result

    bucket.tokens = yielding_tokens

    # 20 callers competing for 5 tokens. With the lock: exactly 5 succeed,
    # 15 time out, bucket settles at 0. Without the lock: would oversubscribe.
    results = await asyncio.gather(
        *(bucket.wait_and_take(timeout=2, tokens=1) for _ in range(20)),
        return_exceptions=True,
    )

    successes = sum(1 for r in results if r is True)
    timeouts = sum(1 for r in results if isinstance(r, TimeoutError))
    assert successes == 5
    assert timeouts == 15
    assert bucket._tokens == 0  # never went negative
