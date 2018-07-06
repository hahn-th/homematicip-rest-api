import logging

from homematicip.device import Device, PlugableSwitch, PlugableSwitchMeasuring, \
    SabotageDevice, ShutterContact, OperationLockableDevice, HeatingThermostat, \
    TemperatureHumiditySensorWithoutDisplay, TemperatureHumiditySensorDisplay, \
    WallMountedThermostatPro, SmokeDetector, FloorTerminalBlock6, PushButton, AlarmSirenIndoor, \
    MotionDetectorIndoor, MotionDetectorPushButton, PresenceDetectorIndoor, KeyRemoteControlAlarm, FullFlushShutter, \
    Dimmer, PluggableDimmer, BrandSwitchMeasuring, FullFlushSwitchMeasuring, Switch, \
    WeatherSensor, WeatherSensorPro, RotaryHandleSensor, TemperatureHumiditySensorOutdoor, \
    WaterSensor
from homematicip.base.enums import *

ERROR_CODE = "errorCode"

_LOGGER = logging.getLogger(__name__)


class AsyncDevice(Device):
    """ Async implementation of a genereric homematic ip device """

    async def set_label(self, label):
        return await self._connection.api_call(*super().set_label(label))

    async def authorizeUpdate(self):
        return await self._connection.api_call(*super().authorizeUpdate())

    async def delete(self):
        return await self._connection.api_call(*super().delete())

    async def set_router_module_enabled(self, enabled=True):
        return await self._connection.api_call(*super().set_router_module_enabled(enabled))

    async def is_update_applicable(self):
        return await self._connection.api_call(*super().is_update_applicable())


class AsyncSwitch(Switch, AsyncDevice):
    """ Generic async switch """

    async def turn_on(self):
        _LOGGER.debug("Async switch turn_on")
        url, data = super().turn_on()
        return await self._connection.api_call(url, data)

    async def turn_off(self):
        _LOGGER.debug("Async switch turn_off")
        url, data = super().turn_off()
        return await self._connection.api_call(url, data)


class AsyncPlugableSwitch(PlugableSwitch, AsyncSwitch):
    """ Async implementation of HMIP-PS (Pluggable Switch) """


class AsyncSabotageDevice(SabotageDevice, AsyncDevice):
    pass


class AsyncOperationLockableDevice(OperationLockableDevice, AsyncDevice):
    async def set_operation_lock(self, operationLock=True):
        return await self._connection.api_call(
            *super().set_operation_lock(operationLock=operationLock))


class AsyncPlugableSwitchMeasuring(PlugableSwitchMeasuring, AsyncSwitch):
    """ HMIP-PSM (Pluggable Switch and Meter) """
    pass


class AsyncBrandSwitchMeasuring(BrandSwitchMeasuring, AsyncSwitch):
    """ HMIP-BSM (Brand Switch and Meter) """


class AsyncFullFlushSwitchMeasuring(FullFlushSwitchMeasuring, AsyncSwitch):
    """ HmIP-FSM (Full flush Switch and Meter) """


class AsyncShutterContact(ShutterContact, AsyncSabotageDevice):
    """ HMIP-SWDO (Door / Window Contact - optical) /
    HMIP-SWDO-I (Door / Window Contact Invisible - optical)"""

    pass

class AsyncRotaryHandleSensor(RotaryHandleSensor, AsyncSabotageDevice):
    """ HmIP-SRH """

class AsyncTemperatureHumiditySensorOutdoor(TemperatureHumiditySensorOutdoor, AsyncDevice):
    """ HmIP-STHO (Temperature and Humidity Sensor outdoor) """

class AsyncHeatingThermostat(HeatingThermostat, AsyncOperationLockableDevice):
    """ HMIP-eTRV (Radiator Thermostat) """
    pass


class AsyncTemperatureHumiditySensorWithoutDisplay(TemperatureHumiditySensorWithoutDisplay,
                                                   AsyncDevice):
    """ HMIP-STH (Temperature and Humidity Sensor without display - indoor) """
    pass


class AsyncTemperatureHumiditySensorDisplay(TemperatureHumiditySensorDisplay, AsyncDevice):
    """ HMIP-STHD (Temperature and Humidity Sensor with display - indoor) """
    # todo: need override these otherwise cannot use them as method parameters. Fix this.
    DISPLAY_ACTUAL = "ACTUAL"
    DISPLAY_SETPOINT = "SETPOINT"
    DISPLAY_ACTUAL_HUMIDITY = "ACTUAL_HUMIDITY"

    async def set_display(self, display=DISPLAY_ACTUAL):
        await self._connection.api_call(*super().set_display(display=display))


class AsyncWallMountedThermostatPro(WallMountedThermostatPro, AsyncTemperatureHumiditySensorDisplay,
                                    AsyncOperationLockableDevice):
    """ HMIP-WTH, HMIP-WTH-2 (Wall Thermostat with Humidity Sensor)
    / HMIP-BWTH (Brand Wall Thermostat with Humidity Sensor)"""
    pass


class AsyncSmokeDetector(SmokeDetector, AsyncDevice):
    """ HMIP-SWSD (Smoke Alarm with Q label) """
    pass


class AsyncFloorTerminalBlock6(FloorTerminalBlock6, AsyncDevice):
    """ HMIP-FAL230-C6 (Floor Heating Actuator - 6 channels, 230 V) """
    pass


class AsyncPushButton(PushButton, AsyncDevice):
    """ HMIP-WRC2 (Wall-mount Remote Control - 2-button) """


class AsyncAlarmSirenIndoor(AlarmSirenIndoor, AsyncSabotageDevice):
    """ HMIP-ASIR (Alarm Siren) """


class AsyncMotionDetectorIndoor(MotionDetectorIndoor, AsyncSabotageDevice):
    """ HMIP-SMI (Motion Detector with Brightness Sensor - indoor) """
    pass


class AsyncMotionDetectorPushButton(MotionDetectorPushButton, AsyncSabotageDevice):
    """ HMIP-SMI55 (Motion Detector with Brightness Sensor and Remote Control - 2-button) """
    pass


class AsyncPresenceDetectorIndoor(PresenceDetectorIndoor, AsyncSabotageDevice):
    """ HMIP-SPI (Presence Sensor - indoor) """
    pass


class AsyncKeyRemoteControlAlarm(KeyRemoteControlAlarm, AsyncDevice):
    """ HMIP-KRCA (Key Ring Remote Control - alarm) """
    pass


class AsyncFullFlushShutter(FullFlushShutter, AsyncDevice):
    """ HMIP-FROLL (Shutter Actuator - flush-mount) / HMIP-BROLL (Shutter Actuator - Brand-mount) """

    async def set_shutter_level(self, level):
        return await self._connection.api_call(*super().set_shutter_level(level))

    async def set_shutter_stop(self):
        return await self._connection.api_call(*super().set_shutter_stop())


class AsyncDimmer(Dimmer, AsyncDevice):
    """Base dimmer device class"""

    async def set_dim_level(self, dimLevel=0.0):
        return await self._connection.api_call(*super().set_dim_level(dimLevel=dimLevel))

class AsyncPluggableDimmer(AsyncDimmer):
    """HmIP-PDT Pluggable Dimmer"""

class AsyncBrandDimmer(AsyncDimmer):
    """HmIP-BDT Brand Dimmer"""

class AsyncWeatherSensor(WeatherSensor, AsyncDevice):
    """ HmIP-SWO-B """

class AsyncWeatherSensorPro(WeatherSensorPro, AsyncDevice):
    """ HmIP-SWO-PR """

class AsyncWaterSensor(WaterSensor, AsyncDevice):
    """ HmIP-SWD """
    async def set_acoustic_alarm_signal(self, acousticAlarmSignal : AcousticAlarmSignal):
        return await self._connection.api_call(*super().set_acoustic_alarm_signal(acousticAlarmSignal=acousticAlarmSignal))

    async def set_acoustic_alarm_timing(self, acousticAlarmTiming : AcousticAlarmTiming):
        return await self._connection.api_call(*super().set_acoustic_alarm_timing(acousticAlarmTiming=acousticAlarmTiming))
    
    async def set_acoustic_water_alarm_trigger(self, acousticWaterAlarmTrigger : WaterAlarmTrigger):
        return await self._connection.api_call(*super().set_acoustic_water_alarm_trigger(acousticWaterAlarmTrigger=acousticWaterAlarmTrigger))

    async def set_inapp_water_alarm_trigger(self, inAppWaterAlarmTrigger : WaterAlarmTrigger):
        return await self._connection.api_call(*super().set_inapp_water_alarm_trigger(inAppWaterAlarmTrigger=inAppWaterAlarmTrigger))

    async def set_siren_water_alarm_trigger(self, sirenWaterAlarmTrigger : WaterAlarmTrigger):
        return await self._connection.api_call(*super().set_siren_water_alarm_trigger(sirenWaterAlarmTrigger=sirenWaterAlarmTrigger))