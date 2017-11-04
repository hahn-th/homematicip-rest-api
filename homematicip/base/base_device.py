from datetime import datetime

import logging

from homematicip.base.base_connection import BaseConnection
from homematicip.base.hmip_ip_object import HmipIpObject

_LOGGER = logging.getLogger(__name__)


class BaseDevice(HmipIpObject):
    _raw_data = None
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

    on_update = None

    def __init__(self, connection: BaseConnection):
        self.connection = connection

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
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "DEVICE_BASE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]
                self.routerModuleSupported = c["routerModuleSupported"]
                self.routerModuleEnabled = c["routerModuleEnabled"]
                break
        self.update()

    def set_label(self, label):
        raise NotImplementedError()

    def _set_label(self, label):
        data = {"deviceId": self.id, "label": label}
        return "device/setDeviceLabel", data

    def is_update_applicable(self):
        raise NotImplementedError()

    def _is_update_applicable(self):
        data = {"deviceId": self.id}
        return "device/isUpdateApplicable", data

    def authorizeUpdate(self):
        raise NotImplementedError()

    def _authorizeUpdate(self):
        data = {"deviceId": self.id}
        return "device/authorizeUpdate", data

    def delete(self):
        raise NotImplementedError()

    def _delete(self):
        data = {"deviceId": self.id}
        return "device/deleteDevice", data

    def set_router_module_enabled(self, enabled=True):
        raise NotImplementedError()

    def _set_router_module_enabled(self, enabled=True):
        data = {"deviceId": self.id, "channelIndex": 0,
                "routerModuleEnabled": enabled}
        return "device/configuration/setRouterModuleEnabled", data


class BaseSabotageDevice(BaseDevice):
    sabotage = None

    def from_json(self, js):
        super().from_json(js)
        for c in js["functionalChannels"].values():
            _type = c["functionalChannelType"]
            if _type == "DEVICE_SABOTAGE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]
                self.sabotage = c["sabotage"]
                break  # not needed to check the other channels

    def __repr__(self):
        return u"{}: sabotage({})".format(
            super().__repr__(), self.sabotage)


class BaseOperationLockableDevice(BaseDevice):
    operationLockActive = None

    def from_json(self, js):
        super().from_json(js)
        for c in js["functionalChannels"].values():
            type = c["functionalChannelType"]
            if type == "DEVICE_OPERATIONLOCK":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]
                self.operationLockActive = c["operationLockActive"]
                break  # not needed to check the other channels

    def _set_operation_lock(self, operation_lock=True):
        data = {"channelIndex": 0, "deviceId": self.id,
                "operationLock": operation_lock}
        return "device/configuration/setOperationLock", data

    def set_operation_lock(self, operation_lock=True):
        raise NotImplementedError()

    def __repr__(self):
        return "{}: operationLockActive({})".format(
            super().__repr__(),
            self.operationLockActive)


class BaseHeatingThermostat(BaseOperationLockableDevice):
    """ HMIP-eTRV (Radiator Thermostat) """

    temperatureOffset = None
    valvePosition = None

    def from_json(self, js):
        super().from_json(js)
        for c in js["functionalChannels"].values():
            _type = c["functionalChannelType"]
            if _type == "HEATING_THERMOSTAT_CHANNEL":
                self.temperatureOffset = c["temperatureOffset"]
                self.valvePosition = c["valvePosition"]

    def __repr__(self):
        return u"{} valvePosition({})".format(
            super().__repr__(), self.valvePosition)


class BaseShutterContact(BaseSabotageDevice):
    """ HMIP-SWDO (Door / Window Contact - optical) """

    windowState = None
    eventDelay = None

    def from_json(self, js):
        super().from_json(js)
        for c in js["functionalChannels"].values():
            type = c["functionalChannelType"]
            if type == "SHUTTER_CONTACT_CHANNEL":
                self.windowState = c["windowState"]
                self.eventDelay = c["eventDelay"]

    def __repr__(self):
        return u"{} windowState({})".format(
            super().__repr__(), self.windowState)


class BaseTemperatureHumiditySensorDisplay(BaseDevice):
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
        for c in js["functionalChannels"].values():
            type = c["functionalChannelType"]
            if type == "WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL":
                self.temperatureOffset = c["temperatureOffset"]
                self.display = c["display"]
                self.actualTemperature = c["actualTemperature"]
                self.humidity = c["humidity"]

    def _set_display(self, display=DISPLAY_ACTUAL):
        data = {"channelIndex": 1, "deviceId": self.id, "display": display}
        return "device/configuration/setClimateControlDisplay", data

    def set_display(self, display=DISPLAY_ACTUAL):
        raise NotImplementedError()

    def __repr__(self):
        return "{}: actualTemperature({}) humidity({})".format(
            super().__repr__(),
            self.actualTemperature, self.humidity)


class BaseWallMountedThermostatPro(BaseTemperatureHumiditySensorDisplay,
                                   BaseOperationLockableDevice):
    """ HMIP-WTH, HMIP-WTH-2 (Wall Thermostat with Humidity Sensor) """

    def from_json(self, js):
        super().from_json(js)
        for c in js["functionalChannels"].values():
            _type = c["functionalChannelType"]
            if _type == "WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL":
                self.temperatureOffset = c["temperatureOffset"]
                self.display = c["display"]
                self.actualTemperature = c["actualTemperature"]
                self.humidity = c["humidity"]


class BaseSmokeDetector(BaseDevice):
    """ HMIP-SWSD (Smoke Alarm with Q label) """

    smokeDetectorAlarmType = None

    def from_json(self, js):
        super().from_json(js)
        for c in js["functionalChannels"].values():
            type = c["functionalChannelType"]
            if type == "SMOKE_DETECTOR_CHANNEL":
                self.smokeDetectorAlarmType = c["smokeDetectorAlarmType"]

    def __repr__(self):
        return u"{}: smokeDetectorAlarmType({})".format(
            super().__repr__(),
            self.smokeDetectorAlarmType)


class BaseFloorTerminalBlock6(BaseDevice):
    """ HMIP-FAL230-C6 (Floor Heating Actuator - 6 channels, 230 V) """

    globalPumpControl = None
    heatingValveType = None

    def from_json(self, js):
        super().from_json(js)
        for c in js["functionalChannels"].values():
            type = c["functionalChannelType"]
            if type == "DEVICE_GLOBAL_PUMP_CONTROL":
                self.unreach = c["unreach"]
                self.globalPumpControl = c["globalPumpControl"]
                self.heatingValveType = c["heatingValveType"]

    def __repr__(self):
        return u"{}: globalPumpControl({})".format(
            super().__repr__(),
            self.globalPumpControl)


class BasePluggableSwitch(BaseDevice):
    on = None

    def from_json(self, js):
        super().from_json(js)
        for c in js["functionalChannels"].values():
            type = c["functionalChannelType"]
            if type == "SWITCH_CHANNEL":
                self.on = c["on"]

    def _set_switch_state(self, on=True):
        """Return set_switch_state data"""
        return "device/control/setSwitchState", {"channelIndex": 1,
                                                 "deviceId": self.id, "on": on}

    def _turn_on(self):
        """Switch the device on."""
        return self._set_switch_state(True)

    def turn_on(self):
        raise NotImplementedError()

    def _turn_off(self):
        """Switch the device off."""
        return self._set_switch_state(False)

    def turn_off(self):
        raise NotImplementedError()


class BasePluggableSwitchMeasuring(BasePluggableSwitch):
    """ HMIP-PSM (Pluggable Switch and Meter) """
    energyCounter = None
    currentPowerConsumption = None

    def from_json(self, js):
        super().from_json(js)
        for c in js["functionalChannels"].values():
            type = c["functionalChannelType"]
            if type == "SWITCH_MEASURING_CHANNEL":
                self.on = c["on"]
                self.energyCounter = c["energyCounter"]
                self.currentPowerConsumption = c["currentPowerConsumption"]

    def __repr__(self):
        return u"{} energyCounter({}) currentPowerConsumption({}W)".format(
            super().__repr__()
            , self.energyCounter, self.currentPowerConsumption)


class BasePushButton(BaseDevice):
    """ HMIP-WRC2 (Wall-mount Remote Control - 2-button) """


class BaseAlarmSirenIndoor(BaseSabotageDevice):
    """ HMIP-ASIR (Alarm Siren) """


class BaseMotionDetectorIndoor(BaseSabotageDevice):
    """ HMIP-SMI (Motion Detector with Brightness Sensor - indoor) """

    motionDetected = None
    illumination = None

    def from_json(self, js):
        super().from_json(js)
        for c in js["functionalChannels"].values():
            type = c["functionalChannelType"]
            if type == "MOTION_DETECTION_CHANNEL":
                self.motionDetected = c["motionDetected"]
                self.illumination = c["illumination"]

    def __repr__(self):
        return "{} motionDetected({}) illumination({})".format(
            super().__repr__(),
            self.motionDetected, self.illumination)


class BaseKeyRemoteControlAlarm(BaseDevice):
    """ HMIP-KRCA (Key Ring Remote Control - alarm) """

    def from_json(self, js):
        super().from_json(js)
        for c in js["functionalChannels"].values:
            type = c["functionalChannelType"]
            if type == "DEVICE_BASE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]

    def __repr__(self):
        return u"{}".format(super().__repr__())


class BaseFullFlushShutter(BaseDevice):
    """ HMIP-FROLL (Shutter Actuator - flush-mount) """

    shutterLevel = None
    bottomToTopReferenceTime = None
    topToBottomReferenceTime = None

    def from_json(self, js):
        super().from_json(js)
        for c in js["functionalChannels"].values():
            _type = c["functionalChannelType"]
            if _type == "SHUTTER_CHANNEL":
                self.shutterLevel = c["shutterLevel"]
                self.bottomToTopReferenceTime = c["bottomToTopReferenceTime"]
                self.topToBottomReferenceTime = c["topToBottomReferenceTime"]

    def __repr__(self):
        return u"{} shutterLevel({}) topToBottom({}) bottomToTop({})".format(
            super().__repr__(),
            self.shutterLevel, self.topToBottomReferenceTime,
            self.bottomToTopReferenceTime)

    def _set_shutter_level(self, level):
        data = {"channelIndex": 1, "deviceId": self.id, "shutterLevel": level}
        return "device/control/setShutterLevel", data

    def set_shutter_level(self, level):
        raise NotImplementedError()

    def _set_shutter_stop(self):
        data = {"channelIndex": 1, "deviceId": self.id}
        return "device/control/stop", data

    def set_shutter_stop(self):
        raise NotImplementedError()
