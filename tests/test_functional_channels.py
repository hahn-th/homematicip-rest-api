import json
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, Mock
import pytest
from conftest import utc_offset
from homematicip.base.base_connection import BaseConnection
from homematicip.base.enums import *
from homematicip.base.functionalChannels import *
from homematicip.device import *
from homematicip.home import Home
from homematicip_demo.helper import (
    fake_home_download_configuration,
    no_ssl_verification,
)

from homematicip.class_maps import TYPE_FUNCTIONALCHANNEL_MAP


def test_acceleration_sensor_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F7110000000000000031", 1)
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

        ch.set_acceleration_sensor_event_filter_period(10.0)
        ch.set_acceleration_sensor_mode(AccelerationSensorMode.ANY_MOTION)
        ch.set_acceleration_sensor_neutral_position(
            AccelerationSensorNeutralPosition.HORIZONTAL
        )
        ch.set_acceleration_sensor_sensitivity(
            AccelerationSensorSensitivity.SENSOR_RANGE_2G
        )
        ch.set_acceleration_sensor_trigger_angle(30)
        ch.set_notification_sound_type(NotificationSoundType.SOUND_SHORT, True)
        ch.set_notification_sound_type(NotificationSoundType.SOUND_SHORT_SHORT, False)

        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F7110000000000000031", 1)
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
        assert (
            ch.notificationSoundTypeLowToHigh == NotificationSoundType.SOUND_SHORT_SHORT
        )


def test_blind_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F711BADCAFE000000001", 1)
        assert isinstance(ch, BlindChannel)
        assert ch.blindModeActive == True
        assert ch.bottomToTopReferenceTime == 41.0
        assert ch.changeOverDelay == 0.5
        assert ch.delayCompensationValue == 1.0
        assert ch.endpositionAutoDetectionEnabled == False
        assert ch.previousShutterLevel == None
        assert ch.previousSlatsLevel == None
        assert ch.selfCalibrationInProgress == None
        assert ch.shutterLevel == 1.0
        assert ch.slatsLevel == 1.0
        assert ch.slatsReferenceTime == 2.0
        assert ch.topToBottomReferenceTime == 41.0

        ch.set_shutter_level(0.5)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F711BADCAFE000000001", 1)
        assert ch.shutterLevel == 0.5

        ch.set_slats_level(0.4, 0.6)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F711BADCAFE000000001", 1)
        assert ch.shutterLevel == 0.6
        assert ch.slatsLevel == 0.4


def test_device_base_floor_heating_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F7110000000000000049", 0)
        assert isinstance(ch, DeviceBaseFloorHeatingChannel)

        assert ch.coolingEmergencyValue == 0
        assert ch.frostProtectionTemperature == 8.0
        assert ch.heatingEmergencyValue == 0.25
        assert ch.minimumFloorHeatingValvePosition == 0.0
        assert ch.temperatureOutOfRange == False
        assert ch.valveProtectionDuration == 5
        assert ch.valveProtectionSwitchingInterval == 14

        assert ch.minimumFloorHeatingValvePosition == 0.0
        ch.set_minimum_floor_heating_valve_position(0.2)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F7110000000000000049", 0)
        assert ch.minimumFloorHeatingValvePosition == 0.2


def test_device_operation_lock_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F7110000000000000015",0)
        assert isinstance(ch, DeviceOperationLockChannel)

        ch.set_operation_lock(False)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F7110000000000000015",0)
        assert ch.operationLockActive is False
        
        ch.set_operation_lock(True)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F7110000000000000015",0)
        assert ch.operationLockActive is True


def test_dimmer_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F711AAAA000000000005", 1)
        assert isinstance(ch, DimmerChannel)
        assert ch.dimLevel == 0.0

        ch.set_dim_level(0.8)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F711AAAA000000000005", 1)
        assert ch.dimLevel == 0.8


def test_door_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F0000000000000FAF9B4", 1)
        assert isinstance(ch, DoorChannel)
        assert ch.doorState == DoorState.CLOSED

        ch.send_door_command(DoorCommand.OPEN)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F0000000000000FAF9B4", 1)

        assert ch.doorState == DoorState.OPEN


def test_door_lock_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F7110000000000000DLD", 1)
        assert isinstance(ch, DoorLockChannel)
        assert ch.lockState == LockState.LOCKED
        assert ch.motorState == MotorState.STOPPED

        result = ch.set_lock_state(LockState.OPEN)

        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F7110000000000000DLD", 1)
        assert ch.lockState == LockState.OPEN


def test_floor_terminal_block_mechanic_channel(fake_home: Home):
    ch = fake_home.search_channel("3014F7110000000000000049", 12)
    assert isinstance(ch, FloorTerminalBlockMechanicChannel)
    assert ch.valveState == ValveState.ADJUSTMENT_TOO_SMALL


def test_impulse_output_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F7110000000000000WGC", 2)
        assert isinstance(ch, ImpulseOutputChannel)
        assert ch.impulseDuration == 0.10000000149011612

        ch.send_start_impulse()
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F7110000000000000WGC", 2)


def test_notification_light_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F711BSL0000000000050", 2)
        assert isinstance(ch, NotificationLightChannel)
        assert ch.dimLevel == 0.0
        assert ch.simpleRGBColorState == RGBColorState.RED

        ch.set_rgb_dim_level_with_time(RGBColorState.BLUE, 0.2, 10, 20)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F711BSL0000000000050", 2)
        assert ch.dimLevel == 0.2
        assert ch.simpleRGBColorState == RGBColorState.BLUE

        ch.set_rgb_dim_level(RGBColorState.BLACK, 0.5)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F711BSL0000000000050", 2)
        assert ch.dimLevel == 0.5
        assert ch.simpleRGBColorState == RGBColorState.BLACK


def test_shading_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F71100BLIND_MODULE00", 1)
        assert isinstance(ch, ShadingChannel)

        assert ch.primaryShadingLevel == 0.94956
        assert ch.secondaryShadingLevel == 0

        ch.set_primary_shading_level(5)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F71100BLIND_MODULE00", 1)
        assert ch.primaryShadingLevel == 5

        ch.set_secondary_shading_level(0.5, 1.0)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F71100BLIND_MODULE00", 1)
        assert ch.primaryShadingLevel == 0.5
        assert ch.secondaryShadingLevel == 1.0


def test_shutter_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F711ACBCDABCADCA66", 1)
        assert isinstance(ch, ShutterChannel)
        assert ch.bottomToTopReferenceTime == 30.080000000000002
        assert ch.changeOverDelay == 0.5
        assert ch.delayCompensationValue == 12.7
        assert ch.endpositionAutoDetectionEnabled == True
        assert ch.shutterLevel == 1.0
        assert ch.previousShutterLevel == None
        assert ch.selfCalibrationInProgress == None
        assert ch.topToBottomReferenceTime == 24.68

        ch.set_shutter_level(0.5)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F711ACBCDABCADCA66", 1)
        assert ch.shutterLevel == 0.5


def test_switch_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F711000000000000FIO6", 11)
        assert isinstance(ch, SwitchChannel)
        assert ch.powerUpSwitchState == "PERMANENT_OFF"
        assert ch.on == False
        assert ch.profileMode == ProfileMode.AUTOMATIC
        assert ch.userDesiredProfileMode == ProfileMode.AUTOMATIC

        ch.set_switch_state(True)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F711000000000000FIO6", 11)
        assert ch.on == True

        ch.turn_off()
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F711000000000000FIO6", 11)
        assert ch.on == False

        ch.turn_on()
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F711000000000000FIO6", 11)
        assert ch.on == True


def test_switch_measuring_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F7110000000000000108", 1)
        assert isinstance(ch, SwitchMeasuringChannel)
        assert ch.energyCounter == 6.333200000000001
        assert ch.currentPowerConsumption == 0.0
        assert ch.on == False

        ch.reset_energy_counter()
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F7110000000000000108", 1)
        assert ch.energyCounter == 0.0

        ch.turn_on()
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F7110000000000000108", 1)
        assert ch.on == True


def test_tilt_vibration_sensor_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F7110TILTVIBRATIONSENSOR", 1)
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

        ch.set_acceleration_sensor_event_filter_period(10.0)
        ch.set_acceleration_sensor_mode(AccelerationSensorMode.ANY_MOTION)
        ch.set_acceleration_sensor_sensitivity(
            AccelerationSensorSensitivity.SENSOR_RANGE_4G
        )
        ch.set_acceleration_sensor_trigger_angle(30)

        fake_home.get_current_state()
        ch = fake_home.search_device_by_id("3014F7110TILTVIBRATIONSENSOR")
        assert ch.accelerationSensorEventFilterPeriod == 10.0
        assert ch.accelerationSensorMode == AccelerationSensorMode.ANY_MOTION
        assert (
            ch.accelerationSensorSensitivity
            == AccelerationSensorSensitivity.SENSOR_RANGE_4G
        )
        assert ch.accelerationSensorTriggerAngle == 30


def test_wall_mounted_thermostate_pro_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F7110000000000000022", 1)
        assert ch.actualTemperature == 24.7
        assert ch.display == ClimateControlDisplay.ACTUAL_HUMIDITY
        assert ch.humidity == 43
        assert ch.vaporAmount == 6.177718198711658
        assert ch.setPointTemperature == 5.0
        assert ch.temperatureOffset == 0.0

        ch.set_display(ClimateControlDisplay.ACTUAL)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F7110000000000000022", 1)
        assert ch.display == ClimateControlDisplay.ACTUAL


def test_water_sensor_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F7110000000000000050", 1)
        assert isinstance(ch, WaterSensorChannel)
        assert ch.acousticAlarmSignal == AcousticAlarmSignal.FREQUENCY_RISING
        assert ch.acousticAlarmTiming == AcousticAlarmTiming.ONCE_PER_MINUTE
        assert ch.acousticWaterAlarmTrigger == WaterAlarmTrigger.WATER_DETECTION
        assert ch.inAppWaterAlarmTrigger == WaterAlarmTrigger.WATER_MOISTURE_DETECTION
        assert ch.moistureDetected is False
        assert ch.sirenWaterAlarmTrigger == WaterAlarmTrigger.WATER_MOISTURE_DETECTION
        assert ch.waterlevelDetected is False

        ch.set_acoustic_alarm_timing(AcousticAlarmTiming.SIX_MINUTES)
        ch.set_acoustic_alarm_signal(AcousticAlarmSignal.FREQUENCY_ALTERNATING_LOW_HIGH)
        ch.set_inapp_water_alarm_trigger(WaterAlarmTrigger.MOISTURE_DETECTION)
        ch.set_acoustic_water_alarm_trigger(WaterAlarmTrigger.NO_ALARM)
        ch.set_siren_water_alarm_trigger(WaterAlarmTrigger.NO_ALARM)

        fake_home.get_current_state()
        d = fake_home.search_channel("3014F7110000000000000050", 1)
        assert ch.acousticAlarmTiming == AcousticAlarmTiming.SIX_MINUTES
        assert (
            ch.acousticAlarmSignal == AcousticAlarmSignal.FREQUENCY_ALTERNATING_LOW_HIGH
        )
        assert ch.acousticWaterAlarmTrigger == WaterAlarmTrigger.NO_ALARM
        assert ch.inAppWaterAlarmTrigger == WaterAlarmTrigger.MOISTURE_DETECTION
        assert ch.sirenWaterAlarmTrigger == WaterAlarmTrigger.NO_ALARM
