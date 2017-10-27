import json
import logging
import asyncio

from homematicip.async import HomeIPObject
from homematicip import device
from homematicip.async.connection import Connection
from homematicip.base.base_device import BasePluggableSwitch, BaseDevice

ERROR_CODE = "errorCode"

_LOGGER = logging.getLogger(__name__)


class Device(BaseDevice):
    """ Async implementation of a genereric homematic ip device """

    def from_json(self, js):
        raise NotImplemented('from_json should not be called from here.')

    def __repr__(self):
        return u"{} {} lowbat({}) unreach({})".format(self.deviceType,
                                                      self.label, self.lowBat,
                                                      self.unreach)


class SabotageDevice(HomeIPObject.HomeMaticIPobject, device.SabotageDevice):
    def __init__(self, connection):
        super().__init__(connection)


class OperationLockableDevice(HomeIPObject.HomeMaticIPobject,
                              device.OperationLockableDevice):
    def __init__(self, connection):
        super().__init__(connection)

    async def set_operation_lock(self, operationLock=True):
        url, data = super().set_operation_lock(operationLock)

        _val = await self._connection._apiCall(url, data)
        return _val

    def from_json(self, js):
        super().from_json(js)
        self.update(js)


class HeatingThermostat(HomeIPObject.HomeMaticIPobject,
                        device.HeatingThermostat):
    """ HMIP-eTRV (Radiator Thermostat) """

    def __init__(self, connection):
        super().__init__(connection)


class ShutterContact(HomeIPObject.HomeMaticIPobject, device.ShutterContact):
    """ HMIP-SWDO (Door / Window Contact - optical) """

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        super().from_json(js)
        self.update(js)


class TemperatureHumiditySensorDisplay(HomeIPObject.HomeMaticIPobject,
                                       device.TemperatureHumiditySensorDisplay):
    """ HMIP-STHD (Temperature and Humidity Sensor with display - indoor) """
    DISPLAY_ACTUAL = "ACTUAL"

    def __init__(self, connection):
        super().__init__(connection)

    async def set_display(self, display=DISPLAY_ACTUAL):
        url, data = super().set_display(display)
        data = {"channelIndex": 1, "deviceId": self.id, "display": display}
        _val = await self._connection._apiCall(url, data)
        return _val


class WallMountedThermostatPro(HomeIPObject.HomeMaticIPobject,
                               device.WallMountedThermostatPro):
    """ HMIP-WTH, HMIP-WTH-2 (Wall Thermostat with Humidity Sensor) """

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        super().from_json(js)
        self.update(js)


class SmokeDetector(HomeIPObject.HomeMaticIPobject, device.SmokeDetector):
    """ HMIP-SWSD (Smoke Alarm with Q label) """

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        super().from_json(js)
        self.update(js)


class FloorTerminalBlock6(HomeIPObject.HomeMaticIPobject,
                          device.FloorTerminalBlock6):
    """ HMIP-FAL230-C6 (Floor Heating Actuator - 6 channels, 230 V) """

    def __init__(self, connection):
        super().__init__(connection)


class PluggableSwitch(BasePluggableSwitch, Device):
    """ Async implementation of HMIP-PS (Pluggable Switch) """

    async def turn_on(self):
        url, data = self._turn_on()
        return await self.connection._rest_call(url, data)

    async def turn_off(self):
        url, data = self._turn_off()
        return await self.connection._rest_call(url, data)


class PlugableSwitchMeasuring(HomeIPObject.HomeMaticIPobject,
                              device.PlugableSwitchMeasuring):
    """ HMIP-PSM (Pluggable Switch and Meter) """

    def __init__(self, connection):
        super().__init__(connection)

    def __repr__(self):
        return self.__unicode__()

    def from_json(self, js):
        super().from_json(js)
        self.update(js)

    async def set_switch_state(self, on=True):
        url, data = super().set_switch_state(on)
        _val = await self._connection._apiCall(url, data)
        return _val

    async def turn_on(self):
        _val = await self.set_switch_state(True)
        return _val

    async def turn_off(self):
        _val = await self.set_switch_state(False)
        return _val


class PushButton(HomeIPObject.HomeMaticIPobject, device.PushButton):
    """ HMIP-WRC2 (Wall-mount Remote Control - 2-button) """


class AlarmSirenIndoor(HomeIPObject.HomeMaticIPobject,
                       device.AlarmSirenIndoor):
    """ HMIP-ASIR (Alarm Siren) """


class MotionDetectorIndoor(HomeIPObject.HomeMaticIPobject,
                           device.MotionDetectorIndoor):
    """ HMIP-SMI (Motion Detector with Brightness Sensor - indoor) """

    def __init__(self, connection):
        super().__init__(connection)


class KeyRemoteControlAlarm(HomeIPObject.HomeMaticIPobject,
                            device.KeyRemoteControlAlarm):
    """ HMIP-KRCA (Key Ring Remote Control - alarm) """

    def __init__(self, connection):
        super().__init__(connection)


class FullFlushShutter(HomeIPObject.HomeMaticIPobject,
                       device.FullFlushShutter):
    """ HMIP-FROLL (Shutter Actuator - flush-mount) """

    def __init__(self, connection):
        super().__init__(connection)

    # def __unicode__(self):
    #     return u"{} shutterLevel({}) topToBottom({}) bottomToTop({})".format(
    #         super(FullFlushShutter, self).__unicode__(),
    #         self.shutterLevel, self.topToBottomReferenceTime,
    #         self.bottomToTopReferenceTime)

    async def set_shutter_level(self, level):
        url, data = super().set_shutter_level(level)

        _val = await self._connection._apiCall(url, data)
        return _val

    async def set_shutter_stop(self):
        url, data = super().set_shutter_stop()
        _val = await self._connection._apiCall(url, data)
        return _val
