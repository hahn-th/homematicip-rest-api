import asyncio
import hashlib
import logging
from unittest.mock import AsyncMock, Mock

import pytest

from homematicip.auth import Auth
from homematicip.connection.rest_connection import RestConnection


@pytest.mark.asyncio
async def test_async_auth_challenge_no_pin(
        fake_connection_context_with_ssl
):
    devicename = "auth_test"

    connection = RestConnection(fake_connection_context_with_ssl)

    auth = Auth(connection, fake_connection_context_with_ssl.client_auth_token, fake_connection_context_with_ssl.accesspoint_id)

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


def test_auth_logging_does_not_log_tokens_or_pin(caplog):
    connection = AsyncMock(spec=RestConnection)
    connection.async_post.side_effect = [
        Mock(status=200, json={}),
        Mock(status=200, json={"authToken": "TOPSECRET"}),
        Mock(status=200, json={"clientId": "CLIENTSECRET"}),
    ]

    auth = Auth(connection, "CLIENTAUTHSECRET", "ACCESSPOINTSECRET")
    auth.set_pin("1234")

    try:
        previous_loop = asyncio.get_event_loop_policy().get_event_loop()
    except RuntimeError:
        previous_loop = None

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _run():
        with caplog.at_level(logging.DEBUG):
            await auth.connection_request("ACCESSPOINTSECRET")
            await auth.request_auth_token()
            await auth.confirm_auth_token("TOPSECRET")

    try:
        loop.run_until_complete(_run())
    finally:
        loop.close()
        asyncio.set_event_loop(previous_loop)

    assert "TOPSECRET" not in caplog.text
    assert "CLIENTSECRET" not in caplog.text
    assert "1234" not in caplog.text
    assert "ACCESSPOINTSECRET" not in caplog.text
