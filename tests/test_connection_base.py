import pytest

from homematicip.base.base_connection import BaseConnection


@pytest.fixture
def get_base_connection():
    _auth_token = 'abc'
    _access_point_id = '123'
    return BaseConnection(_auth_token, _access_point_id)


def test_client_characteristics(get_base_connection):
    _client_char = \
        get_base_connection.client_characteristics['clientCharacteristics'][
            'applicationIdentifier']

    assert _client_char == 'homematicip-python'


def test_init_connection(get_base_connection):
    url, body = get_base_connection._init_connection()
    assert url == 'https://lookup.homematic.com:48335/getHost'
    assert isinstance(body, dict)
