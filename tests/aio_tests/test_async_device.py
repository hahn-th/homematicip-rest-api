from datetime import datetime, timedelta, timezone

import pytest

from homematicip.aio.device import AsyncDevice, AsyncWallMountedThermostatPro
from homematicip.aio.home import AsyncHome
from homematicip.base.enums import *

from conftest import utc_offset

@pytest.mark.asyncio
async def test_basic_device_functions(no_ssl_fake_async_home:AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id('3014F7110000000000000009')
    assert d.label == "Brunnen"
    assert d.routerModuleEnabled is True

    await d.set_label("new label")
    await d.set_router_module_enabled(False)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id('3014F7110000000000000009')
    assert d.label == "new label"
    assert d.routerModuleEnabled is False

    await d.set_label("other label")
    await d.set_router_module_enabled(True)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id('3014F7110000000000000009')
    assert d.label == "other label"
    assert d.routerModuleEnabled is True

    d2 = no_ssl_fake_async_home.search_device_by_id('3014F7110000000000000005')
    await d.delete()
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id('3014F7110000000000000009')
    assert d == None
    assert d2 is no_ssl_fake_async_home.search_device_by_id('3014F7110000000000000005') # make sure that the objects got updated and not completely renewed


@pytest.mark.asyncio
async def test_water_sensor(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000050")
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

    await d.set_acoustic_alarm_timing(AcousticAlarmTiming.SIX_MINUTES)
    await d.set_acoustic_alarm_signal(AcousticAlarmSignal.FREQUENCY_ALTERNATING_LOW_HIGH)
    await d.set_inapp_water_alarm_trigger(WaterAlarmTrigger.MOISTURE_DETECTION)
    await d.set_acoustic_water_alarm_trigger(WaterAlarmTrigger.NO_ALARM)
    await d.set_siren_water_alarm_trigger(WaterAlarmTrigger.NO_ALARM)

    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000050")

    assert d.acousticAlarmTiming == AcousticAlarmTiming.SIX_MINUTES
    assert d.acousticAlarmSignal == AcousticAlarmSignal.FREQUENCY_ALTERNATING_LOW_HIGH
    assert d.acousticWaterAlarmTrigger == WaterAlarmTrigger.NO_ALARM
    assert d.inAppWaterAlarmTrigger == WaterAlarmTrigger.MOISTURE_DETECTION
    assert d.sirenWaterAlarmTrigger == WaterAlarmTrigger.NO_ALARM

def test_all_devices_implemented(no_ssl_fake_async_home:AsyncHome):
    for d in no_ssl_fake_async_home.devices:
        assert type(d) != AsyncDevice

@pytest.mark.asyncio
async def test_wall_mounted_thermostat_pro(no_ssl_fake_async_home : AsyncHome ):
    d = no_ssl_fake_async_home.search_device_by_id('3014F7110000000000000022')
    assert isinstance(d, AsyncWallMountedThermostatPro)
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

    await d.set_display( ClimateControlDisplay.ACTUAL)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id('3014F7110000000000000022')
    assert d.display == ClimateControlDisplay.ACTUAL