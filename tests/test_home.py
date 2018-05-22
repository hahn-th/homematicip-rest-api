from unittest.mock import MagicMock, Mock

import pytest

from homematicip.home import Home
from homematicip.base.base_connection import BaseConnection
from homematicip.rule import *
from homematicip.EventHook import EventHook
import json
from datetime import datetime, timedelta, timezone
from conftest import fake_home_download_configuration, no_ssl_verification


dt = datetime.now(timezone.utc).astimezone()
utc_offset = dt.utcoffset() // timedelta(seconds=1)

def test_update_event(fake_home: Home):
    fake_handler = Mock()
    fake_home.on_update(fake_handler.method)
    fake_home.fire_update_event()
    fake_handler.method.assert_called()

def test_home_base(fake_home: Home):
    assert fake_home.connected == True
    assert fake_home.currentAPVersion == "1.2.4"
    assert fake_home.deviceUpdateStrategy == "AUTOMATICALLY_IF_POSSIBLE"
    assert fake_home.dutyCycle == 8.0
    assert fake_home.pinAssigned == False
    assert fake_home.powerMeterCurrency == "EUR"
    assert fake_home.powerMeterUnitPrice == 0.0
    assert fake_home.timeZoneId == "Europe/Vienna"
    assert fake_home.updateState == "UP_TO_DATE"

    assert fake_home._rawJSONData == fake_home_download_configuration()["home"]

def test_home_location(fake_home: Home):
    assert fake_home.location.city == "1010  Wien, österreich"
    assert fake_home.location.latitude == "48.208088"
    assert fake_home.location.longitude == "16.358608"
    assert fake_home.location._rawJSONData == fake_home_download_configuration()["home"]["location"]
    assert str(fake_home.location) == "city(1010  Wien, österreich) latitude(48.208088) longitude(16.358608)"

def test_home_set_location(fake_home: Home):
    with no_ssl_verification():
        fake_home.set_location("Berlin, Germany", "52.530644", "13.383068")
        fake_home.get_current_state()
        assert fake_home.location.city == "Berlin, Germany"
        assert fake_home.location.latitude == "52.530644"
        assert fake_home.location.longitude == "13.383068"
        assert str(fake_home.location) == "city(Berlin, Germany) latitude(52.530644) longitude(13.383068)"

def test_home_weather(fake_home: Home):
    assert fake_home.weather.humidity == 54
    assert fake_home.weather.maxTemperature == 16.6
    assert fake_home.weather.minTemperature == 16.6
    assert fake_home.weather.temperature == 16.6
    assert fake_home.weather.weatherCondition == "LIGHT_CLOUDY"
    assert fake_home.weather.weatherDayTime == "NIGHT"
    assert fake_home.weather.windDirection == 294
    assert fake_home.weather.windSpeed == 8.568 
    assert fake_home.weather._rawJSONData == fake_home_download_configuration()["home"]["weather"]
    assert str(fake_home.weather) == "temperature(16.6) weatherCondition(LIGHT_CLOUDY) weatherDayTime(NIGHT) minTemperature(16.6) maxTemperature(16.6) humidity(54) windSpeed(8.568) windDirection(294)"

def test_clients(fake_home):
    client = fake_home.search_client_by_id('00000000-0000-0000-0000-000000000000')
    assert client.label == 'TEST-Client'
    assert client.homeId == '00000000-0000-0000-0000-000000000001'
    assert client.id == '00000000-0000-0000-0000-000000000000'
    assert client.refreshToken == None

    assert client._rawJSONData == fake_home_download_configuration()["clients"]['00000000-0000-0000-0000-000000000000']
    assert str(client) == "label(TEST-Client)"

def test_rules(fake_home):
    rule = fake_home.search_rule_by_id('00000000-0000-0000-0000-000000000065')
    assert rule.active == True
    assert rule.label == 'Alarmanlage'
    assert isinstance(rule,SimpleRule)
    assert rule.ruleErrorCategories == []
    assert rule.errorRuleTriggerItems == []
    assert rule.errorRuleConditionItems == []
    assert rule.errorRuleActionItems == []

    assert str(rule) == "SIMPLE Alarmanlage active(True)"