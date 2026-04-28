import asyncio
import time
from unittest.mock import AsyncMock, MagicMock

import aiohttp
import pytest

from homematicip.connection.websocket_handler import WebsocketHandler


class DummyMsg:
    def __init__(self, data, type_):
        self.data = data
        self.type = type_


def _receive_side_effect(messages):
    pending = list(messages)

    async def _receive():
        return pending.pop(0)

    return _receive


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
async def test_is_connected_true():
    client = WebsocketHandler()
    client._websocket_connected.set()
    assert client.is_connected()


@pytest.mark.asyncio
async def test_is_running_false_initial():
    client = WebsocketHandler()
    assert not client.is_running()


@pytest.mark.asyncio
async def test_handle_task_result_logs_cancelled(caplog):
    client = WebsocketHandler()
    task = MagicMock()
    task.result.side_effect = asyncio.CancelledError()
    with caplog.at_level("INFO"):
        client._handle_task_result(task)
    assert any("cancelled" in message for message in caplog.text.splitlines())


@pytest.mark.asyncio
async def test_handle_task_result_logs_exception(caplog):
    client = WebsocketHandler()
    task = MagicMock()
    task.result.side_effect = Exception("fail")
    with caplog.at_level("ERROR"):
        client._handle_task_result(task)
    assert any("Error in reconnect" in message for message in caplog.text.splitlines())


@pytest.mark.asyncio
async def test_cleanup_closes_ws_and_session():
    callback_mock = AsyncMock()
    client = WebsocketHandler()
    client._websocket_connected.set()
    client._disconnect_notified = False
    client.add_on_disconnected_handler(callback_mock)

    await client._cleanup()
    await client._cleanup()

    assert not client._websocket_connected.is_set()
    callback_mock.assert_awaited_once()


@pytest.mark.asyncio
async def test_start_and_stop(monkeypatch):
    client = WebsocketHandler()
    context = MagicMock()
    monkeypatch.setattr(client, "_connect", AsyncMock())
    await client.start(context)
    assert client._reconnect_task is not None
    assert client.is_running()
    await client.stop()
    assert client._reconnect_task is None


@pytest.mark.asyncio
async def test_start_applies_context_settings(monkeypatch):
    client = WebsocketHandler()
    context = MagicMock()
    context.websocket_heartbeat_interval = 11
    context.websocket_connect_timeout = 22
    context.websocket_message_stale_timeout = 33
    context.websocket_initial_backoff = 4
    context.websocket_max_backoff = 55
    monkeypatch.setattr(client, "_connect", AsyncMock())

    await client.start(context)

    assert client.HEARTBEAT_INTERVAL == 11
    assert client.CONNECT_TIMEOUT == 22
    assert client.MESSAGE_STALE_TIMEOUT == 33
    assert client.INITIAL_BACKOFF == 4
    assert client.MAX_BACKOFF == 55


@pytest.mark.asyncio
async def test_listen_calls_handlers():
    client = WebsocketHandler()
    handler = AsyncMock()
    client.add_on_message_handler(handler)
    ws_mock = MagicMock()
    ws_mock.receive = AsyncMock(
        side_effect=_receive_side_effect(
            [
                DummyMsg("test", type_=aiohttp.WSMsgType.TEXT),
                DummyMsg("test2", type_=aiohttp.WSMsgType.BINARY),
                DummyMsg("err", type_=aiohttp.WSMsgType.ERROR),
            ]
        )
    )

    await client._listen(ws_mock)

    handler.assert_any_await("test")
    handler.assert_any_await("test2")
    assert client.message_count() == 2
    assert client.last_message_time() is not None


@pytest.mark.asyncio
async def test_listen_stops_on_close_without_calling_handlers():
    client = WebsocketHandler()
    handler = AsyncMock()
    client.add_on_message_handler(handler)

    ws_mock = MagicMock()
    ws_mock.receive = AsyncMock(
        side_effect=_receive_side_effect(
            [
                DummyMsg(None, type_=aiohttp.WSMsgType.CLOSE),
                DummyMsg("after", type_=aiohttp.WSMsgType.TEXT),
            ]
        )
    )

    await client._listen(ws_mock)

    handler.assert_not_awaited()


@pytest.mark.asyncio
async def test_listen_logs_error_on_error_message(caplog):
    client = WebsocketHandler()
    ws_mock = MagicMock()
    ws_mock.receive = AsyncMock(
        side_effect=_receive_side_effect(
            [
                DummyMsg("bad", type_=aiohttp.WSMsgType.ERROR),
            ]
        )
    )

    with caplog.at_level("ERROR"):
        await client._listen(ws_mock)

    assert "Error in websocket" in caplog.text


@pytest.mark.asyncio
async def test_listen_stale_timeout_triggers_close_and_warning(monkeypatch, caplog):
    client = WebsocketHandler()

    ws_mock = MagicMock()
    ws_mock.close = AsyncMock()

    monkeypatch.setattr(
        asyncio,
        "wait_for",
        AsyncMock(side_effect=asyncio.TimeoutError()),
    )

    with caplog.at_level("WARNING"):
        await client._listen(ws_mock)

    ws_mock.close.assert_awaited_once()
    assert "stale-connection safety net" in caplog.text
    assert "No HomematicIP websocket events received" in caplog.text


@pytest.mark.asyncio
async def test_seconds_since_last_message_returns_none_without_messages():
    client = WebsocketHandler()
    assert client.seconds_since_last_message() is None


@pytest.mark.asyncio
async def test_handle_reconnect_updates_reason_and_attempt_count():
    client = WebsocketHandler()

    await client._handle_reconnect("connection dropped")

    assert client.reconnect_attempt_count() == 1
    assert client.last_disconnect_reason() == "connection dropped"


def test_seconds_since_last_message_works_without_running_loop():
    client = WebsocketHandler()
    client._last_message_time = time.monotonic() - 5

    elapsed = client.seconds_since_last_message()

    assert elapsed is not None
    assert 0 < elapsed < 60
