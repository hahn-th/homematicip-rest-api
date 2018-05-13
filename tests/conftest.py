import pytest
import json
from unittest.mock import MagicMock
from homematicip.async.connection import AsyncConnection
from homematicip.home import Home
from homematicip.base.base_connection import BaseConnection

def AsyncMock(*args, **kwargs):
    m = MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro

def fake_home_download_configuration():
    return json.load(open("tests/json_data/home.json", encoding="UTF-8"))

@pytest.fixture
def fake_home():
    home = Home()
    home.download_configuration = fake_home_download_configuration
    home._connection = BaseConnection()
    home.get_current_state()
    return home

@pytest.fixture
def fake_connection(event_loop):
    _connection = AsyncConnection(event_loop)
    _connection.api_call = AsyncMock(return_value='called')
    return _connection

@pytest.fixture
def async_connection(event_loop):
    _connection = AsyncConnection(event_loop)
    yield _connection
    _connection._websession.close()
