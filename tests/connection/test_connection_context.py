from unittest.mock import AsyncMock

import httpx
import pytest

from homematicip.connection.connection_context import ConnectionContext, ConnectionContextBuilder


@pytest.mark.asyncio
async def test_build_context_with_client_session(mocker):
    response = mocker.Mock(spec=httpx.Response)
    response.status_code = 200
    response.json.return_value = {"urlREST": "https://example.com/rest", "urlWebSocket": "wss://example.com/ws"}

    lookup_url = "https://example.com/lookup"
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.post.return_value = response

    context = await ConnectionContextBuilder.build_context_async(
        "access_point_id",
        lookup_url,
        httpx_client_session=mock_client
    )

    mock_client.post.assert_called_once()
    assert context.rest_url == "https://example.com/rest"
    assert context.websocket_url == "wss://example.com/ws"
    assert context.accesspoint_id == "access_point_id"

@pytest.mark.asyncio
async def test_build_context_without_client_session(mocker):
    response = mocker.Mock(spec=httpx.Response)
    response.status_code = 200
    response.json.return_value = {"urlREST": "https://example.com/rest", "urlWebSocket": "wss://example.com/ws"}

    patched = mocker.patch("homematicip.connection.connection_context.httpx.AsyncClient.post")
    patched.return_value = response

    context = await ConnectionContextBuilder.build_context_async("access_point_id", "https://example.com/lookup")

    patched.assert_called_once()
    assert context.rest_url == "https://example.com/rest"
    assert context.websocket_url == "wss://example.com/ws"
    assert context.accesspoint_id == "access_point_id"