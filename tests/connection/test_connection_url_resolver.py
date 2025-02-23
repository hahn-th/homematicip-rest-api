from http.client import responses

import pytest
import httpx
from unittest.mock import AsyncMock, patch
from homematicip.connection.connection_url_resolver import ConnectionUrlResolver


@pytest.mark.asyncio
async def test_lookup_urls_async_with_client_session(mocker):
    response = mocker.Mock(spec=httpx.Response)
    response.status_code = 200
    response.json.return_value = {"urlREST": "https://example.com/rest", "urlWebSocket": "wss://example.com/ws"}
    client_characteristics = {
        "clientCharacteristics": {
            "apiVersion": "10",
            "applicationIdentifier": "homematicip-python",
            "applicationVersion": "1.0",
            "deviceManufacturer": "none",
            "deviceType": "Computer",
            "language": "en_US",
            "osType": "Linux",
            "osVersion": "5.4.0-42-generic",
        },
        "id": "access_point_id",
    }
    lookup_url = "https://example.com/lookup"
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.post.return_value = response

    rest_url, websocket_url = await ConnectionUrlResolver.lookup_urls_async(
        client_characteristics,
        lookup_url,
        httpx_client_session=mock_client
    )

    mock_client.post.assert_called_once_with(lookup_url, json=client_characteristics)
    assert rest_url == "https://example.com/rest"
    assert websocket_url == "wss://example.com/ws"


@pytest.mark.asyncio
async def test_lookup_urls_async_without_client_session(mocker):
    response = mocker.Mock(spec=httpx.Response)
    response.status_code = 200
    response.json.return_value = {"urlREST": "https://example.com/rest", "urlWebSocket": "wss://example.com/ws"}

    patched = mocker.patch("homematicip.connection.connection_url_resolver.httpx.AsyncClient.post")
    patched.return_value = response

    client_characteristics = {
        "clientCharacteristics": {
            "apiVersion": "10",
            "applicationIdentifier": "homematicip-python",
            "applicationVersion": "1.0",
            "deviceManufacturer": "none",
            "deviceType": "Computer",
            "language": "en_US",
            "osType": "Linux",
            "osVersion": "5.4.0-42-generic",
        },
        "id": "access_point_id",
    }
    lookup_url = "https://example.com/lookup"

    rest_url, websocket_url = await ConnectionUrlResolver.lookup_urls_async(
        client_characteristics,
        lookup_url
    )

    patched.assert_called_once_with(lookup_url, json=client_characteristics)
    assert rest_url == "https://example.com/rest"
    assert websocket_url == "wss://example.com/ws"
