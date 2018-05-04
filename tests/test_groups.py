from unittest.mock import MagicMock, Mock

import pytest

from homematicip.home import Home
from homematicip.base.base_connection import BaseConnection
from homematicip.group import *
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

def test_meta_group(fake_home):
    g = fake_home.search_group_by_id('00000000-0000-0000-0000-000000000020')
    assert isinstance(g, MetaGroup)
    assert g.label == "Badezimmer"
    assert g.lastStatusUpdate == datetime(2018, 4, 23, 20, 49, 16, 479000) + timedelta(0,utc_offset)
    assert g.lowBat == False
    assert g.metaGroup == None
    assert g.sabotage == None
    assert g.configPending == False
    assert g.unreach == False
    assert g.dutyCycle == False
    for d in g.devices:
        assert d.id in ['3014F7110000000000000025', '3014F7110000000000000016']
    for g_sub in g.groups:
        assert g_sub.id in ['00000000-0000-0000-0000-000000000021', '00000000-0000-0000-0000-000000000021']

    assert str(g) == "META Badezimmer"

    assert g._rawJSONData == fake_home_download_configuration()["groups"]["00000000-0000-0000-0000-000000000020"]

def test_heating_group(fake_home):
    g = fake_home.search_group_by_id('00000000-0000-0000-0000-000000000012')
    assert isinstance(g, HeatingGroup)
    for d in g.devices:
        assert d.id in ['3014F7110000000000000004', '3014F7110000000000000022', '3014F7110000000000000011']

    assert g.activeProfile.index == "PROFILE_1"
    assert g.activeProfile.enabled == True
    assert g.activeProfile.name == ""
    assert g.activeProfile.visible == True
    assert g.activeProfile.id == "00000000-0000-0000-0000-000000000023"
    assert g.activeProfile.groupId == "00000000-0000-0000-0000-000000000012"

    profile3 = g.profiles[2]
    assert profile3.index == 'PROFILE_3'
    assert profile3.visible == False
    assert profile3.id == '00000000-0000-0000-0000-000000000025'

    assert g.actualTemperature == 24.7
    assert g.boostDuration == 15
    assert g.boostMode == False
    assert g.controlMode == "AUTOMATIC"
    assert g.controllable == True
    assert g.cooling == False
    assert g.coolingAllowed == False
    assert g.coolingIgnored == False
    assert g.dutyCycle == False
    assert g.ecoAllowed == True
    assert g.ecoIgnored == False
    assert g.externalClockCoolingTemperature == 23.0
    assert g.externalClockEnabled == False
    assert g.externalClockHeatingTemperature == 19.0
    assert g.floorHeatingMode == "FLOOR_HEATING_STANDARD"
    assert g.humidity == 43
    assert g.humidityLimitEnabled == True
    assert g.humidityLimitValue == 60
    assert g.label == "Schlafzimmer"
    assert g.lastStatusUpdate == datetime(2018, 4, 23, 20, 48, 54, 382000) + timedelta(0,utc_offset)
    assert g.lowBat == False
    assert g.maxTemperature == 30.0
    assert g.metaGroup.id == "00000000-0000-0000-0000-000000000011"
    assert g.minTemperature == 5.0
    assert g.partyMode == False
    assert g.setPointTemperature == 5.0
    assert g.unreach == False
    assert g.valvePosition == 0.0
    assert g.windowOpenTemperature == 5.0
    assert g.windowState == "OPEN"

    assert str(g) == ('HEATING Schlafzimmer windowOpenTemperature(5.0) setPointTemperature(5.0) windowState(OPEN) motionDetected(30.0)'
                      ' sabotage(5.0) cooling(False) partyMode(False) controlMode(AUTOMATIC) actualTemperature(24.7) valvePosition(0.0)')

    assert g._rawJSONData == fake_home_download_configuration()["groups"]["00000000-0000-0000-0000-000000000012"]
