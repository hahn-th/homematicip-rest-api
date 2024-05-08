import asyncio
from datetime import datetime, timedelta, timezone

import pytest

from conftest import utc_offset
from homematicip.aio.home import AsyncHome
from homematicip.base.base_connection import HmipWrongHttpStatusError
from homematicip.base.enums import *
from homematicip.base.functionalChannels import *


@pytest.mark.asyncio
async def test_acceleration_sensor_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000031", 1)
    assert isinstance(ch, AccelerationSensorChannel)

    assert ch.accelerationSensorEventFilterPeriod == 3.0
    assert ch.accelerationSensorMode == AccelerationSensorMode.FLAT_DECT
    assert (
        ch.accelerationSensorNeutralPosition
        == AccelerationSensorNeutralPosition.VERTICAL
    )
    assert (
        ch.accelerationSensorSensitivity
        == AccelerationSensorSensitivity.SENSOR_RANGE_4G
    )
    assert ch.accelerationSensorTriggerAngle == 45
    assert ch.notificationSoundTypeHighToLow == NotificationSoundType.SOUND_LONG
    assert ch.notificationSoundTypeLowToHigh == NotificationSoundType.SOUND_LONG

    await ch.async_set_acceleration_sensor_event_filter_period(10.0)
    await ch.async_set_acceleration_sensor_mode(AccelerationSensorMode.ANY_MOTION)
    await ch.async_set_acceleration_sensor_neutral_position(
        AccelerationSensorNeutralPosition.HORIZONTAL
    )
    await ch.async_set_acceleration_sensor_sensitivity(
        AccelerationSensorSensitivity.SENSOR_RANGE_2G
    )
    await ch.async_set_acceleration_sensor_trigger_angle(30)
    await ch.async_set_notification_sound_type(NotificationSoundType.SOUND_SHORT, True)
    await ch.async_set_notification_sound_type(
        NotificationSoundType.SOUND_SHORT_SHORT, False
    )

    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000031", 1)
    assert ch.accelerationSensorEventFilterPeriod == 10.0
    assert ch.accelerationSensorMode == AccelerationSensorMode.ANY_MOTION
    assert (
        ch.accelerationSensorNeutralPosition
        == AccelerationSensorNeutralPosition.HORIZONTAL
    )
    assert (
        ch.accelerationSensorSensitivity
        == AccelerationSensorSensitivity.SENSOR_RANGE_2G
    )
    assert ch.accelerationSensorTriggerAngle == 30
    assert ch.notificationSoundTypeHighToLow == NotificationSoundType.SOUND_SHORT
    assert ch.notificationSoundTypeLowToHigh == NotificationSoundType.SOUND_SHORT_SHORT


@pytest.mark.asyncio
async def test_blind_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F711BADCAFE000000001", 1)
    assert isinstance(ch, BlindChannel)

    await ch.async_set_shutter_level(0.5)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F711BADCAFE000000001", 1)
    assert ch.shutterLevel == 0.5

    await ch.async_set_slats_level(0.4, 0.6)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F711BADCAFE000000001", 1)
    assert ch.shutterLevel == 0.6
    assert ch.slatsLevel == 0.4


@pytest.mark.asyncio
async def test_device_base_floor_heating_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000049", 0)
    assert isinstance(ch, DeviceBaseFloorHeatingChannel)

    assert ch.coolingEmergencyValue == 0
    assert ch.frostProtectionTemperature == 8.0
    assert ch.heatingEmergencyValue == 0.25
    assert ch.minimumFloorHeatingValvePosition == 0.0
    assert ch.temperatureOutOfRange == False
    assert ch.valveProtectionDuration == 5
    assert ch.valveProtectionSwitchingInterval == 14

    assert ch.minimumFloorHeatingValvePosition == 0.0
    await ch.async_set_minimum_floor_heating_valve_position(0.2)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000049", 0)
    assert ch.minimumFloorHeatingValvePosition == 0.2


@pytest.mark.asyncio
async def test_device_operation_lock_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000015",0)
    assert isinstance(ch, DeviceOperationLockChannel)

    await ch.async_set_operation_lock(False)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000015",0)
    assert ch.operationLockActive is False
    
    await ch.async_set_operation_lock(True)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000015",0)
    assert ch.operationLockActive is True


@pytest.mark.asyncio
async def test_dimmer_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F711AAAA000000000005", 1)
    assert isinstance(ch, DimmerChannel)
    assert ch.dimLevel == 0.0

    await ch.async_set_dim_level(0.8)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F711AAAA000000000005", 1)
    assert ch.dimLevel == 0.8


@pytest.mark.asyncio
async def test_door_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F0000000000000FAF9B4", 1)
    assert isinstance(ch, DoorChannel)
    assert ch.doorState == DoorState.CLOSED

    await ch.async_send_door_command(DoorCommand.OPEN)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F0000000000000FAF9B4", 1)

    assert ch.doorState == DoorState.OPEN


@pytest.mark.asyncio
async def test_door_lock_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000DLD", 1)
    assert isinstance(ch, DoorLockChannel)
    assert ch.lockState == LockState.LOCKED
    assert ch.motorState == MotorState.STOPPED

    await ch.async_set_lock_state(LockState.OPEN)

    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000DLD", 1)
    assert ch.lockState == LockState.OPEN


@pytest.mark.asyncio
async def test_impulse_output_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000WGC", 2)
    assert isinstance(ch, ImpulseOutputChannel)
    assert ch.impulseDuration == 0.10000000149011612

    await ch.async_send_start_impulse()
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000WGC", 2)


@pytest.mark.asyncio
async def test_notification_light_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F711BSL0000000000050", 2)
    assert isinstance(ch, NotificationLightChannel)
    assert ch.dimLevel == 0.0
    assert ch.simpleRGBColorState == RGBColorState.RED

    await ch.async_set_rgb_dim_level_with_time(RGBColorState.BLUE, 0.2, 10, 20)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F711BSL0000000000050", 2)
    assert ch.dimLevel == 0.2
    assert ch.simpleRGBColorState == RGBColorState.BLUE

    await ch.async_set_rgb_dim_level(RGBColorState.BLACK, 0.5)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F711BSL0000000000050", 2)
    assert ch.dimLevel == 0.5
    assert ch.simpleRGBColorState == RGBColorState.BLACK

    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F711000000000000BSL2", 3)
    await ch.async_set_optical_signal(OpticalSignalBehaviour.FLASH_MIDDLE, RGBColorState.WHITE, 0.6)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F711000000000000BSL2", 3)
    assert ch.opticalSignalBehaviour == OpticalSignalBehaviour.FLASH_MIDDLE
    assert ch.dimLevel == 0.6
    assert ch.simpleRGBColorState == RGBColorState.WHITE




@pytest.mark.asyncio
async def test_shading_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F71100BLIND_MODULE00", 1)
    assert isinstance(ch, ShadingChannel)

    assert ch.primaryShadingLevel == 0.94956
    assert ch.secondaryShadingLevel == 0

    await ch.async_set_primary_shading_level(5)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F71100BLIND_MODULE00", 1)
    assert ch.primaryShadingLevel == 5

    await ch.async_set_secondary_shading_level(0.5, 1.0)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F71100BLIND_MODULE00", 1)
    assert ch.primaryShadingLevel == 0.5
    assert ch.secondaryShadingLevel == 1.0


@pytest.mark.asyncio
async def test_shutter_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F711ACBCDABCADCA66", 1)
    assert isinstance(ch, ShutterChannel)
    assert ch.bottomToTopReferenceTime == 30.080000000000002
    assert ch.changeOverDelay == 0.5
    assert ch.delayCompensationValue == 12.7
    assert ch.endpositionAutoDetectionEnabled == True
    assert ch.shutterLevel == 1.0
    assert ch.previousShutterLevel == None
    assert ch.selfCalibrationInProgress == None
    assert ch.topToBottomReferenceTime == 24.68

    await ch.async_set_shutter_level(0.5)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F711ACBCDABCADCA66", 1)
    assert ch.shutterLevel == 0.5


@pytest.mark.asyncio
async def test_switch_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F711000000000000FIO6", 11)
    assert isinstance(ch, SwitchChannel)
    assert ch.powerUpSwitchState == "PERMANENT_OFF"
    assert ch.on == False
    assert ch.profileMode == ProfileMode.AUTOMATIC
    assert ch.userDesiredProfileMode == ProfileMode.AUTOMATIC

    await ch.async_set_switch_state(True)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F711000000000000FIO6", 11)
    assert ch.on == True

    await ch.async_turn_off()
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F711000000000000FIO6", 11)
    assert ch.on == False

    await ch.async_turn_on()
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F711000000000000FIO6", 11)
    assert ch.on == True


@pytest.mark.asyncio
async def test_switch_measuring_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000108", 1)
    assert isinstance(ch, SwitchMeasuringChannel)
    assert ch.energyCounter == 6.333200000000001
    assert ch.currentPowerConsumption == 0.0
    assert ch.on == False

    await ch.async_reset_energy_counter()
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000108", 1)
    assert ch.energyCounter == 0.0

    await ch.async_turn_on()
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000108", 1)
    assert ch.on == True


@pytest.mark.asyncio
async def test_tilt_vibration_sensor_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F7110TILTVIBRATIONSENSOR", 1)
    assert isinstance(ch, TiltVibrationSensorChannel)

    assert ch.accelerationSensorEventFilterPeriod == 0.5
    assert ch.accelerationSensorMode == AccelerationSensorMode.FLAT_DECT
    assert (
        ch.accelerationSensorNeutralPosition
        == AccelerationSensorNeutralPosition.VERTICAL
    )
    assert (
        ch.accelerationSensorSensitivity
        == AccelerationSensorSensitivity.SENSOR_RANGE_2G
    )
    assert ch.accelerationSensorTriggerAngle == 45
    assert ch.accelerationSensorTriggered == True

    await ch.async_set_acceleration_sensor_event_filter_period(10.0)
    await ch.async_set_acceleration_sensor_mode(AccelerationSensorMode.ANY_MOTION)
    await ch.async_set_acceleration_sensor_sensitivity(
        AccelerationSensorSensitivity.SENSOR_RANGE_4G
    )
    await ch.async_set_acceleration_sensor_trigger_angle(30)

    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_device_by_id("3014F7110TILTVIBRATIONSENSOR")
    assert ch.accelerationSensorEventFilterPeriod == 10.0
    assert ch.accelerationSensorMode == AccelerationSensorMode.ANY_MOTION
    assert (
        ch.accelerationSensorSensitivity
        == AccelerationSensorSensitivity.SENSOR_RANGE_4G
    )
    assert ch.accelerationSensorTriggerAngle == 30


@pytest.mark.asyncio
async def test_wall_mounted_thermostate_pro_channel(
    no_ssl_fake_async_home: AsyncHome,
):
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000022", 1)
    assert ch.actualTemperature == 24.7
    assert ch.display == ClimateControlDisplay.ACTUAL_HUMIDITY
    assert ch.humidity == 43
    assert ch.vaporAmount == 6.177718198711658
    assert ch.setPointTemperature == 5.0
    assert ch.temperatureOffset == 0.0

    await ch.async_set_display(ClimateControlDisplay.ACTUAL)
    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000022", 1)
    assert ch.display == ClimateControlDisplay.ACTUAL


@pytest.mark.asyncio
async def test_water_sensor_channel(no_ssl_fake_async_home: AsyncHome):
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000050", 1)
    assert isinstance(ch, WaterSensorChannel)
    assert ch.acousticAlarmSignal == AcousticAlarmSignal.FREQUENCY_RISING
    assert ch.acousticAlarmTiming == AcousticAlarmTiming.ONCE_PER_MINUTE
    assert ch.acousticWaterAlarmTrigger == WaterAlarmTrigger.WATER_DETECTION
    assert ch.inAppWaterAlarmTrigger == WaterAlarmTrigger.WATER_MOISTURE_DETECTION
    assert ch.moistureDetected is False
    assert ch.sirenWaterAlarmTrigger == WaterAlarmTrigger.WATER_MOISTURE_DETECTION
    assert ch.waterlevelDetected is False

    await ch.async_set_acoustic_alarm_timing(AcousticAlarmTiming.SIX_MINUTES)
    await ch.async_set_acoustic_alarm_signal(
        AcousticAlarmSignal.FREQUENCY_ALTERNATING_LOW_HIGH
    )
    await ch.async_set_inapp_water_alarm_trigger(WaterAlarmTrigger.MOISTURE_DETECTION)
    await ch.async_set_acoustic_water_alarm_trigger(WaterAlarmTrigger.NO_ALARM)
    await ch.async_set_siren_water_alarm_trigger(WaterAlarmTrigger.NO_ALARM)

    await no_ssl_fake_async_home.get_current_state()
    ch = no_ssl_fake_async_home.search_channel("3014F7110000000000000050", 1)
    assert ch.acousticAlarmTiming == AcousticAlarmTiming.SIX_MINUTES
    assert ch.acousticAlarmSignal == AcousticAlarmSignal.FREQUENCY_ALTERNATING_LOW_HIGH
    assert ch.acousticWaterAlarmTrigger == WaterAlarmTrigger.NO_ALARM
    assert ch.inAppWaterAlarmTrigger == WaterAlarmTrigger.MOISTURE_DETECTION
    assert ch.sirenWaterAlarmTrigger == WaterAlarmTrigger.NO_ALARM
