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
        