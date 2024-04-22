import json
from datetime import datetime, timedelta, timezone

import pytest

from conftest import utc_offset
from homematicip.aio.group import *
from homematicip.aio.home import AsyncHome
from homematicip.base.base_connection import HmipWrongHttpStatusError
from homematicip.base.enums import *


def test_all_groups_implemented(no_ssl_fake_async_home: AsyncHome):
    for g in no_ssl_fake_async_home.groups:
        assert type(g) != AsyncGroup


@pytest.mark.asyncio
async def test_heating_group(no_ssl_fake_async_home: AsyncHome):
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000012"
    )
    assert isinstance(g, AsyncHeatingGroup)
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

    await g.set_boost_duration(20)
    await g.set_boost(True)
    await g.set_active_profile(3)
    await g.set_point_temperature(10.5)
    await g.set_control_mode(ClimateControlMode.MANUAL)
    await no_ssl_fake_async_home.get_current_state()
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000012"
    )
    assert g.boostDuration == 20
    assert g.boostMode is True
    assert g.activeProfile.index == "PROFILE_4"
    assert g.setPointTemperature == 10.5
    assert g.controlMode == ClimateControlMode.MANUAL

    await no_ssl_fake_async_home.delete_group(g)
    await no_ssl_fake_async_home.get_current_state()
    gNotFound = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000012"
    )
    assert gNotFound is None

    with pytest.raises(HmipWrongHttpStatusError):
        result = await g.set_boost_duration(20)

    with pytest.raises(HmipWrongHttpStatusError):
        result = await g.set_boost(True)

    with pytest.raises(HmipWrongHttpStatusError):
        result = await g.set_active_profile(1)

    with pytest.raises(HmipWrongHttpStatusError):
        result = await g.set_point_temperature(10.5)

    with pytest.raises(HmipWrongHttpStatusError):
        result = await g.set_control_mode(ClimateControlMode.MANUAL)


@pytest.mark.asyncio
async def test_switching_group(no_ssl_fake_async_home: AsyncHome):
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000018"
    )
    assert isinstance(g, AsyncSwitchingGroup)
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
    assert g.lastStatusUpdate == datetime(2018, 4, 23, 20, 49, 14, 56000) + timedelta(
        0, utc_offset
    )
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

    await g.turn_off()
    await g.set_label("NEW GROUP")
    await g.set_shutter_level(50)
    await no_ssl_fake_async_home.get_current_state()
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000018"
    )

    await g.set_shutter_stop()

    assert g.on is False
    assert g.label == "NEW GROUP"
    assert g.shutterLevel == 50

    assert str(g) == (
        "SWITCHING NEW GROUP on(False) dimLevel(None) dutyCycle(False) lowBat(None)"
        " processing(False) shutterLevel(50) slatsLevel(None)"
    )

    await g.turn_on()
    await g.set_slats_level(1.0, 20)
    await no_ssl_fake_async_home.get_current_state()
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000018"
    )
    assert g.on is True
    assert g.slatsLevel == 1.0
    assert g.shutterLevel == 20

    await no_ssl_fake_async_home.delete_group(g)
    await no_ssl_fake_async_home.get_current_state()
    gNotFound = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000018"
    )
    assert gNotFound is None

    with pytest.raises(HmipWrongHttpStatusError):
        result = await g.delete()
    with pytest.raises(HmipWrongHttpStatusError):
        result = await g.set_label("LABEL")
    with pytest.raises(HmipWrongHttpStatusError):
        result = await g.turn_off()
    with pytest.raises(HmipWrongHttpStatusError):
        result = await g.set_shutter_level(50)
    with pytest.raises(HmipWrongHttpStatusError):
        result = await g.set_slats_level(2.0, 10)


@pytest.mark.asyncio
async def test_shutter_profile(no_ssl_fake_async_home: AsyncHome):
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000093"
    )
    assert isinstance(g, AsyncShutterProfile)

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

    await g.set_shutter_level(50)
    await g.set_profile_mode(ProfileMode.MANUAL)
    await g.set_shutter_stop()
    await no_ssl_fake_async_home.get_current_state()
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000093"
    )
    assert g.shutterLevel == 50
    assert g.profileMode == ProfileMode.MANUAL

    assert str(g) == (
        "SHUTTER_PROFILE Rollladen Schiebetür processing(False)"
        " shutterLevel(50) slatsLevel(None) profileMode(MANUAL)"
    )

    await g.set_slats_level(1.0, 20)

    await no_ssl_fake_async_home.get_current_state()
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000093"
    )
    assert g.slatsLevel == 1.0
    assert g.shutterLevel == 20


@pytest.mark.asyncio
async def test_extended_linked_shutter_group(no_ssl_fake_async_home: AsyncHome):
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000050"
    )

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

    assert str(g) == "EXTENDED_LINKED_SHUTTER Rollos shutterLevel(1.0) slatsLevel(None)"

    await g.set_slats_level(1.2, 10)
    await no_ssl_fake_async_home.get_current_state()
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000050"
    )

    assert g.slatsLevel == 1.2
    assert g.shutterLevel == 10

    await g.set_shutter_stop()
    await g.set_shutter_level(30)
    await no_ssl_fake_async_home.get_current_state()
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000050"
    )
    assert g.shutterLevel == 30


@pytest.mark.asyncio
async def test_hot_water(no_ssl_fake_async_home: AsyncHome):
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000067"
    )
    assert g.profileMode is None

    await g.set_profile_mode(ProfileMode.AUTOMATIC)
    await no_ssl_fake_async_home.get_current_state()
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000067"
    )

    assert g.profileMode == ProfileMode.AUTOMATIC

    assert str(g) == "HOT_WATER HOT_WATER on(None) onTime(900.0) profileMode(AUTOMATIC)"


@pytest.mark.asyncio
async def test_switching_alarm_group(no_ssl_fake_async_home: AsyncHome):
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000022"
    )
    assert isinstance(g, AlarmSwitchingGroup)

    assert g.signalAcoustic == AcousticAlarmSignal.FREQUENCY_RISING
    assert g.signalOptical == OpticalAlarmSignal.DOUBLE_FLASHING_REPEATING
    assert str(g) == (
        "ALARM_SWITCHING SIREN on(False) dimLevel(None) onTime(180.0) "
        "signalAcoustic(FREQUENCY_RISING) signalOptical(DOUBLE_FLASHING_REPEATING) "
        "smokeDetectorAlarmType(IDLE_OFF) acousticFeedbackEnabled(True)"
    )

    await g.test_signal_acoustic(AcousticAlarmSignal.FREQUENCY_HIGHON_OFF)
    await g.test_signal_optical(OpticalAlarmSignal.BLINKING_ALTERNATELY_REPEATING)

    await g.set_signal_acoustic(AcousticAlarmSignal.FREQUENCY_HIGHON_OFF)
    await g.set_signal_optical(OpticalAlarmSignal.BLINKING_ALTERNATELY_REPEATING)
    await g.set_on_time(5)

    await no_ssl_fake_async_home.get_current_state()
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000022"
    )

    assert g.signalAcoustic == AcousticAlarmSignal.FREQUENCY_HIGHON_OFF
    assert g.signalOptical == OpticalAlarmSignal.BLINKING_ALTERNATELY_REPEATING
    assert g.onTime == 5


@pytest.mark.asyncio
async def test_access_control(no_ssl_fake_async_home: AsyncHome):
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000033"
    )
    await no_ssl_fake_async_home.get_current_state()

    assert str(g) == "ACCESS_CONTROL AmHaustuere2"


@pytest.mark.asyncio
async def test_access_authorization_profile_group(no_ssl_fake_async_home: AsyncHome):
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000032"
    )
    await no_ssl_fake_async_home.get_current_state()

    assert g.label == "Walter"
    assert g.active == True
    assert g.authorizationPinAssigned == True
    assert g.authorized == True


@pytest.mark.asyncio
async def test_indoor_climate_group(no_ssl_fake_async_home: AsyncHome):
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-0000000000IC"
    )
    await no_ssl_fake_async_home.get_current_state()

    assert g.label == "Stanovanje"
    assert g.sabotage == False
    assert g.ventilationLevel == 0.5
    assert g.ventilationState == None
    assert g.windowState == WindowState.CLOSED
    assert str(g) == "INDOOR_CLIMATE Stanovanje sabotage(False) ventilationLevel(0.5) ventilationState(None) windowState(CLOSED)"

@pytest.mark.asyncio
async def test_energy_group(no_ssl_fake_async_home: AsyncHome):
    g = no_ssl_fake_async_home.search_group_by_id("00000000-0000-0000-0000-0000000000EN")
    await no_ssl_fake_async_home.get_current_state()

    assert isinstance(g, AsyncEnergyGroup)