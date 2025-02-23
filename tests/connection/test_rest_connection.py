from unittest.mock import AsyncMock

import httpx
import pytest

from homematicip.connection.rest_connection import RestResult, ConnectionContext, RestConnection


def test_rest_result():
    result = RestResult(status=200)
    assert result.status_text == "OK"

    result = RestResult(status=9999)
    assert result.status_text == "No status code"


def test_conn_update_connection_context(mocker):
    patched = mocker.patch("homematicip.connection.rest_connection.RestConnection._get_header")
    patched.return_value = {"test_a": "a", "test_b": "b"}

    context = ConnectionContext()
    context2 = ConnectionContext(rest_url="asdf")
    conn = RestConnection(context)

    conn.update_connection_context(context2)

    assert patched.called
    assert conn._headers == {"test_a": "a", "test_b": "b"}
    assert conn._context == context2

@pytest.mark.asyncio
async def test_conn_async_post(mocker):
    response = mocker.Mock(spec=httpx.Response)
    response.status_code = 200
    patched = mocker.patch("homematicip.connection.rest_connection.httpx.AsyncClient.post")
    patched.return_value = response

    context = ConnectionContext(rest_url="http://asdf")
    conn = RestConnection(context)

    result = await conn.async_post("url", {"a": "b"}, {"c": "d"})

    assert patched.called
    assert patched.call_args[0][0] == "http://asdf/hmip/url"
    assert patched.call_args[1] == {"json": {"a": "b"}, "headers": {"c": "d"}}
    assert result.status == 200


@pytest.mark.asyncio
async def test_conn_async_post_throttle(mocker):
    response = mocker.Mock(spec=httpx.Response)
    response.status_code = 429
    patched = mocker.patch("homematicip.connection.rest_connection.httpx.AsyncClient.post")
    patched.return_value = response

    context = ConnectionContext(rest_url="http://asdf")
    conn = RestConnection(context)

    with pytest.raises(Exception):
        await conn.async_post("url", {"a": "b"}, {"c": "d"})

@pytest.mark.asyncio
async def test_conn_async_post_with_httpx_client_session(mocker):
    response = mocker.Mock(spec=httpx.Response)
    response.status_code = 200

    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.post.return_value = response

    context = ConnectionContext(rest_url="http://asdf")
    conn = RestConnection(context, httpx_client_session=mock_client)

    result = await conn.async_post("url", {"a": "b"}, {"c": "d"})

    assert mock_client.post.called
    assert mock_client.post.call_args[0][0] == "http://asdf/hmip/url"
    assert mock_client.post.call_args[1] == {"json": {"a": "b"}, "headers": {"c": "d"}}
    assert result.status == 200