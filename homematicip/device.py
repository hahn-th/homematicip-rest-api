# coding=utf-8
from homematicip import HomeMaticIPObject
import json
from datetime import datetime

from homematicip.base.base_device import BaseDevice, BaseSabotageDevice, \
    BaseOperationLockableDevice


class Device(BaseDevice):
    """ this class represents a generic homematic ip device """

    def from_json(self, js):
        raise NotImplementedError('from_json should not be called from here.')


class SabotageDevice(BaseSabotageDevice,Device):
    pass

class OperationLockableDevice(BaseOperationLockableDevice, Device):

    def set_operation_lock(self, operationLock=True):
        data = {"channelIndex": 0, "deviceId": self.id,
                "operationLock": operationLock}
        return self._restCall("device/configuration/setOperationLock",
                              json.dumps(data))

    def __unicode__(self):
        return u"{}: operationLockActive({})".format(
            super(OperationLockableDevice, self).__unicode__(),
            self.operationLockActive)


class HeatingThermostat(OperationLockableDevice):
    """ HMIP-eTRV (Radiator Thermostat) """

    temperatureOffset = None
    valvePosition = None

    def from_json(self, js):
        super(HeatingThermostat, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "HEATING_THERMOSTAT_CHANNEL":
                self.temperatureOffset = c["temperatureOffset"]
                self.valvePosition = c["valvePosition"]

    def __unicode__(self):
        return u"{} valvePosition({})".format(
            super(HeatingThermostat, self).__unicode__(), self.valvePosition)


class ShutterContact(SabotageDevice):
    """ HMIP-SWDO (Door / Window Contact - optical) """
    windowState = None
    eventDelay = None

    def from_json(self, js):
        super(ShutterContact, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SHUTTER_CONTACT_CHANNEL":
                self.windowState = c["windowState"]
                self.eventDelay = c["eventDelay"]

    def __unicode__(self):
        return u"{} windowState({})".format(
            super(ShutterContact, self).__unicode__(), self.windowState)


class TemperatureHumiditySensorDisplay(Device):
    """ HMIP-STHD (Temperature and Humidity Sensor with display - indoor) """

    DISPLAY_ACTUAL = "ACTUAL"
    DISPLAY_SETPOINT = "SETPOINT"
    DISPLAY_ACTUAL_HUMIDITY = "ACTUAL_HUMIDITY"

    temperatureOffset = None
    display = None
    actualTemperature = None
    humidity = None

    def from_json(self, js):
        super(TemperatureHumiditySensorDisplay, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL":
                self.temperatureOffset = c["temperatureOffset"]
                self.display = c["display"]
                self.actualTemperature = c["actualTemperature"]
                self.humidity = c["humidity"]

    def set_display(self, display=DISPLAY_ACTUAL):
        data = {"channelIndex": 1, "deviceId": self.id, "display": display}
        return self._restCall("device/configuration/setClimateControlDisplay",
                              json.dumps(data))

    def __unicode__(self):
        return u"{}: actualTemperature({}) humidity({})".format(
            super(TemperatureHumiditySensorDisplay, self).__unicode__(),
            self.actualTemperature, self.humidity)


class WallMountedThermostatPro(TemperatureHumiditySensorDisplay,
                               OperationLockableDevice):
    """ HMIP-WTH, HMIP-WTH-2 (Wall Thermostat with Humidity Sensor) """

    def from_json(self, js):
        super(WallMountedThermostatPro, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL":
                self.temperatureOffset = c["temperatureOffset"]
                self.display = c["display"]
                self.actualTemperature = c["actualTemperature"]
                self.humidity = c["humidity"]


class SmokeDetector(Device):
    """ HMIP-SWSD (Smoke Alarm with Q label) """

    smokeDetectorAlarmType = None

    def from_json(self, js):
        super(SmokeDetector, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SMOKE_DETECTOR_CHANNEL":
                self.smokeDetectorAlarmType = c["smokeDetectorAlarmType"]

    def __unicode__(self):
        return u"{}: smokeDetectorAlarmType({})".format(
            super(SmokeDetector, self).__unicode__(),
            self.smokeDetectorAlarmType)


class FloorTerminalBlock6(Device):
    """ HMIP-FAL230-C6 (Floor Heating Actuator - 6 channels, 230 V) """

    globalPumpControl = None
    heatingValveType = None

    def from_json(self, js):
        super(FloorTerminalBlock6, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "DEVICE_GLOBAL_PUMP_CONTROL":
                self.unreach = c["unreach"]
                self.globalPumpControl = c["globalPumpControl"]
                self.heatingValveType = c["heatingValveType"]

    def __unicode__(self):
        return u"{}: globalPumpControl({})".format(
            super(FloorTerminalBlock6, self).__unicode__(),
            self.globalPumpControl)


class PlugableSwitch(Device):
    """ HMIP-PS (Pluggable Switch) """

    on = None

    def from_json(self, js):
        super(PlugableSwitch, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SWITCH_CHANNEL":
                self.on = c["on"]

    def __unicode__(self):
        return u"{}: on({})".format(super(PlugableSwitch, self).__unicode__(),
                                    self.on)

    def set_switch_state(self, on=True):
        data = {"channelIndex": 1, "deviceId": self.id, "on": on}
        return self._restCall("device/control/setSwitchState",
                              body=json.dumps(data))

    def turn_on(self):
        return self.set_switch_state(True)

    def turn_off(self):
        return self.set_switch_state(False)


class PlugableSwitchMeasuring(PlugableSwitch):
    """ HMIP-PSM (Pluggable Switch and Meter) """
    energyCounter = None
    currentPowerConsumption = None

    def from_json(self, js):
        super(PlugableSwitchMeasuring, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SWITCH_MEASURING_CHANNEL":
                self.on = c["on"]
                self.energyCounter = c["energyCounter"]
                self.currentPowerConsumption = c["currentPowerConsumption"]

    def __unicode__(self):
        return u"{} energyCounter({}) currentPowerConsumption({}W)".format(
            super(PlugableSwitchMeasuring, self).__unicode__()
            , self.energyCounter, self.currentPowerConsumption)


class PushButton(Device):
    """ HMIP-WRC2 (Wall-mount Remote Control - 2-button) """


class AlarmSirenIndoor(SabotageDevice):
    """ HMIP-ASIR (Alarm Siren) """


class MotionDetectorIndoor(SabotageDevice):
    """ HMIP-SMI (Motion Detector with Brightness Sensor - indoor) """

    motionDetected = None
    illumination = None

    def from_json(self, js):
        super(MotionDetectorIndoor, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "MOTION_DETECTION_CHANNEL":
                self.motionDetected = c["motionDetected"]
                self.illumination = c["illumination"]

    def __unicode__(self):
        return u"{} motionDetected({}) illumination({})".format(
            super(MotionDetectorIndoor, self).__unicode__(),
            self.motionDetected, self.illumination)


class KeyRemoteControlAlarm(Device):
    """ HMIP-KRCA (Key Ring Remote Control - alarm) """

    def from_json(self, js):
        super(KeyRemoteControlAlarm, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "DEVICE_BASE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]

    def __unicode__(self):
        return u"{}".format(super(KeyRemoteControlAlarm, self).__unicode__())


class FullFlushShutter(Device):
    """ HMIP-FROLL (Shutter Actuator - flush-mount) """

    shutterLevel = None
    bottomToTopReferenceTime = None
    topToBottomReferenceTime = None

    def from_json(self, js):
        super(FullFlushShutter, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SHUTTER_CHANNEL":
                self.shutterLevel = c["shutterLevel"]
                self.bottomToTopReferenceTime = c["bottomToTopReferenceTime"]
                self.topToBottomReferenceTime = c["topToBottomReferenceTime"]

    def __unicode__(self):
        return u"{} shutterLevel({}) topToBottom({}) bottomToTop({})".format(
            super(FullFlushShutter, self).__unicode__(),
            self.shutterLevel, self.topToBottomReferenceTime,
            self.bottomToTopReferenceTime)

    def set_shutter_level(self, level):
        data = {"channelIndex": 1, "deviceId": self.id, "shutterLevel": level}
        return self._restCall("device/control/setShutterLevel",
                              body=json.dumps(data))

    def set_shutter_stop(self):
        data = {"channelIndex": 1, "deviceId": self.id}
        return self._restCall("device/control/stop", body=json.dumps(data))
