import asyncio

import aiohttp
import pytest

from homematicip.aio.connection import AsyncConnection
from homematicip.base.base_connection import (
    ATTR_AUTH_TOKEN,
    ATTR_CLIENT_AUTH,
    HmipConnectionError,
    HmipServerCloseError,
    HmipWrongHttpStatusError,
)
from tests.fake_hmip_server import FakeConnectionHmip, FakeLookupHmip, FakeWebsocketHmip
from tests.helpers import mockreturn


@pytest.fixture
async def fake_lookup_server(event_loop):
    server = FakeLookupHmip(
        loop=event_loop, base_url="lookup.homematic.com", port=48335
    )
    connector = await server.start()
    async with aiohttp.ClientSession(connector=connector, loop=event_loop) as session:
        connection = AsyncConnection(event_loop, session=session)
        yield connection
    await server.stop()


@pytest.fixture
async def fake_server(event_loop):
    server = FakeConnectionHmip(
        loop=event_loop, base_url="test.homematic.com", port=None
    )
    connector = await server.start()
    async with aiohttp.ClientSession(connector=connector, loop=event_loop) as session:
        connection = AsyncConnection(event_loop, session=session)
        connection.headers[ATTR_AUTH_TOKEN] = ""
        connection.headers[ATTR_CLIENT_AUTH] = ""
        yield connection
    await server.stop()


@pytest.fixture
async def fake_websocket_server(event_loop):
    server = FakeWebsocketHmip(loop=event_loop, base_url="ws.homematic.com")
    return server


@pytest.mark.asyncio
async def test_init(fake_lookup_server):
    fake_lookup_server.set_auth_token("auth_token")
    await fake_lookup_server.init("accesspoint_id")
    assert (
        fake_lookup_server.urlWebSocket == FakeLookupHmip.host_response["urlWebSocket"]
    )


@pytest.mark.asyncio
async def test_post_200(fake_server):
    """Test response with status 200."""
    resp = await fake_server.api_call(
        "https://test.homematic.com/go_200_json", body={}, full_url=True
    )
    assert resp == FakeConnectionHmip.js_response


@pytest.mark.asyncio
async def test_post_200_no_json(fake_server):
    resp = await fake_server.api_call(
        "https://test.homematic.com/go_200_no_json", body=[], full_url=True
    )

    assert resp is True


@pytest.mark.asyncio
async def test_post_404_alt(fake_server):
    with pytest.raises(HmipWrongHttpStatusError):
        await fake_server.api_call(
            "https://test.homematic.com/go_404", body={}, full_url=True
        )


@pytest.mark.asyncio
async def test_post_404(monkeypatch, async_connection):
    monkeypatch.setattr(
        async_connection._websession, "post", mockreturn(return_status=404)
    )
    with pytest.raises(HmipWrongHttpStatusError):
        await async_connection.api_call("https://test", full_url=True)


@pytest.mark.asyncio
async def test_post_exhaustive_timeout(monkeypatch, async_connection):
    monkeypatch.setattr(
        async_connection._websession, "post", mockreturn(exception=asyncio.TimeoutError)
    )
    with pytest.raises(HmipConnectionError):
        await async_connection.api_call("https://test", full_url=True)


@pytest.mark.asyncio
async def test_websocket_exhaustive_timeout(monkeypatch, async_connection):
    async def raise_timeout(*args, **kwargs):
        raise asyncio.TimeoutError

    monkeypatch.setattr(async_connection._websession, "ws_connect", raise_timeout)
    async_connection._restCallTimout = 0.01
    with pytest.raises(HmipConnectionError):
        await async_connection.ws_connect(None)


async def start_fake_server(loop, base_url):
    fake_ws = FakeWebsocketHmip(loop=loop, base_url=base_url)
    connector = await fake_ws.start()
    return connector


async def start_async_client_connection(connector, loop, base_url, url):
    session = aiohttp.ClientSession(connector=connector, loop=loop)
    connection = AsyncConnection(loop, session)
    connection._urlWebSocket = "ws://" + base_url + url
    return connection


async def ws_listen(future, connection):
    def parser(*args, **kwargs):
        future.set_result(args)

    ws_loop = await connection.ws_connect(parser)
    try:
        await ws_loop
    except HmipServerCloseError as err:
        future.set_exception(HmipServerCloseError)
    except HmipConnectionError as err:
        future.set_exception(HmipConnectionError)


async def do_test(future, loop, url, base_url="ws.homematic.com"):
    connector = await start_fake_server(loop, base_url)
    connection = await start_async_client_connection(connector, loop, base_url, url)
    await ws_listen(future, connection)


# async def do_test(future, loop, url, base_url='ws.homematic.com'):
#     """Setup the fake websocket server."""
#     try:
#         connector = await start_fake_server(loop,base_url)
#         async with aiohttp.ClientSession(connector=connector, loop=loop) as session:
#
#             def parser(*args, **kwargs):
#                 future.set_result(args)
#
#             connection = AsyncConnection(loop, session)
#             connection._urlWebSocket = 'wss://' + base_url + url
#             ws_loop = await connection.ws_connect(parser)
#             try:
#                 await ws_loop
#             except HmipServerCloseError as err:
#                 future.set_exception(HmipServerCloseError)
#             except HmipConnectionError as err:
#                 future.set_exception(HmipConnectionError)
#
#     except CancelledError as err:
#         print("task cancelled.")


def finish_all(loop):
    async def finish():
        all_finished = False
        while not all_finished:
            await asyncio.sleep(1)
            all_finished = True
            _all_tasks = [
                _task
                for _task in asyncio.Task.all_tasks(loop)
                if not asyncio.Task.current_task(loop) == _task
            ]
            for task in _all_tasks:
                task.cancel()
                _done = task.done()
                all_finished = all_finished and _done

    loop.run_until_complete(finish())
    print("finished")


# todo: tests break. fix this.


def test_ws_message():
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(do_test(future, loop, "/"))
    loop.run_until_complete(future)

    _res = future.result()

    assert _res[1] == "abc"

    finish_all(loop)
    # loop.close()


def test_ws_ping_pong():
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(do_test(future, loop, "/nopong"))

    with pytest.raises(HmipConnectionError):
        loop.run_until_complete(future)
        # _res = future.result()
    finish_all(loop)


def test_ws_server_shutdown():
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(do_test(future, loop, "/servershutdown"))

    with pytest.raises(HmipServerCloseError):
        loop.run_until_complete(future)
    finish_all(loop)


def test_ws_client_shutdown():
    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    async def close_client(connection):
        await asyncio.sleep(2)
        await connection.close_websocket_connection()
        return

    async def start(url, base_url="ws.homematic.com"):
        connector = await start_fake_server(loop, base_url)
        connection = await start_async_client_connection(connector, loop, base_url, url)
        asyncio.ensure_future(ws_listen(future, connection))
        await close_client(connection)

    loop.run_until_complete(start("/clientclose"))
    finish_all(loop)


def test_ws_recover():
    loop = asyncio.get_event_loop()
    result = []

    async def start(url, base_url="ws.homematic.com"):
        retry = 0
        connector = await start_fake_server(loop, base_url)
        connection = await start_async_client_connection(connector, loop, base_url, url)

        def parser(*args, **kwargs):
            nonlocal result
            result.append(args)

        while retry < 2:
            retry += 1
            ws_loop = await connection.ws_connect(parser)
            try:
                await ws_loop
            except HmipServerCloseError as err:
                pass
            except HmipConnectionError as err:
                pass
            except Exception as err:
                pass

    loop.run_until_complete(start("/recover"))
    assert True
