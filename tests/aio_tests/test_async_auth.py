import hashlib

import pytest


@pytest.mark.asyncio
async def test_async_auth_challenge_no_pin(
    no_ssl_fake_async_auth, no_ssl_fake_async_home
):

    auth = no_ssl_fake_async_auth

    sgtin = "3014F711A000000BAD0C0DED"
    devicename = "auth_test"

    await auth.init(sgtin, lookup_url=no_ssl_fake_async_home._connection._lookup_url)
    result = await auth.connectionRequest(devicename)

    # The response to the request should be a json data type (as indicated in the header of
    # the response). But it is actually not. So the return value is none. If there were to be any error
    # an exception would be thrown.
    assert result is None

    assert (await auth.isRequestAcknowledged()) is False
    assert (await auth.isRequestAcknowledged()) is False

    await no_ssl_fake_async_home._connection.api_call("auth/simulateBlueButton")

    assert await auth.isRequestAcknowledged() is True

    token = await auth.requestAuthToken()
    assert token == hashlib.sha512(auth.uuid.encode("utf-8")).hexdigest().upper()

    result_id = await auth.confirmAuthToken(token)
    assert result_id == auth.uuid
