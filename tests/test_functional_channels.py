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
        ch = fake_home.search_channel("3014F7110000000000000031",1)
        assert isinstance(ch, AccelerationSensorChannel)

        assert ch.accelerationSensorEventFilterPeriod == 3.0
        assert ch.accelerationSensorMode == AccelerationSensorMode.FLAT_DECT
        assert ch.accelerationSensorNeutralPosition == AccelerationSensorNeutralPosition.VERTICAL
        assert ch.accelerationSensorSensitivity == AccelerationSensorSensitivity.SENSOR_RANGE_4G
        assert ch.accelerationSensorTriggerAngle == 45
        assert ch.notificationSoundTypeHighToLow == NotificationSoundType.SOUND_LONG
        assert ch.notificationSoundTypeLowToHigh == NotificationSoundType.SOUND_LONG

        ch.set_acceleration_sensor_event_filter_period(10.0)
        ch.set_acceleration_sensor_mode(AccelerationSensorMode.ANY_MOTION)
        ch.set_acceleration_sensor_neutral_position(AccelerationSensorNeutralPosition.HORIZONTAL)
        ch.set_acceleration_sensor_sensitivity(AccelerationSensorSensitivity.SENSOR_RANGE_2G)
        ch.set_acceleration_sensor_trigger_angle(30)
        ch.set_notification_sound_type(NotificationSoundType.SOUND_SHORT, True)
        ch.set_notification_sound_type(NotificationSoundType.SOUND_SHORT_SHORT, False)

        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F7110000000000000031",1)
        assert ch.accelerationSensorEventFilterPeriod == 10.0
        assert ch.accelerationSensorMode == AccelerationSensorMode.ANY_MOTION
        assert ch.accelerationSensorNeutralPosition == AccelerationSensorNeutralPosition.HORIZONTAL
        assert ch.accelerationSensorSensitivity == AccelerationSensorSensitivity.SENSOR_RANGE_2G
        assert ch.accelerationSensorTriggerAngle == 30
        assert ch.notificationSoundTypeHighToLow == NotificationSoundType.SOUND_SHORT
        assert ch.notificationSoundTypeLowToHigh == NotificationSoundType.SOUND_SHORT_SHORT
        
def test_door_lock_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F7110000000000000DLD",1)
        assert isinstance(ch, DoorLockChannel)
        assert ch.lockState == LockState.LOCKED
        assert ch.motorState == MotorState.STOPPED

        result = ch.set_lock_state(LockState.OPEN)
        
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F7110000000000000DLD",1)
        assert ch.lockState == LockState.OPEN

def test_switch_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F711000000000000FIO6",11)
        assert isinstance(ch, SwitchChannel)
        assert ch.powerUpSwitchState == "PERMANENT_OFF"
        assert ch.on == False
        assert ch.profileMode == ProfileMode.AUTOMATIC
        assert ch.userDesiredProfileMode == ProfileMode.AUTOMATIC

        ch.set_switch_state(True)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F711000000000000FIO6",11)
        assert ch.on == True

        ch.turn_off()
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F711000000000000FIO6",11)
        assert ch.on == False
        
        ch.turn_on()
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F711000000000000FIO6",11)
        assert ch.on == True
        
def test_wall_mounted_thermostate_pro_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F7110000000000000022",1)
        assert ch.actualTemperature == 24.7
        assert ch.display == ClimateControlDisplay.ACTUAL_HUMIDITY
        assert ch.humidity == 43
        assert ch.vaporAmount == 6.177718198711658
        assert ch.setPointTemperature == 5.0
        assert ch.temperatureOffset == 0.0

        ch.set_display(ClimateControlDisplay.ACTUAL)
        fake_home.get_current_state()
        ch = fake_home.search_channel("3014F7110000000000000022",1)
        assert ch.display == ClimateControlDisplay.ACTUAL