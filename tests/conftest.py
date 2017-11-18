import pytest

from unittest.mock import MagicMock
from homematicip.async.connection import AsyncConnection


def AsyncMock(*args, **kwargs):
    m = MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro


@pytest.fixture
def fake_connection(event_loop):
    _connection = AsyncConnection(event_loop)
    _connection.api_call = AsyncMock(return_value='called')
    return _connection