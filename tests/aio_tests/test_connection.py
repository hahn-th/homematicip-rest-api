import asyncio
import logging
from asyncio import ensure_future
from unittest.mock import Mock

import pytest
from aiohttp import web

from homematicip.aio.connection import AsyncConnection
from homematicip.base.base_connection import HmipConnectionError

logging.basicConfig(level=logging.DEBUG)


async def connection_close_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await asyncio.sleep(5)

    return ws


class FakeServer:
    """Simple fake server serving at localhost.
    To be used for testing various connection management situations like:

    - unable to ping pong
    - server connection close
    - reconnect procedure.
    - etc.

    To be overridden by servers with a more specific task."""

    def __init__(self):
        self.app = None
        self.runner = None

    async def serve(self):
        self.app = web.Application()
        self._add_route()
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, "127.0.0.1", 8123)
        await site.start()
        pass

    def _add_route(self):
        self.app.add_routes([web.get("/", self.handler)])

    async def handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        async for msg in ws:
            await ws.send_str(msg)

        return ws


class NoPingServer(FakeServer):
    async def handler(self, request):
        ws = web.WebSocketResponse(autoping=False)

        await ws.prepare(request)
        async for msg in ws:
            pass
        await asyncio.sleep(1)
        return ws


class NoConnectionServer(FakeServer):
    async def close_server(self, connection, delay=2):
        await asyncio.sleep(delay)
        await connection.close()

    async def handler(self, request):
        ws = web.WebSocketResponse()
        ensure_future(self.close_server(ws))
        await ws.prepare(request)
        async for msg in ws:
            pass
        return ws


class SingleMessageServer(FakeServer):
    async def handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.send_bytes(b"this is a message")
        await asyncio.sleep(3)
        return ws


@pytest.fixture
async def simple_server():
    simple = FakeServer()
    await simple.serve()

    yield

    await simple.runner.cleanup()


@pytest.fixture
async def no_ping_server():
    no_ping = NoPingServer()
    await no_ping.serve()

    yield

    await no_ping.runner.cleanup()


@pytest.fixture
async def connection_lost_server():
    no_connection = NoConnectionServer()
    await no_connection.serve()

    yield

    await no_connection.runner.cleanup()


@pytest.fixture
async def single_message_server():
    single_message = SingleMessageServer()
    await single_message.serve()

    yield

    await single_message.runner.cleanup()


@pytest.fixture
async def client_connection(event_loop):
    connection = AsyncConnection(event_loop)
    connection._urlWebSocket = "ws://localhost:8123/"
    connection.ping_timeout = 1
    yield connection

    await connection._websession.close()


async def ws_listen(connection, on_message=None):
    if on_message is None:
        on_message = Mock()

    def on_error(*args, **kwargs):
        pass

    ws_loop = await connection.ws_connect(on_message=on_message, on_error=on_error)

    return ws_loop


@pytest.mark.asyncio
async def test_ws_no_pong(no_ping_server, client_connection):
    listener = await ws_listen(client_connection)

    assert client_connection.ws_connected

    with pytest.raises(HmipConnectionError):
        await listener
    assert client_connection.ping_pong_task.done()
    assert client_connection.ws_reader_task.done()
    assert not client_connection.ws_connected
    res = listener.result
    pass


@pytest.mark.asyncio
async def test_connection_lost(connection_lost_server, client_connection):
    listener = await ws_listen(client_connection)
    assert client_connection.ws_connected

    with pytest.raises(HmipConnectionError):
        await listener

    assert client_connection.ping_pong_task.done()
    assert client_connection.ws_reader_task.done()
    assert not client_connection.ws_connected


@pytest.mark.asyncio
async def test_user_disconnect_and_reconnect(simple_server, client_connection):
    async def close_connection():
        await asyncio.sleep(2)
        await client_connection.close_websocket_connection()

    listener = await ws_listen(client_connection)
    assert client_connection.ws_connected

    ensure_future(close_connection())

    with pytest.raises(HmipConnectionError):
        await listener

    assert client_connection.ping_pong_task.done()
    assert client_connection.ws_reader_task.done()
    assert not client_connection.ws_connected

    # Now try to reconnect again.

    listener = await ws_listen(client_connection)

    assert client_connection.ws_connected
    ensure_future(close_connection())

    with pytest.raises(HmipConnectionError):
        await listener


@pytest.mark.asyncio
async def test_ws_message(single_message_server, client_connection):
    on_message_mock = Mock()
    listener = await ws_listen(client_connection, on_message=on_message_mock)
    assert client_connection.ws_connected

    with pytest.raises(HmipConnectionError):
        await listener

    assert client_connection.ping_pong_task.done()
    assert client_connection.ws_reader_task.done()
    assert not client_connection.ws_connected

    on_message_mock.assert_called_once_with(None, "this is a message")
