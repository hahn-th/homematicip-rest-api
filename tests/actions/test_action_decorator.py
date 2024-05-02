import pytest

from homematicip.action.action import Action
from homematicip.model.devices import Device
from homematicip.model.functional_channels import FunctionalChannel
from homematicip.model.group import Group
from homematicip.model.hmip_base import HmipBaseModel


@Action.allowed_types("ACCELERATION_SENSOR")
def func1(runner, test, ret_val: bool):
    return ret_val


@Action.allowed_types("ACCELERATION_SENSOR", "SHUTTER_CONTACT", "HUMIDITY_SENSOR")
def func2(runner, test, ret_val: bool):
    return ret_val

def test_object_not_hmip_base_model():
    with pytest.raises(ValueError):
        func1(None, "asdf", True)

def test_object_no_type_field():
    class Test(HmipBaseModel):
        pass

    with pytest.raises(ValueError):
        func1(None, Test(), True)

def test_allowed_types_functional_channel():
    fc = FunctionalChannel(index=1, groupIndex=1, label="", groups=[], deviceId="asdf",
                           functionalChannelType="ACCELERATION_SENSOR")
    assert func1(None, fc, True) is True

    fc = FunctionalChannel(index=1, groupIndex=1, label="", groups=[], deviceId="asdf",
                           functionalChannelType="SHUTTER_CONTACT")
    with pytest.raises(ValueError):
        func1(None, fc, True)


def test_allowed_types_device():
    d = Device(deviceType="asdf", functionalChannels={}, homeId="asdf", id="asdf", label="asdf",
               type="ACCELERATION_SENSOR")
    assert func1(None, d, True) is True

    d = Device(deviceType="asdf", functionalChannels={}, homeId="asdf", id="asdf", label="asdf",
               type="SHUTTER_CONTACT")
    with pytest.raises(ValueError):
        func1(None, d, True)


def test_allowed_types_group():
    g = Group(id="asdf", homeId="asdf", channels=[], type="ACCELERATION_SENSOR")
    assert func1(None, g, True) is True

    g = Group(id="asdf", homeId="asdf", channels=[], type="SHUTTER_CONTACT")
    with pytest.raises(ValueError):
        func1(None, g, True)


def test_allowed_types_multiple():
    fc = FunctionalChannel(index=1, groupIndex=1, label="", groups=[], deviceId="asdf",
                           functionalChannelType="ACCELERATION_SENSOR")
    assert func2(None, fc, True) is True

    fc = FunctionalChannel(index=1, groupIndex=1, label="", groups=[], deviceId="asdf",
                           functionalChannelType="SHUTTER_CONTACT")
    assert func2(None, fc, True) is True

    fc = FunctionalChannel(index=1, groupIndex=1, label="", groups=[], deviceId="asdf",
                           functionalChannelType="HUMIDITY_SENSOR")
    assert func2(None, fc, True) is True

    fc = FunctionalChannel(index=1, groupIndex=1, label="", groups=[], deviceId="asdf",
                           functionalChannelType="LIGHT_SENSOR")
    with pytest.raises(ValueError):
        func2(None, fc, True)

