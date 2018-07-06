import pytest

from homematicip.aio.home import AsyncHome
from homematicip.EventHook import EventHook
from homematicip.aio.device import AsyncDevice
from homematicip.base.enums import *

import json
from datetime import datetime, timedelta, timezone
from conftest import no_ssl_verification


dt = datetime.now(timezone.utc).astimezone()
utc_offset = dt.utcoffset() // timedelta(seconds=1)

@pytest.mark.asyncio
async def test_basic_device_functions(fake_async_home:AsyncHome):
    with no_ssl_verification():
        d = fake_async_home.search_device_by_id('3014F7110000000000000009')
        assert d.label == "Brunnen"
        assert d.routerModuleEnabled == True

        await d.set_label("new label")
        await d.set_router_module_enabled(False)
        await fake_async_home.get_current_state()
        d = fake_async_home.search_device_by_id('3014F7110000000000000009')
        assert d.label == "new label"
        assert d.routerModuleEnabled == False

        await d.set_label("other label")
        await d.set_router_module_enabled(True)
        await fake_async_home.get_current_state()
        d = fake_async_home.search_device_by_id('3014F7110000000000000009')
        assert d.label == "other label"
        assert d.routerModuleEnabled == True

        d2 = fake_async_home.search_device_by_id('3014F7110000000000000005')
        await d.delete()
        await fake_async_home.get_current_state()
        d = fake_async_home.search_device_by_id('3014F7110000000000000009')
        assert d == None
        assert d2 is fake_async_home.search_device_by_id('3014F7110000000000000005') # make sure that the objects got updated and not completely renewed


@pytest.mark.asyncio
async def test_water_sensor(fake_async_home: AsyncHome):
    with no_ssl_verification():
        d = fake_async_home.search_device_by_id("3014F7110000000000000050")
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

        await d.set_acoustic_alarm_timing(AcousticAlarmTiming.SIX_MINUTES)
        await d.set_acoustic_alarm_signal(AcousticAlarmSignal.FREQUENCY_ALTERNATING_LOW_HIGH)
        await d.set_inapp_water_alarm_trigger(WaterAlarmTrigger.MOISTURE_DETECTION)
        await d.set_acoustic_water_alarm_trigger(WaterAlarmTrigger.NO_ALARM)
        await d.set_siren_water_alarm_trigger(WaterAlarmTrigger.NO_ALARM)

        await fake_async_home.get_current_state()
        d = fake_async_home.search_device_by_id("3014F7110000000000000050")

        assert d.acousticAlarmTiming == AcousticAlarmTiming.SIX_MINUTES
        assert d.acousticAlarmSignal == AcousticAlarmSignal.FREQUENCY_ALTERNATING_LOW_HIGH
        assert d.acousticWaterAlarmTrigger == WaterAlarmTrigger.NO_ALARM
        assert d.inAppWaterAlarmTrigger == WaterAlarmTrigger.MOISTURE_DETECTION
        assert d.sirenWaterAlarmTrigger == WaterAlarmTrigger.NO_ALARM

def test_all_devices_implemented(fake_async_home:AsyncHome):
    for d in fake_async_home.devices:
        assert type(d) != AsyncDevice