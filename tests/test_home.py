from unittest.mock import MagicMock, Mock

import pytest

from homematicip.home import Home
from homematicip.base.base_connection import BaseConnection

import json_data.home
import json

def fake_home_download_configuration():
    return json.loads(json_data.home.home_json)

@pytest.fixture
def fake_home():
    home = Home()
    home.download_configuration = fake_home_download_configuration
    home._connection = BaseConnection()
    home.get_current_state()
    return home


def test_update_event(fake_home: Home):
    fake_handler = Mock()
    fake_home.on_update(fake_handler.method)
    fake_home.fire_update_event()
    fake_handler.method.assert_called()

def test_home(fake_home: Home):
    assert fake_home.connected == True
    assert fake_home.currentAPVersion == "1.2.4"
    assert fake_home.deviceUpdateStrategy == "AUTOMATICALLY_IF_POSSIBLE"
    assert fake_home.dutyCycle == 8.0
    assert fake_home.pinAssigned == False
    assert fake_home.powerMeterCurrency == "EUR"
    assert fake_home.powerMeterUnitPrice == 0.0
    assert fake_home.timeZoneId == "Europe/Vienna"
    assert fake_home.updateState == "UP_TO_DATE"
    
    #location
    assert fake_home.location.city == "1010  Wien, \u00d6sterreich"
    assert fake_home.location.latitude == "48.208088"
    assert fake_home.location.longitude == "16.358608"

    #weather
    assert fake_home.weather.humidity == 54
    assert fake_home.weather.maxTemperature == 16.6
    assert fake_home.weather.minTemperature == 16.6
    assert fake_home.weather.temperature == 16.6
    assert fake_home.weather.weatherCondition == "LIGHT_CLOUDY"
    assert fake_home.weather.weatherDayTime == "NIGHT"
    assert fake_home.weather.windDirection == 294
    assert fake_home.weather.windSpeed == 8.568 


def test_clients(fake_home):
    client = fake_home.clients[0]
    assert client.label == 'TEST-Client'
    assert client.homeId == '00000000-0000-0000-0000-000000000001'
    assert client.id == '00000000-0000-0000-0000-000000000000'
    
#def test__parse_device(fake_home):
#    assert False
#
#
#def test_get_devices(fake_home):
#    assert False
#
#
#def test__get_clients(fake_home):
#    assert False
#
#
#def test__parse_group(fake_home):
#    assert False
#
#
#def test__get_groups(fake_home):
#    assert False
