import pytest
import json

from homematicip.async.connection import AsyncConnection
from homematicip.async.device import AsyncPlugableSwitchMeasuring
from tests.helpers import mockreturn
from tests.json_data.plugable_switch_measuring import \
    plugable_switch_measuring, fake_device_id, fake_home_id


@pytest.fixture
def connection(event_loop,monkeypatch):
    _connection = AsyncConnection(event_loop)
    monkeypatch.setattr(_connection._websession, 'post',
                        mockreturn(return_status=200,content_type=None))
    yield _connection
    _connection._websession.close()


@pytest.mark.asyncio
async def test_switch_on(connection):
    switch = AsyncPlugableSwitchMeasuring(connection)
    resp = await switch.turn_on()
    assert resp == True


@pytest.mark.asyncio
async def test_switch_off(connection):
    switch = AsyncPlugableSwitchMeasuring(connection)
    resp = await switch.turn_off()
    assert resp == True

def test_from_json(connection):
    switch = AsyncPlugableSwitchMeasuring(connection)
    switch.from_json(plugable_switch_measuring)
    assert switch.id == fake_device_id
    assert switch.energyCounter == 0.0002
    assert switch.homeId == fake_home_id