from unittest.mock import MagicMock, Mock

import pytest

from homematicip.home import Home
from homematicip.base.base_connection import BaseConnection
from homematicip.rule import *
from homematicip.EventHook import EventHook
import json
from datetime import datetime, timedelta, timezone

dt = datetime.now(timezone.utc).astimezone()
utc_offset = dt.utcoffset() // timedelta(seconds=1)

def fake_home_download_configuration():
    return json.load(open("tests/json_data/home.json"))


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
    assert fake_home.location.city == "1010  Wien, \u00d6sterreich"
    assert fake_home.location.latitude == "48.208088"
    assert fake_home.location.longitude == "16.358608"
    assert fake_home.location._rawJSONData == fake_home_download_configuration()["home"]["location"]
    assert str(fake_home.location) == "city(1010  Wien, \u00d6sterreich) latitude(48.208088) longitude(16.358608)"

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
    client = fake_home.clients[0]
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
