import hashlib

import pytest
from conftest import no_ssl_verification

from homematicip.aio.auth import AsyncAuth
from homematicip.aio.home import AsyncHome


@pytest.mark.asyncio
async def test_async_auth_challenge_no_pin(
    event_loop, fake_async_home: AsyncHome
):
    with no_ssl_verification():
        auth = AsyncAuth(event_loop)

        sgtin = "3014F711A000000BAD0C0DED"
        devicename = "auth_test"

        await auth.init(
            sgtin, lookup_url=fake_async_home._connection._lookup_url
        )
        result = await auth.connectionRequest(devicename)

        # TODO: Investigate why result is always None
        # The response to the request should be a json data type (as indicated in the header of
        # the response). But it is actually not. So the return value is none. If there were to be any
        # an exception would be thrown.
        assert result is None

        assert (await auth.isRequestAcknowledged()) is False
        assert (await auth.isRequestAcknowledged()) is False

        await fake_async_home._connection.api_call("auth/simulateBlueButton")

        assert await auth.isRequestAcknowledged() is True

        token = await auth.requestAuthToken()
        assert (
            token
            == hashlib.sha512(auth.uuid.encode("utf-8")).hexdigest().upper()
        )

        resultId = await auth.confirmAuthToken(token)
        assert resultId == auth.uuid
