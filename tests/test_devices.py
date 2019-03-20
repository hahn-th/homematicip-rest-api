from unittest.mock import MagicMock, Mock

import pytest

from homematicip.home import Home
from homematicip.base.base_connection import BaseConnection
from homematicip.base.enums import *
from homematicip.device import *
from homematicip.base.functionalChannels import *
import json
from datetime import datetime, timedelta, timezone

from conftest import fake_home_download_configuration, no_ssl_verification, utc_offset

def test_multi_io_box(fake_home: Home):
    d = fake_home.search_device_by_id("3014F711ABCD0ABCD000002")
    assert isinstance(d,MultiIOBox)
    assert d.on == True
    assert d.functionalChannels[2].on == False
    assert d.analogOutputLevel == 12.5
    assert d.functionalChannels[5].analogOutputLevel == 12.5

    assert str(d) == ("HmIP-MIOB Multi IO Box lowbat(None) unreach(False) "
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
        "HmIP-FCI1 Kontakt-Schnittstelle Unterputz – 1-fach lowbat(False) unreach(False) rssiDeviceValue(-46) rssiPeerValue(None) configPending(False) "
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
    assert d.lowBat == False
    assert d.routerModuleEnabled == False
    assert d.routerModuleSupported == False
    assert d.rssiDeviceValue == -64
    assert d.rssiPeerValue == None
    assert d.dutyCycle == False
    assert d.configPending == False
    assert (
        str(d)
        == "HMIP-SWDO Fenster lowbat(False) unreach(False) rssiDeviceValue(-64) rssiPeerValue(None) configPending(False) dutyCycle(False) sabotage(False) windowState(CLOSED)"
    )
    assert (
        d._rawJSONData
        == fake_home_download_configuration()["devices"]["3014F7110000000000000001"]
    )

    d = fake_home.search_device_by_id("3014F7110000000000000005")
    assert d.windowState == WindowState.OPEN
    assert d.lastStatusUpdate == None

    assert (
        d.set_router_module_enabled(True) == False
    )  # Shutter contact won't support this


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
    assert d.on == False
    assert d.profileMode == "AUTOMATIC"
    assert d.userDesiredProfileMode == "AUTOMATIC"
    assert d.currentPowerConsumption == 0.0
    assert d.energyCounter == 0.4754
    assert d.lowBat == None
    assert d.routerModuleEnabled == True
    assert d.routerModuleSupported == True
    assert d.rssiDeviceValue == -60
    assert d.rssiPeerValue == -66
    assert d.unreach == False
    assert d.availableFirmwareVersion == "0.0.0"
    assert d.firmwareVersion == "2.6.2"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert d.dutyCycle == False
    assert d.configPending == False

    assert str(d) == (
        "HMIP-PSM Brunnen lowbat(None) unreach(False) rssiDeviceValue(-60) rssiPeerValue(-66) configPending(False) dutyCycle(False) on(False) profileMode(AUTOMATIC)"
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
        assert d.on == True

        d.turn_off()
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F7110000000000000009")
        assert d.on == False

        d.id = "INVALID_ID"
        result = d.turn_off()
        assert result["errorCode"] == "INVALID_DEVICE"


def test_smoke_detector(fake_home: Home):
    d = fake_home.search_device_by_id("3014F7110000000000000020")
    assert isinstance(d, SmokeDetector)
    assert d.label == "Rauchwarnmelder"
    assert d.lastStatusUpdate == datetime(2018, 4, 23, 4, 5, 24, 824000) + timedelta(
        0, utc_offset
    )
    assert d.manufacturerCode == 1
    assert d.modelId == 296
    assert d.modelType == "HmIP-SWSD"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000000020"
    assert d.updateState == DeviceUpdateState.UP_TO_DATE
    assert d.lowBat == False
    assert d.routerModuleEnabled == False
    assert d.routerModuleSupported == False
    assert d.rssiDeviceValue == -54
    assert d.rssiPeerValue == None
    assert d.unreach == False
    assert d.smokeDetectorAlarmType == SmokeDetectorAlarmType.IDLE_OFF
    assert d.availableFirmwareVersion == "0.0.0"
    assert d.firmwareVersion == "1.0.11"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert d.configPending == False
    assert (
        str(d)
        == "HmIP-SWSD Rauchwarnmelder lowbat(False) unreach(False) rssiDeviceValue(-54) rssiPeerValue(None) configPending(False) dutyCycle(False) smokeDetectorAlarmType(IDLE_OFF)"
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
    assert d.lowBat == False
    assert d.operationLockActive == False
    assert d.routerModuleEnabled == False
    assert d.routerModuleSupported == False
    assert d.rssiDeviceValue == -76
    assert d.rssiPeerValue == -63
    assert d.unreach == False
    assert d.dutyCycle == False
    assert d.availableFirmwareVersion == "0.0.0"
    assert d.firmwareVersion == "1.8.0"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert str(d) == (
        "HmIP-WTH-2 Wandthermostat lowbat(False) unreach(False) rssiDeviceValue(-76) rssiPeerValue(-63)"
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
    assert d.lowBat == False
    assert d.operationLockActive == True
    assert d.routerModuleEnabled == False
    assert d.routerModuleSupported == False
    assert d.rssiDeviceValue == -65
    assert d.rssiPeerValue == -66
    assert d.unreach == False
    assert d.automaticValveAdaptionNeeded == False
    assert d.availableFirmwareVersion == "2.0.2"
    assert d.firmwareVersion == "2.0.2"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert d.valveActualTemperature == 20.0

    assert str(d) == (
        "HMIP-eTRV Wohnzimmer-Heizung lowbat(False) unreach(False) rssiDeviceValue(-65) rssiPeerValue(-66) configPending(False) dutyCycle(False) operationLockActive(True)"
        " valvePosition(0.0) valveState(ADAPTION_DONE) temperatureOffset(0.0) setPointTemperature(5.0) valveActualTemperature(20.0)"
    )
    assert (
        d._rawJSONData
        == fake_home_download_configuration()["devices"]["3014F7110000000000000015"]
    )

    with no_ssl_verification():
        d.set_operation_lock(False)
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F7110000000000000015")
        assert d.operationLockActive == False

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
    assert d.lowBat == False
    assert d.routerModuleEnabled == False
    assert d.routerModuleSupported == False
    assert d.rssiDeviceValue == -47
    assert d.rssiPeerValue == -50
    assert d.unreach == False
    assert d.automaticValveAdaptionNeeded == False
    assert d.valveActualTemperature == 21.6

    assert str(d) == (
        "HmIP-eTRV-C Wohnzimmer 3 lowbat(False) unreach(False) rssiDeviceValue(-47) "
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
    assert d.lowBat == False
    assert d.routerModuleEnabled == False
    assert d.routerModuleSupported == False
    assert d.rssiDeviceValue == -55
    assert d.rssiPeerValue == None
    assert d.unreach == False
    assert d.configPending == False
    assert d.dutyCycle == False
    assert str(d) == (
        "HmIP-STHO Temperatur- und Luftfeuchtigkeitssensor - außen lowbat(False) unreach(False)"
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
    assert d.raining == False
    assert d.storm == False
    assert d.sunshine == True
    assert d.todayRainCounter == 6.5
    assert d.todaySunshineDuration == 100
    assert d.totalRainCounter == 6.5
    assert d.totalSunshineDuration == 100
    assert d.weathervaneAlignmentNeeded == False
    assert d.windDirection == 295.0
    assert d.windDirectionVariation == 56.25
    assert d.windSpeed == 2.6
    assert d.windValueType == WindValueType.AVERAGE_VALUE
    assert d.yesterdayRainCounter == 0.0
    assert d.yesterdaySunshineDuration == 0
    assert d.actualTemperature == 15.4
    assert d.lowBat == False
    assert d.routerModuleEnabled == False
    assert d.routerModuleSupported == False
    assert d.rssiDeviceValue == -68
    assert d.rssiPeerValue == None
    assert d.unreach == False
    assert d.configPending == False
    assert d.dutyCycle == False
    assert str(d) == (
        "HmIP-SWO-PR Wettersensor - pro lowbat(False) unreach(False) rssiDeviceValue(-68)"
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
    assert d.lowBat == False
    assert d.routerModuleEnabled == False
    assert d.routerModuleSupported == False
    assert d.rssiDeviceValue == -77
    assert d.rssiPeerValue == None
    assert d.unreach == False
    assert d.configPending == False
    assert d.dutyCycle == False
    assert d.availableFirmwareVersion == "0.0.0"
    assert d.firmwareVersion == "1.0.10"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert d.humidity == 42
    assert d.vaporAmount == 6.177718198711658
    assert d.illumination == 4890.0
    assert d.illuminationThresholdSunshine == 3500.0
    assert d.storm == False
    assert d.sunshine == True
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
        "HmIP-SWO-B Wettersensor lowbat(False) unreach(False) rssiDeviceValue(-77)"
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
    assert d.raining == False
    assert d.storm == False
    assert d.sunshine == False
    assert d.todayRainCounter == 3.8999999999999773
    assert d.todaySunshineDuration == 0
    assert d.totalRainCounter == 544.0999999999999
    assert d.totalSunshineDuration == 132057
    assert d.windSpeed == 15.0
    assert d.windValueType == WindValueType.CURRENT_VALUE
    assert d.yesterdayRainCounter == 25.600000000000023
    assert d.yesterdaySunshineDuration == 0
    assert d.actualTemperature == 4.3
    assert d.lowBat == False
    assert d.routerModuleEnabled == False
    assert d.routerModuleSupported == False
    assert d.rssiDeviceValue == -55
    assert d.rssiPeerValue == None
    assert d.unreach == False
    assert d.configPending == False
    assert d.dutyCycle == False
    assert str(d) == (
        "HmIP-SWO-PL Weather Sensor \u2013 plus lowbat(False) unreach(False) rssiDeviceValue(-55)"
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

    assert d.lowBat == False
    assert d.routerModuleEnabled == False
    assert d.routerModuleSupported == False
    assert d.rssiDeviceValue == -54
    assert d.rssiPeerValue == None
    assert d.dutyCycle == False
    assert d.configPending == False
    assert str(d) == (
        "HmIP-SRH Fenstergriffsensor lowbat(False) unreach(False) rssiDeviceValue(-54) rssiPeerValue(None) configPending(False) dutyCycle(False)"
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
    assert d.lowBat == None
    assert d.routerModuleEnabled == False
    assert d.routerModuleSupported == False
    assert d.rssiDeviceValue == -44
    assert d.rssiPeerValue == -42
    assert d.unreach == False
    assert d.dutyCycle == False
    assert d.configPending == False
    assert d.availableFirmwareVersion == "0.0.0"
    assert d.firmwareVersion == "1.4.8"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c

    assert str(d) == (
        "HmIP-BDT Schlafzimmerlicht lowbat(None) unreach(False) rssiDeviceValue(-44) rssiPeerValue(-42) configPending(False) dutyCycle(False) dimLevel(0.0)"
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
        assert d.permanentlyReachable == True
        assert d.label == "Brunnen"
        assert d.routerModuleEnabled == True
        assert d.energyCounter == 0.4754

        d.set_label("new label")
        d.set_router_module_enabled(False)
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F7110000000000000009")
        assert d.label == "new label"
        assert d.routerModuleEnabled == False

        d.set_label("other label")
        d.set_router_module_enabled(True)
        d.reset_energy_counter()
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F7110000000000000009")
        assert d.label == "other label"
        assert d.routerModuleEnabled == True
        assert d.energyCounter == 0

        d2 = fake_home.search_device_by_id("3014F7110000000000000005")
        d.delete()
        fake_home.get_current_state()
        dNotFound = fake_home.search_device_by_id("3014F7110000000000000009")
        assert dNotFound == None
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
    for d in fake_home.devices:
        assert type(d) != Device


def test_water_sensor(fake_home: Home):
    with no_ssl_verification():
        d = WaterSensor(fake_home._connection)  # just needed for intellisense
        d = fake_home.search_device_by_id("3014F7110000000000000050")
        assert d.label == "Wassersensor"
        assert d.routerModuleEnabled == False
        assert d.routerModuleSupported == False

        assert d.incorrectPositioned == True
        assert d.acousticAlarmSignal == AcousticAlarmSignal.FREQUENCY_RISING
        assert d.acousticAlarmTiming == AcousticAlarmTiming.ONCE_PER_MINUTE
        assert d.acousticWaterAlarmTrigger == WaterAlarmTrigger.WATER_DETECTION
        assert d.inAppWaterAlarmTrigger == WaterAlarmTrigger.WATER_MOISTURE_DETECTION
        assert d.moistureDetected == False
        assert d.sirenWaterAlarmTrigger == WaterAlarmTrigger.WATER_MOISTURE_DETECTION
        assert d.waterlevelDetected == False

        d.set_acoustic_alarm_timing(AcousticAlarmTiming.SIX_MINUTES)
        d.set_acoustic_alarm_signal(AcousticAlarmSignal.FREQUENCY_ALTERNATING_LOW_HIGH)
        d.set_inapp_water_alarm_trigger(WaterAlarmTrigger.MOISTURE_DETECTION)
        d.set_acoustic_water_alarm_trigger(WaterAlarmTrigger.NO_ALARM)
        d.set_siren_water_alarm_trigger(WaterAlarmTrigger.NO_ALARM)

        assert str(d) == (
            "HmIP-SWD Wassersensor lowbat(False) unreach(False) rssiDeviceValue(-65) rssiPeerValue(None) configPending(False) "
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
    assert d.permanentFullRx == True
    assert d.illumination == 14.2
    assert d.currentIllumination == None
    assert d.motionBufferActive == True
    assert d.motionDetected == False
    assert d.motionDetectionSendInterval == MotionDetectionSendInterval.SECONDS_240
    assert d.numberOfBrightnessMeasurements == 7

    assert str(d) == (
        "HmIP-SMI55 Bewegungsmelder für 55er Rahmen – innen lowbat(False) unreach(False) rssiDeviceValue(-46) "
        "rssiPeerValue(None) configPending(False) dutyCycle(False) sabotage(None) motionDetected(False) "
        "illumination(14.2) motionBufferActive(True) motionDetectionSendInterval(SECONDS_240) "
        "numberOfBrightnessMeasurements(7) permanentFullRx(True)"
    )


def test_motion_detector(fake_home: Home):
    d = MotionDetectorIndoor(fake_home._connection)
    d = fake_home.search_device_by_id("3014F711000000000000BB11")

    assert d.illumination == 0.1
    assert d.currentIllumination == None
    assert d.motionBufferActive == False
    assert d.motionDetected == True
    assert d.motionDetectionSendInterval == MotionDetectionSendInterval.SECONDS_480
    assert d.numberOfBrightnessMeasurements == 7

    assert str(d) == (
        "HmIP-SMI Wohnzimmer lowbat(False) unreach(False) rssiDeviceValue(-56) rssiPeerValue(-52) configPending(False) "
        "dutyCycle(False) sabotage(False) motionDetected(True) illumination(0.1) motionBufferActive(False) "
        "motionDetectionSendInterval(SECONDS_480) numberOfBrightnessMeasurements(7)"
    )

    d = MotionDetectorOutdoor(fake_home._connection)
    d = fake_home.search_device_by_id("3014F71100000000000BBB17")

    assert d.illumination == 233.4
    assert d.currentIllumination == None
    assert d.motionBufferActive == True
    assert d.motionDetected == True
    assert d.motionDetectionSendInterval == MotionDetectionSendInterval.SECONDS_240
    assert d.numberOfBrightnessMeasurements == 7

    assert str(d) == (
        "HmIP-SMO-A Außen Küche lowbat(False) unreach(False) rssiDeviceValue(-70) rssiPeerValue(-67) configPending(False) "
        "dutyCycle(False) motionDetected(True) illumination(233.4) motionBufferActive(True) "
        "motionDetectionSendInterval(SECONDS_240) numberOfBrightnessMeasurements(7)"
    )


def test_presence_detector_indoor(fake_home: Home):
    d = PresenceDetectorIndoor(fake_home._connection)
    d = fake_home.search_device_by_id("3014F711AAAAAAAAAAAAAA51")

    assert d.illumination == 1.8
    assert d.currentIllumination == None
    assert d.motionBufferActive == False
    assert d.presenceDetected == False
    assert d.motionDetectionSendInterval == MotionDetectionSendInterval.SECONDS_240
    assert d.numberOfBrightnessMeasurements == 7

    assert str(d) == (
        "HmIP-SPI *** lowbat(False) unreach(False) rssiDeviceValue(-62) rssiPeerValue(-61) configPending(False) "
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
        assert c.on == False
        assert c.profileMode == "AUTOMATIC"

        c = d.functionalChannels[8]

        assert isinstance(c, SwitchChannel)
        assert c.index == 8
        assert c.on == True
        assert c.profileMode == "AUTOMATIC"

        d.turn_off(8)
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F711BBBBBBBBBBBBB18")
        c = d.functionalChannels[8]
        assert c.on == False


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
            "HmIP-SPDR *** lowbat(False) unreach(False) rssiDeviceValue(-76) rssiPeerValue(None) configPending(False) dutyCycle(False)"
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
        assert d.endpositionAutoDetectionEnabled == True
        assert d.previousShutterLevel == None
        assert d.processing == False
        assert d.profileMode == "AUTOMATIC"
        assert d.selfCalibrationInProgress == None
        assert d.shutterLevel == 1.0
        assert d.supportingDelayCompensation == True
        assert d.supportingEndpositionAutoDetection == True
        assert d.supportingSelfCalibration == True
        assert d.topToBottomReferenceTime == 24.68
        assert d.userDesiredProfileMode == "AUTOMATIC"

        assert str(d) == (
            "HmIP-BROLL *** lowbat(None) unreach(False) rssiDeviceValue(-78) rssiPeerValue(-77) configPending(False)"
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
        assert d.blindModeActive == True
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
            "HmIP-FBL Sofa links lowbat(None) unreach(False) rssiDeviceValue(-73) "
            "rssiPeerValue(-78) configPending(False) dutyCycle(False) "
            "shutterLevel(0.3) topToBottom(41.0) bottomToTop(41.0) "
            "slatsLevel(0.8) blindModeActive(True)"
        )


def test_alarm_siren_indoor(fake_home: Home):
    with no_ssl_verification():
        d = AlarmSirenIndoor(fake_home._connection)
        d = fake_home.search_device_by_id("3014F7110000000000BBBBB8")

        assert (
            str(d)
            == "HmIP-ASIR Alarmsirene lowbat(False) unreach(False) rssiDeviceValue(-59) rssiPeerValue(None) configPending(False) dutyCycle(False) sabotage(False)"
        )


def test_floor_terminal_block(fake_home: Home):
    with no_ssl_verification():
        d = FloorTerminalBlock6(fake_home._connection)
        d = fake_home.search_device_by_id("3014F7110000000000BBBBB1")

        assert d.frostProtectionTemperature == 8.0
        assert d.coolingEmergencyValue == 0.0
        assert d.globalPumpControl == True
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
            "HmIP-FAL230-C6 Fußbodenheizungsaktor lowbat(None) unreach(False) rssiDeviceValue(-62) rssiPeerValue(None) configPending(False) dutyCycle(False) "
            "globalPumpControl(True) heatingValveType(NORMALLY_CLOSE) heatingLoadType(LOAD_BALANCING) coolingEmergencyValue(0.0) frostProtectionTemperature(8.0) "
            "heatingEmergencyValue(0.25) valveProtectionDuration(5) valveProtectionSwitchingInterval(14) pumpFollowUpTime(2) pumpLeadTime(2) "
            "pumpProtectionDuration(1) pumpProtectionSwitchingInterval(14)"
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
            "HmIP-BSL Treppe lowbat(None) unreach(False) "
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
            "HmIP-SLO Lichtsensor Nord lowbat(False) unreach(False) rssiDeviceValue(-60) "
            "rssiPeerValue(None) configPending(False) dutyCycle(False) "
            "averageIllumination(807.3) currentIllumination(785.2) "
            "highestIllumination(837.1) lowestIllumination(785.2)"
        )
