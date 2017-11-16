import asyncio
import json
from collections import namedtuple
from json.decoder import JSONDecodeError
from unittest.mock import MagicMock

import aiohttp
import pytest

from aioresponses import aioresponses

from homematicip.async.connection import AsyncConnection
from homematicip.base.base_connection import HmipWrongHttpStatusError, \
    HmipConnectionError, ATTR_AUTH_TOKEN, ATTR_CLIENT_AUTH, BaseConnection
from tests.fake_hmip_server import FakeLookupHmip, FakeConnectionHmip


# @pytest.fixture
# async def fake_lookup_server(event_loop):
#     server = FakeLookupHmip(loop=event_loop, base_url='lookup.homematic.com',
#                             port=48335)
#     connector = await server.start()
#
#     yield connector
#     event_loop.create_task(server.stop())


@pytest.fixture
async def fake_lookup_connection(event_loop):
    server = FakeLookupHmip(loop=event_loop, base_url='lookup.homematic.com',
                            port=48335)
    connector = await server.start()
    async with aiohttp.ClientSession(connector=connector,
                                     loop=event_loop) as session:
        connection = AsyncConnection(event_loop, session=session)
        yield connection
    await server.stop()


@pytest.fixture
async def fake_connection(event_loop):
    server = FakeConnectionHmip(loop=event_loop, base_url='test.homematic.com',
                                port=None)
    connector = await server.start()
    async with aiohttp.ClientSession(connector=connector,
                                     loop=event_loop) as session:
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


mock_url = 'https://test'

response = {
    "value": 1
}


@pytest.mark.asyncio
async def test_init(fake_lookup_connection):
    fake_lookup_connection.set_auth_token('auth_token')
    await fake_lookup_connection.init('accesspoint_id')
    assert fake_lookup_connection.urlWebSocket == \
           FakeLookupHmip.host_response[
               'urlWebSocket']


@pytest.mark.asyncio
async def test_post_200(fake_connection):
    """Test delete resources with status 200."""
    resp = await fake_connection.api_call(
        'https://test.homematic.com/go_200_json', body={}, full_url=True)
    assert resp == FakeConnectionHmip.js_response


def test_post_200_no_json(connection, event_loop):
    with aioresponses() as m:
        m.post(mock_url, status=200, body=json.dumps(response),
               headers={'content-type': ''})

        mocked_response = event_loop.run_until_complete(
            connection.api_call(mock_url, full_url=True))
        assert mocked_response is True


class FakeResponse:
    def __init__(self, status=200, body=None):
        self.status = status
        self.body = body

    async def release(self):
        pass


def mockreturn(return_status=None, return_body=None):
    async def mocked(path, data):
        return FakeResponse(status=return_status, body=return_body)
    return mocked


@pytest.mark.asyncio
async def test_alt_404(monkeypatch, connection):
    # async def mockreturn(path, data=None, headers=None):
    #     return FakeResponse(status=404)

    monkeypatch.setattr(connection._websession, 'post', mockreturn(return_status=404))
    with pytest.raises(HmipWrongHttpStatusError):
        await connection.api_call('https://test', full_url=True)


# def test_post_404(connection, event_loop):
#     with aioresponses() as m:
#         m.post(mock_url, status=404)
#
#         with pytest.raises(HmipWrongHttpStatusError):
#             event_loop.run_until_complete(
#                 connection.api_call(mock_url, full_url=True))

@pytest.mark.asyncio
def test_post_exhaustive_timeout(monkeypatch, connection):
    async def mockreturn(path, data=None, headers=None)

        BaseConnection._restCallRequestCounter


def test_post_connection_error(connection, event_loop):
    with aioresponses() as m:
        """Test connection error by throwing timeoutError."""
        m.post(mock_url, exception=asyncio.TimeoutError('timeout'))
        with pytest.raises(HmipConnectionError):
            event_loop.run_until_complete(
                connection.api_call(mock_url, full_url=True)
            )


def test_post_json_error(connection, event_loop):
    with aioresponses() as m:
        m.post(mock_url, exception=JSONDecodeError('decode error', 'test', 1))
        with pytest.raises(HmipConnectionError):
            event_loop.run_until_complete(
                connection.api_call(mock_url, full_url=True)
            )
