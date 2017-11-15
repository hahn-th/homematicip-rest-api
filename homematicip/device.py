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
    routerModuleSupported = False
    routerModuleEnabled = False
    modelType = ""
    modelId = 0
    oem = ""
    manufacturerCode = 0
    serializedGlobalTradeItemNumber = ""
    rssiDeviceValue = 0
    rssiPeerValue = 0

    def from_json(self, js):
        self.id = js["id"]
        self.homeId = js["homeId"]
        self.label = js["label"]
        time = js["lastStatusUpdate"]
        if time > 0:
            self.lastStatusUpdate = datetime.fromtimestamp(time / 1000.0)
        else:
            self.lastStatusUpdate = None

        self.deviceType = js["type"]
        self.updateState = js["updateState"]
        self.firmwareVersion = js["firmwareVersion"]
        self.availableFirmwareVersion = js["availableFirmwareVersion"]
        self.modelType = js['modelType']
        self.modelId = js['modelId']
        self.oem = js['oem']
        self.manufacturerCode = js['manufacturerCode']
        self.serializedGlobalTradeItemNumber = js['serializedGlobalTradeItemNumber']

        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "DEVICE_BASE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]
                self.routerModuleSupported = c["routerModuleSupported"]
                self.routerModuleEnabled = c["routerModuleEnabled"]
                self.rssiDeviceValue = c["rssiDeviceValue"]
                self.rssiPeerValue = c["rssiPeerValue"]
                break

    def __str__(self):
        return "{} {} lowbat({}) unreach({}) rssiDeviceValue({}) rssiPeerValue({})".format(self.modelType, self.label, self.lowBat, self.unreach, self.rssiDeviceValue, self.rssiPeerValue)

    def set_label(self, label):
        data = {"deviceId": self.id, "label": label}
        return self._restCall("device/setDeviceLabel", json.dumps(data))

    def is_update_applicable(self):
        data = {"deviceId": self.id}
        result = self._restCall("device/isUpdateApplicable", json.dumps(data))
        if result == "":
            return True
        else:
            return result["errorCode"]

    def authorizeUpdate(self):
        data = {"deviceId": self.id}
        return self._restCall("device/authorizeUpdate", json.dumps(data))

    def delete(self):
        data = {"deviceId": self.id}
        return self._restCall("device/deleteDevice", json.dumps(data))

    def set_router_module_enabled(self, enabled=True):
        if not self.routerModuleSupported:
            return False
        data = {"deviceId": self.id, "channelIndex": 0,
                "routerModuleEnabled": enabled}
        result = self._restCall("device/configuration/setRouterModuleEnabled", json.dumps(data))
        if result == "":
            return True
        else:
            return result["errorCode"]


class SabotageDevice(Device):
    sabotage = None

    def from_json(self, js):
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "DEVICE_SABOTAGE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]
                self.sabotage = c["sabotage"]
                self.rssiDeviceValue = c["rssiDeviceValue"]
                self.rssiPeerValue = c["rssiPeerValue"]
                break  # not needed to check the other channels

    def __str__(self):
        return "{}: sabotage({})".format(super().__str__(), self.sabotage)


class OperationLockableDevice(Device):
    operationLockActive = None

    def from_json(self, js):
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "DEVICE_OPERATIONLOCK":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]
                self.operationLockActive = c["operationLockActive"]
                self.rssiDeviceValue = c["rssiDeviceValue"]
                self.rssiPeerValue = c["rssiPeerValue"]
                break  # not needed to check the other channels

    def set_operation_lock(self, operationLock=True):
        data = {"channelIndex": 0, "deviceId": self.id,
                "operationLock": operationLock}
        return self._restCall("device/configuration/setOperationLock", json.dumps(data))

    def __str__(self):
        return "{}: operationLockActive({})".format(super().__str__(),
            self.operationLockActive)


class HeatingThermostat(OperationLockableDevice):
    """ HMIP-eTRV (Radiator Thermostat) """

    temperatureOffset = None
    valvePosition = None

    def from_json(self, js):
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "HEATING_THERMOSTAT_CHANNEL":
                self.temperatureOffset = c["temperatureOffset"]
                self.valvePosition = c["valvePosition"]

    def __str__(self):
        return "{} valvePosition({})".format(super().__str__(), self.valvePosition)


class ShutterContact(SabotageDevice):
    """ HMIP-SWDO (Door / Window Contact - optical) / HMIP-SWDO-I (Door / Window Contact Invisible - optical)"""
    windowState = None
    eventDelay = None

    def from_json(self, js):
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SHUTTER_CONTACT_CHANNEL":
                self.windowState = c["windowState"]
                self.eventDelay = c["eventDelay"]

    def __str__(self):
        return "{} windowState({})".format(super().__str__(), self.windowState)

class TemperatureHumiditySensorWithoutDisplay(Device):
    """ HMIP-STH (Temperature and Humidity Sensor without display - indoor) """

    temperatureOffset = None
    actualTemperature = None
    humidity = None

    def from_json(self, js):
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "WALL_MOUNTED_THERMOSTAT_WITHOUT_DISPLAY_CHANNEL":
                self.temperatureOffset = c["temperatureOffset"]
                self.actualTemperature = c["actualTemperature"]
                self.humidity = c["humidity"]

    def __str__(self):
        return u"{}: actualTemperature({}) humidity({})".format(
               super().__str__(), self.actualTemperature, self.humidity)
                                       
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
        super().from_json(js)
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
        return self._restCall("device/configuration/setClimateControlDisplay", json.dumps(data))

    def __str__(self):
        return "{}: actualTemperature({}) humidity({})".format(super().__str__(), self.actualTemperature, self.humidity)


class WallMountedThermostatPro(TemperatureHumiditySensorDisplay,
                               OperationLockableDevice):
    """ HMIP-WTH, HMIP-WTH-2 (Wall Thermostat with Humidity Sensor) / HMIP-BWTH (Brand Wall Thermostat with Humidity Sensor)"""

    def from_json(self, js):
        super().from_json(js)
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
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SMOKE_DETECTOR_CHANNEL":
                self.smokeDetectorAlarmType = c["smokeDetectorAlarmType"]

    def __str__(self):
        return "{}: smokeDetectorAlarmType({})".format(super().__str__(),
            self.smokeDetectorAlarmType)


class FloorTerminalBlock6(Device):
    """ HMIP-FAL230-C6 (Floor Heating Actuator - 6 channels, 230 V) """

    globalPumpControl = None
    heatingValveType = None

    def from_json(self, js):
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "DEVICE_GLOBAL_PUMP_CONTROL":
                self.unreach = c["unreach"]
                self.globalPumpControl = c["globalPumpControl"]
                self.heatingValveType = c["heatingValveType"]

    def __str__(self):
        return "{}: globalPumpControl({})".format(super().__str__(),
            self.globalPumpControl)


class PlugableSwitch(Device):
    """ HMIP-PS (Pluggable Switch) """

    on = None

    def from_json(self, js):
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SWITCH_CHANNEL":
                self.on = c["on"]

    def __str__(self):
        return "{}: on({})".format(super().__str__(),
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
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SWITCH_MEASURING_CHANNEL":
                self.on = c["on"]
                self.energyCounter = c["energyCounter"]
                self.currentPowerConsumption = c["currentPowerConsumption"]

    def __str__(self):
        return "{} energyCounter({}) currentPowerConsumption({}W)".format(super().__str__()
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
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "MOTION_DETECTION_CHANNEL":
                self.motionDetected = c["motionDetected"]
                self.illumination = c["illumination"]

    def __str__(self):
        return "{} motionDetected({}) illumination({})".format(super().__str__(),
            self.motionDetected, self.illumination)


class PresenceDetectorIndoor(SabotageDevice):
    """ HMIP-SPI (Presence Sensor - indoor) """

    presenceDetected = None
    illumination = None

    def from_json(self, js):
        super(PresenceDetectorIndoor, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "PRESENCE_DETECTION_CHANNEL":
                self.presenceDetected = c["presenceDetected"]
                self.illumination = c["illumination"]

    def __str__(self):
        return "{} motionDetected({}) illumination({})".format(super().__str__(),
            self.presenceDetected, self.illumination)

class KeyRemoteControlAlarm(Device):
    """ HMIP-KRCA (Key Ring Remote Control - alarm) """

    def from_json(self, js):
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "DEVICE_BASE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]

    def __str__(self):
        return "{}".format(super().__str__())


class FullFlushShutter(Device):
    """ HMIP-FROLL (Shutter Actuator - flush-mount) / HMIP-BROLL (Shutter Actuator - Brand-mount) """

    shutterLevel = None
    bottomToTopReferenceTime = None
    topToBottomReferenceTime = None

    def from_json(self, js):
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SHUTTER_CHANNEL":
                self.shutterLevel = c["shutterLevel"]
                self.bottomToTopReferenceTime = c["bottomToTopReferenceTime"]
                self.topToBottomReferenceTime = c["topToBottomReferenceTime"]

    def __str__(self):
        return "{} shutterLevel({}) topToBottom({}) bottomToTop({})".format(super().__str__(),
            self.shutterLevel, self.topToBottomReferenceTime,
            self.bottomToTopReferenceTime)

    def set_shutter_level(self, level):
        data = {"channelIndex": 1, "deviceId": self.id, "shutterLevel": level}
        return self._restCall("device/control/setShutterLevel",
                              body=json.dumps(data))

    def set_shutter_stop(self):
        data = {"channelIndex": 1, "deviceId": self.id}
        return self._restCall("device/control/stop", body=json.dumps(data))
