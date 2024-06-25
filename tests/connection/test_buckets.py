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

    got_1st_token = await bucket.take()
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
