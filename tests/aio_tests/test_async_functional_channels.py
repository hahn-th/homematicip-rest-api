import asyncio
from datetime import datetime, timedelta, timezone

import pytest

from conftest import utc_offset
from homematicip.aio.home import AsyncHome
from homematicip.base.base_connection import HmipWrongHttpStatusError
from homematicip.base.enums import *
from homematicip.base.functionalChannels import *

@pytest.mark.asyncio
async def test_async_acceleration_sensor_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000031",1)
    assert isinstance(ch, AccelerationSensorChannel)

    assert ch.accelerationSensorEventFilterPeriod == 3.0
    assert ch.accelerationSensorMode == AccelerationSensorMode.FLAT_DECT
    assert ch.accelerationSensorNeutralPosition == AccelerationSensorNeutralPosition.VERTICAL
    assert ch.accelerationSensorSensitivity == AccelerationSensorSensitivity.SENSOR_RANGE_4G
    assert ch.accelerationSensorTriggerAngle == 45
    assert ch.notificationSoundTypeHighToLow == NotificationSoundType.SOUND_LONG
    assert ch.notificationSoundTypeLowToHigh == NotificationSoundType.SOUND_LONG

    await ch.async_set_acceleration_sensor_event_filter_period(10.0)
    await ch.async_set_acceleration_sensor_mode(AccelerationSensorMode.ANY_MOTION)
    await ch.async_set_acceleration_sensor_neutral_position(AccelerationSensorNeutralPosition.HORIZONTAL)
    await ch.async_set_acceleration_sensor_sensitivity(AccelerationSensorSensitivity.SENSOR_RANGE_2G)
    await ch.async_set_acceleration_sensor_trigger_angle(30)
    await ch.async_set_notification_sound_type(NotificationSoundType.SOUND_SHORT, True)
    await ch.async_set_notification_sound_type(NotificationSoundType.SOUND_SHORT_SHORT, False)

    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000031",1)
    assert ch.accelerationSensorEventFilterPeriod == 10.0
    assert ch.accelerationSensorMode == AccelerationSensorMode.ANY_MOTION
    assert ch.accelerationSensorNeutralPosition == AccelerationSensorNeutralPosition.HORIZONTAL
    assert ch.accelerationSensorSensitivity == AccelerationSensorSensitivity.SENSOR_RANGE_2G
    assert ch.accelerationSensorTriggerAngle == 30
    assert ch.notificationSoundTypeHighToLow == NotificationSoundType.SOUND_SHORT
    assert ch.notificationSoundTypeLowToHigh == NotificationSoundType.SOUND_SHORT_SHORT

@pytest.mark.asyncio
async def test_async_door_lock_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000DLD",1)
    assert isinstance(ch, DoorLockChannel)
    assert ch.lockState == LockState.LOCKED
    assert ch.motorState == MotorState.STOPPED

    await ch.async_set_lock_state(LockState.OPEN)
    
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000DLD",1)
    assert ch.lockState == LockState.OPEN

@pytest.mark.asyncio
async def test_switch_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F711000000000000FIO6",11)
    assert isinstance(ch, SwitchChannel)
    assert ch.powerUpSwitchState == "PERMANENT_OFF"
    assert ch.on == False
    assert ch.profileMode == ProfileMode.AUTOMATIC
    assert ch.userDesiredProfileMode == ProfileMode.AUTOMATIC

    await ch.async_set_switch_state(True)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F711000000000000FIO6",11)
    assert ch.on == True

    await ch.async_turn_off()
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F711000000000000FIO6",11)
    assert ch.on == False
    
    await ch.async_turn_on()
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F711000000000000FIO6",11)
    assert ch.on == True

@pytest.mark.asyncio
async def test_switch_measuring_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000108",1)
    assert isinstance(ch, SwitchMeasuringChannel)
    assert ch.energyCounter == 6.333200000000001
    assert ch.currentPowerConsumption == 0.0
    assert ch.on == False

    await ch.async_reset_energy_counter()
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000108",1)
    assert ch.energyCounter == 0.0

    await ch.async_turn_on()
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000108",1)
    assert ch.on == True

@pytest.mark.asyncio
async def test_async_wall_mounted_thermostate_pro_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000022",1)
    assert ch.actualTemperature == 24.7
    assert ch.display == ClimateControlDisplay.ACTUAL_HUMIDITY
    assert ch.humidity == 43
    assert ch.vaporAmount == 6.177718198711658
    assert ch.setPointTemperature == 5.0
    assert ch.temperatureOffset == 0.0

    await ch.async_set_display(ClimateControlDisplay.ACTUAL)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000022",1)
    assert ch.display == ClimateControlDisplay.ACTUAL