import pytest

from homematicip.async.device import AsyncPlugableSwitchMeasuring
from tests.json_data.plugable_switch_measuring import \
    plugable_switch_measuring, fake_device_id, fake_home_id





@pytest.mark.asyncio
async def test_switch_on(fake_connection):
    switch = AsyncPlugableSwitchMeasuring(fake_connection)
    resp = await switch.turn_on()
    assert resp == 'called'
    fake_connection.api_call.mock.assert_called_once_with(
        'device/control/setSwitchState', '{"channelIndex": 1, "deviceId": null, "on": true}')

@pytest.mark.asyncio
async def test_switch_off(fake_connection):
    switch = AsyncPlugableSwitchMeasuring(fake_connection)
    resp = await switch.turn_off()
    assert resp == 'called'
    fake_connection.api_call.mock.assert_called_once_with(
        'device/control/setSwitchState', '{"channelIndex": 1, "deviceId": null, "on": false}')


def test_from_json(fake_connection):
    switch = AsyncPlugableSwitchMeasuring(fake_connection)
    switch.from_json(plugable_switch_measuring)
    assert switch.id == fake_device_id
    assert switch.energyCounter == 0.0002
    assert switch.homeId == fake_home_id
