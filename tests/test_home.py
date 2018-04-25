from unittest.mock import MagicMock, Mock

import pytest

from homematicip.home import Home
from homematicip.base.base_connection import BaseConnection
from homematicip.device import *
import json
from datetime import datetime, timedelta, timezone

dt = datetime.now(timezone.utc).astimezone()
utc_offset = dt.utcoffset() // timedelta(seconds=1)

def fake_home_download_configuration():
    return json.load(open("tests/json_data/home.json"))


@pytest.fixture
def fake_home():
    home = Home()
    home.download_configuration = fake_home_download_configuration
    home._connection = BaseConnection()
    home.get_current_state()
    return home


def test_update_event(fake_home: Home):
    fake_handler = Mock()
    fake_home.on_update(fake_handler.method)
    fake_home.fire_update_event()
    fake_handler.method.assert_called()

def test_home(fake_home: Home):
    assert fake_home.connected == True
    assert fake_home.currentAPVersion == "1.2.4"
    assert fake_home.deviceUpdateStrategy == "AUTOMATICALLY_IF_POSSIBLE"
    assert fake_home.dutyCycle == 8.0
    assert fake_home.pinAssigned == False
    assert fake_home.powerMeterCurrency == "EUR"
    assert fake_home.powerMeterUnitPrice == 0.0
    assert fake_home.timeZoneId == "Europe/Vienna"
    assert fake_home.updateState == "UP_TO_DATE"
    
    #location
    assert fake_home.location.city == "1010  Wien, \u00d6sterreich"
    assert fake_home.location.latitude == "48.208088"
    assert fake_home.location.longitude == "16.358608"

    #weather
    assert fake_home.weather.humidity == 54
    assert fake_home.weather.maxTemperature == 16.6
    assert fake_home.weather.minTemperature == 16.6
    assert fake_home.weather.temperature == 16.6
    assert fake_home.weather.weatherCondition == "LIGHT_CLOUDY"
    assert fake_home.weather.weatherDayTime == "NIGHT"
    assert fake_home.weather.windDirection == 294
    assert fake_home.weather.windSpeed == 8.568 


def test_clients(fake_home):
    client = fake_home.clients[0]
    assert client.label == 'TEST-Client'
    assert client.homeId == '00000000-0000-0000-0000-000000000001'
    assert client.id == '00000000-0000-0000-0000-000000000000'
    
def test_shutter_device(fake_home):
    d = fake_home.search_device_by_id('3014F7110000000000000001')
    assert isinstance(d, ShutterContact)
    assert d.label == "Fenster"
    assert d.lastStatusUpdate == datetime(2018, 4, 23, 20, 37, 34, 304000) + timedelta(0,utc_offset)
    assert d.manufacturerCode == 1
    assert d.modelId == 258
    assert d.modelType == "HMIP-SWDO"
    assert d.oem == "eQ-3"
    assert d.windowState == "CLOSED"
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000000001"
    assert d.availableFirmwareVersion == "1.16.8"
    assert d.firmwareVersion == "1.16.8"
    assert d.lowBat == False
    assert d.routerModuleEnabled == False
    assert d.routerModuleSupported == False
    assert d.rssiDeviceValue == -64
    assert d.rssiPeerValue == None
    assert d.dutyCycle == False
    assert d.configPending == False
    assert str(d) == 'HMIP-SWDO Fenster lowbat(False) unreach(False) rssiDeviceValue(-64) rssiPeerValue(None) configPending(False) dutyCycle(False): sabotage(False) windowState(CLOSED)'


    d = fake_home.search_device_by_id('3014F7110000000000000005')
    assert d.windowState == "OPEN"
    assert d.lastStatusUpdate == None

def test_pluggable_switch_measuring(fake_home):
    d = fake_home.search_device_by_id('3014F7110000000000000009')
    assert isinstance(d, PlugableSwitchMeasuring)
    assert d.label == "Brunnen"
    assert d.lastStatusUpdate == (datetime(2018, 4, 23, 20, 36, 26, 303000) + timedelta(0,utc_offset))
    assert d.manufacturerCode == 1
    assert d.modelId == 262
    assert d.modelType == "HMIP-PSM"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000000009"
    assert d.updateState == "UP_TO_DATE"
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
    assert d.dutyCycle == False
    assert d.configPending == False

    assert str(d) == ('HMIP-PSM Brunnen lowbat(None) unreach(False) rssiDeviceValue(-60) rssiPeerValue(-66) configPending(False) dutyCycle(False): on(False) profileMode(AUTOMATIC)'
                     ' userDesiredProfileMode(AUTOMATIC) energyCounter(0.4754) currentPowerConsumption(0.0W)')

def test_smoke_detector(fake_home):
    d = fake_home.search_device_by_id('3014F7110000000000000020')
    assert isinstance(d, SmokeDetector)
    assert d.label == "Rauchwarnmelder"
    assert d.lastStatusUpdate == datetime(2018, 4, 23, 4, 5, 24, 824000) + timedelta(0,utc_offset)
    assert d.manufacturerCode == 1
    assert d.modelId == 296
    assert d.modelType == "HmIP-SWSD"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000000020"
    assert d.updateState == "UP_TO_DATE"
    assert d.lowBat == False
    assert d.routerModuleEnabled == False
    assert d.routerModuleSupported == False
    assert d.rssiDeviceValue == -54
    assert d.rssiPeerValue == None
    assert d.unreach == False
    assert d.smokeDetectorAlarmType == "IDLE_OFF"
    assert d.availableFirmwareVersion == "0.0.0"
    assert d.firmwareVersion == "1.0.11"
    assert d.configPending == False
    assert str(d) == 'HmIP-SWSD Rauchwarnmelder lowbat(False) unreach(False) rssiDeviceValue(-54) rssiPeerValue(None) configPending(False) dutyCycle(False): smokeDetectorAlarmType(IDLE_OFF)'

def test_wall_mounted_thermostat_pro(fake_home):
    d = fake_home.search_device_by_id('3014F7110000000000000022')
    assert isinstance(d, WallMountedThermostatPro)
    assert d.id == "3014F7110000000000000022"
    assert d.label == "Wandthermostat"
    assert d.lastStatusUpdate == datetime(2018, 4, 23, 20, 48, 54, 382000) + timedelta(0,utc_offset)
    assert d.manufacturerCode == 1
    assert d.modelId == 297
    assert d.modelType == "HmIP-WTH-2"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000000022"
    assert d.updateState == "UP_TO_DATE"
    assert d.humidity == 43
    assert d.setPointTemperature == 5.0
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
    assert str(d)

def test_heating_thermostat(fake_home):
    d = fake_home.search_device_by_id('3014F7110000000000000015')
    assert isinstance(d, HeatingThermostat)
    assert d.label == "Wohnzimmer-Heizung"
    assert d.lastStatusUpdate == datetime(2018, 4, 23, 20, 5, 50, 325000) + timedelta(0,utc_offset)
    assert d.manufacturerCode == 1
    assert d.modelId == 269
    assert d.modelType == "HMIP-eTRV"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000000015"
    assert d.updateState == "UP_TO_DATE"
    assert d.setPointTemperature == 5.0
    assert d.temperatureOffset == 0.0
    assert d.valvePosition == 0.0
    assert d.valveState == "ADAPTION_DONE"
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

    assert str(d) == ('HMIP-eTRV Wohnzimmer-Heizung lowbat(False) unreach(False) rssiDeviceValue(-65) rssiPeerValue(-66) configPending(False) dutyCycle(False): operationLockActive(True)'
                    ' valvePosition(0.0) valveState(ADAPTION_DONE)')

def test_temperature_humidity_sensor_outdoor(fake_home):
    d = fake_home.search_device_by_id('3014F711AAAA000000000002')
    assert isinstance(d, TemperatureHumiditySensorOutdoor)
    assert d.label == "Temperatur- und Luftfeuchtigkeitssensor \u2013 au\u00dfen"
    assert d.lastStatusUpdate == datetime(2018, 3, 11, 11, 8, 6, 465000) + timedelta(0,utc_offset)
    assert d.manufacturerCode == 1
    assert d.modelId == 314
    assert d.modelType == "HmIP-STHO"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F711AAAA000000000002"
    assert d.updateState == "UP_TO_DATE"
    assert d.humidity == 70
    assert d.actualTemperature == 15.1
    assert d.lowBat == False
    assert d.routerModuleEnabled == False
    assert d.routerModuleSupported == False
    assert d.rssiDeviceValue == -55
    assert d.rssiPeerValue == None
    assert d.unreach == False
    assert d.configPending == False
    assert d.dutyCycle == False
    assert str(d)== ('HmIP-STHO Temperatur- und Luftfeuchtigkeitssensor – außen lowbat(False) unreach(False) rssiDeviceValue(-55) rssiPeerValue(None) configPending(False)'
                    ' dutyCycle(False): actualTemperature(15.1) humidity(70)')

def test_weather_sensor_pro(fake_home):
    d = fake_home.search_device_by_id('3014F711AAAA000000000001')
    assert isinstance(d, WeatherSensorPro)
    assert d.label == "Wettersensor – pro"
    assert d.lastStatusUpdate == datetime(2018, 3, 11, 11, 10, 14, 834000) + timedelta(0,utc_offset)
    assert d.manufacturerCode == 1
    assert d.modelId == 352
    assert d.modelType == "HmIP-SWO-PR"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F711AAAA000000000001"
    assert d.updateState == "UP_TO_DATE"
    assert d.availableFirmwareVersion == "0.0.0"
    assert d.firmwareVersion == "1.0.10"
    assert d.humidity == 65
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
    assert d.windValueType == "AVERAGE_VALUE"
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
    assert str(d) == ('HmIP-SWO-PR Wettersensor – pro lowbat(False) unreach(False) rssiDeviceValue(-68) rssiPeerValue(None) configPending(False) dutyCycle(False) humidity(65)'
                      ' illumination(4153.0) illuminationThresholdSunshine(10.0) raining(False) storm(False) sunshine(True)todayRainCounter(6.5) todaySunshineDuration(100)'
                      ' totalRainCounter(6.5) totalSunshineDuration(100)weathervaneAlignmentNeeded(False) windDirection(295.0) windDirectionVariation(56.25) windSpeed(2.6)'
                      ' windValueType(AVERAGE_VALUE)yesterdayRainCounter(0.0) yesterdaySunshineDuration(0)')

#def test__parse_device(fake_home):
#    assert False
#
#
#def test_get_devices(fake_home):
#    assert False
#
#
#def test__get_clients(fake_home):
#    assert False
#
#
#def test__parse_group(fake_home):
#    assert False
#
#
#def test__get_groups(fake_home):
#    assert False
