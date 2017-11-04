from unittest.mock import Mock, MagicMock

import asyncio

from homematicip.async.connection import Connection
import pytest

from homematicip.async.device import PluggableSwitch


@pytest.fixture
def mock_connection():
    mocked = Mock(spec=Connection)
    mocked._rest_call = asyncio.coroutine(MagicMock(return_value='called'))
    return mocked


@pytest.mark.asyncio
async def test_switch_on(mock_connection):
    switch = PluggableSwitch(mock_connection)
    resp = await switch.turn_on()
    assert resp == 'called'


@pytest.mark.asyncio
async def test_switch_off(mock_connection):
    switch = PluggableSwitch(mock_connection)
    resp = await switch.turn_off()
    assert resp == 'called'


@pytest.mark.asyncio
async def test_set_label(mock_connection):
    switch = PluggableSwitch(mock_connection)
    resp = await switch.set_label("label")
    assert resp == 'called'
