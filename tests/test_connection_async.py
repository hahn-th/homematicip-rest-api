import asyncio
import json
from json.decoder import JSONDecodeError

import pytest

from aioresponses import aioresponses

from homematicip.async.connection import Connection, \
    HmipBadResponseCodeException, HmipConnectionException


@pytest.fixture
def connection():
    _loop = asyncio.get_event_loop()
    _auth_token = 'abc'
    _access_point_id = '123'
    _connection = Connection(_loop, _auth_token, _access_point_id)
    yield _connection
    _connection._websession.close()


@pytest.fixture
def loop():
    return asyncio.get_event_loop()


mock_url = 'https://test'

response = {
    "value": 1
}


def test_post_200(connection, loop):
    """Test delete resources with status 200."""
    with aioresponses() as m:
        m.post(mock_url, status=200, body=json.dumps(response),
               headers={'content-type': 'application/json'})

        mocked_response = loop.run_until_complete(
            connection._rest_call(mock_url, full_url=True))
        assert mocked_response == response


def test_post_200_no_json(connection, loop):
    with aioresponses() as m:
        m.post(mock_url, status=200, body=json.dumps(response),
               headers={'content-type': ''})

        mocked_response = loop.run_until_complete(
            connection._rest_call(mock_url, full_url=True))
        assert mocked_response is True


def test_post_404(connection, loop):
    with aioresponses() as m:
        m.post(mock_url, status=404)

        with pytest.raises(HmipBadResponseCodeException):
            loop.run_until_complete(
                connection._rest_call(mock_url, full_url=True))


def test_post_connection_error(connection, loop):
    with aioresponses() as m:
        """Test connection error by throwing timeoutError."""
        m.post(mock_url, exception=asyncio.TimeoutError('timeout'))
        with pytest.raises(HmipConnectionException):
            loop.run_until_complete(
                connection._rest_call(mock_url, full_url=True)
            )


def test_post_json_error(connection, loop):
    with aioresponses() as m:
        m.post(mock_url, exception=JSONDecodeError('decode error', 'test', 1))
        with pytest.raises(JSONDecodeError):
            loop.run_until_complete(
                connection._rest_call(mock_url, full_url=True)
            )
