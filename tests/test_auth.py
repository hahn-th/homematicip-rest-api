import pytest

from homematicip.auth import Auth
from homematicip.connection.rest_connection import ConnectionContext, RestResult


def test_auth_init():
    context = ConnectionContext()
    auth = Auth(context)

    assert auth.connection is not None
    assert auth.headers is not None
    assert auth.client_id is not None


@pytest.mark.asyncio
async def test_connection_request(mocker):
    patched = mocker.patch("homematicip.connection.rest_connection.RestConnection.async_post")
    patched.return_value = RestResult(status=200)

    context = ConnectionContext()
    auth = Auth(context)

    result = await auth.connection_request(access_point="1234", pin="5678")

    assert patched.called
    assert patched.call_args[0][0] == "auth/connectionRequest"
    assert patched.call_args[0][1] == {"deviceId": auth.client_id, "deviceName": "homematicip-python", "sgtin": "1234"}
    assert patched.call_args[0][2] == {"content-type": "application/json", "accept": "application/json", "VERSION": "12", "PIN": "5678"}
    assert result.status == 200

@pytest.mark.asyncio
async def test_is_request_acknowledged(mocker):
    patched = mocker.patch("homematicip.connection.rest_connection.RestConnection.async_post")
    patched.return_value = RestResult(status=200)

    context = ConnectionContext()
    auth = Auth(context)

    result = await auth.is_request_acknowledged()

    assert patched.called
    assert patched.call_args[0][0] == "auth/isRequestAcknowledged"
    assert patched.call_args[0][1] == {"deviceId": auth.client_id}
    assert patched.call_args[0][2] == {"content-type": "application/json", "accept": "application/json", "VERSION": "12"}
    assert result

@pytest.mark.asyncio
async def test_request_auth_token(mocker):
    patched = mocker.patch("homematicip.connection.rest_connection.RestConnection.async_post")
    patched.return_value = RestResult(status=200, json={"authToken": "1234"})

    context = ConnectionContext()
    auth = Auth(context)

    result = await auth.request_auth_token()

    assert patched.called
    assert patched.call_args[0][0] == "auth/requestAuthToken"
    assert patched.call_args[0][1] == {"deviceId": auth.client_id}
    assert patched.call_args[0][2] == {"content-type": "application/json", "accept": "application/json", "VERSION": "12"}
    assert result == "1234"


@pytest.mark.asyncio
async def test_confirm_auth_token(mocker):
    context = ConnectionContext()
    auth = Auth(context)

    patched = mocker.patch("homematicip.connection.rest_connection.RestConnection.async_post")
    patched.return_value = RestResult(status=200, json={"clientId": auth.client_id})

    result = await auth.confirm_auth_token("1234")

    assert patched.called
    assert patched.call_args[0][0] == "auth/confirmAuthToken"
    assert patched.call_args[0][1] == {"deviceId": auth.client_id, "authToken": "1234"}
    assert patched.call_args[0][2] == {"content-type": "application/json", "accept": "application/json", "VERSION": "12"}
    assert result == auth.client_id
