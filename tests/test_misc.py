import pytest

from homematicip.base.enums import *
from homematicip.base.helpers import bytes2str, detect_encoding
from homematicip.base.homematicip_object import HomeMaticIPObject
from homematicip.EventHook import EventHook


def event_hook_handler2(mustBe2):
    assert mustBe2 == 2


def event_hook_handler3(mustBe3):
    assert mustBe3 == 3


def test_event_hook():
    eh = EventHook()
    eh += event_hook_handler2
    eh.fire(2)
    eh += event_hook_handler3
    eh -= event_hook_handler2
    eh.fire(3)


def test_detect_encoding():
    testString = "This is my special string to test the encoding"
    assert detect_encoding(testString.encode("utf-8")) == "utf-8"
    assert detect_encoding(testString.encode("utf-8-sig")) == "utf-8-sig"
    assert detect_encoding(testString.encode("utf-16")) == "utf-16"
    assert detect_encoding(testString.encode("utf-32")) == "utf-32"
    assert detect_encoding(testString.encode("utf-16-be")) == "utf-16-be"
    assert detect_encoding(testString.encode("utf-32-be")) == "utf-32-be"
    assert detect_encoding(testString.encode("utf-16-le")) == "utf-16-le"
    assert detect_encoding(testString.encode("utf-32-le")) == "utf-32-le"


def test_bytes2str():
    testString = "This is my special string to test the encoding"
    assert bytes2str(testString.encode("utf-8")) == testString
    assert bytes2str(testString.encode("utf-8-sig")) == testString
    assert bytes2str(testString.encode("utf-16")) == testString
    assert bytes2str(testString.encode("utf-32")) == testString
    assert bytes2str(testString.encode("utf-16-be")) == testString
    assert bytes2str(testString.encode("utf-32-be")) == testString
    assert bytes2str(testString.encode("utf-16-le")) == testString
    assert bytes2str(testString.encode("utf-32-le")) == testString
    assert bytes2str(testString) == testString
    with pytest.raises(TypeError):
        assert bytes2str(44) == testString


def test_auto_name_enum():
    assert DeviceType.from_str("PUSH_BUTTON") == DeviceType.PUSH_BUTTON
    assert DeviceType.from_str(None) is None
    assert DeviceType.from_str("I_DONT_EXIST", DeviceType.DEVICE) == DeviceType.DEVICE
    assert DeviceType.from_str("I_DONT_EXIST_EITHER") is None
