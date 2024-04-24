import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest

from conftest import utc_offset
from homematicip.base.base_connection import BaseConnection
from homematicip.base.enums import *
from homematicip.device import AccelerationSensor, Device, BaseDevice
from homematicip.EventHook import EventHook
from homematicip.functionalHomes import *
from homematicip.group import Group, MetaGroup
from homematicip.home import Home
from homematicip.rule import *
from homematicip.securityEvent import *
from homematicip_demo.helper import (
    fake_home_download_configuration,
    no_ssl_verification,
)


def test_update_event(fake_home: Home):
    fake_handler = Mock()
    fake_home.on_update(fake_handler.method)
    fake_home.fire_update_event()
    fake_handler.method.assert_called()
    fake_home.remove_callback(fake_handler.method)
    assert fake_handler.method not in fake_home._on_update


def test_remove_event(fake_home: Home):
    fake_handler = Mock()
    fake_home.on_remove(fake_handler.method)
    fake_home.fire_remove_event()
    fake_handler.method.assert_called()
    fake_home.remove_callback(fake_handler.method)
    assert fake_handler.method not in fake_home._on_remove


def test_create_event(fake_home: Home):
    fake_handler = Mock()
    fake_home.on_create(fake_handler.method)
    fake_home.fire_create_event()
    fake_handler.method.assert_called()
    fake_home.remove_callback(fake_handler.method)
    assert fake_handler.method not in fake_home._on_create


def test_home_base(fake_home: Home):
    assert fake_home.connected is True
    assert fake_home.currentAPVersion == "1.2.4"
    assert (
        fake_home.deviceUpdateStrategy == DeviceUpdateStrategy.AUTOMATICALLY_IF_POSSIBLE
    )
    assert fake_home.dutyCycle == 8.0
    assert fake_home.pinAssigned is False
    assert fake_home.powerMeterCurrency == "EUR"
    assert fake_home.powerMeterUnitPrice == 0.0
    assert fake_home.timeZoneId == "Europe/Vienna"
    assert fake_home.updateState == HomeUpdateState.UP_TO_DATE
    assert fake_home.apExchangeState == ApExchangeState.NONE

    assert fake_home._rawJSONData == fake_home_download_configuration()["home"]


def test_home_location(fake_home: Home):
    assert fake_home.location.city == "1010  Wien, Österreich"
    assert fake_home.location.latitude == "48.208088"
    assert fake_home.location.longitude == "16.358608"
    assert (
        fake_home.location._rawJSONData
        == fake_home_download_configuration()["home"]["location"]
    )
    assert (
        str(fake_home.location)
        == "city(1010  Wien, Österreich) latitude(48.208088) longitude(16.358608)"
    )


def test_home_set_location(fake_home: Home):
    with no_ssl_verification():
        fake_home.set_location("Berlin, Germany", "52.530644", "13.383068")
        fake_home.get_current_state()
        assert fake_home.location.city == "Berlin, Germany"
        assert fake_home.location.latitude == "52.530644"
        assert fake_home.location.longitude == "13.383068"
        assert (
            str(fake_home.location)
            == "city(Berlin, Germany) latitude(52.530644) longitude(13.383068)"
        )


def test_home_weather(fake_home: Home):
    assert fake_home.weather.humidity == 54
    assert fake_home.weather.maxTemperature == 16.6
    assert fake_home.weather.minTemperature == 16.6
    assert fake_home.weather.temperature == 16.6
    assert fake_home.weather.weatherCondition == WeatherCondition.LIGHT_CLOUDY
    assert fake_home.weather.weatherDayTime == WeatherDayTime.NIGHT
    assert fake_home.weather.windDirection == 294
    assert fake_home.weather.windSpeed == 8.568
    assert (
        fake_home.weather._rawJSONData
        == fake_home_download_configuration()["home"]["weather"]
    )
    assert (
        str(fake_home.weather)
        == "temperature(16.6) weatherCondition(LIGHT_CLOUDY) weatherDayTime(NIGHT) minTemperature(16.6) maxTemperature(16.6) humidity(54) vaporAmount(5.465858858389302) windSpeed(8.568) windDirection(294)"
    )


def test_clients(fake_home: Home):
    client = fake_home.search_client_by_id("00000000-0000-0000-0000-000000000000")
    assert client.label == "TEST-Client"
    assert client.homeId == "00000000-0000-0000-0000-000000000001"
    assert client.id == "00000000-0000-0000-0000-000000000000"
    assert client.clientType == ClientType.APP

    assert (
        client._rawJSONData
        == fake_home_download_configuration()["clients"][
            "00000000-0000-0000-0000-000000000000"
        ]
    )
    assert str(client) == "label(TEST-Client)"


def test_rules(fake_home: Home):
    with no_ssl_verification():
        rule = fake_home.search_rule_by_id("00000000-0000-0000-0000-000000000065")
        assert rule.active is True
        assert rule.label == "Alarmanlage"
        assert isinstance(rule, SimpleRule)
        assert rule.ruleErrorCategories == []
        assert rule.errorRuleTriggerItems == []
        assert rule.errorRuleConditionItems == []
        assert rule.errorRuleActionItems == []

        assert str(rule) == "SIMPLE Alarmanlage active(True)"

        # disable test
        rule.disable()
        rule.set_label("DISABLED_RULE")
        fake_home.get_current_state()
        rule = fake_home.search_rule_by_id("00000000-0000-0000-0000-000000000065")
        assert rule.active is False
        assert rule.label == "DISABLED_RULE"

        # enable test
        rule.enable()
        rule.set_label("ENABLED_RULE")
        fake_home.get_current_state()
        rule = fake_home.search_rule_by_id("00000000-0000-0000-0000-000000000065")
        assert rule.active is True
        assert rule.label == "ENABLED_RULE"

        rule.id = "INVALID_ID"
        result = rule.disable()
        assert result["errorCode"] == "INVALID_RULE"
        result = rule.set_label("NEW LABEL")
        assert result["errorCode"] == "INVALID_RULE"


def test_security_zones_activation(fake_home: Home):
    with no_ssl_verification():
        internal, external = fake_home.get_security_zones_activation()
        assert internal is False
        assert external is False

        fake_home.set_security_zones_activation(True, True)
        fake_home.get_current_state()

        internal, external = fake_home.get_security_zones_activation()
        assert internal is True
        assert external is True


def test_set_pin(fake_home: Home):
    with no_ssl_verification():

        def get_pin(fake_home):
            result = fake_home._rest_call("home/getPin")
            return result["pin"]

        assert get_pin(fake_home) is None

        fake_home.set_pin(1234)
        assert get_pin(fake_home) == 1234

        fake_home.set_pin(
            5555
        )  # ignore errors. just check if the old pin is still active
        assert get_pin(fake_home) == 1234

        fake_home.set_pin(5555, 1234)
        assert get_pin(fake_home) == 5555

        fake_home.set_pin(None, 5555)
        assert get_pin(fake_home) is None


def test_set_timezone(fake_home: Home):
    with no_ssl_verification():
        assert fake_home.timeZoneId == "Europe/Vienna"
        fake_home.set_timezone("Europe/Berlin")
        fake_home.get_current_state()
        assert fake_home.timeZoneId == "Europe/Berlin"

        fake_home.set_timezone("Europe/Vienna")
        fake_home.get_current_state()
        assert fake_home.timeZoneId == "Europe/Vienna"


def test_set_powermeter_unit_price(fake_home: Home):
    with no_ssl_verification():
        fake_home.set_powermeter_unit_price(12.0)
        fake_home.get_current_state()
        assert fake_home.powerMeterUnitPrice == 12.0
        fake_home.set_powermeter_unit_price(8.5)
        fake_home.get_current_state()
        assert fake_home.powerMeterUnitPrice == 8.5


def test_indoor_climate_home(fake_home: Home):
    with no_ssl_verification():
        for fh in fake_home.functionalHomes:
            if not isinstance(fh, IndoorClimateHome):
                continue
            assert fh.active is True
            assert fh.absenceType == AbsenceType.NOT_ABSENT
            assert fh.coolingEnabled is False
            assert fh.ecoDuration == EcoDuration.PERMANENT
            assert fh.ecoTemperature == 17.0
            assert fh.optimumStartStopEnabled is False

            minutes = 20
            fake_home.activate_absence_with_duration(minutes)
            absence_end = datetime.now() + timedelta(minutes=minutes)
            absence_end = absence_end.replace(second=0, microsecond=0)

            fake_home.get_current_state()

            assert fh.absenceType == AbsenceType.PERIOD
            assert fh.absenceEndTime == absence_end

            absence_end = datetime.strptime("2100_01_01 22:22", "%Y_%m_%d %H:%M")

            fake_home.activate_absence_with_period(absence_end)

            fake_home.get_current_state()

            assert fh.absenceType == AbsenceType.PERIOD
            assert fh.absenceEndTime == absence_end

            fake_home.activate_absence_permanent()

            fake_home.get_current_state()

            assert fh.absenceType == AbsenceType.PERMANENT
            assert fh.absenceEndTime == datetime.strptime(
                "2100_12_31 23:59", "%Y_%m_%d %H:%M"
            )
            assert fh.ecoDuration == EcoDuration.PERMANENT

            fake_home.deactivate_absence()

            fake_home.get_current_state()
            assert fh.absenceType == AbsenceType.NOT_ABSENT
            assert fh.absenceEndTime is None


def test_get_functionalHome(fake_home: Home):
    functionalHome = fake_home.get_functionalHome(SecurityAndAlarmHome)
    assert isinstance(functionalHome, SecurityAndAlarmHome)

    functionalHome = fake_home.get_functionalHome(IndoorClimateHome)
    assert isinstance(functionalHome, IndoorClimateHome)

    functionalHome = fake_home.get_functionalHome(WeatherAndEnvironmentHome)
    assert isinstance(functionalHome, WeatherAndEnvironmentHome)

    functionalHome = fake_home.get_functionalHome(AccessControlHome)
    assert isinstance(functionalHome, AccessControlHome)

    functionalHome = fake_home.get_functionalHome(Home)
    assert functionalHome is None


def test_security_setIntrusionAlertThroughSmokeDetectors(fake_home: Home):
    with no_ssl_verification():
        securityAlarmHome = fake_home.get_functionalHome(SecurityAndAlarmHome)
        assert securityAlarmHome.intrusionAlertThroughSmokeDetectors is False

        fake_home.set_intrusion_alert_through_smoke_detectors(True)
        fake_home.get_current_state()
        securityAlarmHome = fake_home.get_functionalHome(SecurityAndAlarmHome)
        assert securityAlarmHome.intrusionAlertThroughSmokeDetectors is True

        fake_home.set_intrusion_alert_through_smoke_detectors(False)
        fake_home.get_current_state()
        securityAlarmHome = fake_home.get_functionalHome(SecurityAndAlarmHome)
        assert securityAlarmHome.intrusionAlertThroughSmokeDetectors is False


def test_heating_vacation(fake_home: Home):
    with no_ssl_verification():
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow = tomorrow.replace(second=0, microsecond=0)

        fake_home.activate_vacation(tomorrow, 12)

        fake_home.get_current_state()
        heatingHome = fake_home.get_functionalHome(IndoorClimateHome)
        assert heatingHome.absenceEndTime == tomorrow
        assert heatingHome.absenceType == AbsenceType.VACATION

        fake_home.deactivate_vacation()

        fake_home.get_current_state()
        heatingHome = fake_home.get_functionalHome(IndoorClimateHome)
        assert heatingHome.absenceEndTime is None
        assert heatingHome.absenceType == AbsenceType.NOT_ABSENT


def test_security_setZoneActivationDelay(fake_home: Home):
    with no_ssl_verification():
        securityAlarmHome = fake_home.get_functionalHome(SecurityAndAlarmHome)
        assert securityAlarmHome.zoneActivationDelay == 0.0

        fake_home.set_zone_activation_delay(5.0)
        fake_home.get_current_state()
        securityAlarmHome = fake_home.get_functionalHome(SecurityAndAlarmHome)
        assert securityAlarmHome.zoneActivationDelay == 5.0

        fake_home.set_zone_activation_delay(0.0)
        fake_home.get_current_state()
        securityAlarmHome = fake_home.get_functionalHome(SecurityAndAlarmHome)
        assert securityAlarmHome.zoneActivationDelay == 0.0


def test_home_getSecurityJournal(fake_home: Home):
    with no_ssl_verification():
        journal = fake_home.get_security_journal()
        # todo make more advanced tests
        assert isinstance(journal[0], ActivationChangedEvent)
        assert isinstance(journal[1], ActivationChangedEvent)
        assert isinstance(journal[2], AccessPointDisconnectedEvent)
        assert isinstance(journal[3], AccessPointConnectedEvent)
        assert isinstance(journal[4], SensorEvent)
        assert isinstance(journal[5], SabotageEvent)
        assert isinstance(journal[6], MoistureDetectionEvent)
        assert isinstance(journal[7], SecurityEvent)


def test_home_unknown_types(fake_home: Home):
    with no_ssl_verification():
        fake_home._rest_call(
            "fake/loadConfig", json.dumps({"file": "unknown_types.json"})
        )
        fake_home.get_current_state(clearConfig=True)
        group = fake_home.groups[0]
        assert type(group) == Group
        assert group.groupType == "DUMMY_GROUP"

        device = fake_home.devices[0]
        assert type(device) == BaseDevice
        assert device.deviceType == "DUMMY_DEVICE"

        funcHome = fake_home.functionalHomes[0]
        assert type(funcHome) == FunctionalHome
        assert funcHome.solution == "DUMMY_FUNCTIONAL_HOME"


def test_home_getOAuthOTK(fake_home: Home):
    with no_ssl_verification():
        token = fake_home.get_OAuth_OTK()
        assert token.authToken == "C001ED"
        assert token.expirationTimestamp == datetime(
            2018, 12, 23, 11, 38, 21, 680000
        ) + timedelta(0, utc_offset)


def test_search_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F71100000000000WWRC6", 10)
        assert ch.index == 10
        assert ch.device.id == "3014F71100000000000WWRC6"
