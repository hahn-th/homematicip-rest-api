import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from homematicip.connection.websocket_handler import WebsocketHandler


class DummyMsg:
    def __init__(self, data, type_):
        self.data = data
        self.type = type_


@pytest.mark.asyncio
async def test_add_on_message_handler():
    client = WebsocketHandler()
    handler = MagicMock()
    client.add_on_message_handler(handler)
    assert handler in client._on_message_handlers


@pytest.mark.asyncio
async def test_is_connected_false_initial():
    client = WebsocketHandler()
    assert not client.is_connected()


@pytest.mark.asyncio
async def test_is_connected_true(monkeypatch):
    client = WebsocketHandler()
    client._websocket_connected.set()
    assert client.is_connected()

@pytest.mark.asyncio
async def test_handle_task_result_logs_cancelled(caplog):
    client = WebsocketHandler()
    task = MagicMock()
    task.result.side_effect = asyncio.CancelledError()
    with caplog.at_level('INFO'):
        client._handle_task_result(task)
    assert any('cancelled' in m for m in caplog.text.splitlines())


@pytest.mark.asyncio
async def test_handle_task_result_logs_exception(caplog):
    client = WebsocketHandler()
    task = MagicMock()
    task.result.side_effect = Exception('fail')
    with caplog.at_level('ERROR'):
        client._handle_task_result(task)
    assert any('Error in reconnect' in m for m in caplog.text.splitlines())


@pytest.mark.asyncio
async def test_cleanup_closes_ws_and_session(monkeypatch):
    callback_mock = AsyncMock()
    client = WebsocketHandler()
    client._websocket_connected.set()
    client.add_on_disconnected_handler(callback_mock)

    await client._cleanup()

    assert not client._websocket_connected.is_set()
    callback_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_start_and_stop(monkeypatch):
    client = WebsocketHandler()
    context = MagicMock()
    monkeypatch.setattr(client, '_connect', AsyncMock())
    await client.start(context)
    assert client._reconnect_task is not None
    await client.stop()
    assert client._reconnect_task is None


@pytest.mark.asyncio
async def test_listen_calls_handlers(monkeypatch):
    client = WebsocketHandler()
    handler = AsyncMock()
    client.add_on_message_handler(handler)
    ws_mock = MagicMock()
    ws_mock.__aiter__.return_value = [
        DummyMsg('test', type_=aiohttp.WSMsgType.TEXT),
        DummyMsg('test2', type_=aiohttp.WSMsgType.BINARY),
        DummyMsg('err', type_=aiohttp.WSMsgType.ERROR)
    ]
    with patch('logging.Logger.debug'), patch('logging.Logger.error'):
        await client._listen(ws_mock)
    handler.assert_any_await('test')
    handler.assert_any_await('test2')
