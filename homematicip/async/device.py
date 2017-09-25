import json

from datetime import datetime

import asyncio

from homematicip.async import HomeIPObject

ERROR_CODE = "errorCode"




class Device(HomeIPObject.HomeMaticIPobject):
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

    def __init__(self, connection):
        super().__init__(connection)

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

    @asyncio.coroutine
    def set_label(self, label):
        data = {"deviceId": self.id, "label": label}
        _val = yield from self._restCall("device/setDeviceLabel",
                                         json.dumps(data))
        return _val

    @asyncio.coroutine
    def is_update_applicable(self):
        data = {"deviceId": self.id}
        result = yield from self._restCall("device/isUpdateApplicable",
                                           json.dumps(data))
        if result == "":
            return True
        else:
            return result[ERROR_CODE]

    @asyncio.coroutine
    def authorizeUpdate(self):
        data = {"deviceId": self.id}
        _val = yield from self._restCall("device/authorizeUpdate",
                                         json.dumps(data))
        return _val

    @asyncio.coroutine
    def delete(self):
        data = {"deviceId": self.id}
        _val = yield from self._restCall("device/deleteDevice",
                                         json.dumps(data))
        return _val

    @asyncio.coroutine
    def set_router_module_enabled(self, enabled=True):
        if not self.routerModuleSupported:
            return False
        data = {"deviceId": self.id, "channelIndex": 0,
                "routerModuleEnabled": enabled}
        result = yield from self._restCall(
            "device/configuration/setRouterModuleEnabled",
            json.dumps(data))
        if result == "":
            return True
        else:
            return result[ERROR_CODE]

    def __repr__(self):
        return u"{} {} lowbat({}) unreach({})".format(self.deviceType,
                                                      self.label, self.lowBat,
                                                      self.unreach)


class SabotageDevice(Device):
    sabotage = None

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        super(SabotageDevice, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "DEVICE_SABOTAGE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]
                self.sabotage = c["sabotage"]
                break  # not needed to check the other channels

                # def __unicode__(self):
                #     return u"{}: sabotage({})".format(
                #         super(SabotageDevice, self).__unicode__(), self.sabotage)


class OperationLockableDevice(Device):
    operationLockActive = None

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        super(OperationLockableDevice, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "DEVICE_OPERATIONLOCK":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]
                self.operationLockActive = c["operationLockActive"]
                break  # not needed to check the other channels

    @asyncio.coroutine
    def set_operation_lock(self, operationLock=True):
        data = {"channelIndex": 0, "deviceId": self.id,
                "operationLock": operationLock}
        _val = yield from self._restCall(
            "device/configuration/setOperationLock", json.dumps(data))
        return _val


        # def __unicode__(self):
        #     return u"{}: operationLockActive({})".format(
        #         super(OperationLockableDevice, self).__unicode__(),
        #         self.operationLockActive)


class HeatingThermostat(OperationLockableDevice):
    """ HMIP-eTRV (Radiator Thermostat) """

    temperatureOffset = None
    valvePosition = None

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "HEATING_THERMOSTAT_CHANNEL":
                self.temperatureOffset = c["temperatureOffset"]
                self.valvePosition = c["valvePosition"]

                # def __unicode__(self):
                #     return u"{} valvePosition({})".format(
                #         super(HeatingThermostat, self).__unicode__(), self.valvePosition)


class ShutterContact(SabotageDevice):
    """ HMIP-SWDO (Door / Window Contact - optical) """
    windowState = None
    eventDelay = None

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SHUTTER_CONTACT_CHANNEL":
                self.windowState = c["windowState"]
                self.eventDelay = c["eventDelay"]

                # def __unicode__(self):
                #     return u"{} windowState({})".format(
                #         super(ShutterContact, self).__unicode__(), self.windowState)


class TemperatureHumiditySensorDisplay(Device):
    """ HMIP-STHD (Temperature and Humidity Sensor with display - indoor) """

    DISPLAY_ACTUAL = "ACTUAL"
    DISPLAY_SETPOINT = "SETPOINT"
    DISPLAY_ACTUAL_HUMIDITY = "ACTUAL_HUMIDITY"

    temperatureOffset = None
    display = None
    actualTemperature = None
    humidity = None

    def __init__(self, connection):
        super().__init__(connection)

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

    @asyncio.coroutine
    def set_display(self, display=DISPLAY_ACTUAL):
        data = {"channelIndex": 1, "deviceId": self.id, "display": display}
        _val = yield from self._restCall(
            "device/configuration/setClimateControlDisplay",
            json.dumps(data))
        return _val


        # def __unicode__(self):
        #     return u"{}: actualTemperature({}) humidity({})".format(
        #         super(TemperatureHumiditySensorDisplay, self).__unicode__(),
        #         self.actualTemperature, self.humidity)


class WallMountedThermostatPro(TemperatureHumiditySensorDisplay,
                               OperationLockableDevice):
    """ HMIP-WTH, HMIP-WTH-2 (Wall Thermostat with Humidity Sensor) """

    def __init__(self, connection):
        super().__init__(connection)

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

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        super(SmokeDetector, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SMOKE_DETECTOR_CHANNEL":
                self.smokeDetectorAlarmType = c["smokeDetectorAlarmType"]

                # def __unicode__(self):
                #     return u"{}: smokeDetectorAlarmType({})".format(
                #         super(SmokeDetector, self).__unicode__(),
                #         self.smokeDetectorAlarmType)


class FloorTerminalBlock6(Device):
    """ HMIP-FAL230-C6 (Floor Heating Actuator - 6 channels, 230 V) """

    globalPumpControl = None
    heatingValveType = None

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        super(FloorTerminalBlock6, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "DEVICE_GLOBAL_PUMP_CONTROL":
                self.unreach = c["unreach"]
                self.globalPumpControl = c["globalPumpControl"]
                self.heatingValveType = c["heatingValveType"]

                # def __unicode__(self):
                #     return u"{}: globalPumpControl({})".format(
                #         super(FloorTerminalBlock6, self).__unicode__(),
                #         self.globalPumpControl)


class PlugableSwitch(Device):
    """ HMIP-PS (Pluggable Switch) """

    on = None

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        super(PlugableSwitch, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SWITCH_CHANNEL":
                self.on = c["on"]

    def __repr__(self):
        return u"{}: on({})".format(super().__repr__(),
                                    self.on)

    @asyncio.coroutine
    def set_switch_state(self, on=True):
        data = {"channelIndex": 1, "deviceId": self.id, "on": on}
        _val = yield from self._restCall("device/control/setSwitchState",
                                         body=json.dumps(data))
        return _val

    @asyncio.coroutine
    def turn_on(self):
        _val = yield from self.set_switch_state(True)
        return _val

    @asyncio.coroutine
    def turn_off(self):
        _val = yield from self.set_switch_state(False)
        return _val


class PlugableSwitchMeasuring(PlugableSwitch):
    """ HMIP-PSM (Pluggable Switch and Meter) """
    energyCounter = None
    currentPowerConsumption = None

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SWITCH_MEASURING_CHANNEL":
                self.on = c["on"]
                self.energyCounter = c["energyCounter"]
                self.currentPowerConsumption = c["currentPowerConsumption"]

    def __repr__(self):
        return u"{} energyCounter({}) currentPowerConsumption({}W)".format(
            super().__repr__()
            , self.energyCounter, self.currentPowerConsumption)


class PushButton(Device):
    """ HMIP-WRC2 (Wall-mount Remote Control - 2-button) """


class AlarmSirenIndoor(SabotageDevice):
    """ HMIP-ASIR (Alarm Siren) """


class MotionDetectorIndoor(SabotageDevice):
    """ HMIP-SMI (Motion Detector with Brightness Sensor - indoor) """

    motionDetected = None
    illumination = None

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        super(MotionDetectorIndoor, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "MOTION_DETECTION_CHANNEL":
                self.motionDetected = c["motionDetected"]
                self.illumination = c["illumination"]

                # def __unicode__(self):
                #     return u"{} motionDetected({}) illumination({})".format(
                #         super(MotionDetectorIndoor, self).__unicode__(),
                #         self.motionDetected, self.illumination)


class KeyRemoteControlAlarm(Device):
    """ HMIP-KRCA (Key Ring Remote Control - alarm) """

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        super(KeyRemoteControlAlarm, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "DEVICE_BASE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]

                # def __unicode__(self):
                #     return u"{}".format(super(KeyRemoteControlAlarm, self).__unicode__())


class FullFlushShutter(Device):
    """ HMIP-FROLL (Shutter Actuator - flush-mount) """

    shutterLevel = None
    bottomToTopReferenceTime = None
    topToBottomReferenceTime = None

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        super(FullFlushShutter, self).from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SHUTTER_CHANNEL":
                self.shutterLevel = c["shutterLevel"]
                self.bottomToTopReferenceTime = c["bottomToTopReferenceTime"]
                self.topToBottomReferenceTime = c["topToBottomReferenceTime"]

    # def __unicode__(self):
    #     return u"{} shutterLevel({}) topToBottom({}) bottomToTop({})".format(
    #         super(FullFlushShutter, self).__unicode__(),
    #         self.shutterLevel, self.topToBottomReferenceTime,
    #         self.bottomToTopReferenceTime)

    @asyncio.coroutine
    def set_shutter_level(self, level):
        data = {"channelIndex": 1, "deviceId": self.id, "shutterLevel": level}
        _val = yield from self._restCall("device/control/setShutterLevel",
                                         body=json.dumps(data))
        return _val

    @asyncio.coroutine
    def set_shutter_stop(self):
        data = {"channelIndex": 1, "deviceId": self.id}
        _val = yield from self._restCall("device/control/stop",
                                         body=json.dumps(data))
        return _val
