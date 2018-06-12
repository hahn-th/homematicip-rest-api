import pytest

from homematicip.aio.home import AsyncHome
from homematicip.EventHook import EventHook
from homematicip.aio.auth import AsyncAuth

import json
from datetime import datetime, timedelta, timezone
from conftest import no_ssl_verification


@pytest.mark.asyncio
async def test_async_auth_challenge_no_pin(event_loop,fake_async_home:AsyncHome):
    with no_ssl_verification():
        auth = AsyncAuth(event_loop)


        sgtin = "3014F711A000000BAD0C0DED"
        devicename = "auth_test"

        await auth.init(sgtin, lookup_url=fake_async_home._connection._lookup_url)
        result = await auth.connectionRequest(devicename)
        #TODO: Investigate why result is always None


        #assert result.status_code == 200
        #assert (await auth.isRequestAcknowledged()) == False
        #assert (await auth.isRequestAcknowledged()) == False

        #fake_async_home._connection.api_call("auth/simulateBlueButton")

        #assert await auth.isRequestAcknowledged() == True

        #token = auth.requestAuthToken()
        #assert await token == hashlib.sha512(auth.uuid.encode('utf-8')).hexdigest().upper()

        #resultId = auth.confirmAuthToken(token)
        #assert await resultId == auth.uuid