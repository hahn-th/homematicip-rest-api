import json
from datetime import datetime, timedelta, timezone

import pytest

from conftest import utc_offset
from homematicip.group import *
from homematicip.home import Home
from homematicip_demo.helper import (
    fake_home_download_configuration,
    no_ssl_verification,
)


def test_meta_group(fake_home: Home):
    g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000020")
    assert isinstance(g, MetaGroup)
    assert g.label == "Badezimmer"
    assert g.lastStatusUpdate == datetime(2018, 4, 23, 20, 49, 16, 479000) + timedelta(
        0, utc_offset
    )
    assert g.lowBat is False
    assert g.metaGroup is None
    assert g.sabotage is None
    assert g.configPending is False
    assert g.unreach is False
    assert g.dutyCycle is False
    assert g.incorrectPositioned is None
    for d in g.devices:
        assert d.id in [
            "3014F7110000000000000025",
            "3014F7110000000000000016",
            "3014F7110000000000000050",
        ]
    for g_sub in g.groups:
        assert g_sub.id in [
            "00000000-0000-0000-0000-000000000021",
            "00000000-0000-0000-0000-000000000021",
        ]

    assert str(g) == "META Badezimmer"

    assert (
        g._rawJSONData
        == fake_home_download_configuration()["groups"][
            "00000000-0000-0000-0000-000000000020"
        ]
    )


def test_heating_group(fake_home: Home):
    g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000012")
    assert isinstance(g, HeatingGroup)
    for d in g.devices:
        assert d.id in [
            "3014F7110000000000000004",
            "3014F7110000000000000022",
            "3014F7110000000000000008",
        ]

    assert g.activeProfile.index == "PROFILE_1"
    assert g.activeProfile.enabled is True
    assert g.activeProfile.name == "STD"
    assert g.activeProfile.visible is True
    assert g.activeProfile.id == "00000000-0000-0000-0000-000000000023"
    assert g.activeProfile.groupId == "00000000-0000-0000-0000-000000000012"

    profile3 = g.profiles[2]
    assert profile3.index == "PROFILE_3"
    assert profile3.visible is False
    assert profile3.id == "00000000-0000-0000-0000-000000000025"

    assert g.actualTemperature == 24.7
    assert g.boostDuration == 15
    assert g.boostMode is False
    assert g.controlMode == ClimateControlMode.AUTOMATIC
    assert g.controllable is True
    assert g.cooling is False
    assert g.coolingAllowed is False
    assert g.coolingIgnored is False
    assert g.dutyCycle is False
    assert g.ecoAllowed is True
    assert g.ecoIgnored is False
    assert g.externalClockCoolingTemperature == 23.0
    assert g.externalClockEnabled is False
    assert g.externalClockHeatingTemperature == 19.0
    assert g.floorHeatingMode == "FLOOR_HEATING_STANDARD"
    assert g.humidity == 43
    assert g.humidityLimitEnabled is True
    assert g.humidityLimitValue == 60
    assert g.label == "Schlafzimmer"
    assert g.lastStatusUpdate == datetime(2018, 4, 23, 20, 48, 54, 382000) + timedelta(
        0, utc_offset
    )
    assert g.lowBat is False
    assert g.maxTemperature == 30.0
    assert g.metaGroup.id == "00000000-0000-0000-0000-000000000011"
    assert g.minTemperature == 5.0
    assert g.partyMode is False
    assert g.setPointTemperature == 5.0
    assert g.unreach is False
    assert g.valvePosition == 0.0
    assert g.windowOpenTemperature == 5.0
    assert g.windowState == "OPEN"
    assert g.lastSetPointReachedTimestamp == datetime.fromtimestamp(
        1557767559939 / 1000.0
    )
    assert g.lastSetPointUpdatedTimestamp == datetime.fromtimestamp(
        1557767559939 / 1000.0
    )

    assert str(g) == (
        "HEATING Schlafzimmer windowOpenTemperature(5.0) setPointTemperature(5.0) windowState(OPEN) motionDetected(30.0)"
        " sabotage(5.0) cooling(False) partyMode(False) controlMode(AUTOMATIC) actualTemperature(24.7) valvePosition(0.0)"
    )

    assert (
        g._rawJSONData
        == fake_home_download_configuration()["groups"][
            "00000000-0000-0000-0000-000000000012"
        ]
    )

    with no_ssl_verification():
        g.set_boost_duration(20)
        g.set_boost(True)
        g.set_active_profile(3)
        g.set_point_temperature(10.5)
        g.set_control_mode(ClimateControlMode.MANUAL)

        fake_home.get_current_state()
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000012")
        assert g.boostDuration == 20
        assert g.boostMode is True
        assert g.activeProfile.index == "PROFILE_4"
        assert g.setPointTemperature == 10.5
        assert g.controlMode == ClimateControlMode.MANUAL

        fake_home.delete_group(g)
        fake_home.get_current_state()
        gNotFound = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000012")
        assert gNotFound is None

        result = g.set_boost_duration(20)
        assert result["errorCode"] == "INVALID_GROUP"

        result = g.set_boost(True)
        assert result["errorCode"] == "INVALID_GROUP"

        result = g.set_active_profile(1)
        assert result["errorCode"] == "INVALID_GROUP"

        result = g.set_point_temperature(10.5)
        assert result["errorCode"] == "INVALID_GROUP"

        result = g.set_control_mode(ClimateControlMode.MANUAL)
        assert result["errorCode"] == "INVALID_GROUP"


def test_security_group(fake_home: Home):
    g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000009")
    assert isinstance(g, SecurityGroup)
    for d in g.devices:
        assert d.id in ["3014F7110000000000000001", "3014F7110000000000000019"]

    assert g.dutyCycle is False
    assert g.homeId == "00000000-0000-0000-0000-000000000001"
    assert g.id == "00000000-0000-0000-0000-000000000009"
    assert g.label == "Büro"
    assert g.lastStatusUpdate == datetime(2018, 4, 23, 20, 37, 34, 304000) + timedelta(
        0, utc_offset
    )
    assert g.lowBat is False
    assert g.metaGroup.id == "00000000-0000-0000-0000-000000000008"
    assert g.motionDetected is None
    assert g.presenceDetected is None
    assert g.sabotage is False
    assert g.smokeDetectorAlarmType == SmokeDetectorAlarmType.IDLE_OFF
    assert g.unreach is False
    assert g.windowState == "CLOSED"

    assert str(g) == (
        "SECURITY Büro windowState(CLOSED) motionDetected(None) presenceDetected(None) sabotage(False)"
        " smokeDetectorAlarmType(IDLE_OFF) dutyCycle(False) lowBat(False) powerMainsFailure(None) moistureDetected(None) waterlevelDetected(None)"
    )


def test_extended_linked_garage_door(fake_home: Home):
    g = fake_home.search_group_by_id("b27049fd-ba6c-4fed-0000-eb063742ff75")
    assert isinstance(g, ExtendedLinkedGarageDoorGroup)

    assert g.dutyCycle is None
    assert g.homeId == "00000000-0000-0000-0000-000000000001"
    assert g.id == "b27049fd-ba6c-4fed-0000-eb063742ff75"
    assert g.label == "Garagengruppe"
    assert g.lowBat is None
    assert g.metaGroup.id == "00000000-0000-0000-0000-000000000008"
    assert g.unreach is None
    assert g.ventilationPositionSupported == False

    assert str(g) == (
        "EXTENDED_LINKED_GARAGE_DOOR Garagengruppe doorState(None) dutyCycle(None) lowBat(None) ventilationPositionSupported(False)"
    )


def test_security_zone(fake_home: Home):
    g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000005")
    assert isinstance(g, SecurityZoneGroup)  # asserts groupType also
    for d in g.devices:
        assert d.id in [
            "3014F7110000000000000000",
            "3014F7110000000000000001",
            "3014F7110000000000000002",
            "3014F7110000000000000003",
            "3014F7110000000000000004",
            "3014F7110000000000000005",
            "3014F7110000000000000006",
        ]

    assert g.homeId == "00000000-0000-0000-0000-000000000001"
    assert g.id == "00000000-0000-0000-0000-000000000005"
    assert g.label == "EXTERNAL"
    assert g.lastStatusUpdate == datetime(2018, 4, 23, 20, 48, 46, 498000) + timedelta(
        0, utc_offset
    )
    assert g.metaGroup is None
    assert g.unreach is False

    assert g.active is False
    assert g.silent is True
    assert g.windowState == "OPEN"
    assert g.motionDetected is None
    assert g.sabotage is False
    assert len(g.ignorableDevices) == 0
    assert g.presenceDetected is None  # not in from_json()?

    assert str(g) == (
        "SECURITY_ZONE EXTERNAL active(False) silent(True) windowState(OPEN)"
        " motionDetected(None) sabotage(False) presenceDetected(None) ignorableDevices(#0)"
    )


def test_switching_group(fake_home: Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000018")
        assert isinstance(g, SwitchingGroup)
        for d in g.devices:
            assert d.id in [
                "3014F7110000000000000010",
                "3014F7110000000000000009",
                "3014F7110000000000000008",
            ]

        assert g.dimLevel is None
        assert g.dutyCycle is False
        assert g.homeId == "00000000-0000-0000-0000-000000000001"
        assert g.id == "00000000-0000-0000-0000-000000000018"
        assert g.label == "Strom"
        assert g.lastStatusUpdate == datetime(
            2018, 4, 23, 20, 49, 14, 56000
        ) + timedelta(0, utc_offset)
        assert g.lowBat is None
        assert g.metaGroup.id == "00000000-0000-0000-0000-000000000017"
        assert g.on is True
        assert g.processing is False
        assert g.shutterLevel is None
        assert g.slatsLevel is None
        assert g.unreach is False
        assert g.primaryShadingLevel == 1.0
        assert g.primaryShadingStateType == ShadingStateType.POSITION_USED
        assert g.secondaryShadingLevel == None
        assert g.secondaryShadingStateType == ShadingStateType.NOT_EXISTENT

        assert str(g) == (
            "SWITCHING Strom on(True) dimLevel(None) dutyCycle(False) lowBat(None)"
            " processing(False) shutterLevel(None) slatsLevel(None)"
        )

        g.turn_off()
        g.set_label("NEW GROUP")
        g.set_shutter_level(50)
        fake_home.get_current_state()
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000018")
        assert g.on is False
        assert g.label == "NEW GROUP"
        assert g.shutterLevel == 50

        assert str(g) == (
            "SWITCHING NEW GROUP on(False) dimLevel(None) dutyCycle(False) lowBat(None)"
            " processing(False) shutterLevel(50) slatsLevel(None)"
        )
        g.turn_on()
        g.set_slats_level(1.0, 20)

        fake_home.get_current_state()
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000018")
        assert g.on is True
        assert g.slatsLevel == 1.0
        assert g.shutterLevel == 20
        g.set_shutter_stop()

        fake_home.delete_group(g)
        fake_home.get_current_state()
        gNotFound = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000018")
        assert gNotFound is None

        result = g.delete()
        assert result["errorCode"] == "INVALID_GROUP"

        result = g.set_label("LABEL")
        assert result["errorCode"] == "INVALID_GROUP"

        result = g.turn_off()
        assert result["errorCode"] == "INVALID_GROUP"

        result = g.set_shutter_level(50)
        assert result["errorCode"] == "INVALID_GROUP"

        result = g.set_slats_level(1.0, 20)
        assert result["errorCode"] == "INVALID_GROUP"


def test_shutter_profile(fake_home: Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000093")
        assert isinstance(g, ShutterProfile)

        assert g.dutyCycle is False
        assert g.homeId == "00000000-0000-0000-0000-000000000001"
        assert g.label == "Rollladen Schiebet\u00fcr"
        assert g.lowBat is None
        assert g.metaGroup is None
        assert g.processing is False
        assert g.shutterLevel == 0.97
        assert g.slatsLevel is None
        assert g.unreach is False
        assert g.primaryShadingLevel == 0.97
        assert g.primaryShadingStateType == ShadingStateType.POSITION_USED
        assert g.secondaryShadingLevel is None
        assert g.secondaryShadingStateType == ShadingStateType.NOT_EXISTENT
        assert g.profileMode == ProfileMode.AUTOMATIC

        assert str(g) == (
            "SHUTTER_PROFILE Rollladen Schiebetür processing(False)"
            " shutterLevel(0.97) slatsLevel(None) profileMode(AUTOMATIC)"
        )

        g.set_shutter_level(0.5)
        g.set_profile_mode(ProfileMode.MANUAL)
        fake_home.get_current_state()
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000093")
        assert g.shutterLevel == 0.5
        assert g.profileMode == ProfileMode.MANUAL

        assert str(g) == (
            "SHUTTER_PROFILE Rollladen Schiebetür processing(False)"
            " shutterLevel(0.5) slatsLevel(None) profileMode(MANUAL)"
        )

        g.set_slats_level(1.0, 0.4)

        fake_home.get_current_state()
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000093")
        assert g.slatsLevel == 1.0
        assert g.shutterLevel == 0.4
        g.set_shutter_stop()


def test_environment_group(fake_home: Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id("00000000-AAAA-0000-0000-000000000001")
        assert isinstance(g, EnvironmentGroup)

        assert g.actualTemperature == 15.4
        assert g.illumination == 4703.0
        assert g.raining is False
        assert g.humidity == 65
        assert g.windSpeed == 29.1

        assert (
            str(g)
            == "ENVIRONMENT Terrasse actualTemperature(15.4) illumination(4703.0) raining(False) windSpeed(29.1) humidity(65)"
        )


def test_heating_dehumidifier_group(fake_home: Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000055")
        assert isinstance(g, HeatingDehumidifierGroup)
        assert g.on is None
        assert str(g) == "HEATING_DEHUMIDIFIER HEATING_DEHUMIDIFIER on(None)"


def test_heating_cooling_demand_pump_group(fake_home: Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000057")
        assert isinstance(g, HeatingCoolingDemandPumpGroup)
        assert g.on is None
        assert g.pumpFollowUpTime == 2
        assert g.pumpLeadTime == 2
        assert g.pumpProtectionDuration == 1
        assert g.pumpProtectionSwitchingInterval == 14
        assert str(g) == (
            "HEATING_COOLING_DEMAND_PUMP HEATING_COOLING_DEMAND_PUMP on(None) pumpProtectionDuration(1)"
            " pumpProtectionSwitchingInterval(14) pumpFollowUpTime(2) pumpLeadTime(2)"
        )


def test_switching_alarm_group(fake_home: Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000022")
        assert isinstance(g, AlarmSwitchingGroup)

        assert g.signalAcoustic == AcousticAlarmSignal.FREQUENCY_RISING
        assert g.signalOptical == OpticalAlarmSignal.DOUBLE_FLASHING_REPEATING
        assert str(g) == (
            "ALARM_SWITCHING SIREN on(False) dimLevel(None) onTime(180.0) "
            "signalAcoustic(FREQUENCY_RISING) signalOptical(DOUBLE_FLASHING_REPEATING) "
            "smokeDetectorAlarmType(IDLE_OFF) acousticFeedbackEnabled(True)"
        )

        g.test_signal_acoustic(AcousticAlarmSignal.FREQUENCY_HIGHON_OFF)
        g.test_signal_optical(OpticalAlarmSignal.BLINKING_ALTERNATELY_REPEATING)

        g.set_signal_acoustic(AcousticAlarmSignal.FREQUENCY_HIGHON_OFF)
        g.set_signal_optical(OpticalAlarmSignal.BLINKING_ALTERNATELY_REPEATING)
        g.set_on_time(5)

        fake_home.get_current_state()
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000022")

        assert g.signalAcoustic == AcousticAlarmSignal.FREQUENCY_HIGHON_OFF
        assert g.signalOptical == OpticalAlarmSignal.BLINKING_ALTERNATELY_REPEATING
        assert g.onTime == 5

        g.id = "00000000-0000-0000-0000-BADBADBADB22"
        result = g.set_signal_acoustic(AcousticAlarmSignal.FREQUENCY_HIGHON_OFF)
        assert result["errorCode"] == "INVALID_GROUP"

        result = g.set_signal_optical(OpticalAlarmSignal.BLINKING_ALTERNATELY_REPEATING)
        assert result["errorCode"] == "INVALID_GROUP"

        result = g.test_signal_acoustic(AcousticAlarmSignal.FREQUENCY_HIGHON_OFF)
        assert result["errorCode"] == "INVALID_GROUP"

        result = g.test_signal_optical(
            OpticalAlarmSignal.BLINKING_ALTERNATELY_REPEATING
        )
        assert result["errorCode"] == "INVALID_GROUP"


def test_heating_failure_alert_group(fake_home: Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id("00000000-BBBB-0000-0000-000000000052")
        assert str(g) == (
            "HEATING_FAILURE_ALERT_RULE_GROUP HEATING_FAILURE_ALERT_RULE_GROUP"
            " enabled(True) heatingFailureValidationResult(NO_HEATING_FAILURE)"
            " checkInterval(600) validationTimeout(86400000)"
            " lastExecutionTimestamp(2019-02-21 19:30:00.084000)"
        )


def test_humidity_warning_rule_group(fake_home: Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id("00000000-0000-0000-AAAA-000000000029")
        assert str(g) == (
            "HUMIDITY_WARNING_RULE_GROUP Büro enabled(True) "
            "humidityValidationResult(LESSER_LOWER_THRESHOLD) "
            "humidityLowerThreshold(40) humidityUpperThreshold(60) "
            "triggered(False) lastExecutionTimestamp(2019-02-28 22:05:05.665000) "
            "lastStatusUpdate(2019-02-28 22:08:24.260000) ventilationRecommended(True)"
        )
        assert g.outdoorClimateSensor is None

        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000049")
        d = fake_home.search_device_by_id("3014F7110000000000000038")
        assert g.outdoorClimateSensor == d


def test_extended_linked_shutter_group(fake_home: Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000050")

        assert g.groupVisibility == GroupVisibility.VISIBLE
        assert g.dutyCycle is False
        assert g.label == "Rollos"
        assert g.primaryShadingLevel == 1.0
        assert g.primaryShadingStateType == ShadingStateType.POSITION_USED
        assert g.secondaryShadingLevel is None
        assert g.secondaryShadingStateType == ShadingStateType.NOT_EXISTENT
        assert g.slatsLevel is None
        assert g.shutterLevel == 1.0
        assert g.topShutterLevel == 0.0
        assert g.topSlatsLevel == 0.0
        assert g.bottomShutterLevel == 1.0
        assert g.bottomSlatsLevel == 1.0

        assert (
            str(g)
            == "EXTENDED_LINKED_SHUTTER Rollos shutterLevel(1.0) slatsLevel(None)"
        )

        g.set_slats_level(1.2, 10)
        fake_home.get_current_state()
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000050")

        assert g.slatsLevel == 1.2
        assert g.shutterLevel == 10

        g.set_shutter_stop()
        g.set_shutter_level(30)
        fake_home.get_current_state()
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000050")
        assert g.shutterLevel == 30


def test_access_authorization_profile_group(fake_home: Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000032")
        assert g.label == "Walter"
        assert g.active == True
        assert g.authorizationPinAssigned == True
        assert g.authorized == True


def test_access_control_group(fake_home: Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000033")
        assert g.label == "AmHaustuere2"


def test_hot_water(fake_home: Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000067")
        assert g.profileMode is None

        g.set_profile_mode(ProfileMode.AUTOMATIC)
        fake_home.get_current_state()
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-000000000067")
        assert g.profileMode == ProfileMode.AUTOMATIC

        assert (
            str(g)
            == "HOT_WATER HOT_WATER on(None) onTime(900.0) profileMode(AUTOMATIC)"
        )


def test_indoor_climate_group(fake_home: Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-0000000000IC")
        assert g.label == "Stanovanje"
        assert g.sabotage == False
        assert g.ventilationLevel == 0.5
        assert g.ventilationState == None
        assert g.windowState == WindowState.CLOSED
        assert (
            str(g)
            == "INDOOR_CLIMATE Stanovanje sabotage(False) ventilationLevel(0.5) ventilationState(None) windowState(CLOSED)"
        )

def test_energy_group(fake_home: Home):
    with no_ssl_verification():
        g = fake_home.search_group_by_id("00000000-0000-0000-0000-0000000000EN")
        assert g.label == "EnergyGroupHWR"
        assert isinstance(g, EnergyGroup)


def test_all_groups_implemented(fake_home: Home):
    for g in fake_home.groups:
        assert type(g) != Group
