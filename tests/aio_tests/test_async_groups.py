import pytest
import json
from datetime import datetime, timedelta, timezone

from homematicip.aio.group import *
from homematicip.aio.home import AsyncHome
from homematicip.base.base_connection import HmipWrongHttpStatusError
from homematicip.base.enums import *

from conftest import utc_offset


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
            "3014F7110000000000000011",
        ]

    assert g.activeProfile.index == "PROFILE_1"
    assert g.activeProfile.enabled == True
    assert g.activeProfile.name == ""
    assert g.activeProfile.visible == True
    assert g.activeProfile.id == "00000000-0000-0000-0000-000000000023"
    assert g.activeProfile.groupId == "00000000-0000-0000-0000-000000000012"

    profile3 = g.profiles[2]
    assert profile3.index == "PROFILE_3"
    assert profile3.visible == False
    assert profile3.id == "00000000-0000-0000-0000-000000000025"

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
    assert g.lastStatusUpdate == datetime(2018, 4, 23, 20, 48, 54, 382000) + timedelta(
        0, utc_offset
    )
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

    assert str(g) == (
        "HEATING Schlafzimmer: windowOpenTemperature(5.0) setPointTemperature(5.0) windowState(OPEN) motionDetected(30.0)"
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
    assert g.boostMode == True
    assert g.activeProfile.index == "PROFILE_4"
    assert g.setPointTemperature == 10.5
    assert g.controlMode == ClimateControlMode.MANUAL

    await no_ssl_fake_async_home.delete_group(g)
    await no_ssl_fake_async_home.get_current_state()
    gNotFound = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000012"
    )
    assert gNotFound == None

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

    assert g.dimLevel == None
    assert g.dutyCycle == False
    assert g.homeId == "00000000-0000-0000-0000-000000000001"
    assert g.id == "00000000-0000-0000-0000-000000000018"
    assert g.label == "Strom"
    assert g.lastStatusUpdate == datetime(2018, 4, 23, 20, 49, 14, 56000) + timedelta(
        0, utc_offset
    )
    assert g.lowBat == None
    assert g.metaGroup.id == "00000000-0000-0000-0000-000000000017"
    assert g.on == True
    assert g.processing == None
    assert g.shutterLevel == None
    assert g.slatsLevel == None
    assert g.unreach == False

    assert str(g) == (
        "SWITCHING Strom: on(True) dimLevel(None) processing(None) shutterLevel(None) slatsLevel(None)"
        " dutyCycle(False) lowBat(None)"
    )

    await g.turn_off()
    await g.set_label("NEW GROUP")
    await g.set_shutter_level(50)
    await no_ssl_fake_async_home.get_current_state()
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000018"
    )
    assert g.on == False
    assert g.label == "NEW GROUP"
    assert g.shutterLevel == 50

    assert str(g) == (
        "SWITCHING NEW GROUP: on(False) dimLevel(None) processing(None) shutterLevel(50) slatsLevel(None)"
        " dutyCycle(False) lowBat(None)"
    )
    await g.turn_on()
    await no_ssl_fake_async_home.get_current_state()
    g = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000018"
    )
    assert g.on == True

    await no_ssl_fake_async_home.delete_group(g)
    await no_ssl_fake_async_home.get_current_state()
    gNotFound = no_ssl_fake_async_home.search_group_by_id(
        "00000000-0000-0000-0000-000000000018"
    )
    assert gNotFound == None

    with pytest.raises(HmipWrongHttpStatusError):
        result = await g.delete()
    with pytest.raises(HmipWrongHttpStatusError):
        result = await g.set_label("LABEL")
    with pytest.raises(HmipWrongHttpStatusError):
        result = await g.turn_off()
    with pytest.raises(HmipWrongHttpStatusError):
        result = await g.set_shutter_level(50)
