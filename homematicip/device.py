# coding=utf-8
from homematicip import HomeMaticIPObject
import json
from datetime import datetime


class Device(HomeMaticIPObject.HomeMaticIPObject):
    """ this class represents a generic homematic ip device """
    id = None
    homeId = None
    label = None
    lastStatusUpdate = None
    deviceType = None
    updateState = None
    firmwareVersion = None
    availableFirmwareVersion = None
    unreach = None
    lowBat = None

    def from_json(self, js):
        self.id = js["id"]
        self.homeId = js["homeId"]
        self.label = js["label"]
        self.lastStatusUpdate = datetime.fromtimestamp(js["lastStatusUpdate"] / 1000.0)
        self.deviceType = js["type"]
        self.updateState = js["updateState"]
        self.firmwareVersion = js["firmwareVersion"]
        self.availableFirmwareVersion = js["availableFirmwareVersion"]

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"{} {}".format(self.deviceType, self.label)

    def set_label(self, label):
        data = { "deviceId" : self.id, "label" : label }
        return self._restCall("home/setDeviceLabel", json.dumps(data))

    def is_update_applicable(self):
        data = { "deviceId" : self.id }
        result = self._restCall("device/isUpdateApplicable", json.dumps(data))
        if result == "":
            return True
        else:
            return result["errorCode"]

    def authorizeUpdate(self):
        data = { "deviceId" : self.id }
        return self._restCall("device/authorizeUpdate", json.dumps(data))
    

class HeatingThermostat(Device):
    """ HMIP-eTRV (Radiator Thermostat) """

    temperatureOffset = None
    operationLockActive = None
    valvePosition = None

    def from_json(self, js):
        super(HeatingThermostat, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "HEATING_THERMOSTAT_CHANNEL":
                self.temperatureOffset = c["temperatureOffset"]
                self.valvePosition = c["valvePosition"]
            elif type == "DEVICE_OPERATIONLOCK":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]
                self.operationLockActive = c["operationLockActive"]

    def __unicode__(self):
        return u"{}: valvePosition({})".format(super(HeatingThermostat, self).__unicode__(), self.valvePosition)


class ShutterContact(Device):
    """ HMIP-SWDO (Door / Window Contact - optical) """

    sabotage = None
    open = None
    eventDelay = None

    def from_json(self, js):
        super(ShutterContact, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SHUTTER_CONTACT_CHANNEL":
                self.open = c["open"]
                self.eventDelay = c["eventDelay"]
            elif type == "DEVICE_SABOTAGE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]
                self.sabotage = c["sabotage"]

    def __unicode__(self):
        return u"{}: open({}) sabotage ({})".format(super(ShutterContact, self).__unicode__(), self.open, self.sabotage)


class WallMountedThermostatPro(Device):
    """ HMIP-WTH, HMIP-WTH-2 (Wall Thermostat with Humidity Sensor) """

    DISPLAY_ACTUAL = "ACTUAL"
    DISPLAY_SETPOINT = "SETPOINT"
    DISPLAY_ACTUAL_HUMIDITY = "ACTUAL_HUMIDITY"

    temperatureOffset = None
    display = None
    operationLockActive = None
    actualTemperature = None
    humidity = None

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

            elif type == "DEVICE_OPERATIONLOCK":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]
                self.operationLockActive = c["operationLockActive"]

    def set_display(self, display=DISPLAY_ACTUAL):
        data = {"channelIndex": 1, "deviceId": self.id, "display": display}
        return self._restCall("device/configuration/setClimateControlDisplay", json.dumps(data))

    def __unicode__(self):
        return u"{}: actualTemperature({}) humidity({})".format(super(WallMountedThermostatPro, self).__unicode__(),
                                                                self.actualTemperature, self.humidity)

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

            elif type == "DEVICE_BASE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]

    def set_display(self, display=DISPLAY_ACTUAL):
        data = {"channelIndex": 1, "deviceId": self.id, "display": display}
        return self._restCall("device/configuration/setClimateControlDisplay", json.dumps(data))

    def __unicode__(self):
        return u"{}: actualTemperature({}) humidity({})".format(super(TemperatureHumiditySensorDisplay, self).__unicode__(),
                                                                self.actualTemperature, self.humidity)

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
            elif type == "DEVICE_BASE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]

    def __unicode__(self):
        return u"{}: smokeDetectorAlarmType({})".format(super(SmokeDetector, self).__unicode__(),
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
        return u"{}: globalPumpControl({})".format(super(FloorTerminalBlock6, self).__unicode__(),
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
            elif type == "DEVICE_BASE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]

    def __unicode__(self):
        return u"{}: on({})".format(super(PlugableSwitch, self).__unicode__(), self.on)

    def set_switch_state(self, on=True):
        data = { "channelIndex": 1, "deviceId":self.id, "on":on }
        return self._restCall("device/control/setSwitchState", body=json.dumps(data))
    
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
        return u"{} energyCounter({}) currentPowerConsumption({}W)".format(super(PlugableSwitchMeasuring, self).__unicode__()
                                                                                   , self.energyCounter,self.currentPowerConsumption)


class PushButton(Device):
    """ HMIP-WRC2 (Wall-mount Remote Control - 2-button) """

    def from_json(self, js):
        super(PushButton, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "DEVICE_BASE":              
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]

    def __unicode__(self):
        return u"{}".format(super(PushButton, self).__unicode__())


class AlarmSirenIndoor(Device):
    """ HMIP-ASIR (Alarm Siren) """

    sabotage = None

    def from_json(self, js):
        super(AlarmSirenIndoor, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]            
            if type == "DEVICE_SABOTAGE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]
                self.sabotage = c["sabotage"]

    def __unicode__(self):
        return u"{}: sabotage ({})".format(super(AlarmSirenIndoor, self).__unicode__(), self.sabotage)

class MotionDetectorIndoor(Device):
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
            elif type == "DEVICE_SABOTAGE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]
                self.sabotage = c["sabotage"]

    def __unicode__(self):
        return u"{}: sabotage({}) motionDetected({}) illumination({})".format(super(MotionDetectorIndoor, self).__unicode__(),
                                                                              self.sabotage, self.motionDetected, self.illumination)

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