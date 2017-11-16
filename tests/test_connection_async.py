import asyncio

import aiohttp
import pytest

from homematicip.async.connection import AsyncConnection
from homematicip.base.base_connection import HmipWrongHttpStatusError, HmipConnectionError, \
    ATTR_AUTH_TOKEN, ATTR_CLIENT_AUTH
from tests.fake_hmip_server import FakeLookupHmip, FakeConnectionHmip
from tests.helpers import mockreturn


@pytest.fixture
async def fake_lookup_connection(event_loop):
    server = FakeLookupHmip(loop=event_loop, base_url='lookup.homematic.com',
                            port=48335)
    connector = await server.start()
    async with aiohttp.ClientSession(connector=connector, loop=event_loop) as session:
        connection = AsyncConnection(event_loop, session=session)
        yield connection
    await server.stop()


@pytest.fixture
async def fake_connection(event_loop):
    server = FakeConnectionHmip(loop=event_loop, base_url='test.homematic.com',
                                port=None)
    connector = await server.start()
    async with aiohttp.ClientSession(connector=connector, loop=event_loop) as session:
        connection = AsyncConnection(event_loop, session=session)
        connection.headers[ATTR_AUTH_TOKEN] = ''
        connection.headers[ATTR_CLIENT_AUTH] = ''
        yield connection
    await server.stop()


@pytest.fixture
def connection(event_loop):
    _connection = AsyncConnection(event_loop)
    yield _connection
    _connection._websession.close()


@pytest.mark.asyncio
async def test_init(fake_lookup_connection):
    fake_lookup_connection.set_auth_token('auth_token')
    await fake_lookup_connection.init('accesspoint_id')
    assert fake_lookup_connection.urlWebSocket == FakeLookupHmip.host_response['urlWebSocket']


@pytest.mark.asyncio
async def test_post_200(fake_connection):
    """Test response with status 200."""
    resp = await fake_connection.api_call('https://test.homematic.com/go_200_json',
                                          body={},
                                          full_url=True)
    assert resp == FakeConnectionHmip.js_response


@pytest.mark.asyncio
async def test_post_200_no_json(fake_connection):
    resp = await fake_connection.api_call(
        'https://test.homematic.com/go_200_no_json', body=[], full_url=True)

    assert resp is True


@pytest.mark.asyncio
async def test_post_404_alt(fake_connection):
    with pytest.raises(HmipWrongHttpStatusError):
        await fake_connection.api_call('https://test.homematic.com/go_404', body={}, full_url=True)


@pytest.mark.asyncio
async def test_post_404(monkeypatch, connection):
    monkeypatch.setattr(connection._websession, 'post', mockreturn(return_status=404))
    with pytest.raises(HmipWrongHttpStatusError):
        await connection.api_call('https://test', full_url=True)


@pytest.mark.asyncio
async def test_post_exhaustive_timeout(monkeypatch, connection):
    monkeypatch.setattr(connection._websession, 'post', mockreturn(exception=asyncio.TimeoutError))
    with pytest.raises(HmipConnectionError):
        await connection.api_call('https://test', full_url=True)
