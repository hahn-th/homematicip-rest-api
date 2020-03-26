from unittest.mock import Mock

import pytest

from homematicip.aio.device import AsyncPlugableSwitchMeasuring
from tests.json_data.plugable_switch_measuring import (
    fake_device_id,
    fake_home_id,
    plugable_switch_measuring,
)


@pytest.fixture
def fake_switch(fake_connection):
    switch = AsyncPlugableSwitchMeasuring(fake_connection)
    return switch


def test_update_event(fake_switch):
    fake_handler = Mock()
    fake_switch.on_update(fake_handler.method)
    fake_switch.fire_update_event()
    fake_handler.method.assert_called()


@pytest.mark.asyncio
async def test_switch_on(fake_switch):
    resp = await fake_switch.turn_on()
    assert resp == "called"
    fake_switch._connection.api_call.mock.assert_called_once_with(
        "device/control/setSwitchState",
        '{"channelIndex": 1, "deviceId": null, "on": true}',
    )


@pytest.mark.asyncio
async def test_switch_off(fake_switch):
    resp = await fake_switch.turn_off()
    assert resp == "called"
    fake_switch._connection.api_call.mock.assert_called_once_with(
        "device/control/setSwitchState",
        '{"channelIndex": 1, "deviceId": null, "on": false}',
    )


def test_from_json(fake_switch):
    fake_switch.from_json(plugable_switch_measuring)
    assert fake_switch.id == fake_device_id
    assert fake_switch.energyCounter == 0.0002
    assert fake_switch.homeId == fake_home_id
