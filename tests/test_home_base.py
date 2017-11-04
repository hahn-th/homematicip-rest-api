from datetime import datetime
from unittest.mock import Mock, MagicMock

import pytest

from homematicip.base.base_device import BaseDevice
from homematicip.base.base_home import BaseHome
from homematicip.base.constants import HEATING_THERMOSTAT, SHUTTER_CONTACT, \
    WALL_MOUNTED_THERMOSTAT_PRO, SMOKE_DETECTOR, FLOOR_TERMINAL_BLOCK_6, \
    PLUGABLE_SWITCH_MEASURING, TEMPERATURE_HUMIDITY_SENSOR_DISPLAY, \
    PUSH_BUTTON, ALARM_SIREN_INDOOR, MOTION_DETECTOR_INDOOR, \
    KEY_REMOTE_CONTROL_ALARM, PLUGABLE_SWITCH, FULL_FLUSH_SHUTTER
from tests.incoming import current_state


@pytest.fixture
def base_home() -> BaseHome:
    _connection = MagicMock()
    _home = BaseHome(_connection)
    return _home


location = ['city', 'latitude', 'longitude']


@pytest.fixture
def mock_devices():
    devices = {'abc': BaseDevice(None), 'def': BaseDevice(None)}
    return devices


@pytest.fixture
def mock_group():
    return Mock()


@pytest.fixture
def mocked_class_map(monkeypatch):
    def mocked_device(key, default):
        _device = MagicMock()
        monkeypatch.setattr(_device, 'from_json', lambda: True)
        return _device

    _map = MagicMock()
    monkeypatch.setattr(_map, 'get', mocked_device)

    return _map


def test_search_device_by_id(base_home, mock_devices):
    base_home.devices = mock_devices
    _device = base_home.search_device_by_id('abc')
    assert isinstance(_device, BaseDevice)
    _device = base_home.search_device_by_id('klm')
    assert _device is None


def test_search_group_by_id():
    assert False


def test_get_devices(base_home, mocked_type_class_map):
    base_home._type_class_map = mocked_type_class_map
    base_home._get_devices(current_state)
    assert len(base_home.devices) == 4


def test__add_device():
    pass


def test_from_json():
    assert False


def test__set_security_zones_activation(base_home):
    _val = base_home._set_security_zones_activation()
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_set_security_zones_activation(base_home):
    with pytest.raises(NotImplementedError):
        base_home.set_security_zones_activation()


def test__set_location(base_home):
    _val = base_home._set_location(*location)
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_set_location(base_home):
    with pytest.raises(NotImplementedError):
        base_home.set_location(*location)


def test__set_intrusion_alert_through_smoke_detectors(base_home):
    _val = base_home._set_intrusion_alert_through_smoke_detectors()
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_set_intrusion_alert_through_smoke_detectors(base_home):
    with pytest.raises(NotImplementedError):
        base_home.set_intrusion_alert_through_smoke_detectors()


def test__activate_absence_with_period(base_home):
    _val = base_home._activate_absence_with_period(datetime.now())
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_activate_absence_with_period(base_home):
    with pytest.raises(NotImplementedError):
        base_home.activate_absence_with_period(datetime.now())


def test__activate_absence_with_duration(base_home):
    _val = base_home._activate_absence_with_duration(10)
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_activate_absence_with_duration(base_home):
    with pytest.raises(NotImplementedError):
        base_home.activate_absence_with_duration(10)


def test__deactivate_absence(base_home):
    _val = base_home._deactivate_absence()
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_deactivate_absence(base_home):
    with pytest.raises(NotImplementedError):
        base_home.deactivate_absence()


def test__activate_vacation(base_home):
    _val = base_home._activate_vacation(datetime.now(), 20)
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_activate_vacation(base_home):
    with pytest.raises(NotImplementedError):
        base_home.activate_vacation(datetime.now(), 20)


def test__deactivate_vacation(base_home):
    _val = base_home._deactivate_vacation()
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_deactivate_vacation(base_home):
    with pytest.raises(NotImplementedError):
        base_home.deactivate_vacation()


def test__set_pin(base_home):
    _val = base_home._set_pin(1234)
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_set_pin(base_home):
    with pytest.raises(NotImplementedError):
        base_home.set_pin(1234)


def test__set_zone_activation_delay(base_home):
    _val = base_home._set_zone_activation_delay(20)
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_set_zone_activation_delay(base_home):
    with pytest.raises(NotImplementedError):
        base_home.set_zone_activation_delay(20)


def test_get_security_journal(base_home):
    with pytest.raises(NotImplementedError):
        base_home.get_security_journal()


def test__get_security_journal(base_home):
    _val = base_home._get_security_journal()
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_delete_group(base_home, mock_group):
    with pytest.raises(NotImplementedError):
        base_home.delete_group(mock_group)


def test__delete_group(base_home, mock_group):
    _val = base_home._delete_group(mock_group)
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_get_OAuth_OTK(base_home):
    with pytest.raises(NotImplementedError):
        base_home.get_OAuth_OTK()


def test__get_OAuth_OTK(base_home):
    _val = base_home._get_OAuth_OTK()
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_set_timezone(base_home):
    """ sets the timezone for the AP. e.g. "Europe/Berlin" """
    with pytest.raises(NotImplementedError):
        base_home.set_timezone("Europe/Berlin")


def test__set_timezone(base_home):
    _val = base_home._set_timezone("Europe/Berlin")
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test__set_powermeter_unit_price(base_home):
    _val = base_home._set_powermeter_unit_price(10)
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)


def test_set_powermeter_unit_price(base_home):
    with pytest.raises(NotImplementedError):
        base_home.set_powermeter_unit_price(10)


def test_set_zones_device_assignment(base_home):
    """ sets the devices for the security zones
            :param internal_devices the devices which should be used for the internal zone
            :param external_devices the devices which should be used for the external(hull) zone
            :return the result of _restCall
            """
    with pytest.raises(NotImplementedError):
        base_home.set_zones_device_assignment([], [])


def test__set_zones_device_assignment(base_home):
    _val = base_home._set_zones_device_assignment([], [])
    assert isinstance(_val, tuple)
    assert len(_val) == 2
    assert isinstance(_val[0], str)
