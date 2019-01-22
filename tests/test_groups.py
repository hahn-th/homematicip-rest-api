import pytest

from homematicip.group import *
from homematicip.home import Home
import json
from datetime import datetime, timedelta, timezone

from conftest import fake_home_download_configuration, no_ssl_verification, utc_offset


def test_meta_group(fake_home : Home):
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
    assert g.incorrectPositioned == None
    for d in g.devices:
        assert d.id in ['3014F7110000000000000025', '3014F7110000000000000016', '3014F7110000000000000050']
    for g_sub in g.groups:
        assert g_sub.id in ['00000000-0000-0000-0000-000000000021', '00000000-0000-0000-0000-000000000021']

    assert str(g) == "META Badezimmer"

    assert g._rawJSONData == fake_home_download_configuration()["groups"]["00000000-0000-0000-0000-000000000020"]

def test_heating_group(fake_home : Home):
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
    assert g.controlMode == ClimateControlMode.AUTOMATIC
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

    assert str(g) == ('HEATING Schlafzimmer: windowOpenTemperature(5.0) setPointTemperature(5.0) windowState(OPEN) motionDetected(30.0)'
                      ' sabotage(5.0) cooling(False) partyMode(False) controlMode(AUTOMATIC) actualTemperature(24.7) valvePosition(0.0)')

    assert g._rawJSONData == fake_home_download_configuration()["groups"]["00000000-0000-0000-0000-000000000012"]

    with no_ssl_verification():
        g.set_boost_duration(20)
        g.set_boost(True)
        g.set_active_profile(3)
        g.set_point_temperature(10.5)
        g.set_control_mode(ClimateControlMode.MANUAL)

        fake_home.get_current_state()
        g = fake_home.search_group_by_id('00000000-0000-0000-0000-000000000012')
        assert g.boostDuration == 20
        assert g.boostMode == True
        assert g.activeProfile.index == "PROFILE_4"
        assert g.setPointTemperature == 10.5
        assert g.controlMode == ClimateControlMode.MANUAL

        fake_home.delete_group(g)
        fake_home.get_current_state()
        gNotFound = fake_home.search_group_by_id('00000000-0000-0000-0000-000000000012')
        assert gNotFound == None

        result = g.set_boost_duration(20)
        assert result["errorCode"] == 'INVALID_GROUP'

        result = g.set_boost(True)
        assert result["errorCode"] == 'INVALID_GROUP'

        result = g.set_active_profile(1)
        assert result["errorCode"] == 'INVALID_GROUP'

        result = g.set_point_temperature(10.5)
        assert result["errorCode"] == 'INVALID_GROUP'

        result = g.set_control_mode(ClimateControlMode.MANUAL)
        assert result["errorCode"] == 'INVALID_GROUP'



def test_security_group(fake_home : Home):
    g = fake_home.search_group_by_id('00000000-0000-0000-0000-000000000009')
    assert isinstance(g, SecurityGroup)
    for d in g.devices:
        assert d.id in ['3014F7110000000000000001', '3014F7110000000000000019']

    assert g.dutyCycle == False
    assert g.homeId == "00000000-0000-0000-0000-000000000001"
    assert g.id == "00000000-0000-0000-0000-000000000009"
    assert g.label == "Büro"
    assert g.lastStatusUpdate == datetime(2018, 4, 23, 20, 37, 34, 304000) + timedelta(0,utc_offset)
    assert g.lowBat == False
    assert g.metaGroup.id == "00000000-0000-0000-0000-000000000008"
    assert g.motionDetected == None
    assert g.presenceDetected == None
    assert g.sabotage == False
    assert g.smokeDetectorAlarmType == SmokeDetectorAlarmType.IDLE_OFF
    assert g.unreach == False
    assert g.windowState == "CLOSED"

    assert str(g) == ('SECURITY Büro: windowState(CLOSED) motionDetected(None) presenceDetected(None) sabotage(False)'
                      ' smokeDetectorAlarmType(IDLE_OFF) dutyCycle(False) lowBat(False) powerMainsFailure(None) moistureDetected(None) waterlevelDetected(None)')

def test_switching_group(fake_home : Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id('00000000-0000-0000-0000-000000000018')
        assert isinstance(g, SwitchingGroup)
        for d in g.devices:
            assert d.id in ['3014F7110000000000000010', '3014F7110000000000000009', '3014F7110000000000000008']

        assert g.dimLevel == None
        assert g.dutyCycle == False
        assert g.homeId == "00000000-0000-0000-0000-000000000001"
        assert g.id == "00000000-0000-0000-0000-000000000018"
        assert g.label == "Strom"
        assert g.lastStatusUpdate == datetime(2018, 4, 23, 20, 49, 14, 56000) + timedelta(0,utc_offset)
        assert g.lowBat == None
        assert g.metaGroup.id == "00000000-0000-0000-0000-000000000017"
        assert g.on == True
        assert g.processing == None
        assert g.shutterLevel == None
        assert g.slatsLevel == None
        assert g.unreach == False

        assert str(g) == ('SWITCHING Strom: on(True) dimLevel(None) processing(None) shutterLevel(None) slatsLevel(None)'
                          ' dutyCycle(False) lowBat(None)')

        g.turn_off()
        g.set_label("NEW GROUP")
        g.set_shutter_level(50)
        fake_home.get_current_state()
        g = fake_home.search_group_by_id('00000000-0000-0000-0000-000000000018')
        assert g.on == False
        assert g.label == "NEW GROUP"
        assert g.shutterLevel == 50

        assert str(g) == ('SWITCHING NEW GROUP: on(False) dimLevel(None) processing(None) shutterLevel(50) slatsLevel(None)'
                          ' dutyCycle(False) lowBat(None)')
        g.turn_on()
        fake_home.get_current_state()
        g = fake_home.search_group_by_id('00000000-0000-0000-0000-000000000018')
        assert g.on == True

        
        fake_home.delete_group(g)
        fake_home.get_current_state()
        gNotFound = fake_home.search_group_by_id('00000000-0000-0000-0000-000000000018')
        assert gNotFound == None

        result = g.delete()
        assert result["errorCode"] == 'INVALID_GROUP'

        result = g.set_label('LABEL')
        assert result["errorCode"] == 'INVALID_GROUP'

        result = g.turn_off()
        assert result["errorCode"] == 'INVALID_GROUP'

        result = g.set_shutter_level(50)
        assert result["errorCode"] == 'INVALID_GROUP'

def test_environment_group(fake_home : Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id('00000000-AAAA-0000-0000-000000000001')
        assert isinstance(g, EnvironmentGroup)

        assert g.actualTemperature == 15.4
        assert g.illumination == 4703.0
        assert g.raining == False
        assert g.humidity == 65
        assert g.windSpeed == 29.1

        assert str(g) == "ENVIRONMENT Terrasse: actualTemperature(15.4) illumination(4703.0) raining(False) windSpeed(29.1) humidity(65)"

def test_heating_dehumidifier_group(fake_home : Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id('00000000-0000-0000-0000-000000000055')
        assert isinstance(g, HeatingDehumidifierGroup)
        assert g.on == None
        assert str(g) == "HEATING_DEHUMIDIFIER HEATING_DEHUMIDIFIER: on(None)"

def test_heating_cooling_demand_pump_group(fake_home : Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id('00000000-0000-0000-0000-000000000057')
        assert isinstance(g, HeatingCoolingDemandPumpGroup)
        assert g.on == None
        assert g.heatDemandRuleEnabled == False
        assert g.pumpFollowUpTime == 2
        assert g.pumpLeadTime == 2
        assert g.pumpProtectionDuration == 1
        assert g.pumpProtectionSwitchingInterval == 14
        assert str(g) == ("HEATING_COOLING_DEMAND_PUMP HEATING_COOLING_DEMAND_PUMP: on(None) pumpProtectionDuration(1)"
                         " pumpProtectionSwitchingInterval(14) pumpFollowUpTime(2) pumpLeadTime(2)"
                         " heatDemandRuleEnabled(False)")

def test_all_groups_implemented(fake_home : Home):
    for g in fake_home.groups:
        assert type(g) != Group

