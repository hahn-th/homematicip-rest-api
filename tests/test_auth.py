import hashlib

import pytest

from homematicip.auth import Auth
from homematicip.connection_v2.connection_context import ConnectionContext


@pytest.mark.asyncio
async def test_async_auth_challenge_no_pin(
        fake_connection_context_with_ssl
):
    devicename = "auth_test"

    auth = Auth(fake_connection_context_with_ssl)

    result = await auth.connection_request(devicename)
    assert result.status == 200

    assert (await auth.is_request_acknowledged()) is False
    assert (await auth.is_request_acknowledged()) is False

    await auth.connection.async_post("auth/simulateBlueButton")

    assert await auth.is_request_acknowledged() is True

    token = await auth.request_auth_token()
    assert token == hashlib.sha512(auth.client_id.encode("utf-8")).hexdigest().upper()

    result_id = await auth.confirm_auth_token(token)
    assert result_id == auth.client_id
