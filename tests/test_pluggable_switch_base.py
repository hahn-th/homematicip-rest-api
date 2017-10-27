import pytest

from unittest.mock import MagicMock
from homematicip.base.base_device import BasePluggableSwitch


@pytest.fixture
def plugable_switch() -> BasePluggableSwitch:
    mock = MagicMock()
    _switch = BasePluggableSwitch(mock)
    return _switch


def test_switch_on(plugable_switch):
    url, data = plugable_switch._turn_on()
    assert url == "device/control/setSwitchState"
    assert data == {"channelIndex": 1, "deviceId": None, "on": True}


def test_switch_off(plugable_switch):
    url, data = plugable_switch._turn_off()
    assert url == "device/control/setSwitchState"
    assert data == {"channelIndex": 1, "deviceId": None, "on": False}
