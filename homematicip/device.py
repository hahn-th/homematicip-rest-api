# coding=utf-8
import json
from datetime import datetime
import logging

from homematicip.base.helpers import get_functional_channel
from homematicip.base.enums import *
from homematicip import HomeMaticIPObject

LOGGER = logging.getLogger(__name__)

class Device(HomeMaticIPObject.HomeMaticIPObject):
    """ this class represents a generic homematic ip device """
    def __init__(self,connection):
        super().__init__(connection)
        self.id = None
        self.homeId = None
        self.label = None
        self.lastStatusUpdate = None
        self.deviceType = None
        self.updateState = None
        self.firmwareVersion = None
        self.availableFirmwareVersion = None
        self.unreach = None
        self.lowBat = None
        self.routerModuleSupported = False
        self.routerModuleEnabled = False
        self.modelType = ""
        self.modelId = 0
        self.oem = ""
        self.manufacturerCode = 0
        self.serializedGlobalTradeItemNumber = ""
        self.rssiDeviceValue = 0
        self.rssiPeerValue = 0
        self.dutyCycle = False
        self.configPending = False

    def from_json(self, js):
        super().from_json(js)
        self.id = js["id"]
        self.homeId = js["homeId"]
        self.label = js["label"]

        self.lastStatusUpdate = self.fromtimestamp(js["lastStatusUpdate"])

        self.deviceType = js["type"]
        self.updateState = js["updateState"]
        self.firmwareVersion = js["firmwareVersion"]
        self.availableFirmwareVersion = js["availableFirmwareVersion"]
        self.modelType = js['modelType']
        self.modelId = js['modelId']
        self.oem = js['oem']
        self.manufacturerCode = js['manufacturerCode']
        self.serializedGlobalTradeItemNumber = js['serializedGlobalTradeItemNumber']

        c = get_functional_channel("DEVICE_BASE", js)
        if c:
            self.unreach = c["unreach"]
            self.lowBat = c["lowBat"]
            self.routerModuleSupported = c["routerModuleSupported"]
            self.routerModuleEnabled = c["routerModuleEnabled"]
            self.rssiDeviceValue = c["rssiDeviceValue"]
            self.rssiPeerValue = c["rssiPeerValue"]
            self.dutyCycle = c["dutyCycle"]
            self.configPending = c["configPending"]

    def __str__(self):
        return "{} {} lowbat({}) unreach({}) rssiDeviceValue({}) rssiPeerValue({}) configPending({}) dutyCycle({})".format(self.modelType, self.label, self.lowBat, self.unreach, self.rssiDeviceValue,
            self.rssiPeerValue, self.configPending, self.dutyCycle)

    def set_label(self, label):
        data = {"deviceId": self.id, "label": label}
        return self._restCall("device/setDeviceLabel", json.dumps(data))

    def is_update_applicable(self):
        data = {"deviceId": self.id}
        return self._restCall("device/isUpdateApplicable", json.dumps(data))

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
        return self._restCall("device/configuration/setRouterModuleEnabled", json.dumps(data))


class SabotageDevice(Device):
    def __init__(self,connection):
        super().__init__(connection)
        self.sabotage = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DEVICE_SABOTAGE", js)
        if c:
            self.unreach = c["unreach"]
            self.lowBat = c["lowBat"]
            self.sabotage = c["sabotage"]
            self.rssiDeviceValue = c["rssiDeviceValue"]
            self.rssiPeerValue = c["rssiPeerValue"]
            self.dutyCycle = c["dutyCycle"]
            self.configPending = c["configPending"]

    def __str__(self):
        return "{}: sabotage({})".format(super().__str__(), self.sabotage)


class OperationLockableDevice(Device):
    def __init__(self,connection):
        super().__init__(connection)
        self.operationLockActive = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DEVICE_OPERATIONLOCK", js)
        if c:
            self.unreach = c["unreach"]
            self.lowBat = c["lowBat"]
            self.operationLockActive = c["operationLockActive"]
            self.rssiDeviceValue = c["rssiDeviceValue"]
            self.rssiPeerValue = c["rssiPeerValue"]
            self.dutyCycle = c["dutyCycle"]
            self.configPending = c["configPending"]

    def set_operation_lock(self, operationLock=True):
        data = {"channelIndex": 0, "deviceId": self.id, "operationLock": operationLock}
        return self._restCall("device/configuration/setOperationLock", json.dumps(data))

    def __str__(self):
        return "{}: operationLockActive({})".format(super().__str__(),
                                                    self.operationLockActive)


class HeatingThermostat(OperationLockableDevice):
    """ HMIP-eTRV (Radiator Thermostat) """

    def __init__(self,connection):
        super().__init__(connection)
        self.temperatureOffset = 0
        self.valvePosition = 0.0
        self.valveState = ValveState.ERROR_POSITION
        self.setPointTemperature = 0.0
        self.automaticValveAdaptionNeeded = False

    def from_json(self, js):
        super().from_json(js)
        automaticValveAdaptionNeeded = js["automaticValveAdaptionNeeded"]
        c = get_functional_channel("HEATING_THERMOSTAT_CHANNEL", js)
        if c:
            self.temperatureOffset = c["temperatureOffset"]
            self.valvePosition = c["valvePosition"]
            self.valveState = ValveState.from_str(c["valveState"])
            self.setPointTemperature = c["setPointTemperature"]

    def __str__(self):
        return "{} valvePosition({}) valveState({}) temperatureOffset({}) setPointTemperature({})".format(super().__str__(), self.valvePosition,
                                                                                                                             self.valveState,
                                                                                                                             self.temperatureOffset,
                                                                                                                             self.setPointTemperature)


class ShutterContact(SabotageDevice):
    """ HMIP-SWDO (Door / Window Contact - optical) / HMIP-SWDO-I (Door / Window Contact Invisible - optical)"""
    def __init__(self,connection):
        super().__init__(connection)
        self.windowState = WindowState.CLOSED
        self.eventDelay = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("SHUTTER_CONTACT_CHANNEL", js)
        if c:
            self.windowState = WindowState.from_str(c["windowState"])
            self.eventDelay = c["eventDelay"]

    def __str__(self):
        return "{} windowState({})".format(super().__str__(), self.windowState)

class RotaryHandleSensor(SabotageDevice):
    """ HmIP-SRH """
    def __init__(self,connection):
        super().__init__(connection)
        self.windowState = WindowState.CLOSED
        self.eventDelay = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("ROTARY_HANDLE_CHANNEL", js)
        if c:
            self.windowState = WindowState.from_str(c["windowState"])
            self.eventDelay = c["eventDelay"]

    def __str__(self):
        return "{} windowState({})".format(super().__str__(), self.windowState)

class TemperatureHumiditySensorOutdoor(Device):
    """ HmIP-STHO (Temperature and Humidity Sensor outdoor) """

    def __init__(self,connection):
        super().__init__(connection)
        self.actualTemperature = None
        self.humidity = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("CLIMATE_SENSOR_CHANNEL", js)
        if c:
            self.actualTemperature = c["actualTemperature"]
            self.humidity = c["humidity"]

    def __str__(self):
        return u"{}: actualTemperature({}) humidity({})".format(super().__str__(), self.actualTemperature, self.humidity)

class TemperatureHumiditySensorWithoutDisplay(Device):
    """ HMIP-STH (Temperature and Humidity Sensor without display - indoor) """

    def __init__(self,connection):
        super().__init__(connection)
        self.temperatureOffset = None
        self.actualTemperature = None
        self.humidity = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("WALL_MOUNTED_THERMOSTAT_WITHOUT_DISPLAY_CHANNEL", js)
        if c:
            self.temperatureOffset = c["temperatureOffset"]
            self.actualTemperature = c["actualTemperature"]
            self.humidity = c["humidity"]

    def __str__(self):
        return u"{}: actualTemperature({}) humidity({})".format(super().__str__(), self.actualTemperature, self.humidity)


class TemperatureHumiditySensorDisplay(Device):
    """ HMIP-STHD (Temperature and Humidity Sensor with display - indoor) """

    def __init__(self,connection):
        super().__init__(connection)
        self.temperatureOffset = None
        self.display = ClimateControlDisplay.ACTUAL
        self.actualTemperature = None
        self.humidity = None
        self.setPointTemperature = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL", js)
        if c:
            self.temperatureOffset = c["temperatureOffset"]
            self.display = ClimateControlDisplay.from_str(c["display"])
            self.actualTemperature = c["actualTemperature"]
            self.humidity = c["humidity"]
            self.setPointTemperature = c["setPointTemperature"]

    def set_display(self, display : ClimateControlDisplay = ClimateControlDisplay.ACTUAL):
        data = {"channelIndex": 1, "deviceId": self.id, "display": str(display)}
        return self._restCall("device/configuration/setClimateControlDisplay", json.dumps(data))

    def __str__(self):
        return "{}: actualTemperature({}) humidity({}) setPointTemperature({})".format(super().__str__(),
                                                                                self.actualTemperature,
                                                                                self.humidity,
                                                                                self.setPointTemperature)


class WallMountedThermostatPro(TemperatureHumiditySensorDisplay,
                               OperationLockableDevice):
    """ HMIP-WTH, HMIP-WTH-2 (Wall Thermostat with Humidity Sensor) / HMIP-BWTH (Brand Wall Thermostat with Humidity Sensor)"""

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL", js)
        if c:
            self.temperatureOffset = c["temperatureOffset"]
            self.display = ClimateControlDisplay.from_str(c["display"])
            self.actualTemperature = c["actualTemperature"]
            self.humidity = c["humidity"]
            self.setPointTemperature = c["setPointTemperature"]

class SmokeDetector(Device):
    """ HMIP-SWSD (Smoke Alarm with Q label) """

    def __init__(self,connection):
        super().__init__(connection)
        self.smokeDetectorAlarmType = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("SMOKE_DETECTOR_CHANNEL", js)
        if c:
            self.smokeDetectorAlarmType = c["smokeDetectorAlarmType"]

    def __str__(self):
        return "{}: smokeDetectorAlarmType({})".format(super().__str__(),
                                                       self.smokeDetectorAlarmType)


class FloorTerminalBlock6(Device):
    """ HMIP-FAL230-C6 (Floor Heating Actuator - 6 channels, 230 V) """


    def __init__(self,connection):
        super().__init__(connection)
        self.globalPumpControl = None
        self.heatingValveType = HeatingValveType.NORMALLY_CLOSE

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DEVICE_GLOBAL_PUMP_CONTROL", js)
        if c:
            self.unreach = c["unreach"]
            self.globalPumpControl = c["globalPumpControl"]
            self.heatingValveType = HeatingValveType.from_str(c["heatingValveType"])

    def __str__(self):
        return "{}: globalPumpControl({})".format(super().__str__(),
                                                  self.globalPumpControl)


class Switch(Device):
    """ Generic Switch class """


    def __init__(self,connection):
        super().__init__(connection)
        self.on = None
        self.profileMode = None
        self.userDesiredProfileMode = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("SWITCH_CHANNEL", js)
        if c:
            self.on = c["on"]
            self.profileMode = c["profileMode"]
            self.userDesiredProfileMode = c["userDesiredProfileMode"]

    def __str__(self):
        return "{}: on({}) profileMode({}) userDesiredProfileMode({})".format(super().__str__(), self.on, self.profileMode, self.userDesiredProfileMode)

    def set_switch_state(self, on=True):
        data = {"channelIndex": 1, "deviceId": self.id, "on": on}
        return self._restCall("device/control/setSwitchState",
                              body=json.dumps(data))

    def turn_on(self):
        return self.set_switch_state(True)

    def turn_off(self):
        return self.set_switch_state(False)

class PlugableSwitch(Switch):
    """ HMIP-PS (Pluggable Switch) """

class PrintedCircuitBoardSwitchBattery(Switch):
    """ HmIP-PCBS-BAT (Printed Curcuit Board Switch Battery) """

class SwitchMeasuring(Switch):
    """ Generic class for Switch and Meter """

    def __init__(self,connection):
        super().__init__(connection)
        self.energyCounter = None
        self.currentPowerConsumption = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("SWITCH_MEASURING_CHANNEL", js)
        if c:
            self.on = c["on"]
            self.energyCounter = c["energyCounter"]
            self.currentPowerConsumption = c["currentPowerConsumption"]
            self.profileMode = c["profileMode"]
            self.userDesiredProfileMode = c["userDesiredProfileMode"]

    def __str__(self):
        return "{} energyCounter({}) currentPowerConsumption({}W)".format(super().__str__(), self.energyCounter, self.currentPowerConsumption)

class PlugableSwitchMeasuring(SwitchMeasuring):
    """ HMIP-PSM (Pluggable Switch and Meter) """

class BrandSwitchMeasuring(SwitchMeasuring):
    """ HMIP-BSM (Brand Switch and Meter) """


class FullFlushSwitchMeasuring(SwitchMeasuring):
    """ HmIP-FSM (Full flush Switch and Meter) """

class PushButton(Device):
    """ HMIP-WRC2 (Wall-mount Remote Control - 2-button) """


class AlarmSirenIndoor(SabotageDevice):
    """ HMIP-ASIR (Alarm Siren) """


class MotionDetectorIndoor(SabotageDevice):
    """ HMIP-SMI (Motion Detector with Brightness Sensor - indoor) """


    def __init__(self,connection):
        super().__init__(connection)
        self.motionDetected = None
        self.illumination = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("MOTION_DETECTION_CHANNEL", js)
        if c:
            self.motionDetected = c["motionDetected"]
            self.illumination = c["illumination"]

    def __str__(self):
        return "{} motionDetected({}) illumination({})".format(super().__str__(),
                                                               self.motionDetected,
                                                               self.illumination)


class MotionDetectorPushButton(MotionDetectorIndoor):
    """ HMIP-SMI55 (Motion Detector with Brightness Sensor and Remote Control - 2-button) """


class PresenceDetectorIndoor(SabotageDevice):
    """ HMIP-SPI (Presence Sensor - indoor) """


    def __init__(self,connection):
        super().__init__(connection)
        self.presenceDetected = None
        self.illumination = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("PRESENCE_DETECTION_CHANNEL", js)
        if c:
            self.presenceDetected = c["presenceDetected"]
            self.illumination = c["illumination"]

    def __str__(self):
        return "{} motionDetected({}) illumination({})".format(super().__str__(),
                                                               self.presenceDetected,
                                                               self.illumination)


class KeyRemoteControlAlarm(Device):
    """ HMIP-KRCA (Key Ring Remote Control - alarm) """

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DEVICE_BASE", js)
        if c:
            self.unreach = c["unreach"]
            self.lowBat = c["lowBat"]

    def __str__(self):
        return "{}".format(super().__str__())


class FullFlushShutter(Device):
    """HMIP-FROLL (Shutter Actuator - flush-mount) / HMIP-BROLL (Shutter Actuator - Brand-mount)"""


    def __init__(self,connection):
        super().__init__(connection)
        self.shutterLevel = None
        self.bottomToTopReferenceTime = None
        self.topToBottomReferenceTime = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("SHUTTER_CHANNEL", js)
        if c:
            self.shutterLevel = c["shutterLevel"]
            self.bottomToTopReferenceTime = c["bottomToTopReferenceTime"]
            self.topToBottomReferenceTime = c["topToBottomReferenceTime"]

    def __str__(self):
        return "{} shutterLevel({}) topToBottom({}) bottomToTop({})".format(super().__str__(), self.shutterLevel, self.topToBottomReferenceTime,
            self.bottomToTopReferenceTime)

    def set_shutter_level(self, level):
        data = {"channelIndex": 1, "deviceId": self.id, "shutterLevel": level}
        return self._restCall("device/control/setShutterLevel", body=json.dumps(data))

    def set_shutter_stop(self):
        data = {"channelIndex": 1, "deviceId": self.id}
        return self._restCall("device/control/stop", body=json.dumps(data))


class Dimmer(Device):
    """Base dimmer device class"""

    def __init__(self,connection):
        super().__init__(connection)
        self.dimLevel = 0.0
        self.profileMode = ""
        self.userDesiredProfileMode = ""

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DIMMER_CHANNEL", js)
        if c:
            self.dimLevel = c["dimLevel"]
            self.profileMode = c["profileMode"]
            self.userDesiredProfileMode = c["userDesiredProfileMode"]

    def __str__(self):
        return "{} dimLevel({}) profileMode({}) userDesiredProfileMode({})".format(super().__str__(), self.dimLevel, self.profileMode, self.userDesiredProfileMode)

    def set_dim_level(self, dimLevel=0.0):
        data = {"channelIndex": 1, "deviceId": self.id, "dimLevel": dimLevel}
        return self._restCall("device/control/setDimLevel", json.dumps(data))

class PluggableDimmer(Dimmer):
    """HmIP-PDT Pluggable Dimmer"""

class BrandDimmer(Dimmer):
    """HmIP-BDT Brand Dimmer"""


class WeatherSensor(Device):
    """ HmIP-SWO-B """
    def __init__(self,connection):
        super().__init__(connection)
        self.actualTemperature = 0
        self.humidity = 0
        self.illumination = 0
        self.illuminationThresholdSunshine = 0
        self.storm = False
        self.sunshine = False
        self.todaySunshineDuration = 0
        self.totalSunshineDuration = 0
        self.windSpeed = 0
        self.windValueType = "AVERAGE_VALUE"
        self.yesterdaySunshineDuration = 0

    def from_json(self, js):
        super().from_json(js)

        c = get_functional_channel("WEATHER_SENSOR_CHANNEL", js)
        if c:
            self.actualTemperature = c["actualTemperature"]
            self.humidity = c["humidity"]
            self.illumination = c["illumination"]
            self.illuminationThresholdSunshine = c["illuminationThresholdSunshine"]
            self.storm = c["storm"]
            self.sunshine = c["sunshine"]
            self.todaySunshineDuration = c["todaySunshineDuration"]
            self.totalSunshineDuration = c["totalSunshineDuration"]
            self.windSpeed = c["windSpeed"]
            self.windValueType = c["windValueType"]
            self.yesterdaySunshineDuration = c["yesterdaySunshineDuration"]

    def __str__(self):
        return ("{} actualTemperature({}) humidity({}) illumination({}) illuminationThresholdSunshine({}) storm({}) sunshine({}) "
                "todaySunshineDuration({}) totalSunshineDuration({}) "
                "windSpeed({}) windValueType({}) "
                "yesterdaySunshineDuration({})").format(super().__str__(), self.actualTemperature,
                                                                            self.humidity,
                                                                            self.illumination,
                                                                            self.illuminationThresholdSunshine,
                                                                            self.storm,
                                                                            self.sunshine,
                                                                            self.todaySunshineDuration,
                                                                            self.totalSunshineDuration,
                                                                            self.windSpeed,
                                                                            self.windValueType,
                                                                            self.yesterdaySunshineDuration)


class WeatherSensorPro(Device):
    """ HmIP-SWO-PR """
    def __init__(self,connection):
        super().__init__(connection)
        self.actualTemperature = 0
        self.humidity = 0
        self.illumination = 0
        self.illuminationThresholdSunshine = 0
        self.raining = False
        self.storm = False
        self.sunshine = False
        self.todayRainCounter = 0
        self.todaySunshineDuration = 0
        self.totalRainCounter = 0
        self.totalSunshineDuration = 0
        self.weathervaneAlignmentNeeded = False
        self.windDirection = 0
        self.windDirectionVariation = 0
        self.windSpeed = 0
        self.windValueType = "AVERAGE_VALUE"
        self.yesterdayRainCounter = 0
        self.yesterdaySunshineDuration = 0

    def from_json(self, js):
        super().from_json(js)

        c = get_functional_channel("WEATHER_SENSOR_PRO_CHANNEL", js)
        if c:
            self.actualTemperature = c["actualTemperature"]
            self.humidity = c["humidity"]
            self.illumination = c["illumination"]
            self.illuminationThresholdSunshine = c["illuminationThresholdSunshine"]
            self.raining = c["raining"]
            self.storm = c["storm"]
            self.sunshine = c["sunshine"]
            self.todayRainCounter = c["todayRainCounter"]
            self.todaySunshineDuration = c["todaySunshineDuration"]
            self.totalRainCounter = c["totalRainCounter"]
            self.totalSunshineDuration = c["totalSunshineDuration"]
            self.weathervaneAlignmentNeeded = c["weathervaneAlignmentNeeded"]
            self.windDirection = c["windDirection"]
            self.windDirectionVariation = c["windDirectionVariation"]
            self.windSpeed = c["windSpeed"]
            self.windValueType = c["windValueType"]
            self.yesterdayRainCounter = c["yesterdayRainCounter"]
            self.yesterdaySunshineDuration = c["yesterdaySunshineDuration"]

    def __str__(self):
        return ("{} humidity({}) illumination({}) illuminationThresholdSunshine({}) raining({}) storm({}) sunshine({})"
                "todayRainCounter({}) todaySunshineDuration({}) totalRainCounter({}) totalSunshineDuration({})"
                "weathervaneAlignmentNeeded({}) windDirection({}) windDirectionVariation({}) windSpeed({}) windValueType({})"
                "yesterdayRainCounter({}) yesterdaySunshineDuration({})").format(super().__str__(),self.humidity,self.illumination,
                                                                                 self.illuminationThresholdSunshine,self.raining,
                                                                                 self.storm,self.sunshine,self.todayRainCounter,
                                                                                 self.todaySunshineDuration,self.totalRainCounter,
                                                                                 self.totalSunshineDuration,self.weathervaneAlignmentNeeded,
                                                                                 self.windDirection,self.windDirectionVariation,self.windSpeed,
                                                                                 self.windValueType,self.yesterdayRainCounter,
                                                                                 self.yesterdaySunshineDuration)

    #Any set/calibration functions?

class WaterSensor(Device):
    """ HmIP-SWD ( Water Sensor ) """


    def __init__(self,connection):
        super().__init__(connection)
        self.incorrectPositioned = False
        self.acousticAlarmSignal = AcousticAlarmSignal.DISABLE_ACOUSTIC_SIGNAL
        self.acousticAlarmTiming = AcousticAlarmTiming.PERMANENT
        self.acousticWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.inAppWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.moistureDetected = False
        self.sirenWateralarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.waterlevelDetected = False
        
    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DEVICE_INCORRECT_POSITIONED", js)
        if c:
            self.unreach = c["unreach"]
            self.lowBat = c["lowBat"]
            self.routerModuleSupported = c["routerModuleSupported"]
            self.routerModuleEnabled = c["routerModuleEnabled"]
            self.rssiDeviceValue = c["rssiDeviceValue"]
            self.rssiPeerValue = c["rssiPeerValue"]
            self.dutyCycle = c["dutyCycle"]
            self.configPending = c["configPending"]
            self.incorrectPositioned = c["incorrectPositioned"]

        c = get_functional_channel("WATER_SENSOR_CHANNEL", js)
        if c:
            self.acousticAlarmSignal = AcousticAlarmSignal.from_str(c["acousticAlarmSignal"])
            self.acousticAlarmTiming = AcousticAlarmTiming.from_str(c["acousticAlarmTiming"])
            self.acousticWaterAlarmTrigger = WaterAlarmTrigger.from_str(c["acousticWaterAlarmTrigger"])
            self.inAppWaterAlarmTrigger = WaterAlarmTrigger.from_str(c["inAppWaterAlarmTrigger"])
            self.moistureDetected = c["moistureDetected"]
            self.sirenWaterAlarmTrigger = WaterAlarmTrigger.from_str(c["sirenWaterAlarmTrigger"])
            self.waterlevelDetected = c["waterlevelDetected"]

    def __str__(self):
        return ("{} incorrectPositioned({}) acousticAlarmSignal({}) acousticAlarmTiming({}) acousticWaterAlarmTrigger({})"
               " inAppWaterAlarmTrigger({}) moistureDetected({}) sirenWaterAlarmTrigger({}) waterlevelDetected({})").format(super().__str__()
                                                                                                                           , self.incorrectPositioned
                                                                                                                           , self.acousticAlarmSignal
                                                                                                                           , self.acousticAlarmTiming
                                                                                                                           , self.acousticWaterAlarmTrigger
                                                                                                                           , self.inAppWaterAlarmTrigger
                                                                                                                           , self.moistureDetected
                                                                                                                           , self.sirenWaterAlarmTrigger
                                                                                                                           , self.waterlevelDetected)

    def set_acoustic_alarm_signal(self, acousticAlarmSignal : AcousticAlarmSignal):
        data = {"channelIndex": 1, "deviceId": self.id, "acousticAlarmSignal": str(acousticAlarmSignal)}
        return self._restCall("device/configuration/setAcousticAlarmSignal", json.dumps(data))

    def set_acoustic_alarm_timing(self, acousticAlarmTiming : AcousticAlarmTiming):
        data = {"channelIndex": 1, "deviceId": self.id, "acousticAlarmTiming": str(acousticAlarmTiming)}
        return self._restCall("device/configuration/setAcousticAlarmTiming", json.dumps(data))
    
    def set_acoustic_water_alarm_trigger(self, acousticWaterAlarmTrigger : WaterAlarmTrigger):
        data = {"channelIndex": 1, "deviceId": self.id, "acousticWaterAlarmTrigger": str(acousticWaterAlarmTrigger)}
        return self._restCall("device/configuration/setAcousticWaterAlarmTrigger", json.dumps(data))

    def set_inapp_water_alarm_trigger(self, inAppWaterAlarmTrigger : WaterAlarmTrigger):
        data = {"channelIndex": 1, "deviceId": self.id, "inAppWaterAlarmTrigger": str(inAppWaterAlarmTrigger)}
        return self._restCall("device/configuration/setInAppWaterAlarmTrigger", json.dumps(data))

    def set_siren_water_alarm_trigger(self, sirenWaterAlarmTrigger : WaterAlarmTrigger):
        LOGGER.warning("set_siren_water_alarm_trigger is currently not available in the HMIP App. It might not be available in the cloud yet")
        data = {"channelIndex": 1, "deviceId": self.id, "sirenWaterAlarmTrigger": str(sirenWaterAlarmTrigger)}
        return self._restCall("device/configuration/setSirenWaterAlarmTrigger", json.dumps(data))