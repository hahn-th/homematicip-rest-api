import asyncio
import json
from json.decoder import JSONDecodeError

import aiohttp
import pytest

from aioresponses import aioresponses

from homematicip.async.connection import AsyncConnection
from homematicip.base.base_connection import HmipWrongHttpStatusError, \
    HmipConnectionError
from tests.fake_hmip_server import FakeLookupHmip


@pytest.fixture
async def fake_lookup_server(event_loop):
    server = FakeLookupHmip(loop=event_loop, base_url='lookup.homematic.com',
                               port=48335)
    connector = await server.start()
    yield connector
    event_loop.create_task(server.stop())



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
async def test_init(fake_lookup_server, event_loop):
    async with aiohttp.ClientSession(connector=fake_lookup_server,
                                     loop=event_loop) as session:
        connection = AsyncConnection(event_loop, session=session)
        connection.set_auth_token('auth_token')
        await connection.init('accesspoint_id')
        assert connection._urlWebSocket == FakeLookupHmip.get_host_response[
            'urlWebSocket']


def test_post_200(connection, event_loop):
    """Test delete resources with status 200."""
    with aioresponses() as m:
        m.post(mock_url, status=200, body=json.dumps(response),
               headers={'content-type': 'application/json'})

        mocked_response = event_loop.run_until_complete(
            connection.api_call(mock_url, full_url=True))
        assert mocked_response == response


def test_post_200_no_json(connection, event_loop):
    with aioresponses() as m:
        m.post(mock_url, status=200, body=json.dumps(response),
               headers={'content-type': ''})

        mocked_response = event_loop.run_until_complete(
            connection.api_call(mock_url, full_url=True))
        assert mocked_response is True


def test_post_404(connection, event_loop):
    with aioresponses() as m:
        m.post(mock_url, status=404)

        with pytest.raises(HmipWrongHttpStatusError):
            event_loop.run_until_complete(
                connection.api_call(mock_url, full_url=True))


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
