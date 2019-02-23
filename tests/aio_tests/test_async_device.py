from datetime import datetime, timedelta, timezone

import pytest

from homematicip.aio.device import *
from homematicip.aio.home import AsyncHome
from homematicip.base.enums import *
from homematicip.base.base_connection import HmipWrongHttpStatusError
from homematicip.base.functionalChannels import *

from conftest import utc_offset


@pytest.mark.asyncio
async def test_basic_device_functions(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000009")
    assert d.label == "Brunnen"
    assert d.routerModuleEnabled is True
    assert d.energyCounter == 0.4754

    await d.set_label("new label")
    await d.set_router_module_enabled(False)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000009")
    assert d.label == "new label"
    assert d.routerModuleEnabled is False

    await d.set_label("other label")
    await d.set_router_module_enabled(True)
    await d.reset_energy_counter()
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000009")
    assert d.label == "other label"
    assert d.routerModuleEnabled is True
    assert d.energyCounter == 0

    d2 = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000005")
    await d.delete()
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000009")
    assert d == None
    assert d2 is no_ssl_fake_async_home.search_device_by_id(
        "3014F7110000000000000005"
    )  # make sure that the objects got updated and not completely renewed


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
    await d.set_acoustic_alarm_signal(
        AcousticAlarmSignal.FREQUENCY_ALTERNATING_LOW_HIGH
    )
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


def test_all_devices_implemented(no_ssl_fake_async_home: AsyncHome):
    for d in no_ssl_fake_async_home.devices:
        assert type(d) != AsyncDevice


@pytest.mark.asyncio
async def test_wall_mounted_thermostat_pro(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000022")
    assert isinstance(d, AsyncWallMountedThermostatPro)
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

    await d.set_display(ClimateControlDisplay.ACTUAL)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000022")

    assert d.display == ClimateControlDisplay.ACTUAL


@pytest.mark.asyncio
async def test_pluggable_switch_measuring(no_ssl_fake_async_home: AsyncHome):
    no_ssl_fake_async_home = no_ssl_fake_async_home
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000009")
    assert isinstance(d, AsyncPlugableSwitchMeasuring)
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

    await d.turn_on()
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000009")
    assert d.on == True

    await d.turn_off()
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000009")
    assert d.on == False

    d.id = "INVALID_ID"
    with pytest.raises(HmipWrongHttpStatusError):
        result = await d.turn_off()


@pytest.mark.asyncio
async def test_heating_thermostat(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000015")
    assert isinstance(d, AsyncHeatingThermostat)
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

    assert str(d) == (
        "HMIP-eTRV Wohnzimmer-Heizung lowbat(False) unreach(False) "
        "rssiDeviceValue(-65) rssiPeerValue(-66) configPending(False) "
        "dutyCycle(False) operationLockActive(True) "
        "valvePosition(0.0) valveState(ADAPTION_DONE) "
        "temperatureOffset(0.0) setPointTemperature(5.0) "
        "valveActualTemperature(20.0)"
    )

    await d.set_operation_lock(False)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000015")
    assert d.operationLockActive == False

    d.id = "INVALID_ID"
    with pytest.raises(HmipWrongHttpStatusError):
        result = await d.set_operation_lock(True)


@pytest.mark.asyncio
async def test_brand_switch_notification_light(no_ssl_fake_async_home: AsyncHome):
    d = AsyncBrandSwitchNotificationLight(no_ssl_fake_async_home._connection)
    d = no_ssl_fake_async_home.search_device_by_id("3014F711BSL0000000000050")

    c = d.functionalChannels[d.topLightChannelIndex]
    assert isinstance(c, NotificationLightChannel)
    assert c.simpleRGBColorState == RGBColorState.RED
    assert c.dimLevel == 0.0

    c = d.functionalChannels[d.bottomLightChannelIndex]
    assert isinstance(c, NotificationLightChannel)
    assert c.simpleRGBColorState == RGBColorState.GREEN
    assert c.dimLevel == 1.0

    await d.set_rgb_dim_level(d.topLightChannelIndex, RGBColorState.BLUE, 0.5)
    await d.set_rgb_dim_level_with_time(
        d.bottomLightChannelIndex, RGBColorState.YELLOW, 0.7, 10, 20
    )

    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F711BSL0000000000050")

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


@pytest.mark.asyncio
async def test_full_flush_shutter(no_ssl_fake_async_home: AsyncHome):
    d = FullFlushShutter(no_ssl_fake_async_home._connection)
    d = no_ssl_fake_async_home.search_device_by_id("3014F711ACBCDABCADCA66")
    assert d.shutterLevel == 1.0

    await d.set_shutter_level(0.4)
    await d.set_shutter_stop()  # this will not do anything in the test run
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F711ACBCDABCADCA66")
    assert d.shutterLevel == 0.4


@pytest.mark.asyncio
async def test_full_flush_blind(no_ssl_fake_async_home: AsyncHome):
    d = AsyncFullFlushBlind(no_ssl_fake_async_home._connection)
    d = no_ssl_fake_async_home.search_device_by_id("3014F711BADCAFE000000001")

    assert d.shutterLevel == 1.0
    assert d.slatsLevel == 1.0
    assert d.blindModeActive == True
    assert d.slatsReferenceTime == 2.0

    await d.set_slats_level(0.4)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F711BADCAFE000000001")
    assert d.shutterLevel == 1.0
    assert d.slatsLevel == 0.4

    await d.set_slats_level(0.8, 0.3)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F711BADCAFE000000001")
    assert d.shutterLevel == 0.3
    assert d.slatsLevel == 0.8
