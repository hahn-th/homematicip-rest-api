# coding=utf-8
import json
from datetime import datetime
import logging

from homematicip.base.helpers import get_functional_channel
from homematicip.base.enums import *
from homematicip import HomeMaticIPObject
from homematicip.group import Group

from typing import Iterable
from collections import Counter

LOGGER = logging.getLogger(__name__)


class Device(HomeMaticIPObject.HomeMaticIPObject):
    """ this class represents a generic homematic ip device """

    def __init__(self, connection):
        super().__init__(connection)
        self.id = None
        self.homeId = None
        self.label = None
        self.lastStatusUpdate = None
        self.deviceType = None
        self.updateState = DeviceUpdateState.UP_TO_DATE
        self.firmwareVersion = None
        self.firmwareVersionInteger = (
            0
        )  # firmwareVersion = A.B.C -> firmwareVersionInteger ((A<<16)|(B<<8)|C)
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
        self.permanentlyReachable = False
        self.liveUpdateState = LiveUpdateState.LIVE_UPDATE_NOT_SUPPORTED
        self.functionalChannels = []
        self.functionalChannelCount = Counter()

        # must be imported in init. otherwise we have cross import issues
        from homematicip.class_maps import TYPE_FUNCTIONALCHANNEL_MAP

        self._typeFunctionalChannelMap = TYPE_FUNCTIONALCHANNEL_MAP

        self._baseChannel = "DEVICE_BASE"

    def from_json(self, js):
        super().from_json(js)
        self.id = js["id"]
        self.homeId = js["homeId"]
        self.label = js["label"]

        self.lastStatusUpdate = self.fromtimestamp(js["lastStatusUpdate"])

        self.deviceType = js["type"]
        self.updateState = DeviceUpdateState.from_str(js["updateState"])
        self.firmwareVersion = js["firmwareVersion"]
        self.firmwareVersionInteger = js["firmwareVersionInteger"]
        self.availableFirmwareVersion = js["availableFirmwareVersion"]
        self.modelType = js["modelType"]
        self.modelId = js["modelId"]
        self.oem = js["oem"]
        self.manufacturerCode = js["manufacturerCode"]
        self.serializedGlobalTradeItemNumber = js["serializedGlobalTradeItemNumber"]
        self.permanentlyReachable = js["permanentlyReachable"]
        self.liveUpdateState = LiveUpdateState.from_str(js["liveUpdateState"])

        c = get_functional_channel(self._baseChannel, js)
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
        return "{} {} lowbat({}) unreach({}) rssiDeviceValue({}) rssiPeerValue({}) configPending({}) dutyCycle({})".format(
            self.modelType,
            self.label,
            self.lowBat,
            self.unreach,
            self.rssiDeviceValue,
            self.rssiPeerValue,
            self.configPending,
            self.dutyCycle,
        )

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
        data = {"deviceId": self.id, "channelIndex": 0, "routerModuleEnabled": enabled}
        return self._restCall(
            "device/configuration/setRouterModuleEnabled", json.dumps(data)
        )

    def load_functionalChannels(self, groups: Iterable[Group]):
        """ this function will load the functionalChannels into the device """
        self.functionalChannels = []
        for channel in self._rawJSONData["functionalChannels"].values():
            fc = self._parse_functionalChannel(channel, groups)
            self.functionalChannels.append(fc)
        self.functionalChannelCount = Counter(
            x.functionalChannelType for x in self.functionalChannels
        )

    def _parse_functionalChannel(self, json_state, groups: Iterable[Group]):
        fc = None
        try:
            channelType = FunctionalChannelType.from_str(
                json_state["functionalChannelType"]
            )
            fc = self._typeFunctionalChannelMap[channelType]()
            fc.from_json(json_state, groups)
        except:
            fc = self._typeFunctionalChannelMap[
                FunctionalChannelType.FUNCTIONAL_CHANNEL
            ]()
            fc.from_json(json_state, groups)
            LOGGER.warning(
                "There is no class for functionalChannel '%s' yet",
                json_state["functionalChannelType"],
            )
        return fc


class SabotageDevice(Device):
    def __init__(self, connection):
        super().__init__(connection)
        self.sabotage = None
        self._baseChannel = "DEVICE_SABOTAGE"

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DEVICE_SABOTAGE", js)
        if c:
            self.sabotage = c["sabotage"]

    def __str__(self):
        return "{} sabotage({})".format(super().__str__(), self.sabotage)


class OperationLockableDevice(Device):
    def __init__(self, connection):
        super().__init__(connection)
        self.operationLockActive = None
        self._baseChannel = "DEVICE_OPERATIONLOCK"

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DEVICE_OPERATIONLOCK", js)
        if c:
            self.operationLockActive = c["operationLockActive"]

    def set_operation_lock(self, operationLock=True):
        data = {"channelIndex": 0, "deviceId": self.id, "operationLock": operationLock}
        return self._restCall("device/configuration/setOperationLock", json.dumps(data))

    def __str__(self):
        return "{} operationLockActive({})".format(
            super().__str__(), self.operationLockActive
        )


class HeatingThermostat(OperationLockableDevice):
    """ HMIP-eTRV (Radiator Thermostat) """

    def __init__(self, connection):
        super().__init__(connection)
        #:float: the offset temperature for the thermostat (+/- 3.5)
        self.temperatureOffset = 0.0
        #:float: the current position of the valve 0.0 = closed, 1.0 max opened
        self.valvePosition = 0.0
        #:ValveState: the current state of the valve
        self.valveState = ValveState.ERROR_POSITION
        #:float: the current temperature which should be reached in the room
        self.setPointTemperature = 0.0
        #:float: the current measured temperature at the valve
        self.valveActualTemperature = 0.0
        #:bool: must the adaption re-run?
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
            self.valveActualTemperature = c["valveActualTemperature"]

    def __str__(self):
        return "{} valvePosition({}) valveState({}) temperatureOffset({}) setPointTemperature({}) valveActualTemperature({})".format(
            super().__str__(),
            self.valvePosition,
            self.valveState,
            self.temperatureOffset,
            self.setPointTemperature,
            self.valveActualTemperature,
        )


class HeatingThermostatCompact(SabotageDevice):
    """ HmIP-eTRV-C (Heating-thermostat compact without display) """

    def __init__(self, connection):
        super().__init__(connection)
        #:float: the offset temperature for the thermostat (+/- 3.5)
        self.temperatureOffset = 0.0
        #:float: the current position of the valve 0.0 = closed, 1.0 max opened
        self.valvePosition = 0.0
        #:ValveState: the current state of the valve
        self.valveState = ValveState.ERROR_POSITION
        #:float: the current temperature which should be reached in the room
        self.setPointTemperature = 0.0
        #:float: the current measured temperature at the valve
        self.valveActualTemperature = 0.0
        #:bool: must the adaption re-run?
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
            self.valveActualTemperature = c["valveActualTemperature"]

    def __str__(self):
        return "{} valvePosition({}) valveState({}) temperatureOffset({}) setPointTemperature({}) valveActualTemperature({})".format(
            super().__str__(),
            self.valvePosition,
            self.valveState,
            self.temperatureOffset,
            self.setPointTemperature,
            self.valveActualTemperature,
        )


class ShutterContact(SabotageDevice):
    """ HMIP-SWDO (Door / Window Contact - optical) / HMIP-SWDO-I (Door / Window Contact Invisible - optical) / 
         HmIP-SWDM /  HmIP-SWDM-B2  (Door / Window Contact - magnetic )"""

    def __init__(self, connection):
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

    def __init__(self, connection):
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

    def __init__(self, connection):
        super().__init__(connection)
        self.actualTemperature = 0
        self.humidity = 0
        self.vaporAmount = 0.0

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("CLIMATE_SENSOR_CHANNEL", js)
        if c:
            self.actualTemperature = c["actualTemperature"]
            self.humidity = c["humidity"]
            self.vaporAmount = c["vaporAmount"]

    def __str__(self):
        return "{} actualTemperature({}) humidity({}) vaporAmount({})".format(
            super().__str__(), self.actualTemperature, self.humidity, self.vaporAmount
        )


class TemperatureHumiditySensorWithoutDisplay(Device):
    """ HMIP-STH (Temperature and Humidity Sensor without display - indoor) """

    def __init__(self, connection):
        super().__init__(connection)
        self.temperatureOffset = 0
        self.actualTemperature = 0
        self.humidity = 0
        self.vaporAmount = 0.0

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel(
            "WALL_MOUNTED_THERMOSTAT_WITHOUT_DISPLAY_CHANNEL", js
        )
        if c:
            self.temperatureOffset = c["temperatureOffset"]
            self.actualTemperature = c["actualTemperature"]
            self.humidity = c["humidity"]
            self.vaporAmount = c["vaporAmount"]

    def __str__(self):
        return "{} actualTemperature({}) humidity({}) vaporAmount({})".format(
            super().__str__(), self.actualTemperature, self.humidity, self.vaporAmount
        )


class TemperatureHumiditySensorDisplay(Device):
    """ HMIP-STHD (Temperature and Humidity Sensor with display - indoor) """

    def __init__(self, connection):
        super().__init__(connection)
        self.temperatureOffset = 0
        self.display = ClimateControlDisplay.ACTUAL
        self.actualTemperature = 0
        self.humidity = 0
        self.setPointTemperature = 0
        self.vaporAmount = 0.0

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL", js)
        if c:
            self.temperatureOffset = c["temperatureOffset"]
            self.display = ClimateControlDisplay.from_str(c["display"])
            self.actualTemperature = c["actualTemperature"]
            self.humidity = c["humidity"]
            self.setPointTemperature = c["setPointTemperature"]
            self.vaporAmount = c["vaporAmount"]

    def set_display(
        self, display: ClimateControlDisplay = ClimateControlDisplay.ACTUAL
    ):
        data = {"channelIndex": 1, "deviceId": self.id, "display": str(display)}
        return self._restCall(
            "device/configuration/setClimateControlDisplay", json.dumps(data)
        )

    def __str__(self):
        return "{} actualTemperature({}) humidity({}) vaporAmount({}) setPointTemperature({})".format(
            super().__str__(),
            self.actualTemperature,
            self.humidity,
            self.vaporAmount,
            self.setPointTemperature,
        )


class WallMountedThermostatPro(
    TemperatureHumiditySensorDisplay, OperationLockableDevice
):
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

    def __init__(self, connection):
        super().__init__(connection)
        self.smokeDetectorAlarmType = SmokeDetectorAlarmType.IDLE_OFF

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("SMOKE_DETECTOR_CHANNEL", js)
        if c:
            self.smokeDetectorAlarmType = SmokeDetectorAlarmType.from_str(
                c["smokeDetectorAlarmType"]
            )

    def __str__(self):
        return "{} smokeDetectorAlarmType({})".format(
            super().__str__(), self.smokeDetectorAlarmType
        )


class FloorTerminalBlock6(Device):
    """ HMIP-FAL230-C6 (Floor Heating Actuator - 6 channels, 230 V) """

    def __init__(self, connection):
        super().__init__(connection)
        self.globalPumpControl = False
        self.heatingValveType = HeatingValveType.NORMALLY_CLOSE
        self.heatingLoadType = HeatingLoadType.LOAD_BALANCING
        self.frostProtectionTemperature = 0.0
        self.heatingEmergencyValue = 0.0
        self.valveProtectionDuration = 0
        self.valveProtectionSwitchingInterval = 20
        self.coolingEmergencyValue = 0

        self.pumpFollowUpTime = 0
        self.pumpLeadTime = 0
        self.pumpProtectionDuration = 0
        self.pumpProtectionSwitchingInterval = 20

        self._baseChannel = "DEVICE_GLOBAL_PUMP_CONTROL"

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DEVICE_GLOBAL_PUMP_CONTROL", js)
        if c:
            self.globalPumpControl = c["globalPumpControl"]
            self.heatingValveType = HeatingValveType.from_str(c["heatingValveType"])
            self.heatingLoadType = HeatingLoadType.from_str(c["heatingLoadType"])
            self.coolingEmergencyValue = c["coolingEmergencyValue"]

            self.frostProtectionTemperature = c["frostProtectionTemperature"]
            self.heatingEmergencyValue = c["heatingEmergencyValue"]
            self.valveProtectionDuration = c["valveProtectionDuration"]
            self.valveProtectionSwitchingInterval = c[
                "valveProtectionSwitchingInterval"
            ]

        c = get_functional_channel("FLOOR_TERMINAL_BLOCK_LOCAL_PUMP_CHANNEL", js)
        if c:
            self.pumpFollowUpTime = c["pumpFollowUpTime"]
            self.pumpLeadTime = c["pumpLeadTime"]
            self.pumpProtectionDuration = c["pumpProtectionDuration"]
            self.pumpProtectionSwitchingInterval = c["pumpProtectionSwitchingInterval"]

    def __str__(self):
        return (
            "{} globalPumpControl({}) heatingValveType({}) heatingLoadType({}) coolingEmergencyValue({}) frostProtectionTemperature({}) heatingEmergencyValue({}) "
            "valveProtectionDuration({}) valveProtectionSwitchingInterval({}) pumpFollowUpTime({}) pumpLeadTime({}) pumpProtectionDuration({}) "
            "pumpProtectionSwitchingInterval({})"
        ).format(
            super().__str__(),
            self.globalPumpControl,
            self.heatingValveType,
            self.heatingLoadType,
            self.coolingEmergencyValue,
            self.frostProtectionTemperature,
            self.heatingEmergencyValue,
            self.valveProtectionDuration,
            self.valveProtectionSwitchingInterval,
            self.pumpFollowUpTime,
            self.pumpLeadTime,
            self.pumpProtectionDuration,
            self.pumpProtectionSwitchingInterval,
        )


class FloorTerminalBlock10(FloorTerminalBlock6):
    """ HMIP-FAL24-C10  (Floor Heating Actuator – 10x channels, 24V) """


class Switch(Device):
    """ Generic Switch class """

    def __init__(self, connection):
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
        return "{} on({}) profileMode({}) userDesiredProfileMode({})".format(
            super().__str__(), self.on, self.profileMode, self.userDesiredProfileMode
        )

    def set_switch_state(self, on=True, channelIndex=1):
        data = {"channelIndex": channelIndex, "deviceId": self.id, "on": on}
        return self._restCall("device/control/setSwitchState", body=json.dumps(data))

    def turn_on(self, channelIndex=1):
        return self.set_switch_state(True, channelIndex)

    def turn_off(self, channelIndex=1):
        return self.set_switch_state(False, channelIndex)


class PlugableSwitch(Switch):
    """ HMIP-PS (Pluggable Switch), HMIP-PCBS (Switch Circuit Board - 1 channel) """


class PrintedCircuitBoardSwitchBattery(Switch):
    """ HmIP-PCBS-BAT (Printed Curcuit Board Switch Battery) """


class PrintedCircuitBoardSwitch2(Switch):
    """ HMIP-PCBS2 (Switch Circuit Board - 2x channels) """


class OpenCollector8Module(Switch):
    """ HmIP-MOD-OC8 ( Open Collector Module ) """


class SwitchMeasuring(Switch):
    """ Generic class for Switch and Meter """

    def __init__(self, connection):
        super().__init__(connection)
        self.energyCounter = 0
        self.currentPowerConsumption = 0

    def reset_energy_counter(self):
        data = {"channelIndex": 1, "deviceId": self.id}
        return self._restCall(
            "device/control/resetEnergyCounter", body=json.dumps(data)
        )

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
        return "{} energyCounter({}) currentPowerConsumption({}W)".format(
            super().__str__(), self.energyCounter, self.currentPowerConsumption
        )


class MultiIOBox(Switch):
    """ HMIP-MIOB (Multi IO Box for floor heating & cooling)  """

    def __init__(self, connection):
        super().__init__(connection)
        self.analogOutputLevel = 0.0

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("ANALOG_OUTPUT_CHANNEL", js)
        if c:
            self.analogOutputLevel = c["analogOutputLevel"]

    def __str__(self):
        return "{} analogOutputLevel({})".format(
            super().__str__(), self.analogOutputLevel
        )


class BrandSwitchNotificationLight(Switch):
    """ HMIP-BSL (Switch Actuator for brand switches – with signal lamp) """

    def __init__(self, connection):
        super().__init__(connection)
        #:int:the channel number for the top light
        self.topLightChannelIndex = 2
        #:int:the channel number for the bottom light
        self.bottomLightChannelIndex = 3

    def __str__(self):
        top = self.functionalChannels[self.topLightChannelIndex]
        bottom = self.functionalChannels[self.bottomLightChannelIndex]
        return "{} topDimLevel({}) topColor({}) bottomDimLevel({}) bottomColor({})".format(
            super().__str__(),
            top.dimLevel,
            top.simpleRGBColorState,
            bottom.dimLevel,
            bottom.simpleRGBColorState,
        )

    def set_rgb_dim_level(self, channelIndex: int, rgb: RGBColorState, dimLevel: float):
        """ sets the color and dimlevel of the lamp

        Args:
            channelIndex(int): the channelIndex of the lamp. Use self.topLightChannelIndex or self.bottomLightChannelIndex
            rgb(RGBColorState): the color of the lamp
            dimLevel(float): the dimLevel of the lamp. 0.0 = off, 1.0 = MAX

        Returns:
            the result of the _restCall
        """
        data = {
            "channelIndex": channelIndex,
            "deviceId": self.id,
            "simpleRGBColorState": rgb,
            "dimLevel": dimLevel,
        }
        return self._restCall(
            "device/control/setSimpleRGBColorDimLevel", body=json.dumps(data)
        )

    def set_rgb_dim_level_with_time(
        self,
        channelIndex: int,
        rgb: RGBColorState,
        dimLevel: float,
        onTime: float,
        rampTime: float,
    ):
        """ sets the color and dimlevel of the lamp

        Args:
            channelIndex(int): the channelIndex of the lamp. Use self.topLightChannelIndex or self.bottomLightChannelIndex
            rgb(RGBColorState): the color of the lamp
            dimLevel(float): the dimLevel of the lamp. 0.0 = off, 1.0 = MAX
            onTime(float):
            rampTime(float):
        Returns:
            the result of the _restCall
        """
        data = {
            "channelIndex": channelIndex,
            "deviceId": self.id,
            "simpleRGBColorState": rgb,
            "dimLevel": dimLevel,
            "onTime": onTime,
            "rampTime": rampTime,
        }
        return self._restCall(
            "device/control/setSimpleRGBColorDimLevelWithTime", body=json.dumps(data)
        )


class PlugableSwitchMeasuring(SwitchMeasuring):
    """ HMIP-PSM (Pluggable Switch and Meter) """


class BrandSwitchMeasuring(SwitchMeasuring):
    """ HMIP-BSM (Brand Switch and Meter) """


class FullFlushSwitchMeasuring(SwitchMeasuring):
    """ HMIP-FSM, HMIP-FSM16 (Full flush Switch and Meter) """


class PushButton(Device):
    """ HMIP-WRC2 (Wall-mount Remote Control - 2-button) """


class PushButton6(PushButton):
    """ HMIP-WRC6 (Wall-mount Remote Control - 6-button) """


class BrandPushButton(PushButton):
    """ HMIP-BRC2 (Remote Control for brand switches – 2x channels) """


class KeyRemoteControl4(PushButton):
    """ HMIP-KRC4 (Key Ring Remote Control - 4 buttons) """


class RemoteControl8(PushButton):
    """ HmIP-RC8 (Remote Control - 8 buttons) """


class AlarmSirenIndoor(SabotageDevice):
    """ HMIP-ASIR (Alarm Siren) """

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("ALARM_SIREN_CHANNEL", js)
        if c:
            # The ALARM_SIREN_CHANNEL doesn't have any values yet.
            pass


class MotionDetectorIndoor(SabotageDevice):
    """ HMIP-SMI (Motion Detector with Brightness Sensor - indoor) """

    def __init__(self, connection):
        super().__init__(connection)
        self.currentIllumination = None
        self.motionDetected = None
        self.illumination = None
        self.motionBufferActive = False
        self.motionDetectionSendInterval = MotionDetectionSendInterval.SECONDS_30
        self.numberOfBrightnessMeasurements = 0

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("MOTION_DETECTION_CHANNEL", js)
        if c:
            self.motionDetected = c["motionDetected"]
            self.illumination = c["illumination"]
            self.motionBufferActive = c["motionBufferActive"]
            self.motionDetectionSendInterval = MotionDetectionSendInterval.from_str(
                c["motionDetectionSendInterval"]
            )
            self.numberOfBrightnessMeasurements = c["numberOfBrightnessMeasurements"]
            self.currentIllumination = c["currentIllumination"]

    def __str__(self):
        return "{} motionDetected({}) illumination({}) motionBufferActive({}) motionDetectionSendInterval({}) numberOfBrightnessMeasurements({})".format(
            super().__str__(),
            self.motionDetected,
            self.illumination,
            self.motionBufferActive,
            self.motionDetectionSendInterval,
            self.numberOfBrightnessMeasurements,
        )


class MotionDetectorOutdoor(Device):
    """ HmIP-SMO-A (Motion Detector with Brightness Sensor - outdoor) """

    def __init__(self, connection):
        super().__init__(connection)
        self.currentIllumination = None
        self.motionDetected = None
        self.illumination = None
        self.motionBufferActive = False
        self.motionDetectionSendInterval = MotionDetectionSendInterval.SECONDS_30
        self.numberOfBrightnessMeasurements = 0

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("MOTION_DETECTION_CHANNEL", js)
        if c:
            self.motionDetected = c["motionDetected"]
            self.illumination = c["illumination"]
            self.motionBufferActive = c["motionBufferActive"]
            self.motionDetectionSendInterval = MotionDetectionSendInterval.from_str(
                c["motionDetectionSendInterval"]
            )
            self.numberOfBrightnessMeasurements = c["numberOfBrightnessMeasurements"]
            self.currentIllumination = c["currentIllumination"]

    def __str__(self):
        return "{} motionDetected({}) illumination({}) motionBufferActive({}) motionDetectionSendInterval({}) numberOfBrightnessMeasurements({})".format(
            super().__str__(),
            self.motionDetected,
            self.illumination,
            self.motionBufferActive,
            self.motionDetectionSendInterval,
            self.numberOfBrightnessMeasurements,
        )


class MotionDetectorPushButton(MotionDetectorIndoor):
    """ HMIP-SMI55 (Motion Detector with Brightness Sensor and Remote Control - 2-button) """

    def __init__(self, connection):
        super().__init__(connection)
        self._baseChannel = "DEVICE_PERMANENT_FULL_RX"
        self.permanentFullRx = False

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DEVICE_PERMANENT_FULL_RX", js)
        if c:
            self.permanentFullRx = c["permanentFullRx"]

    def __str__(self):
        return "{} permanentFullRx({})".format(super().__str__(), self.permanentFullRx)


class PresenceDetectorIndoor(SabotageDevice):
    """ HMIP-SPI (Presence Sensor - indoor) """

    def __init__(self, connection):
        super().__init__(connection)
        self.presenceDetected = False
        self.currentIllumination = None
        self.illumination = 0
        self.motionBufferActive = False
        self.motionDetectionSendInterval = MotionDetectionSendInterval.SECONDS_30
        self.numberOfBrightnessMeasurements = 0

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("PRESENCE_DETECTION_CHANNEL", js)
        if c:
            self.presenceDetected = c["presenceDetected"]
            self.currentIllumination = c["currentIllumination"]
            self.illumination = c["illumination"]
            self.motionBufferActive = c["motionBufferActive"]
            self.motionDetectionSendInterval = MotionDetectionSendInterval.from_str(
                c["motionDetectionSendInterval"]
            )
            self.numberOfBrightnessMeasurements = c["numberOfBrightnessMeasurements"]

    def __str__(self):
        return "{} presenceDetected({}) illumination({}) motionBufferActive({}) motionDetectionSendInterval({}) numberOfBrightnessMeasurements({})".format(
            super().__str__(),
            self.presenceDetected,
            self.illumination,
            self.motionBufferActive,
            self.motionDetectionSendInterval,
            self.numberOfBrightnessMeasurements,
        )


class PassageDetector(SabotageDevice):
    """ HMIP-SPDR (Passage Detector) """

    def __init__(self, connection):
        super().__init__(connection)
        self.leftCounter = 0
        self.leftRightCounterDelta = 0
        self.passageBlindtime = 0.0
        self.passageDirection = PassageDirection.RIGHT
        self.passageSensorSensitivity = 0.0
        self.passageTimeout = 0.0
        self.rightCounter = 0

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("PASSAGE_DETECTOR_CHANNEL", js)
        if c:
            self.leftCounter = c["leftCounter"]
            self.leftRightCounterDelta = c["leftRightCounterDelta"]
            self.passageBlindtime = c["passageBlindtime"]
            self.passageDirection = PassageDirection.from_str(c["passageDirection"])
            self.passageSensorSensitivity = c["passageSensorSensitivity"]
            self.passageTimeout = c["passageTimeout"]
            self.rightCounter = c["rightCounter"]

    def __str__(self):
        return "{} leftCounter({}) leftRightCounterDelta({}) passageBlindtime({}) passageDirection({}) passageSensorSensitivity({}) passageTimeout({}) rightCounter({})".format(
            super().__str__(),
            self.leftCounter,
            self.leftRightCounterDelta,
            self.passageBlindtime,
            self.passageDirection,
            self.passageSensorSensitivity,
            self.passageTimeout,
            self.rightCounter,
        )


class KeyRemoteControlAlarm(Device):
    """ HMIP-KRCA (Key Ring Remote Control - alarm) """


class FullFlushShutter(Device):
    """HMIP-FROLL (Shutter Actuator - flush-mount) / HMIP-BROLL (Shutter Actuator - Brand-mount)"""

    def __init__(self, connection):
        super().__init__(connection)
        self.shutterLevel = 0
        self.changeOverDelay = 0.0
        self.bottomToTopReferenceTime = 0.0
        self.topToBottomReferenceTime = 0.0
        self.delayCompensationValue = 0
        self.endpositionAutoDetectionEnabled = False
        self.previousShutterLevel = None
        self.processing = False
        self.profileMode = "AUTOMATIC"
        self.selfCalibrationInProgress = None
        self.supportingDelayCompensation = False
        self.supportingEndpositionAutoDetection = False
        self.supportingSelfCalibration = False
        self.userDesiredProfileMode = "AUTOMATIC"

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("SHUTTER_CHANNEL", js)
        if c:
            self.shutterLevel = c["shutterLevel"]
            self.changeOverDelay = c["changeOverDelay"]
            self.delayCompensationValue = c["delayCompensationValue"]
            self.bottomToTopReferenceTime = c["bottomToTopReferenceTime"]
            self.topToBottomReferenceTime = c["topToBottomReferenceTime"]
            self.endpositionAutoDetectionEnabled = c["endpositionAutoDetectionEnabled"]
            self.previousShutterLevel = c["previousShutterLevel"]
            self.processing = c["processing"]
            self.profileMode = c["profileMode"]
            self.selfCalibrationInProgress = c["selfCalibrationInProgress"]
            self.supportingDelayCompensation = c["supportingDelayCompensation"]
            self.supportingEndpositionAutoDetection = c[
                "supportingEndpositionAutoDetection"
            ]
            self.supportingSelfCalibration = c["supportingSelfCalibration"]
            self.userDesiredProfileMode = c["userDesiredProfileMode"]

    def __str__(self):
        return "{} shutterLevel({}) topToBottom({}) bottomToTop({})".format(
            super().__str__(),
            self.shutterLevel,
            self.topToBottomReferenceTime,
            self.bottomToTopReferenceTime,
        )

    def set_shutter_level(self, level=0.0):
        """ sets the shutter level

        Args:
            level(float): the new level of the shutter. 0.0 = open, 1.0 = closed
        Returns:
            the result of the _restCall
        """
        data = {"channelIndex": 1, "deviceId": self.id, "shutterLevel": level}
        return self._restCall("device/control/setShutterLevel", body=json.dumps(data))

    def set_shutter_stop(self):
        """ stops the current shutter operation
        Returns:
            the result of the _restCall
        """
        data = {"channelIndex": 1, "deviceId": self.id}
        return self._restCall("device/control/stop", body=json.dumps(data))


class FullFlushBlind(FullFlushShutter):
    """HMIP-FBL (Blind Actuator - flush-mount)"""

    def __init__(self, connection):
        super().__init__(connection)
        self.slatsLevel = 0
        self.slatsReferenceTime = 0.0
        self.previousSlatsLevel = 0
        self.blindModeActive = False

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("BLIND_CHANNEL", js)
        if c:
            self.shutterLevel = c["shutterLevel"]
            self.changeOverDelay = c["changeOverDelay"]
            self.delayCompensationValue = c["delayCompensationValue"]
            self.bottomToTopReferenceTime = c["bottomToTopReferenceTime"]
            self.topToBottomReferenceTime = c["topToBottomReferenceTime"]
            self.endpositionAutoDetectionEnabled = c["endpositionAutoDetectionEnabled"]
            self.previousShutterLevel = c["previousShutterLevel"]
            self.processing = c["processing"]
            self.profileMode = c["profileMode"]
            self.selfCalibrationInProgress = c["selfCalibrationInProgress"]
            self.supportingDelayCompensation = c["supportingDelayCompensation"]
            self.supportingEndpositionAutoDetection = c[
                "supportingEndpositionAutoDetection"
            ]
            self.supportingSelfCalibration = c["supportingSelfCalibration"]
            self.userDesiredProfileMode = c["userDesiredProfileMode"]

            self.slatsLevel = c["slatsLevel"]
            self.slatsReferenceTime = c["slatsReferenceTime"]
            self.previousSlatsLevel = c["previousSlatsLevel"]
            self.blindModeActive = c["blindModeActive"]

    def set_slats_level(self, slatsLevel=0.0, shutterLevel=None):
        """ sets the slats and shutter level

        Args:
            slatsLevel(float): the new level of the slats. 0.0 = open, 1.0 = closed,
            shutterLevel(float): the new level of the shutter. 0.0 = open, 1.0 = closed, None = use the current value
        Returns:
            the result of the _restCall
        """
        if shutterLevel is None:
            shutterLevel = self.shutterLevel
        data = {
            "channelIndex": 1,
            "deviceId": self.id,
            "slatsLevel": slatsLevel,
            "shutterLevel": shutterLevel,
        }
        return self._restCall("device/control/setSlatsLevel", json.dumps(data))

    def __str__(self):
        return "{} slatsLevel({}) blindModeActive({})".format(
            super().__str__(), self.slatsLevel, self.blindModeActive
        )


class BrandBlind(FullFlushBlind):
    """ HMIP-BBL (Blind Actuator for brand switches) """


class LightSensor(Device):
    """ HMIP-SLO (Light Sensor outdoor) """

    def __init__(self, connection):
        super().__init__(connection)
        #:float:the average illumination value
        self.averageIllumination = 0.0
        #:float:the current illumination value
        self.currentIllumination = 0.0
        #:float:the highest illumination value
        self.highestIllumination = 0.0
        #:float:the lowest illumination value
        self.lowestIllumination = 0.0

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("LIGHT_SENSOR_CHANNEL", js)
        if c:
            self.averageIllumination = c["averageIllumination"]
            self.currentIllumination = c["currentIllumination"]
            self.highestIllumination = c["highestIllumination"]
            self.lowestIllumination = c["lowestIllumination"]

    def __str__(self):
        return "{} averageIllumination({}) currentIllumination({}) highestIllumination({}) lowestIllumination({})".format(
            super().__str__(),
            self.averageIllumination,
            self.currentIllumination,
            self.highestIllumination,
            self.lowestIllumination,
        )


class Dimmer(Device):
    """Base dimmer device class"""

    def __init__(self, connection):
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
        return "{} dimLevel({}) profileMode({}) userDesiredProfileMode({})".format(
            super().__str__(),
            self.dimLevel,
            self.profileMode,
            self.userDesiredProfileMode,
        )

    def set_dim_level(self, dimLevel=0.0):
        data = {"channelIndex": 1, "deviceId": self.id, "dimLevel": dimLevel}
        return self._restCall("device/control/setDimLevel", json.dumps(data))


class PluggableDimmer(Dimmer):
    """HmIP-PDT Pluggable Dimmer"""


class BrandDimmer(Dimmer):
    """HmIP-BDT Brand Dimmer"""


class FullFlushDimmer(Dimmer):
    """HmIP-FDT Dimming Actuator flush-mount"""


class WeatherSensor(Device):
    """ HmIP-SWO-B """

    def __init__(self, connection):
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
        self.windValueType = WindValueType.AVERAGE_VALUE
        self.yesterdaySunshineDuration = 0
        self.vaporAmount = 0.0

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
            self.windValueType = WindValueType.from_str(c["windValueType"])
            self.yesterdaySunshineDuration = c["yesterdaySunshineDuration"]
            self.vaporAmount = c["vaporAmount"]

    def __str__(self):
        return (
            "{} actualTemperature({}) humidity({}) vaporAmount({}) illumination({}) illuminationThresholdSunshine({}) storm({}) sunshine({}) "
            "todaySunshineDuration({}) totalSunshineDuration({}) "
            "windSpeed({}) windValueType({}) "
            "yesterdaySunshineDuration({})"
        ).format(
            super().__str__(),
            self.actualTemperature,
            self.humidity,
            self.vaporAmount,
            self.illumination,
            self.illuminationThresholdSunshine,
            self.storm,
            self.sunshine,
            self.todaySunshineDuration,
            self.totalSunshineDuration,
            self.windSpeed,
            self.windValueType,
            self.yesterdaySunshineDuration,
        )


class WeatherSensorPlus(Device):
    """ HmIP-SWO-PL """

    def __init__(self, connection):
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
        self.windSpeed = 0
        self.windValueType = WindValueType.AVERAGE_VALUE
        self.yesterdayRainCounter = 0
        self.yesterdaySunshineDuration = 0
        self.vaporAmount = 0.0

    def from_json(self, js):
        super().from_json(js)

        c = get_functional_channel("WEATHER_SENSOR_PLUS_CHANNEL", js)
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
            self.windSpeed = c["windSpeed"]
            self.windValueType = WindValueType.from_str(c["windValueType"])
            self.yesterdayRainCounter = c["yesterdayRainCounter"]
            self.yesterdaySunshineDuration = c["yesterdaySunshineDuration"]
            self.vaporAmount = c["vaporAmount"]

    def __str__(self):
        return (
            "{} actualTemperature({}) humidity({}) vaporAmount({}) illumination({}) illuminationThresholdSunshine({}) raining({}) storm({}) sunshine({}) "
            "todayRainCounter({}) todaySunshineDuration({}) totalRainCounter({}) totalSunshineDuration({}) "
            "windSpeed({}) windValueType({}) yesterdayRainCounter({}) yesterdaySunshineDuration({})"
        ).format(
            super().__str__(),
            self.actualTemperature,
            self.humidity,
            self.vaporAmount,
            self.illumination,
            self.illuminationThresholdSunshine,
            self.raining,
            self.storm,
            self.sunshine,
            self.todayRainCounter,
            self.todaySunshineDuration,
            self.totalRainCounter,
            self.totalSunshineDuration,
            self.windSpeed,
            self.windValueType,
            self.yesterdayRainCounter,
            self.yesterdaySunshineDuration,
        )


class WeatherSensorPro(Device):
    """ HmIP-SWO-PR """

    def __init__(self, connection):
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
        self.windValueType = WindValueType.AVERAGE_VALUE
        self.yesterdayRainCounter = 0
        self.yesterdaySunshineDuration = 0
        self.vaporAmount = 0.0

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
            self.windValueType = WindValueType.from_str(c["windValueType"])
            self.yesterdayRainCounter = c["yesterdayRainCounter"]
            self.yesterdaySunshineDuration = c["yesterdaySunshineDuration"]
            self.vaporAmount = c["vaporAmount"]

    def __str__(self):
        return (
            "{} actualTemperature({}) humidity({}) vaporAmount({}) illumination({}) illuminationThresholdSunshine({}) raining({}) storm({}) sunshine({}) "
            "todayRainCounter({}) todaySunshineDuration({}) totalRainCounter({}) totalSunshineDuration({}) "
            "weathervaneAlignmentNeeded({}) windDirection({}) windDirectionVariation({}) windSpeed({}) windValueType({}) "
            "yesterdayRainCounter({}) yesterdaySunshineDuration({})"
        ).format(
            super().__str__(),
            self.actualTemperature,
            self.humidity,
            self.vaporAmount,
            self.illumination,
            self.illuminationThresholdSunshine,
            self.raining,
            self.storm,
            self.sunshine,
            self.todayRainCounter,
            self.todaySunshineDuration,
            self.totalRainCounter,
            self.totalSunshineDuration,
            self.weathervaneAlignmentNeeded,
            self.windDirection,
            self.windDirectionVariation,
            self.windSpeed,
            self.windValueType,
            self.yesterdayRainCounter,
            self.yesterdaySunshineDuration,
        )

    # Any set/calibration functions?


class WaterSensor(Device):
    """ HmIP-SWD ( Water Sensor ) """

    def __init__(self, connection):
        super().__init__(connection)
        self.incorrectPositioned = False
        self.acousticAlarmSignal = AcousticAlarmSignal.DISABLE_ACOUSTIC_SIGNAL
        self.acousticAlarmTiming = AcousticAlarmTiming.PERMANENT
        self.acousticWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.inAppWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.moistureDetected = False
        self.sirenWateralarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.waterlevelDetected = False
        self._baseChannel = "DEVICE_INCORRECT_POSITIONED"

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DEVICE_INCORRECT_POSITIONED", js)
        if c:
            self.incorrectPositioned = c["incorrectPositioned"]

        c = get_functional_channel("WATER_SENSOR_CHANNEL", js)
        if c:
            self.acousticAlarmSignal = AcousticAlarmSignal.from_str(
                c["acousticAlarmSignal"]
            )
            self.acousticAlarmTiming = AcousticAlarmTiming.from_str(
                c["acousticAlarmTiming"]
            )
            self.acousticWaterAlarmTrigger = WaterAlarmTrigger.from_str(
                c["acousticWaterAlarmTrigger"]
            )
            self.inAppWaterAlarmTrigger = WaterAlarmTrigger.from_str(
                c["inAppWaterAlarmTrigger"]
            )
            self.moistureDetected = c["moistureDetected"]
            self.sirenWaterAlarmTrigger = WaterAlarmTrigger.from_str(
                c["sirenWaterAlarmTrigger"]
            )
            self.waterlevelDetected = c["waterlevelDetected"]

    def __str__(self):
        return (
            "{} incorrectPositioned({}) acousticAlarmSignal({}) acousticAlarmTiming({}) acousticWaterAlarmTrigger({})"
            " inAppWaterAlarmTrigger({}) moistureDetected({}) sirenWaterAlarmTrigger({}) waterlevelDetected({})"
        ).format(
            super().__str__(),
            self.incorrectPositioned,
            self.acousticAlarmSignal,
            self.acousticAlarmTiming,
            self.acousticWaterAlarmTrigger,
            self.inAppWaterAlarmTrigger,
            self.moistureDetected,
            self.sirenWaterAlarmTrigger,
            self.waterlevelDetected,
        )

    def set_acoustic_alarm_signal(self, acousticAlarmSignal: AcousticAlarmSignal):
        data = {
            "channelIndex": 1,
            "deviceId": self.id,
            "acousticAlarmSignal": str(acousticAlarmSignal),
        }
        return self._restCall(
            "device/configuration/setAcousticAlarmSignal", json.dumps(data)
        )

    def set_acoustic_alarm_timing(self, acousticAlarmTiming: AcousticAlarmTiming):
        data = {
            "channelIndex": 1,
            "deviceId": self.id,
            "acousticAlarmTiming": str(acousticAlarmTiming),
        }
        return self._restCall(
            "device/configuration/setAcousticAlarmTiming", json.dumps(data)
        )

    def set_acoustic_water_alarm_trigger(
        self, acousticWaterAlarmTrigger: WaterAlarmTrigger
    ):
        data = {
            "channelIndex": 1,
            "deviceId": self.id,
            "acousticWaterAlarmTrigger": str(acousticWaterAlarmTrigger),
        }
        return self._restCall(
            "device/configuration/setAcousticWaterAlarmTrigger", json.dumps(data)
        )

    def set_inapp_water_alarm_trigger(self, inAppWaterAlarmTrigger: WaterAlarmTrigger):
        data = {
            "channelIndex": 1,
            "deviceId": self.id,
            "inAppWaterAlarmTrigger": str(inAppWaterAlarmTrigger),
        }
        return self._restCall(
            "device/configuration/setInAppWaterAlarmTrigger", json.dumps(data)
        )

    def set_siren_water_alarm_trigger(self, sirenWaterAlarmTrigger: WaterAlarmTrigger):
        LOGGER.warning(
            "set_siren_water_alarm_trigger is currently not available in the HMIP App. It might not be available in the cloud yet"
        )
        data = {
            "channelIndex": 1,
            "deviceId": self.id,
            "sirenWaterAlarmTrigger": str(sirenWaterAlarmTrigger),
        }
        return self._restCall(
            "device/configuration/setSirenWaterAlarmTrigger", json.dumps(data)
        )


class FullFlushContactInterface(Device):
    """ HMIP-FCI1 (Contact Interface flush-mount – 1 channel) """

    def __init__(self, connection):
        super().__init__(connection)
        self.binaryBehaviorType = BinaryBehaviorType.NORMALLY_OPEN
        self.multiModeInputMode = MultiModeInputMode.BINARY_BEHAVIOR
        self.windowState = WindowState.OPEN

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("MULTI_MODE_INPUT_CHANNEL", js)
        if c:
            self.binaryBehaviorType = BinaryBehaviorType.from_str(
                c["binaryBehaviorType"]
            )
            self.multiModeInputMode = MultiModeInputMode.from_str(
                c["multiModeInputMode"]
            )
            self.windowState = WindowState.from_str(c["windowState"])

    def __str__(self):
        return "{} binaryBehaviorType({}) multiModeInputMode({}) windowState({})".format(
            super().__str__(),
            self.binaryBehaviorType,
            self.multiModeInputMode,
            self.windowState,
        )
