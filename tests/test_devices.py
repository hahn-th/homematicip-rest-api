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


def test_room_control_device(fake_home: Home):
    d = fake_home.search_device_by_id("3014F711000BBBB000000000")
    assert isinstance(d, RoomControlDevice)

    assert d.vaporAmount == 10.662700840292974
    assert d.temperatureOffset == 0.0
    assert d.setPointTemperature == 20.0
    assert d.actualTemperature == 23.0

    assert str(d) == (
        "ALPHA-IP-RBG Raumbediengerät lowBat(False) unreach(False) rssiDeviceValue(-45) "
        "rssiPeerValue(-54) configPending(False) dutyCycle(False) operationLockActive(False) "
        "actualTemperature(23.0) humidity(52) vaporAmount(10.662700840292974) setPointTemperature(20.0)"
    )


def test_room_control_device_analog(fake_home: Home):
    d = fake_home.search_device_by_id("3014F711000000BBBB000005")
    assert isinstance(d, RoomControlDeviceAnalog)

    assert d.temperatureOffset == 0.0
    assert d.setPointTemperature == 23.0
    assert d.actualTemperature == 23.3

    assert str(d) == (
        "ALPHA-IP-RBGa Raumbediengerät lowBat(False) unreach(False) rssiDeviceValue(-41) "
        "rssiPeerValue(-29) configPending(False) dutyCycle(False) actualTemperature(23.3) "
        "setPointTemperature(23.0) temperatureOffset(0.0)"
    )


def test_acceleration_sensor(fake_home: Home):
    d = fake_home.search_device_by_id("3014F7110000000000000031")
    assert isinstance(d, AccelerationSensor)
    assert d.accelerationSensorEventFilterPeriod == 3.0
    assert d.accelerationSensorMode == AccelerationSensorMode.FLAT_DECT
    assert (
        d.accelerationSensorNeutralPosition
        == AccelerationSensorNeutralPosition.VERTICAL
    )
    assert (
        d.accelerationSensorSensitivity == AccelerationSensorSensitivity.SENSOR_RANGE_4G
    )
    assert d.accelerationSensorTriggerAngle == 45
    assert d.accelerationSensorTriggered is True
    assert d.notificationSoundTypeHighToLow == NotificationSoundType.SOUND_LONG
    assert d.notificationSoundTypeLowToHigh == NotificationSoundType.SOUND_LONG

    assert str(d) == (
        "HmIP-SAM Garagentor lowBat(False) unreach(False) "
        "rssiDeviceValue(-88) rssiPeerValue(None) configPending(False)"
        " dutyCycle(False) accelerationSensorEventFilterPeriod(3.0)"
        " accelerationSensorMode(FLAT_DECT) accelerationSensorNeutralPosition(VERTICAL)"
        " accelerationSensorSensitivity(SENSOR_RANGE_4G) accelerationSensorTriggerAngle(45)"
        " accelerationSensorTriggered(True) notificationSoundTypeHighToLow(SOUND_LONG)"
        " notificationSoundTypeLowToHigh(SOUND_LONG)"
    )

    with no_ssl_verification():
        d.set_acceleration_sensor_event_filter_period(10.0)
        d.set_acceleration_sensor_mode(AccelerationSensorMode.ANY_MOTION)
        d.set_acceleration_sensor_neutral_position(
            AccelerationSensorNeutralPosition.HORIZONTAL
        )
        d.set_acceleration_sensor_sensitivity(
            AccelerationSensorSensitivity.SENSOR_RANGE_2G
        )
        d.set_acceleration_sensor_trigger_angle(30)
        d.set_notification_sound_type(NotificationSoundType.SOUND_SHORT, True)
        d.set_notification_sound_type(NotificationSoundType.SOUND_SHORT_SHORT, False)

        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F7110000000000000031")

        assert d.accelerationSensorEventFilterPeriod == 10.0
        assert d.accelerationSensorMode == AccelerationSensorMode.ANY_MOTION
        assert (
            d.accelerationSensorNeutralPosition
            == AccelerationSensorNeutralPosition.HORIZONTAL
        )
        assert (
            d.accelerationSensorSensitivity
            == AccelerationSensorSensitivity.SENSOR_RANGE_2G
        )
        assert d.accelerationSensorTriggerAngle == 30
        assert d.notificationSoundTypeHighToLow == NotificationSoundType.SOUND_SHORT
        assert (
            d.notificationSoundTypeLowToHigh == NotificationSoundType.SOUND_SHORT_SHORT
        )


def test_multi_io_box(fake_home: Home):
    d = fake_home.search_device_by_id("3014F711ABCD0ABCD000002")
    assert isinstance(d, MultiIOBox)
    assert d.on is True
    assert d.functionalChannels[2].on is False
    assert d.analogOutputLevel == 12.5
    assert d.functionalChannels[5].analogOutputLevel == 12.5

    assert str(d) == (
        "HmIP-MIOB Multi IO Box lowBat(None) unreach(False) "
        "rssiDeviceValue(-79) rssiPeerValue(None) configPending(False) "
        "dutyCycle(False) on(True) profileMode(None) "
        "userDesiredProfileMode(AUTOMATIC) analogOutputLevel(12.5)"
    )


def test_full_flush_contact_interface(fake_home: Home):
    d = fake_home.search_device_by_id("3014F7110000000000000029")
    assert isinstance(d, FullFlushContactInterface)

    assert d.binaryBehaviorType == BinaryBehaviorType.NORMALLY_CLOSE
    assert d.windowState == WindowState.CLOSED
    assert d.multiModeInputMode == MultiModeInputMode.KEY_BEHAVIOR

    assert str(d) == (
        "HmIP-FCI1 Kontakt-Schnittstelle Unterputz – 1-fach lowBat(False) unreach(False) rssiDeviceValue(-46) rssiPeerValue(None) configPending(False) "
        "dutyCycle(False) binaryBehaviorType(NORMALLY_CLOSE) multiModeInputMode(KEY_BEHAVIOR) windowState(CLOSED)"
    )


def test_shutter_device(fake_home: Home):
    d = fake_home.search_device_by_id("3014F7110000000000000001")
    assert isinstance(d, ShutterContact)
    assert d.label == "Fenster"
    assert d.lastStatusUpdate == datetime(2018, 4, 23, 20, 37, 34, 304000) + timedelta(
        0, utc_offset
    )
    assert d.manufacturerCode == 1
    assert d.modelId == 258
    assert d.modelType == "HMIP-SWDO"
    assert d.oem == "eQ-3"
    assert d.windowState == WindowState.CLOSED
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000000001"
    assert d.availableFirmwareVersion == "1.16.8"
    assert d.firmwareVersion == "1.16.8"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert d.lowBat is False
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -64
    assert d.rssiPeerValue is None
    assert d.dutyCycle is False
    assert d.configPending is False
    assert (
        str(d)
        == "HMIP-SWDO Fenster lowBat(False) unreach(False) rssiDeviceValue(-64) rssiPeerValue(None) configPending(False) dutyCycle(False) sabotage(False) windowState(CLOSED)"
    )
    assert (
        d._rawJSONData
        == fake_home_download_configuration()["devices"]["3014F7110000000000000001"]
    )

    d = fake_home.search_device_by_id("3014F7110000000000000005")
    assert d.windowState == WindowState.OPEN
    assert d.lastStatusUpdate is None

    assert (
        d.set_router_module_enabled(True) is False
    )  # Shutter contact won't support this


def test_shutter_device_magnetic(fake_home: Home):
    d = fake_home.search_device_by_id("3014F7110000000000005551")
    assert isinstance(d, ShutterContactMagnetic)
    assert d.label == "Eingangstürkontakt"
    assert d.lastStatusUpdate == datetime(2018, 4, 23, 20, 37, 34, 304000) + timedelta(
        0, utc_offset
    )
    assert d.manufacturerCode == 1
    assert d.modelId == 340
    assert d.modelType == "HmIP-SWDM"
    assert d.oem == "eQ-3"
    assert d.windowState == WindowState.CLOSED
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000005551"
    assert d.availableFirmwareVersion == "0.0.0"
    assert d.firmwareVersion == "1.2.12"
    assert d.firmwareVersionInteger == 66060
    assert d.lowBat is False
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -73
    assert d.rssiPeerValue is None
    assert d.dutyCycle is False
    assert d.configPending is False
    assert (
        str(d)
        == "HmIP-SWDM Eingangstürkontakt lowBat(False) unreach(False) rssiDeviceValue(-73) rssiPeerValue(None) configPending(False) dutyCycle(False) windowState(CLOSED)"
    )
    assert (
        d._rawJSONData
        == fake_home_download_configuration()["devices"]["3014F7110000000000005551"]
    )


def test_contact_interface_device(fake_home: Home):
    d = fake_home.search_device_by_id("3014F7110000000000000064")
    assert isinstance(d, ContactInterface)
    assert d.label == "Schließer Magnet"
    assert d.lastStatusUpdate == datetime(2018, 4, 23, 20, 37, 34, 304000) + timedelta(
        0, utc_offset
    )
    assert d.manufacturerCode == 1
    assert d.modelId == 375
    assert d.modelType == "HmIP-SCI"
    assert d.oem == "eQ-3"
    assert d.windowState == WindowState.CLOSED
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000000064"
    assert d.availableFirmwareVersion == "1.0.6"
    assert d.firmwareVersion == "1.0.6"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert d.lowBat is False
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -42
    assert d.rssiPeerValue is None
    assert d.dutyCycle is False
    assert d.configPending is False
    assert d.deviceOverheated is True
    assert d.deviceOverloaded is True
    assert d.deviceUndervoltage is True
    assert d.temperatureOutOfRange is True
    assert d.coProFaulty is True
    assert d.coProRestartNeeded is True
    assert d.coProUpdateFailure is True

    assert str(d) == (
        "HmIP-SCI Schließer Magnet lowBat(False) unreach(False) rssiDeviceValue(-42) rssiPeerValue(None) "
        "configPending(False) dutyCycle(False) coProFaulty(True) coProRestartNeeded(True) "
        "coProUpdateFailure(True) deviceOverheated(True) deviceOverloaded(True) temperatureOutOfRange(True) "
        "deviceUndervoltage(True) sabotage(False) windowState(CLOSED)"
    )
    assert (
        d._rawJSONData
        == fake_home_download_configuration()["devices"]["3014F7110000000000000064"]
    )


def test_pluggable_switch_measuring(fake_home: Home):
    d = fake_home.search_device_by_id("3014F7110000000000000009")
    assert isinstance(d, PlugableSwitchMeasuring)
    assert d.label == "Brunnen"
    assert d.lastStatusUpdate == (
        datetime(2018, 4, 23, 20, 36, 26, 303000) + timedelta(0, utc_offset)
    )
    assert d.manufacturerCode == 1
    assert d.modelId == 262
    assert d.modelType == "HMIP-PSM"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000000009"
    assert d.updateState == DeviceUpdateState.UP_TO_DATE
    assert d.on is False
    assert d.profileMode == "AUTOMATIC"
    assert d.userDesiredProfileMode == "AUTOMATIC"
    assert d.currentPowerConsumption == 0.0
    assert d.energyCounter == 0.4754
    assert d.lowBat is None
    assert d.routerModuleEnabled is True
    assert d.routerModuleSupported is True
    assert d.rssiDeviceValue == -60
    assert d.rssiPeerValue == -66
    assert d.unreach is False
    assert d.availableFirmwareVersion == "0.0.0"
    assert d.firmwareVersion == "2.6.2"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert d.dutyCycle is False
    assert d.configPending is False

    assert str(d) == (
        "HMIP-PSM Brunnen lowBat(None) unreach(False) rssiDeviceValue(-60) rssiPeerValue(-66) configPending(False) dutyCycle(False) on(False) profileMode(AUTOMATIC)"
        " userDesiredProfileMode(AUTOMATIC) energyCounter(0.4754) currentPowerConsumption(0.0W)"
    )
    assert (
        d._rawJSONData
        == fake_home_download_configuration()["devices"]["3014F7110000000000000009"]
    )

    with no_ssl_verification():
        d.turn_on()
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F7110000000000000009")
        assert d.on is True

        d.turn_off()
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F7110000000000000009")
        assert d.on is False

        d.id = "INVALID_ID"
        result = d.turn_off()
        assert result["errorCode"] == "INVALID_DEVICE"


def test_smoke_detector(fake_home: Home):
    d = fake_home.search_device_by_id("3014F7110000000000000020")
    assert isinstance(d, SmokeDetector)
    assert d.label == "Rauchwarnmelder3"
    assert d.lastStatusUpdate == datetime(2018, 4, 23, 4, 5, 24, 824000) + timedelta(
        0, utc_offset
    )
    assert d.manufacturerCode == 1
    assert d.modelId == 296
    assert d.modelType == "HmIP-SWSD"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000000020"
    assert d.updateState == DeviceUpdateState.UP_TO_DATE
    assert d.lowBat is False
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -54
    assert d.rssiPeerValue is None
    assert d.unreach is False
    assert d.smokeDetectorAlarmType == SmokeDetectorAlarmType.IDLE_OFF
    assert d.availableFirmwareVersion == "0.0.0"
    assert d.firmwareVersion == "1.0.11"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert d.configPending is False
    assert (
        str(d)
        == "HmIP-SWSD Rauchwarnmelder3 lowBat(False) unreach(False) rssiDeviceValue(-54) rssiPeerValue(None) configPending(False) dutyCycle(False) smokeDetectorAlarmType(IDLE_OFF)"
    )
    assert (
        d._rawJSONData
        == fake_home_download_configuration()["devices"]["3014F7110000000000000020"]
    )


def test_wall_mounted_thermostat_pro(fake_home: Home):
    d = fake_home.search_device_by_id("3014F7110000000000000022")
    assert isinstance(d, WallMountedThermostatPro)
    assert d.id == "3014F7110000000000000022"
    assert d.label == "Wandthermostat"
    assert d.lastStatusUpdate == datetime(2018, 4, 23, 20, 48, 54, 382000) + timedelta(
        0, utc_offset
    )
    assert d.manufacturerCode == 1
    assert d.modelId == 297
    assert d.modelType == "HmIP-WTH-2"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000000022"
    assert d.updateState == DeviceUpdateState.UP_TO_DATE
    assert d.humidity == 43
    assert d.vaporAmount == 6.177718198711658
    assert d.setPointTemperature == 5.0
    assert d.display == ClimateControlDisplay.ACTUAL_HUMIDITY
    assert d.temperatureOffset == 0.0
    assert d.lowBat is False
    assert d.operationLockActive is False
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -76
    assert d.rssiPeerValue == -63
    assert d.unreach is False
    assert d.dutyCycle is False
    assert d.availableFirmwareVersion == "0.0.0"
    assert d.firmwareVersion == "1.8.0"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert str(d) == (
        "HmIP-WTH-2 Wandthermostat lowBat(False) unreach(False) rssiDeviceValue(-76) rssiPeerValue(-63)"
        " configPending(False) dutyCycle(False) operationLockActive(False)"
        " actualTemperature(24.7) humidity(43) vaporAmount(6.177718198711658) setPointTemperature(5.0)"
    )
    assert (
        d._rawJSONData
        == fake_home_download_configuration()["devices"]["3014F7110000000000000022"]
    )

    with no_ssl_verification():
        d.set_display(ClimateControlDisplay.ACTUAL)
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F7110000000000000022")
        assert d.display == ClimateControlDisplay.ACTUAL

        d.id = "INVALID_ID"
        result = d.set_display(ClimateControlDisplay.ACTUAL)
        assert result["errorCode"] == "INVALID_DEVICE"


def test_heating_thermostat(fake_home: Home):
    d = fake_home.search_device_by_id("3014F7110000000000000015")
    assert isinstance(d, HeatingThermostat)
    assert d.label == "Wohnzimmer-Heizung"
    assert d.lastStatusUpdate == datetime(2018, 4, 23, 20, 5, 50, 325000) + timedelta(
        0, utc_offset
    )
    assert d.manufacturerCode == 1
    assert d.modelId == 269
    assert d.modelType == "HMIP-eTRV"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000000015"
    assert d.updateState == DeviceUpdateState.UP_TO_DATE
    assert d.setPointTemperature == 5.0
    assert d.temperatureOffset == 0.0
    assert d.valvePosition == 0.0
    assert d.valveState == ValveState.ADAPTION_DONE
    assert d.lowBat is False
    assert d.operationLockActive is True
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -65
    assert d.rssiPeerValue == -66
    assert d.unreach is False
    assert d.automaticValveAdaptionNeeded is False
    assert d.availableFirmwareVersion == "2.0.2"
    assert d.firmwareVersion == "2.0.2"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert d.valveActualTemperature == 20.0

    assert str(d) == (
        "HMIP-eTRV Wohnzimmer-Heizung lowBat(False) unreach(False) "
        "rssiDeviceValue(-65) rssiPeerValue(-66) configPending(False) "
        "dutyCycle(False) operationLockActive(True) valvePosition(0.0) "
        "valveState(ADAPTION_DONE) temperatureOffset(0.0) "
        "setPointTemperature(5.0) valveActualTemperature(20.0)"
    )
    assert (
        d._rawJSONData
        == fake_home_download_configuration()["devices"]["3014F7110000000000000015"]
    )

    with no_ssl_verification():
        d.set_operation_lock(False)
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F7110000000000000015")
        assert d.operationLockActive is False

        d.id = "INVALID_ID"
        result = d.set_operation_lock(True)
        assert result["errorCode"] == "INVALID_DEVICE"


def test_heating_thermostat_compact(fake_home: Home):
    d = fake_home.search_device_by_id("3014F71100000000ABCDEF10")
    assert isinstance(d, HeatingThermostatCompact)
    assert d.label == "Wohnzimmer 3"
    assert d.modelType == "HmIP-eTRV-C"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F71100000000ABCDEF10"
    assert d.updateState == DeviceUpdateState.UP_TO_DATE
    assert d.setPointTemperature == 21.0
    assert d.temperatureOffset == 0.0
    assert d.valvePosition == 0.0
    assert d.valveState == ValveState.ADAPTION_DONE
    assert d.lowBat is False
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -47
    assert d.rssiPeerValue == -50
    assert d.unreach is False
    assert d.automaticValveAdaptionNeeded is False
    assert d.valveActualTemperature == 21.6

    assert str(d) == (
        "HmIP-eTRV-C Wohnzimmer 3 lowBat(False) unreach(False) rssiDeviceValue(-47) "
        "rssiPeerValue(-50) configPending(False) dutyCycle(False) sabotage(None) "
        "valvePosition(0.0) valveState(ADAPTION_DONE) temperatureOffset(0.0) "
        "setPointTemperature(21.0) valveActualTemperature(21.6)"
    )


def test_temperature_humidity_sensor_outdoor(fake_home: Home):
    d = fake_home.search_device_by_id("3014F711AAAA000000000002")
    assert isinstance(d, TemperatureHumiditySensorOutdoor)
    assert d.label == "Temperatur- und Luftfeuchtigkeitssensor - außen"
    assert d.lastStatusUpdate == datetime(2018, 4, 23, 20, 5, 50, 325000) + timedelta(
        0, utc_offset
    )
    assert d.manufacturerCode == 1
    assert d.modelId == 314
    assert d.modelType == "HmIP-STHO"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F711AAAA000000000002"
    assert d.updateState == DeviceUpdateState.UP_TO_DATE
    assert d.humidity == 70
    assert d.vaporAmount == 6.177718198711658
    assert d.actualTemperature == 15.1
    assert d.lowBat is False
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -55
    assert d.rssiPeerValue is None
    assert d.unreach is False
    assert d.configPending is False
    assert d.dutyCycle is False
    assert str(d) == (
        "HmIP-STHO Temperatur- und Luftfeuchtigkeitssensor - außen lowBat(False) unreach(False)"
        " rssiDeviceValue(-55) rssiPeerValue(None) configPending(False)"
        " dutyCycle(False) actualTemperature(15.1) humidity(70) vaporAmount(6.177718198711658)"
    )
    assert (
        d._rawJSONData
        == fake_home_download_configuration()["devices"]["3014F711AAAA000000000002"]
    )


def test_weather_sensor_pro(fake_home: Home):
    d = fake_home.search_device_by_id("3014F711AAAA000000000001")
    assert isinstance(d, WeatherSensorPro)
    assert d.label == "Wettersensor - pro"
    assert d.lastStatusUpdate == datetime(2018, 4, 23, 20, 5, 50, 325000) + timedelta(
        0, utc_offset
    )
    assert d.manufacturerCode == 1
    assert d.modelId == 352
    assert d.modelType == "HmIP-SWO-PR"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F711AAAA000000000001"
    assert d.updateState == DeviceUpdateState.UP_TO_DATE
    assert d.availableFirmwareVersion == "0.0.0"
    assert d.firmwareVersion == "1.0.10"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert d.humidity == 65
    assert d.vaporAmount == 6.177718198711658
    assert d.illumination == 4153.0
    assert d.illuminationThresholdSunshine == 10.0
    assert d.raining is False
    assert d.storm is False
    assert d.sunshine is True
    assert d.todayRainCounter == 6.5
    assert d.todaySunshineDuration == 100
    assert d.totalRainCounter == 6.5
    assert d.totalSunshineDuration == 100
    assert d.weathervaneAlignmentNeeded is False
    assert d.windDirection == 295.0
    assert d.windDirectionVariation == 56.25
    assert d.windSpeed == 2.6
    assert d.windValueType == WindValueType.AVERAGE_VALUE
    assert d.yesterdayRainCounter == 0.0
    assert d.yesterdaySunshineDuration == 0
    assert d.actualTemperature == 15.4
    assert d.lowBat is False
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -68
    assert d.rssiPeerValue is None
    assert d.unreach is False
    assert d.configPending is False
    assert d.dutyCycle is False
    assert str(d) == (
        "HmIP-SWO-PR Wettersensor - pro lowBat(False) unreach(False) rssiDeviceValue(-68)"
        " rssiPeerValue(None) configPending(False) dutyCycle(False)"
        " actualTemperature(15.4) humidity(65) vaporAmount(6.177718198711658)"
        " illumination(4153.0) illuminationThresholdSunshine(10.0)"
        " raining(False) storm(False) sunshine(True) todayRainCounter(6.5) todaySunshineDuration(100)"
        " totalRainCounter(6.5) totalSunshineDuration(100)"
        " weathervaneAlignmentNeeded(False) windDirection(295.0)"
        " windDirectionVariation(56.25) windSpeed(2.6)"
        " windValueType(AVERAGE_VALUE) yesterdayRainCounter(0.0) yesterdaySunshineDuration(0)"
    )
    assert (
        d._rawJSONData
        == fake_home_download_configuration()["devices"]["3014F711AAAA000000000001"]
    )


def test_weather_sensor(fake_home: Home):
    d = fake_home.search_device_by_id("3014F711AAAA000000000003")
    assert isinstance(d, WeatherSensor)
    assert d.lastStatusUpdate == datetime(2018, 4, 23, 20, 5, 50, 325000) + timedelta(
        0, utc_offset
    )
    assert d.lowBat is False
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -77
    assert d.rssiPeerValue is None
    assert d.unreach is False
    assert d.configPending is False
    assert d.dutyCycle is False
    assert d.availableFirmwareVersion == "0.0.0"
    assert d.firmwareVersion == "1.0.10"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert d.humidity == 42
    assert d.vaporAmount == 6.177718198711658
    assert d.illumination == 4890.0
    assert d.illuminationThresholdSunshine == 3500.0
    assert d.storm is False
    assert d.sunshine is True
    assert d.todaySunshineDuration == 51
    assert d.totalSunshineDuration == 54
    assert d.windSpeed == 6.6
    assert d.windValueType == WindValueType.MAX_VALUE
    assert d.yesterdaySunshineDuration == 3
    assert d.actualTemperature == 15.2
    assert d.label == "Wettersensor"
    assert d.manufacturerCode == 1
    assert d.modelId == 350
    assert d.modelType == "HmIP-SWO-B"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F711AAAA000000000003"
    assert d.updateState == DeviceUpdateState.UP_TO_DATE
    assert str(d) == (
        "HmIP-SWO-B Wettersensor lowBat(False) unreach(False) rssiDeviceValue(-77)"
        " rssiPeerValue(None) configPending(False) dutyCycle(False)"
        " actualTemperature(15.2) humidity(42) vaporAmount(6.177718198711658)"
        " illumination(4890.0) illuminationThresholdSunshine(3500.0) storm(False) sunshine(True)"
        " todaySunshineDuration(51) totalSunshineDuration(54) windSpeed(6.6)"
        " windValueType(MAX_VALUE) yesterdaySunshineDuration(3)"
    )
    assert (
        d._rawJSONData
        == fake_home_download_configuration()["devices"]["3014F711AAAA000000000003"]
    )


def test_weather_sensor_plus(fake_home: Home):
    d = fake_home.search_device_by_id("3014F7110000000000000038")
    assert isinstance(d, WeatherSensorPlus)
    assert d.humidity == 97
    assert d.vaporAmount == 6.177718198711658
    assert d.illumination == 26.4
    assert d.illuminationThresholdSunshine == 3500.0
    assert d.raining is False
    assert d.storm is False
    assert d.sunshine is False
    assert d.todayRainCounter == 3.8999999999999773
    assert d.todaySunshineDuration == 0
    assert d.totalRainCounter == 544.0999999999999
    assert d.totalSunshineDuration == 132057
    assert d.windSpeed == 15.0
    assert d.windValueType == WindValueType.CURRENT_VALUE
    assert d.yesterdayRainCounter == 25.600000000000023
    assert d.yesterdaySunshineDuration == 0
    assert d.actualTemperature == 4.3
    assert d.lowBat is False
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -55
    assert d.rssiPeerValue is None
    assert d.unreach is False
    assert d.configPending is False
    assert d.dutyCycle is False
    assert str(d) == (
        "HmIP-SWO-PL Weather Sensor \u2013 plus lowBat(False) unreach(False) rssiDeviceValue(-55)"
        " rssiPeerValue(None) configPending(False) dutyCycle(False) actualTemperature(4.3)"
        " humidity(97) vaporAmount(6.177718198711658) illumination(26.4)"
        " illuminationThresholdSunshine(3500.0) raining(False) storm(False)"
        " sunshine(False) todayRainCounter(3.8999999999999773) todaySunshineDuration(0)"
        " totalRainCounter(544.0999999999999) totalSunshineDuration(132057) windSpeed(15.0)"
        " windValueType(CURRENT_VALUE) yesterdayRainCounter(25.600000000000023) yesterdaySunshineDuration(0)"
    )
    assert (
        d._rawJSONData
        == fake_home_download_configuration()["devices"]["3014F7110000000000000038"]
    )


def test_rotary_handle_sensor(fake_home: Home):
    d = fake_home.search_device_by_id("3014F711AAAA000000000004")
    assert isinstance(d, RotaryHandleSensor)
    assert d.label == "Fenstergriffsensor"
    assert d.lastStatusUpdate == datetime(2018, 4, 27, 8, 6, 25, 462000) + timedelta(
        0, utc_offset
    )
    assert d.manufacturerCode == 1
    assert d.modelId == 286
    assert d.modelType == "HmIP-SRH"
    assert d.oem == "eQ-3"
    assert d.windowState == WindowState.TILTED
    assert d.serializedGlobalTradeItemNumber == "3014F711AAAA000000000004"
    assert d.availableFirmwareVersion == "1.2.10"
    assert d.firmwareVersion == "1.2.10"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c

    assert d.lowBat is False
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -54
    assert d.rssiPeerValue is None
    assert d.dutyCycle is False
    assert d.configPending is False
    assert str(d) == (
        "HmIP-SRH Fenstergriffsensor lowBat(False) unreach(False) rssiDeviceValue(-54) rssiPeerValue(None) configPending(False) dutyCycle(False)"
        " sabotage(False) windowState(TILTED)"
    )
    assert (
        d._rawJSONData
        == fake_home_download_configuration()["devices"]["3014F711AAAA000000000004"]
    )


def test_dimmer(fake_home: Home):
    d = fake_home.search_device_by_id("3014F711AAAA000000000005")
    assert isinstance(d, BrandDimmer)
    assert d.label == "Schlafzimmerlicht"
    assert d.lastStatusUpdate == datetime(2018, 4, 27, 8, 6, 25, 462000) + timedelta(
        0, utc_offset
    )
    assert d.modelId == 290
    assert d.modelType == "HmIP-BDT"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F711AAAA000000000005"
    assert d.updateState == DeviceUpdateState.UP_TO_DATE
    assert d.profileMode == "AUTOMATIC"
    assert d.userDesiredProfileMode == "AUTOMATIC"
    assert d.dimLevel == 0.0
    assert d.lowBat is None
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -44
    assert d.rssiPeerValue == -42
    assert d.unreach is False
    assert d.dutyCycle is False
    assert d.configPending is False
    assert d.availableFirmwareVersion == "0.0.0"
    assert d.firmwareVersion == "1.4.8"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c

    assert str(d) == (
        "HmIP-BDT Schlafzimmerlicht lowBat(None) unreach(False) rssiDeviceValue(-44) rssiPeerValue(-42) configPending(False) dutyCycle(False) dimLevel(0.0)"
        " profileMode(AUTOMATIC) userDesiredProfileMode(AUTOMATIC)"
    )

    with no_ssl_verification():
        d.set_dim_level(1.0)
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F711AAAA000000000005")
        assert d.dimLevel == 1.0

        d.set_dim_level(0.5)
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F711AAAA000000000005")
        assert d.dimLevel == 0.5

        d.id = "INVALID_ID"
        result = d.set_dim_level(0.5)
        assert result["errorCode"] == "INVALID_DEVICE"


def test_basic_device_functions(fake_home: Home):
    with no_ssl_verification():
        d = fake_home.search_device_by_id("3014F7110000000000000009")
        assert d.permanentlyReachable is True
        assert d.label == "Brunnen"
        assert d.routerModuleEnabled is True
        assert d.energyCounter == 0.4754

        d.set_label("new label")
        d.set_router_module_enabled(False)
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F7110000000000000009")
        assert d.label == "new label"
        assert d.routerModuleEnabled is False

        d.set_label("other label")
        d.set_router_module_enabled(True)
        d.reset_energy_counter()
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F7110000000000000009")
        assert d.label == "other label"
        assert d.routerModuleEnabled is True
        assert d.energyCounter == 0

        d2 = fake_home.search_device_by_id("3014F7110000000000000005")
        d.delete()
        fake_home.get_current_state()
        dNotFound = fake_home.search_device_by_id("3014F7110000000000000009")
        assert dNotFound is None
        assert d2 is fake_home.search_device_by_id(
            "3014F7110000000000000005"
        )  # make sure that the objects got updated and not completely renewed

        # check if the server is answering properly
        result = d.set_label("BLa")
        assert result["errorCode"] == "INVALID_DEVICE"
        result = d.delete()
        assert result["errorCode"] == "INVALID_DEVICE"

        result = d.reset_energy_counter()
        assert result["errorCode"] == "INVALID_DEVICE"

        result = d.set_router_module_enabled(False)
        assert result["errorCode"] == "INVALID_DEVICE"


def test_all_devices_implemented(fake_home: Home):
    not_implemented = False
    for d in fake_home.devices:
        if type(d) != Device:  # pragma: no cover
            print(f"{d.deviceType} isn't implemented yet")
            not_implemented = True
    assert not_implemented


def test_water_sensor(fake_home: Home):
    with no_ssl_verification():
        d = WaterSensor(fake_home._connection)  # just needed for intellisense
        d = fake_home.search_device_by_id("3014F7110000000000000050")
        assert d.label == "Wassersensor"
        assert d.routerModuleEnabled is False
        assert d.routerModuleSupported is False

        assert d.incorrectPositioned is True
        assert d.acousticAlarmSignal == AcousticAlarmSignal.FREQUENCY_RISING
        assert d.acousticAlarmTiming == AcousticAlarmTiming.ONCE_PER_MINUTE
        assert d.acousticWaterAlarmTrigger == WaterAlarmTrigger.WATER_DETECTION
        assert d.inAppWaterAlarmTrigger == WaterAlarmTrigger.WATER_MOISTURE_DETECTION
        assert d.moistureDetected is False
        assert d.sirenWaterAlarmTrigger == WaterAlarmTrigger.WATER_MOISTURE_DETECTION
        assert d.waterlevelDetected is False

        d.set_acoustic_alarm_timing(AcousticAlarmTiming.SIX_MINUTES)
        d.set_acoustic_alarm_signal(AcousticAlarmSignal.FREQUENCY_ALTERNATING_LOW_HIGH)
        d.set_inapp_water_alarm_trigger(WaterAlarmTrigger.MOISTURE_DETECTION)
        d.set_acoustic_water_alarm_trigger(WaterAlarmTrigger.NO_ALARM)
        d.set_siren_water_alarm_trigger(WaterAlarmTrigger.NO_ALARM)

        assert str(d) == (
            "HmIP-SWD Wassersensor lowBat(False) unreach(False) rssiDeviceValue(-65) rssiPeerValue(None) configPending(False) "
            "dutyCycle(False) incorrectPositioned(True) acousticAlarmSignal(FREQUENCY_RISING) acousticAlarmTiming(ONCE_PER_MINUTE) "
            "acousticWaterAlarmTrigger(WATER_DETECTION) inAppWaterAlarmTrigger(WATER_MOISTURE_DETECTION) moistureDetected(False) "
            "sirenWaterAlarmTrigger(WATER_MOISTURE_DETECTION) waterlevelDetected(False)"
        )

        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F7110000000000000050")

        assert d.acousticAlarmTiming == AcousticAlarmTiming.SIX_MINUTES
        assert (
            d.acousticAlarmSignal == AcousticAlarmSignal.FREQUENCY_ALTERNATING_LOW_HIGH
        )
        assert d.acousticWaterAlarmTrigger == WaterAlarmTrigger.NO_ALARM
        assert d.inAppWaterAlarmTrigger == WaterAlarmTrigger.MOISTURE_DETECTION
        assert d.sirenWaterAlarmTrigger == WaterAlarmTrigger.NO_ALARM

        d.id = "INVALID_ID"
        result = d.set_acoustic_alarm_timing(AcousticAlarmTiming.SIX_MINUTES)
        assert result["errorCode"] == "INVALID_DEVICE"
        result = d.set_acoustic_alarm_signal(
            AcousticAlarmSignal.FREQUENCY_ALTERNATING_LOW_HIGH
        )
        assert result["errorCode"] == "INVALID_DEVICE"
        result = d.set_inapp_water_alarm_trigger(WaterAlarmTrigger.MOISTURE_DETECTION)
        assert result["errorCode"] == "INVALID_DEVICE"
        result = d.set_acoustic_water_alarm_trigger(WaterAlarmTrigger.NO_ALARM)
        assert result["errorCode"] == "INVALID_DEVICE"
        result = d.set_siren_water_alarm_trigger(WaterAlarmTrigger.NO_ALARM)
        assert result["errorCode"] == "INVALID_DEVICE"


def test_motion_detector_push_button(fake_home: Home):
    d = MotionDetectorPushButton(fake_home._connection)
    d = fake_home.search_device_by_id("3014F711000000000AAAAA25")

    assert isinstance(d, MotionDetectorPushButton)
    assert d.permanentFullRx is True
    assert d.illumination == 14.2
    assert d.currentIllumination is None
    assert d.motionBufferActive is True
    assert d.motionDetected is False
    assert d.motionDetectionSendInterval == MotionDetectionSendInterval.SECONDS_240
    assert d.numberOfBrightnessMeasurements == 7

    assert str(d) == (
        "HmIP-SMI55 Bewegungsmelder für 55er Rahmen – innen lowBat(False) unreach(False) rssiDeviceValue(-46) "
        "rssiPeerValue(None) configPending(False) dutyCycle(False) motionDetected(False) "
        "illumination(14.2) motionBufferActive(True) motionDetectionSendInterval(SECONDS_240) "
        "numberOfBrightnessMeasurements(7) currentIllumination(None) permanentFullRx(True)"
    )


def test_motion_detector(fake_home: Home):
    d = MotionDetectorIndoor(fake_home._connection)
    d = fake_home.search_device_by_id("3014F711000000000000BB11")

    assert d.illumination == 0.1
    assert d.currentIllumination is None
    assert d.motionBufferActive is False
    assert d.motionDetected is True
    assert d.motionDetectionSendInterval == MotionDetectionSendInterval.SECONDS_480
    assert d.numberOfBrightnessMeasurements == 7

    assert str(d) == (
        "HmIP-SMI Wohnzimmer lowBat(False) unreach(False) rssiDeviceValue(-56) rssiPeerValue(-52) configPending(False) "
        "dutyCycle(False) sabotage(False) motionDetected(True) illumination(0.1) motionBufferActive(False) "
        "motionDetectionSendInterval(SECONDS_480) numberOfBrightnessMeasurements(7)"
    )

    d = MotionDetectorOutdoor(fake_home._connection)
    d = fake_home.search_device_by_id("3014F71100000000000BBB17")

    assert d.illumination == 233.4
    assert d.currentIllumination is None
    assert d.motionBufferActive is True
    assert d.motionDetected is True
    assert d.motionDetectionSendInterval == MotionDetectionSendInterval.SECONDS_240
    assert d.numberOfBrightnessMeasurements == 7

    assert str(d) == (
        "HmIP-SMO-A Außen Küche lowBat(False) unreach(False) rssiDeviceValue(-70) rssiPeerValue(-67) configPending(False) "
        "dutyCycle(False) motionDetected(True) illumination(233.4) motionBufferActive(True) "
        "motionDetectionSendInterval(SECONDS_240) numberOfBrightnessMeasurements(7) currentIllumination(None)"
    )


def test_presence_detector_indoor(fake_home: Home):
    d = PresenceDetectorIndoor(fake_home._connection)
    d = fake_home.search_device_by_id("3014F711AAAAAAAAAAAAAA51")

    assert d.illumination == 1.8
    assert d.currentIllumination is None
    assert d.motionBufferActive is False
    assert d.presenceDetected is False
    assert d.motionDetectionSendInterval == MotionDetectionSendInterval.SECONDS_240
    assert d.numberOfBrightnessMeasurements == 7

    assert str(d) == (
        "HmIP-SPI SPI_1 lowBat(False) unreach(False) rssiDeviceValue(-62) rssiPeerValue(-61) configPending(False) "
        "dutyCycle(False) sabotage(False) presenceDetected(False) illumination(1.8) motionBufferActive(False) "
        "motionDetectionSendInterval(SECONDS_240) numberOfBrightnessMeasurements(7)"
    )


def test_push_button_6(fake_home: Home):
    d = PushButton6(fake_home._connection)
    d = fake_home.search_device_by_id("3014F711BBBBBBBBBBBBB017")

    assert d.modelId == 300
    assert d.label == "Wandtaster - 6-fach"


def test_remote_control_8(fake_home: Home):
    d = PushButton6(fake_home._connection)
    d = fake_home.search_device_by_id("3014F711BBBBBBBBBBBBB016")

    assert d.modelId == 299
    assert d.label == "Fernbedienung - 8 Tasten"


def test_open_collector_8(fake_home: Home):
    with no_ssl_verification():
        d = OpenCollector8Module(fake_home._connection)
        d = fake_home.search_device_by_id("3014F711BBBBBBBBBBBBB18")

        c = d.functionalChannels[2]

        assert isinstance(c, SwitchChannel)
        assert c.index == 2
        assert c.on is False
        assert c.profileMode == "AUTOMATIC"

        c = d.functionalChannels[8]

        assert isinstance(c, SwitchChannel)
        assert c.index == 8
        assert c.on is True
        assert c.profileMode == "AUTOMATIC"

        d.turn_off(8)
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F711BBBBBBBBBBBBB18")
        c = d.functionalChannels[8]
        assert c.on is False


def test_passage_detector(fake_home: Home):
    with no_ssl_verification():
        d = PassageDetector(fake_home._connection)
        d = fake_home.search_device_by_id("3014F7110000000000000054")
        assert d.leftCounter == 966
        assert d.leftRightCounterDelta == 164
        assert d.passageBlindtime == 1.5
        assert d.passageDirection == PassageDirection.LEFT
        assert d.passageSensorSensitivity == 50.0
        assert d.passageTimeout == 0.5
        assert d.rightCounter == 802

        assert str(d) == (
            "HmIP-SPDR SPDR_1 lowBat(False) unreach(False) rssiDeviceValue(-76) rssiPeerValue(None) configPending(False) dutyCycle(False)"
            " sabotage(False) leftCounter(966) leftRightCounterDelta(164) passageBlindtime(1.5) passageDirection(LEFT) passageSensorSensitivity(50.0)"
            " passageTimeout(0.5) rightCounter(802)"
        )


def test_full_flush_shutter(fake_home: Home):
    with no_ssl_verification():
        d = FullFlushShutter(fake_home._connection)
        d = fake_home.search_device_by_id("3014F711ACBCDABCADCA66")

        assert d.bottomToTopReferenceTime == 30.080000000000002
        assert d.changeOverDelay == 0.5
        assert d.delayCompensationValue == 12.7
        assert d.endpositionAutoDetectionEnabled is True
        assert d.previousShutterLevel is None
        assert d.processing is False
        assert d.profileMode == "AUTOMATIC"
        assert d.selfCalibrationInProgress is None
        assert d.shutterLevel == 1.0
        assert d.supportingDelayCompensation is True
        assert d.supportingEndpositionAutoDetection is True
        assert d.supportingSelfCalibration is True
        assert d.topToBottomReferenceTime == 24.68
        assert d.userDesiredProfileMode == "AUTOMATIC"

        assert str(d) == (
            "HmIP-BROLL BROLL_1 lowBat(None) unreach(False) rssiDeviceValue(-78) rssiPeerValue(-77) configPending(False)"
            " dutyCycle(False) shutterLevel(1.0) topToBottom(24.68) bottomToTop(30.080000000000002)"
        )

        d.set_shutter_level(0.4)
        d.set_shutter_stop()  # this will not do anything in the test run
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F711ACBCDABCADCA66")
        assert d.shutterLevel == 0.4


def test_full_flush_blind(fake_home: Home):
    with no_ssl_verification():
        d = FullFlushBlind(fake_home._connection)
        d = fake_home.search_device_by_id("3014F711BADCAFE000000001")

        assert d.shutterLevel == 1.0
        assert d.slatsLevel == 1.0
        assert d.blindModeActive is True
        assert d.slatsReferenceTime == 2.0

        d.set_slats_level(0.4)
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F711BADCAFE000000001")
        assert d.shutterLevel == 1.0
        assert d.slatsLevel == 0.4

        d.set_slats_level(0.8, 0.3)
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F711BADCAFE000000001")
        assert d.shutterLevel == 0.3
        assert d.slatsLevel == 0.8

        assert str(d) == (
            "HmIP-FBL Sofa links lowBat(None) unreach(False) rssiDeviceValue(-73) "
            "rssiPeerValue(-78) configPending(False) dutyCycle(False) "
            "shutterLevel(0.3) topToBottom(41.0) bottomToTop(41.0) "
            "slatsLevel(0.8) blindModeActive(True)"
        )


def test_brand_blind(fake_home: Home):
    with no_ssl_verification():
        d = BrandBlind(fake_home._connection)
        d = fake_home.search_device_by_id("3014F71100000000000BBL24")
        assert isinstance(d, BrandBlind)

        assert str(d) == (
            "HmIP-BBL Jalousie Schiebetür lowBat(None) unreach(False) "
            "rssiDeviceValue(-64) rssiPeerValue(-76) configPending(False) "
            "dutyCycle(False) shutterLevel(0.885) topToBottom(53.68) bottomToTop(54.88) "
            "slatsLevel(1.0) blindModeActive(True)"
        )


def test_alarm_siren_indoor(fake_home: Home):
    with no_ssl_verification():
        d = AlarmSirenIndoor(fake_home._connection)
        d = fake_home.search_device_by_id("3014F7110000000000BBBBB8")

        assert str(d) == (
            "HmIP-ASIR Alarmsirene lowBat(False) unreach(False) rssiDeviceValue(-59) "
            "rssiPeerValue(None) configPending(False) dutyCycle(False) sabotage(False)"
        )


def test_alarm_siren_outdoor(fake_home: Home):
    with no_ssl_verification():
        d = AlarmSirenIndoor(fake_home._connection)
        d = fake_home.search_device_by_id("3014F7110000ABCDABCD0033")

        assert str(d) == (
            "HmIP-ASIR-O Alarmsirene – außen lowBat(False) unreach(False) rssiDeviceValue(-51) "
            "rssiPeerValue(None) configPending(False) dutyCycle(False) sabotage(False) badBatteryHealth(True)"
        )


def test_floor_terminal_block(fake_home: Home):
    with no_ssl_verification():
        d = FloorTerminalBlock6(fake_home._connection)
        d = fake_home.search_device_by_id("3014F7110000000000BBBBB1")

        assert d.frostProtectionTemperature == 8.0
        assert d.coolingEmergencyValue == 0.0
        assert d.globalPumpControl is True
        assert d.heatingEmergencyValue == 0.25
        assert d.heatingLoadType == HeatingLoadType.LOAD_BALANCING
        assert d.heatingValveType == HeatingValveType.NORMALLY_CLOSE
        assert d.valveProtectionDuration == 5
        assert d.valveProtectionSwitchingInterval == 14

        assert d.pumpFollowUpTime == 2
        assert d.pumpLeadTime == 2
        assert d.pumpProtectionDuration == 1
        assert d.pumpProtectionSwitchingInterval == 14

        assert str(d) == (
            "HmIP-FAL230-C6 Fußbodenheizungsaktor lowBat(None) unreach(False) "
            "rssiDeviceValue(-62) rssiPeerValue(None) configPending(False) dutyCycle(False) "
            "globalPumpControl(True) heatingValveType(NORMALLY_CLOSE) heatingLoadType(LOAD_BALANCING) "
            "coolingEmergencyValue(0.0) frostProtectionTemperature(8.0) "
            "heatingEmergencyValue(0.25) valveProtectionDuration(5) valveProtectionSwitchingInterval(14) "
            "pumpFollowUpTime(2) pumpLeadTime(2) "
            "pumpProtectionDuration(1) pumpProtectionSwitchingInterval(14)"
        )

        d = FloorTerminalBlock10(fake_home._connection)
        d = fake_home.search_device_by_id("3014F71100000000FAL24C10")

        assert str(d) == (
            "HmIP-FAL24-C10 Fußbodenheizungsaktor lowBat(None) unreach(False) "
            "rssiDeviceValue(-73) rssiPeerValue(-74) configPending(False) "
            "dutyCycle(False) globalPumpControl(True) heatingValveType(NORMALLY_CLOSE) "
            "heatingLoadType(LOAD_BALANCING) coolingEmergencyValue(0.0) "
            "frostProtectionTemperature(8.0) heatingEmergencyValue(0.25) "
            "valveProtectionDuration(5) valveProtectionSwitchingInterval(14) "
            "pumpFollowUpTime(2) pumpLeadTime(2) pumpProtectionDuration(1) "
            "pumpProtectionSwitchingInterval(14)"
        )

        d = FloorTerminalBlock12(fake_home._connection)
        d = fake_home.search_device_by_id("3014F7110000000000000049")
        assert d.minimumFloorHeatingValvePosition == 0.0

        d.set_minimum_floor_heating_valve_position(0.2)

        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F7110000000000000049")
        assert d.minimumFloorHeatingValvePosition == 0.2

        assert str(d) == (
            "HmIP-FALMOT-C12 Fußbodenheizungsaktor OG motorisch lowBat(None) unreach(False) "
            "rssiDeviceValue(-55) rssiPeerValue(None) configPending(False) dutyCycle(False) "
            "minimumFloorHeatingValvePosition(0.2) "
            "pulseWidthModulationAtLowFloorHeatingValvePositionEnabled(True) coolingEmergencyValue(0.0) "
            "frostProtectionTemperature(8.0) valveProtectionDuration(5) valveProtectionSwitchingInterval(14)"
        )


def test_key_remote_control(fake_home: Home):
    with no_ssl_verification():
        d = fake_home.search_device_by_id("3014F711ABCDEF0000000014")
        assert isinstance(d, KeyRemoteControl4)


def test_brand_switch_notification_light(fake_home: Home):
    with no_ssl_verification():
        d = BrandSwitchNotificationLight(fake_home._connection)
        d = fake_home.search_device_by_id("3014F711BSL0000000000050")

        c = d.functionalChannels[d.topLightChannelIndex]
        assert isinstance(c, NotificationLightChannel)
        assert c.simpleRGBColorState == RGBColorState.RED
        assert c.dimLevel == 0.0

        c = d.functionalChannels[d.bottomLightChannelIndex]
        assert isinstance(c, NotificationLightChannel)
        assert c.simpleRGBColorState == RGBColorState.GREEN
        assert c.dimLevel == 1.0

        d.set_rgb_dim_level(d.topLightChannelIndex, RGBColorState.BLUE, 0.5)
        d.set_rgb_dim_level_with_time(
            d.bottomLightChannelIndex, RGBColorState.YELLOW, 0.7, 10, 20
        )

        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F711BSL0000000000050")

        c = d.functionalChannels[d.topLightChannelIndex]
        assert isinstance(c, NotificationLightChannel)
        assert c.simpleRGBColorState == RGBColorState.BLUE
        assert c.dimLevel == 0.5

        c = d.functionalChannels[d.bottomLightChannelIndex]
        assert isinstance(c, NotificationLightChannel)
        assert c.simpleRGBColorState == RGBColorState.YELLOW
        assert c.dimLevel == 0.7

        assert str(d) == (
            "HmIP-BSL Treppe lowBat(None) unreach(False) "
            "rssiDeviceValue(-67) rssiPeerValue(-70) configPending(False) "
            "dutyCycle(False) on(True) profileMode(AUTOMATIC) "
            "userDesiredProfileMode(AUTOMATIC) topDimLevel(0.5) "
            "topColor(BLUE) bottomDimLevel(0.7) bottomColor(YELLOW)"
        )


def test_light_sensor(fake_home: Home):
    with no_ssl_verification():
        d = LightSensor(fake_home._connection)
        d = fake_home.search_device_by_id("3014F711SLO0000000000026")

        assert d.averageIllumination == 807.3
        assert d.currentIllumination == 785.2
        assert d.highestIllumination == 837.1
        assert d.lowestIllumination == 785.2

        assert str(d) == (
            "HmIP-SLO Lichtsensor Nord lowBat(False) unreach(False) rssiDeviceValue(-60) "
            "rssiPeerValue(None) configPending(False) dutyCycle(False) "
            "averageIllumination(807.3) currentIllumination(785.2) "
            "highestIllumination(837.1) lowestIllumination(785.2)"
        )


def test_door_sensor_tm(fake_home: Home):
    with no_ssl_verification():
        d = fake_home.search_device_by_id("3014F0000000000000FAF9B4")

        assert d.doorState == DoorState.CLOSED
        assert d.on is False
        assert d.processing is False
        assert d.ventilationPositionSupported is True

        assert str(d) == (
            "HmIP-MOD-TM Garage Door Module lowBat(None) unreach(False) rssiDeviceValue(-52) "
            "rssiPeerValue(-54) configPending(False) dutyCycle(False) doorState(CLOSED) "
            "on(False) processing(False) ventilationPositionSupported(True)"
        )

        d.send_door_command(doorCommand=DoorCommand.OPEN)

        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F0000000000000FAF9B4")
        assert d.doorState == DoorState.OPEN


def test_hoermann_drives_module(fake_home: Home):
    with no_ssl_verification():
        d = fake_home.search_device_by_id("3014F7110000000HOERMANN")

        assert d.doorState == DoorState.CLOSED
        assert d.on is False
        assert d.processing is False
        assert d.ventilationPositionSupported is True

        assert str(d) == (
            "HmIP-MOD-TM Garage Door lowBat(None) unreach(False) rssiDeviceValue(-71) "
            "rssiPeerValue(-76) configPending(False) dutyCycle(False) doorState(CLOSED) "
            "on(False) processing(False) ventilationPositionSupported(True)"
        )

        d.send_door_command(doorCommand=DoorCommand.CLOSE)

        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F7110000000HOERMANN")
        assert d.doorState == DoorState.CLOSED


def test_pluggable_mains_failure(fake_home: Home):
    with no_ssl_verification():
        d = fake_home.search_device_by_id("3014F7110000000000ABCD50")

        assert d.powerMainsFailure is False
        assert d.genericAlarmSignal is AlarmSignalType.FULL_ALARM

        assert str(d) == (
            "HmIP-PMFS Netzausfallüberwachung lowBat(None) unreach(False) rssiDeviceValue(-58) "
            "rssiPeerValue(None) configPending(False) dutyCycle(False) powerMainsFailure(False) "
            "genericAlarmSignal(FULL_ALARM)"
        )


def test_wall_thermostat_basic(fake_home: Home):
    with no_ssl_verification():
        d = fake_home.search_device_by_id("3014F711000000000000AAA5")

        assert d.display == ClimateControlDisplay.ACTUAL
        assert d.humidity == 42

        assert str(d) == (
            "HmIP-WTH-B Thermostat Schlafen Tal lowBat(False) unreach(False) rssiDeviceValue(-58) "
            "rssiPeerValue(-59) configPending(False) dutyCycle(False) operationLockActive(False) "
            "actualTemperature(16.0) humidity(42) vaporAmount(5.710127947243264) "
            "setPointTemperature(12.0)"
        )
