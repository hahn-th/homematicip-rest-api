import asyncio
from datetime import datetime, timedelta, timezone

import pytest

from conftest import utc_offset
from homematicip.aio.device import *
from homematicip.aio.home import AsyncHome
from homematicip.base.base_connection import HmipWrongHttpStatusError
from homematicip.base.enums import *
from homematicip.base.functionalChannels import *


@pytest.mark.asyncio
async def test_room_control_device(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F711000BBBB000000000")
    assert isinstance(d, AsyncRoomControlDevice)

    assert d.vaporAmount == 10.662700840292974
    assert d.temperatureOffset == 0.0
    assert d.setPointTemperature == 20.0
    assert d.actualTemperature == 23.0

    assert str(d) == (
        "ALPHA-IP-RBG Raumbediengerät lowBat(False) unreach(False) rssiDeviceValue(-45) "
        "rssiPeerValue(-54) configPending(False) dutyCycle(False) operationLockActive(False) "
        "actualTemperature(23.0) humidity(52) vaporAmount(10.662700840292974) setPointTemperature(20.0)"
    )


@pytest.mark.asyncio
async def test_room_control_device_analog(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F711000000BBBB000005")
    assert isinstance(d, AsyncRoomControlDeviceAnalog)

    assert d.temperatureOffset == 0.0
    assert d.setPointTemperature == 23.0
    assert d.actualTemperature == 23.3

    assert str(d) == (
        "ALPHA-IP-RBGa Raumbediengerät Analog lowBat(False) unreach(False) rssiDeviceValue(-41) "
        "rssiPeerValue(-29) configPending(False) dutyCycle(False) actualTemperature(23.3) "
        "setPointTemperature(23.0) temperatureOffset(0.0)"
    )


@pytest.mark.asyncio
async def test_acceleration_sensor(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000031")
    assert isinstance(d, AsyncAccelerationSensor)
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
    await asyncio.gather(
        d.set_acceleration_sensor_event_filter_period(10.0),
        d.set_acceleration_sensor_mode(AccelerationSensorMode.ANY_MOTION),
        d.set_acceleration_sensor_neutral_position(
            AccelerationSensorNeutralPosition.HORIZONTAL
        ),
        d.set_acceleration_sensor_sensitivity(
            AccelerationSensorSensitivity.SENSOR_RANGE_2G
        ),
        d.set_acceleration_sensor_trigger_angle(30),
        d.set_notification_sound_type(NotificationSoundType.SOUND_SHORT, True),
        d.set_notification_sound_type(NotificationSoundType.SOUND_SHORT_SHORT, False),
    )
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000031")

    assert d.accelerationSensorEventFilterPeriod == 10.0
    assert d.accelerationSensorMode == AccelerationSensorMode.ANY_MOTION
    assert (
        d.accelerationSensorNeutralPosition
        == AccelerationSensorNeutralPosition.HORIZONTAL
    )
    assert (
        d.accelerationSensorSensitivity == AccelerationSensorSensitivity.SENSOR_RANGE_2G
    )
    assert d.accelerationSensorTriggerAngle == 30
    assert d.notificationSoundTypeHighToLow == NotificationSoundType.SOUND_SHORT
    assert d.notificationSoundTypeLowToHigh == NotificationSoundType.SOUND_SHORT_SHORT


@pytest.mark.asyncio
async def test_tilt_vibration_sensor(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110TILTVIBRATIONSENSOR")
    assert isinstance(d, TiltVibrationSensor)
    assert d.accelerationSensorEventFilterPeriod == 0.5
    assert d.accelerationSensorMode == AccelerationSensorMode.FLAT_DECT
    assert (
        d.accelerationSensorSensitivity == AccelerationSensorSensitivity.SENSOR_RANGE_2G
    )
    assert d.accelerationSensorTriggerAngle == 45
    assert d.accelerationSensorTriggered is True

    assert str(d) == (
        "HmIP-STV Garage Neigungs- und Erschütterungssensor lowBat(False) unreach(False)"
        " rssiDeviceValue(-59) rssiPeerValue(None) configPending(False) dutyCycle(False)"
        " accelerationSensorEventFilterPeriod(0.5) accelerationSensorMode(FLAT_DECT) "
        "accelerationSensorSensitivity(SENSOR_RANGE_2G) accelerationSensorTriggerAngle(45)"
        " accelerationSensorTriggered(True)"
    )
    await asyncio.gather(
        d.set_acceleration_sensor_event_filter_period(10.0),
        d.set_acceleration_sensor_mode(AccelerationSensorMode.ANY_MOTION),
        d.set_acceleration_sensor_sensitivity(
            AccelerationSensorSensitivity.SENSOR_RANGE_4G
        ),
        d.set_acceleration_sensor_trigger_angle(30),
    )
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110TILTVIBRATIONSENSOR")

    assert d.accelerationSensorEventFilterPeriod == 10.0
    assert d.accelerationSensorMode == AccelerationSensorMode.ANY_MOTION
    assert (
        d.accelerationSensorSensitivity == AccelerationSensorSensitivity.SENSOR_RANGE_4G
    )
    assert d.accelerationSensorTriggerAngle == 30


@pytest.mark.asyncio
async def test_floor_terminal_block(no_ssl_fake_async_home: AsyncHome):
    d = AsyncFloorTerminalBlock6(no_ssl_fake_async_home._connection)
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000BBBBB1")

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

    d = AsyncFloorTerminalBlock10(no_ssl_fake_async_home._connection)
    d = no_ssl_fake_async_home.search_device_by_id("3014F71100000000FAL24C10")

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

    d = AsyncFloorTerminalBlock12(no_ssl_fake_async_home._connection)
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000049")
    assert d.minimumFloorHeatingValvePosition == 0.0

    await d.set_minimum_floor_heating_valve_position(0.2)

    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000049")
    assert d.minimumFloorHeatingValvePosition == 0.2

    assert str(d) == (
        "HmIP-FALMOT-C12 Fußbodenheizungsaktor OG motorisch lowBat(None) unreach(False) "
        "rssiDeviceValue(-55) rssiPeerValue(None) configPending(False) dutyCycle(False) "
        "minimumFloorHeatingValvePosition(0.2) "
        "pulseWidthModulationAtLowFloorHeatingValvePositionEnabled(True) coolingEmergencyValue(0.0) "
        "frostProtectionTemperature(8.0) valveProtectionDuration(5) valveProtectionSwitchingInterval(14)"
    )

    d = AsyncWiredFloorTerminalBlock12(no_ssl_fake_async_home._connection)
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000053")
    assert d.minimumFloorHeatingValvePosition == 0.0

    await d.set_minimum_floor_heating_valve_position(0.2)

    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000053")
    assert d.minimumFloorHeatingValvePosition == 0.2

    assert str(d) == (
        "HmIPW-FALMOT-C12 Wired Fußbodenheizungsaktor – 12-fach, motorisch lowBat(None) unreach(False) "
        "rssiDeviceValue(None) rssiPeerValue(None) configPending(False) dutyCycle(None) "
        "minimumFloorHeatingValvePosition(0.2) "
        "pulseWidthModulationAtLowFloorHeatingValvePositionEnabled(False) coolingEmergencyValue(0.0) "
        "frostProtectionTemperature(8.0) valveProtectionDuration(5) valveProtectionSwitchingInterval(14)"
    )


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
    assert d is None
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
    not_implemented = False
    for d in no_ssl_fake_async_home.devices:
        if type(d) != AsyncBaseDevice:  # pragma: no cover
            print(f"{d.deviceType} isn't implemented yet")
            not_implemented = True
    assert not_implemented


def test_external_device(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id(
        "HUE00000-0000-0000-0000-000000000008"
    )
    assert isinstance(d, AsyncExternalDevice)
    assert d.connectionType == ConnectionType.EXTERNAL
    assert d.deviceArchetype == DeviceArchetype.EXTERNAL
    assert d.externalService == "HUE"
    assert d.firmwareVersion == "1.88.1"
    assert d.hasCustomLabel == False
    assert d.homeId == "00000000-0000-0000-0000-000000000001"
    assert d.id == "HUE00000-0000-0000-0000-000000000008"
    assert d.label == "Hinten rechts"
    # 1669539365772
    assert d.lastStatusUpdate == datetime(
        2022, 11, 27, 9, 56, 5, 772000
    )  # + timedelta(0, utc_offset)
    assert d.modelType == "LTW013"
    assert d.permanentlyReachable == True
    assert d.supported == True
    assert d.deviceType == DeviceType.EXTERNAL

    assert len(d.functionalChannels) == 2

    fc0 = d.functionalChannels[0]
    fc1 = d.functionalChannels[1]
    assert isinstance(fc0, ExternalBaseChannel)

    assert isinstance(fc1, ExternalUniversalLightChannel)
    assert fc1.channelRole == "UNIVERSAL_LIGHT_ACTUATOR"
    assert fc1.colorTemperature == 3165
    assert fc1.dimLevel == 0.0
    assert fc1.hue == None
    assert fc1.maximumColorTemperature == 6500
    assert fc1.minimalColorTemperature == 2000
    assert fc1.on == False
    assert fc1.saturationLevel == None


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

    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000WTH")
    assert isinstance(d, AsyncWallMountedThermostatPro)


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

    await d.turn_on()
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000009")
    assert d.on is True

    await d.turn_off()
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000009")
    assert d.on is False

    d.id = "INVALID_ID"
    with pytest.raises(HmipWrongHttpStatusError):
        result = await d.turn_off()


@pytest.mark.asyncio
async def test_din_rail_dimmer_3(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F711A000DIN_RAIL_DIMMER3")
    assert isinstance(d, AsyncDinRailDimmer3)
    assert d.dimLevel == d.c1dimLevel
    assert d.c1dimLevel == 0.1
    assert d.c2dimLevel == 0.2
    assert d.c3dimLevel == 0.3

    assert d.functionalChannels[1].dimLevel == 0.1
    await d.set_dim_level(0.5, 1)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F711A000DIN_RAIL_DIMMER3")
    assert d.functionalChannels[1].dimLevel == 0.5

    assert d.functionalChannels[2].dimLevel == 0.2
    await d.set_dim_level(0.67, 2)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F711A000DIN_RAIL_DIMMER3")
    assert d.functionalChannels[2].dimLevel == 0.67

    assert d.functionalChannels[3].dimLevel == 0.3
    await d.set_dim_level(0.8, 3)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F711A000DIN_RAIL_DIMMER3")
    assert d.functionalChannels[3].dimLevel == 0.8


@pytest.mark.asyncio
async def test_din_rail_switch_4(no_ssl_fake_async_home: AsyncHome):
    no_ssl_fake_async_home = no_ssl_fake_async_home
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000005521")
    assert isinstance(d, AsyncDinRailSwitch4)
    assert d.label == "Schaltaktor Verteiler"
    assert d.lastStatusUpdate == (
        datetime(2020, 11, 13, 11, 49, 43, 993000) + timedelta(0, utc_offset)
    )
    assert d.manufacturerCode == 1
    assert d.modelId == 405
    assert d.modelType == "HmIP-DRSI4"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000005521"
    assert d.updateState == DeviceUpdateState.UP_TO_DATE
    assert d.on is None
    assert d.profileMode is None
    assert d.userDesiredProfileMode is None
    assert d.lowBat is None
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -82
    assert d.rssiPeerValue == -78
    assert d.unreach is False
    assert d.availableFirmwareVersion == "1.4.2"
    assert d.firmwareVersion == "1.4.2"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert d.dutyCycle is False
    assert d.configPending is False

    assert str(d) == (
        "HmIP-DRSI4 Schaltaktor Verteiler lowBat(None) unreach(False) rssiDeviceValue(-82) rssiPeerValue(-78) "
        "configPending(False) dutyCycle(False) deviceOverheated(False) devicePowerFailureDetected(False) on(None) "
        "profileMode(None) userDesiredProfileMode(None)"
    )

    for channel in range(1, 4):
        await d.turn_on(channel)
        await no_ssl_fake_async_home.get_current_state()
        d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000005521")
        assert d.functionalChannels[channel].on is True

        await d.turn_off(channel)
        await no_ssl_fake_async_home.get_current_state()
        d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000005521")
        assert d.functionalChannels[channel].on is False


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

    assert str(d) == (
        "HMIP-eTRV Wohnzimmer-Heizung lowBat(False) unreach(False) "
        "rssiDeviceValue(-65) rssiPeerValue(-66) configPending(False) "
        "dutyCycle(False) operationLockActive(True) valvePosition(0.0) "
        "valveState(ADAPTION_DONE) temperatureOffset(0.0) "
        "setPointTemperature(5.0) valveActualTemperature(20.0)"
    )

    await d.set_operation_lock(False)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000015")
    assert d.operationLockActive is False

    d.id = "INVALID_ID"
    with pytest.raises(HmipWrongHttpStatusError):
        result = await d.set_operation_lock(True)


@pytest.mark.asyncio
async def test_heating_thermostat_evo(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000E70")
    assert isinstance(d, AsyncHeatingThermostatEvo)
    assert d.label == "Wohnzimmer 4"
    assert d.manufacturerCode == 1
    assert d.modelId == 425
    assert d.modelType == "HmIP-eTRV-E"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000000E70"
    assert d.updateState == DeviceUpdateState.UP_TO_DATE
    assert d.setPointTemperature == 19.0
    assert d.temperatureOffset == 0.5
    assert d.valvePosition == 0.33
    assert d.valveActualTemperature == 18.7
    assert d.valveState == ValveState.ADAPTION_DONE
    assert d.lowBat is False
    assert d.operationLockActive is False
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -64
    assert d.rssiPeerValue == -67
    assert d.unreach is False
    assert d.automaticValveAdaptionNeeded is False

    assert str(d) == (
        "HmIP-eTRV-E Wohnzimmer 4 lowBat(False) unreach(False) "
        "rssiDeviceValue(-64) rssiPeerValue(-67) configPending(False) "
        "dutyCycle(False) mountingOrientation(RIGHT) operationLockActive(False) valvePosition(0.33) "
        "valveState(ADAPTION_DONE) temperatureOffset(0.5) "
        "setPointTemperature(19.0) valveActualTemperature(18.7)"
    )

    await d.set_operation_lock(True)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000E70")
    assert d.operationLockActive is True

    d.id = "INVALID_ID"
    with pytest.raises(HmipWrongHttpStatusError):
        result = await d.set_operation_lock(True)


@pytest.mark.asyncio
async def test_heating_thermostat_etrv_i9f(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F711000000000ETRVI9F")
    assert isinstance(d, AsyncHeatingThermostat)


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
        "HmIP-BSL Treppe lowBat(None) unreach(False) "
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
    assert d.blindModeActive is True
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


@pytest.mark.asyncio
async def test_din_rail_blind_4(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000022311")
    assert isinstance(d, AsyncDinRailBlind4)
    assert d.label == "Jalousieaktor 1 für Hutschienenmontage – 4-fach"
    assert d.lastStatusUpdate == (
        datetime(2020, 11, 3, 13, 35, 24, 509000) + timedelta(0, utc_offset)
    )
    assert d.manufacturerCode == 1
    assert d.modelId == 406
    assert d.modelType == "HmIP-DRBLI4"
    assert d.oem == "eQ-3"
    assert d.serializedGlobalTradeItemNumber == "3014F7110000000000022311"
    assert d.updateState == DeviceUpdateState.UP_TO_DATE
    assert d.lowBat is None
    assert d.routerModuleEnabled is False
    assert d.routerModuleSupported is False
    assert d.rssiDeviceValue == -70
    assert d.rssiPeerValue == -63
    assert d.unreach is False
    assert d.availableFirmwareVersion == "1.6.0"
    assert d.firmwareVersion == "1.6.0"
    a, b, c = [int(i) for i in d.firmwareVersion.split(".")]
    assert d.firmwareVersionInteger == (a << 16) | (b << 8) | c
    assert d.dutyCycle is False
    assert d.configPending is False

    for channel in range(1, 4):
        await d.set_shutter_level(0.35, channelIndex=channel)
        await no_ssl_fake_async_home.get_current_state()
        d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000022311")
        assert d.functionalChannels[channel].shutterLevel == 0.35

        await d.set_slats_level(0.8, channelIndex=channel)
        await no_ssl_fake_async_home.get_current_state()
        d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000022311")
        assert d.functionalChannels[channel].shutterLevel == 0.35
        assert d.functionalChannels[channel].slatsLevel == 0.8

        await d.set_slats_level(0.8, 0.3, channelIndex=channel)
        await no_ssl_fake_async_home.get_current_state()
        d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000022311")
        assert d.functionalChannels[channel].shutterLevel == 0.3
        assert d.functionalChannels[channel].slatsLevel == 0.8


@pytest.mark.asyncio
async def test_wired_din_rail_blind_4(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F71100000000000DRBL4")
    assert isinstance(d, AsyncWiredDinRailBlind4)


@pytest.mark.asyncio
async def test_door_sensor_tm(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F0000000000000FAF9B4")

    assert d.doorState == DoorState.CLOSED
    assert d.on == False
    assert d.processing == False
    assert d.ventilationPositionSupported == True

    await no_ssl_fake_async_home.get_current_state()
    await d.send_door_command(DoorCommand.OPEN)
    await no_ssl_fake_async_home.get_current_state()
    assert d.doorState == DoorState.OPEN


@pytest.mark.asyncio
async def test_hoermann_drives_module(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000HOERMANN")

    assert d.doorState == DoorState.CLOSED
    assert d.on is False
    assert d.processing is False
    assert d.ventilationPositionSupported is True


@pytest.mark.asyncio
async def test_pluggable_mains_failure(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000ABCD50")

    assert d.powerMainsFailure is False
    assert d.genericAlarmSignal is AlarmSignalType.FULL_ALARM

    assert str(d) == (
        "HmIP-PMFS Netzausfallüberwachung lowBat(None) unreach(False) rssiDeviceValue(-58) "
        "rssiPeerValue(None) configPending(False) dutyCycle(False) powerMainsFailure(False) "
        "genericAlarmSignal(FULL_ALARM)"
    )


@pytest.mark.asyncio
async def test_wall_thermostat_basic(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F711000000000000AAA5")

    assert d.display == ClimateControlDisplay.ACTUAL
    assert d.humidity == 42

    assert str(d) == (
        "HmIP-WTH-B Thermostat Schlafen Tal lowBat(False) unreach(False) rssiDeviceValue(-58) "
        "rssiPeerValue(-59) configPending(False) dutyCycle(False) operationLockActive(False) "
        "actualTemperature(16.0) humidity(42) vaporAmount(5.710127947243264) "
        "setPointTemperature(12.0)"
    )


@pytest.mark.asyncio
async def test_blind_module(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F71100BLIND_MODULE00")

    assert str(d) == (
        "HmIP-HDM1 Sonnenschutz Balkontür lowBat(False) unreach(False) rssiDeviceValue(-85) "
        "rssiPeerValue(-78) configPending(False) dutyCycle(False) automationDriveSpeed(SLOW_SPEED) "
        "manualDriveSpeed(NOMINAL_SPEED) favoritePrimaryShadingPosition(0.5) "
        "favoriteSecondaryShadingPosition(0.5) primaryCloseAdjustable(True) "
        "primaryOpenAdjustable(True) primaryShadingStateType(POSITION_USED) "
        "secondaryCloseAdjustable(False) secondaryOpenAdjustable(False) "
        "secondaryShadingStateType(NOT_EXISTENT) primaryShadingLevel(0.94956) "
        "secondaryShadingLevel(0) previousPrimaryShadingLevel(None) "
        "previousSecondaryShadingLevel(None) identifyOemSupported(True) productId(10) "
        "profileMode(AUTOMATIC) userDesiredProfileMode(AUTOMATIC) shadingDriveVersion(None) "
        "shadingPackagePosition(TOP) shadingPositionAdjustmentActive(None) "
        "shadingPositionAdjustmentClientId(None)"
    )

    await d.set_primary_shading_level(5)

    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F71100BLIND_MODULE00")
    assert d.primaryShadingLevel == 5

    await d.stop()

    await d.set_secondary_shading_level(0.5, 1.0)

    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F71100BLIND_MODULE00")
    assert d.primaryShadingLevel == 0.5
    assert d.secondaryShadingLevel == 1.0


@pytest.mark.asyncio
async def test_home_control_access_point(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F711A000000BAD0C0DED")

    assert str(d) == (
        "HmIP-HAP HOME_CONTROL_ACCESS_POINT lowBat(None) unreach(False) rssiDeviceValue(None) "
        "rssiPeerValue(None) configPending(False) dutyCycle(False) dutyCycleLevel(8.0) "
        "accessPointPriority(1) signalBrightness(1.0)"
    )


@pytest.mark.asyncio
async def test_wired_din_rail_access_point(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F71100000000000WDRAP")
    assert isinstance(d, AsyncWiredDinRailAccessPoint)


@pytest.mark.asyncio
async def test_rain_sensor(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000RAIN_SENSOR")

    assert d.raining == True
    assert d.rainSensorSensitivity == 50.0

    assert str(d) == (
        "HmIP-SRD Regensensor lowBat(None) unreach(False) rssiDeviceValue(-91) "
        "rssiPeerValue(None) configPending(False) dutyCycle(False) "
        "rainSensorSensitivity(50.0) raining(True)"
    )


@pytest.mark.asyncio
async def test_door_lock_drive(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000DLD")

    assert d.lockState == LockState.LOCKED
    assert d.motorState == MotorState.STOPPED

    await no_ssl_fake_async_home.get_current_state()
    await d.set_lock_state(LockState.OPEN)
    await no_ssl_fake_async_home.get_current_state()
    assert d.lockState == LockState.OPEN


@pytest.mark.asyncio
async def test_door_lock_sensor(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000DLS")

    assert d.doorLockDirection == "LEFT"
    assert d.doorLockNeutralPosition == "HORIZONTAL"
    assert d.doorLockTurns == 2
    assert d.lockState == None


@pytest.mark.asyncio
async def test_door_bell_button(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000DBB")
    assert isinstance(d, AsyncDoorBellButton)


@pytest.mark.asyncio
async def test_door_bell_contact_interface(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000DSDPCB")
    assert isinstance(d, AsyncDoorBellContactInterface)
    assert d.functionalChannels[1].doorBellSensorEventTimestamp == 1673006015756


@pytest.mark.asyncio
async def test_energy_sensor_interface_channel(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000ESI")
    assert isinstance(d, AsyncEnergySensorsInterface)


@pytest.mark.asyncio
async def test_multibox_io(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F711ABCD0ABCD000002")
    assert isinstance(d, AsyncMultiIOBox)

    await d.turn_on(1)
    await no_ssl_fake_async_home.get_current_state()
    assert d.functionalChannels[1].on == True
    await d.turn_off(1)
    await no_ssl_fake_async_home.get_current_state()
    assert d.functionalChannels[1].on == False


@pytest.mark.asyncio
async def test_wired_din_rail_switch_4(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F711000WIREDSWITCH4")
    assert isinstance(d, AsyncWiredSwitch4)

    for i in range(1, 4):
        await d.turn_on(i)
        await no_ssl_fake_async_home.get_current_state()
        assert d.functionalChannels[i].on == True
        await d.turn_off(i)
        await no_ssl_fake_async_home.get_current_state()
        assert d.functionalChannels[i].on == False


@pytest.mark.asyncio
async def test_async_wired_input_switch_6(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F711000000000000FIO6")
    assert isinstance(d, AsyncWiredInputSwitch6)


@pytest.mark.asyncio
async def test_async_wired_push_button(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F71100000000000WWRC6")
    assert isinstance(d, AsyncWiredPushButton)

    result = await d.set_dim_level(10, 0.5)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F71100000000000WWRC6")
    c = d.functionalChannels[2]
    assert c.dimLevel == 0.5

    await d.set_optical_signal(
        10, OpticalSignalBehaviour.BILLOW_MIDDLE, RGBColorState.BLUE
    )
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F71100000000000WWRC6")
    c = d.functionalChannels[2]
    assert c.dimLevel == 1.01
    assert c.opticalSignalBehaviour == OpticalSignalBehaviour.BILLOW_MIDDLE
    assert c.simpleRGBColorState == "BLUE"

    c = d.functionalChannels[5]
    assert isinstance(c, OpticalSignalGroupChannel)
    await d.set_dim_level(13, 0.5)
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F71100000000000WWRC6")
    c = d.functionalChannels[5]
    assert c.dimLevel == 0.5

    await d.set_optical_signal(
        13, OpticalSignalBehaviour.BILLOW_MIDDLE, RGBColorState.BLUE
    )
    await no_ssl_fake_async_home.get_current_state()
    d = no_ssl_fake_async_home.search_device_by_id("3014F71100000000000WWRC6")
    c = d.functionalChannels[5]
    assert c.dimLevel == 1.01
    assert c.opticalSignalBehaviour == OpticalSignalBehaviour.BILLOW_MIDDLE
    assert c.simpleRGBColorState == "BLUE"

    await d.turn_on(13)
    await no_ssl_fake_async_home.get_current_state()
    c = d.functionalChannels[5]
    assert c.on == True

    await d.turn_off(13)
    await no_ssl_fake_async_home.get_current_state()
    c = d.functionalChannels[5]
    assert c.on == False

    await d.turn_on(13)
    await no_ssl_fake_async_home.get_current_state()
    c = d.functionalChannels[5]
    assert c.on == True


@pytest.mark.asyncio
async def test_async_wired_motion_detector_push_button(
    no_ssl_fake_async_home: AsyncHome,
):
    d = no_ssl_fake_async_home.search_device_by_id("3014F71100000000000SMI55")
    assert isinstance(d, AsyncWiredMotionDetectorPushButton)


@pytest.mark.asyncio
async def test_async_wired_presence_detector(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F711000000000000WSPI")
    assert isinstance(d, AsyncPresenceDetectorIndoor)


@pytest.mark.asyncio
async def test_carbon_dioxide_sensor(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F711000000000SCTH230")
    assert isinstance(d, AsyncCarbonDioxideSensor)
    c = d.functionalChannels[1]
    assert c.actualTemperature == 25.5
    assert c.carbonDioxideConcentration == 1181.0
    assert c.carbonDioxideVisualisationEnabled == True
    assert c.humidity == 37
    assert c.vaporAmount == 8.739326558877478


@pytest.mark.asyncio
async def test_dali_Gateway(no_ssl_fake_async_home: AsyncHome):
    d = no_ssl_fake_async_home.search_device_by_id("3014F711000000000000DALI")
    assert isinstance(d, AsyncDaliGateway)
