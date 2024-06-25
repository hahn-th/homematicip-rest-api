import httpx

from homematicip.connection.rate_limited_rest_connection import RateLimitedRestConnection
from homematicip.connection.rest_connection import ConnectionContext


async def test_send_single_request(mocker):
    response = mocker.Mock(spec=httpx.Response)
    response.status_code = 200
    patched = mocker.patch("homematicip.connection.rest_connection.httpx.AsyncClient.post")
    patched.return_value = response

    context = ConnectionContext(rest_url="http://asdf")
    conn = RateLimitedRestConnection(context, 1, 1)

    result = await conn.async_post("url", {"a": "b"}, {"c": "d"})

    assert patched.called
    assert patched.call_args[0][0] == "http://asdf/hmip/url"
    assert patched.call_args[1] == {"json": {"a": "b"}, "headers": {"c": "d"}}
    assert result.status == 200


async def test_send_and_wait_requests(mocker):
    response = mocker.Mock(spec=httpx.Response)
    response.status_code = 200
    patched = mocker.patch("homematicip.connection.rest_connection.httpx.AsyncClient.post")
    patched.return_value = response

    context = ConnectionContext(rest_url="http://asdf")
    conn = RateLimitedRestConnection(context, 1, 1)

    await conn.async_post("url", {"a": "b"}, {"c": "d"})
    await conn.async_post("url", {"a": "b"}, {"c": "d"})
    await conn.async_post("url", {"a": "b"}, {"c": "d"})

    assert patched.call_count == 3