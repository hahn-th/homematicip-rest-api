import json
import logging
import asyncio

from homematicip import device
from homematicip.async.connection import Connection
from homematicip.base.base_device import BasePluggableSwitch, BaseDevice, \
    BaseSabotageDevice, BaseOperationLockableDevice, BaseHeatingThermostat, \
    BaseShutterContact, BaseTemperatureHumiditySensorDisplay, \
    BaseWallMountedThermostatPro, BaseSmokeDetector, BaseFloorTerminalBlock6, \
    BasePluggableSwitchMeasuring, BasePushButton, BaseAlarmSirenIndoor, \
    BaseMotionDetectorIndoor, BaseKeyRemoteControlAlarm, BaseFullFlushShutter

ERROR_CODE = "errorCode"

_LOGGER = logging.getLogger(__name__)


class Device(BaseDevice):
    """ Async implementation of a genereric homematic ip device """

    def from_json(self, js):
        raise NotImplementedError('from_json should not be called from here.')

    def __repr__(self):
        return u"{} {} lowbat({}) unreach({})".format(self.deviceType,
                                                      self.label, self.lowBat,
                                                      self.unreach)


class SabotageDevice(BaseSabotageDevice, Device):
    def __init__(self, connection):
        super().__init__(connection)


class OperationLockableDevice(BaseOperationLockableDevice,
                              Device):
    async def set_operation_lock(self, operationLock=True):
        url, data = self._set_operation_lock()

        _val = await self.connection._rest_call(url, data)
        return _val


class HeatingThermostat(BaseHeatingThermostat, Device):
    """ HMIP-eTRV (Radiator Thermostat) """
    pass


class ShutterContact(BaseShutterContact, Device):
    """ HMIP-SWDO (Door / Window Contact - optical) """


class TemperatureHumiditySensorDisplay(BaseTemperatureHumiditySensorDisplay,
                                       Device):
    """ HMIP-STHD (Temperature and Humidity Sensor with display - indoor) """
    DISPLAY_ACTUAL = "ACTUAL"

    async def set_display(self, display=DISPLAY_ACTUAL):
        url, data = super().set_display(display)
        data = {"channelIndex": 1, "deviceId": self.id, "display": display}
        _val = await self.connection._rest_call(url, data)
        return _val


class WallMountedThermostatPro(BaseWallMountedThermostatPro,
                               Device):
    """ HMIP-WTH, HMIP-WTH-2 (Wall Thermostat with Humidity Sensor) """


class SmokeDetector(BaseSmokeDetector, Device):
    """ HMIP-SWSD (Smoke Alarm with Q label) """


class FloorTerminalBlock6(BaseFloorTerminalBlock6,
                          Device):
    """ HMIP-FAL230-C6 (Floor Heating Actuator - 6 channels, 230 V) """


class PluggableSwitch(BasePluggableSwitch, Device):
    """ Async implementation of HMIP-PS (Pluggable Switch) """

    async def turn_on(self):
        url, data = self._turn_on()
        return await self.connection._rest_call(url, data)

    async def turn_off(self):
        url, data = self._turn_off()
        return await self.connection._rest_call(url, data)


class PlugableSwitchMeasuring(BasePluggableSwitchMeasuring,
                              Device):
    """ HMIP-PSM (Pluggable Switch and Meter) """

    async def set_switch_state(self, on=True):
        url, data = self._set_switch_state(on)
        _val = await self.connection._rest_call(url, data)
        return _val

    async def turn_on(self):
        url, data = self._turn_on()
        return await self.connection._rest_call(url, data)

    async def turn_off(self):
        url, data = self._turn_off()
        return await self.connection._rest_call(url, data)


class PushButton(BasePushButton, Device):
    """ HMIP-WRC2 (Wall-mount Remote Control - 2-button) """


class AlarmSirenIndoor(BaseAlarmSirenIndoor, Device):
    """ HMIP-ASIR (Alarm Siren) """


class MotionDetectorIndoor(BaseMotionDetectorIndoor, Device):
    """ HMIP-SMI (Motion Detector with Brightness Sensor - indoor) """


class KeyRemoteControlAlarm(BaseKeyRemoteControlAlarm, Device):
    """ HMIP-KRCA (Key Ring Remote Control - alarm) """


class FullFlushShutter(BaseFullFlushShutter, Device):
    """ HMIP-FROLL (Shutter Actuator - flush-mount) """

    async def set_shutter_level(self, level):
        url, data = self._set_shutter_level(level)

        _val = await self.connection._rest_call(url, data)
        return _val

    async def set_shutter_stop(self):
        url, data = self._set_shutter_stop()
        _val = await self.connection._rest_call(url, data)
        return _val
