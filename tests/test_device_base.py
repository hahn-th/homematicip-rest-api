import json
from unittest.mock import MagicMock

import pytest

from homematicip.base.base_device import BaseDevice


@pytest.fixture
def base_device():
    _connection = MagicMock()
    return BaseDevice(_connection)


@pytest.fixture
def base_device_with_id(base_device):
    base_device.id = 'abc'
    return base_device


@pytest.fixture
def js():
    js = {}
    js["id"] = 10
    js["homeId"] = 10
    js["label"] = 'abc'
    js["lastStatusUpdate"] = 1509092579.767934
    js["type"] = 10
    js["updateState"] = 'state'
    js["firmwareVersion"] = 123
    js["availableFirmwareVersion"] = 345
    js['functionalChannels'] = []
    return js


def test_from_json(base_device, js):
    assert base_device.id is None
    base_device.from_json(js)
    assert base_device.id == js['id']


def test_set_label(base_device_with_id):
    with pytest.raises(NotImplementedError):
        base_device_with_id.set_label('abc')


def test__set_label(base_device_with_id):
    _val = base_device_with_id._set_label('abc')
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_is_update_applicable(base_device_with_id):
    with pytest.raises(NotImplementedError):
        base_device_with_id.is_update_applicable()


def test__is_update_applicable(base_device_with_id):
    _val = base_device_with_id._is_update_applicable()
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_authorizeUpdate(base_device_with_id):
    with pytest.raises(NotImplementedError):
        base_device_with_id.authorizeUpdate()


def test__authorizeUpdate(base_device_with_id):
    _val = base_device_with_id._authorizeUpdate()
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_delete(base_device_with_id):
    with pytest.raises(NotImplementedError):
        base_device_with_id.delete()


def test__delete(base_device_with_id):
    _val = base_device_with_id._delete()
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_set_router_module_enabled(base_device_with_id):
    with pytest.raises(NotImplementedError):
        base_device_with_id.set_router_module_enabled(True)


def test__set_router_module_enabled(base_device_with_id):
    _val = base_device_with_id._set_router_module_enabled(True)
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)
