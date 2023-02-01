# coding=utf-8
import json
import logging
from collections import Counter
from typing import Iterable

from homematicip.base.functionalChannels import FunctionalChannel
from homematicip.base.enums import *
from homematicip.base.helpers import get_functional_channel, get_functional_channels
from homematicip.base.HomeMaticIPObject import HomeMaticIPObject
from homematicip.group import Group

LOGGER = logging.getLogger(__name__)


class BaseDevice(HomeMaticIPObject):
    """Base device class. This is the foundation for homematicip and external (hue) devices"""

    _supportedFeatureAttributeMap = {}

    def __init__(self, connection):
        super().__init__(connection)
        self.id = None
        self.homeId = None
        self.label = None
        self.connectionType = ConnectionType.HMIP_LAN
        self.deviceArchetype = DeviceArchetype.HMIP
        self.lastStatusUpdate = None
        self.firmwareVersion = None
        self.modelType = ""
        self.permanentlyReachable = False
        self.functionalChannels = []
        self.functionalChannelCount = Counter()
        self.deviceType = None

        # must be imported in init. otherwise we have cross import issues
        from homematicip.class_maps import TYPE_FUNCTIONALCHANNEL_MAP

        self._typeFunctionalChannelMap = TYPE_FUNCTIONALCHANNEL_MAP

    def from_json(self, js):
        super().from_json(js)
        self.id = js["id"]
        self.homeId = js["homeId"]
        self.label = js["label"]

        self.lastStatusUpdate = self.fromtimestamp(js["lastStatusUpdate"])
        self.firmwareVersion = js["firmwareVersion"]
        self.modelType = js["modelType"]
        self.permanentlyReachable = js["permanentlyReachable"]
        self.deviceType = js["type"]

        self.connectionType = ConnectionType.from_str(js["connectionType"])

        if "deviceArchetype" in js:
            self.deviceArchetype = DeviceArchetype.from_str(js["deviceArchetype"])

    def load_functionalChannels(
        self, groups: Iterable[Group], channels: Iterable[FunctionalChannel]
    ):
        """this function will load the functionalChannels into the device"""
        for channel in self._rawJSONData["functionalChannels"].values():
            items = [ch for ch in self.functionalChannels if ch.index == channel["index"]]
            fc = items[0] if items else None
            
            if fc is not None:
                fc.from_json(channel, groups)
            else:
                fc = self._parse_functionalChannel(channel, groups)
                channels.append(fc)
                self.functionalChannels.append(fc)

        self.functionalChannelCount = Counter(
            x.functionalChannelType for x in self.functionalChannels
        )
    # def load_functionalChannels(self, groups: Iterable[Group]):
    #     """this function will load the functionalChannels into the device"""
    #     self.functionalChannels = []
    #     for channel in self._rawJSONData["functionalChannels"].values():
    #         fc = self._parse_functionalChannel(channel, groups)
    #         self.functionalChannels.append(fc)
    #     self.functionalChannelCount = Counter(
    #         x.functionalChannelType for x in self.functionalChannels
    #     )

    def _parse_functionalChannel(self, json_state, groups: Iterable[Group]):
        fc = None
        try:
            channelType = FunctionalChannelType.from_str(
                json_state["functionalChannelType"]
            )
            fc = self._typeFunctionalChannelMap[channelType](self, self._connection)
            fc.from_json(json_state, groups)
        except:
            fc = self._typeFunctionalChannelMap[
                FunctionalChannelType.FUNCTIONAL_CHANNEL
            ](self, self._connection)
            fc.from_json(json_state, groups)
            fc.device = self
            LOGGER.warning(
                "There is no class for functionalChannel '%s' yet",
                json_state["functionalChannelType"],
            )
        return fc


class Device(BaseDevice):
    """this class represents a generic homematic ip device"""

    _supportedFeatureAttributeMap = {
        "IFeatureDeviceOverheated": ["deviceOverheated"],
        "IFeatureDeviceOverloaded": ["deviceOverloaded"],
        "IFeatureDeviceUndervoltage": ["deviceUndervoltage"],
        "IFeatureDeviceTemperatureOutOfRange": ["temperatureOutOfRange"],
        "IFeatureDeviceCoProError": ["coProFaulty"],
        "IFeatureDeviceCoProRestart": ["coProRestartNeeded"],
        "IFeatureDeviceCoProUpdate": ["coProUpdateFailure"],
        "IFeatureMinimumFloorHeatingValvePosition": [
            "minimumFloorHeatingValvePosition"
        ],
        "IFeaturePulseWidthModulationAtLowFloorHeatingValvePosition": [
            "pulseWidthModulationAtLowFloorHeatingValvePositionEnabled"
        ],
        "IFeatureBusConfigMismatch": ["busConfigMismatch"],
        "IFeatureShortCircuitDataLine": ["shortCircuitDataLine"],
        "IFeatureRssiValue": ["rssiDeviceValue"],
        "IOptionalFeatureDutyCycle": ["dutyCycle"],
        "IFeaturePowerShortCircuit": ["powerShortCircuit"],
        "IOptionalFeatureLowBat": ["lowBat"],
        "IFeatureDevicePowerFailure": ["devicePowerFailureDetected"],
        "IFeatureDeviceUndervoltage": ["deviceUndervoltage"],
        "IFeatureMulticastRouter": ["multicastRoutingEnabled"],
        "IFeatureDeviceIdentify": [],
        "IFeatureProfilePeriodLimit": [],
        "IOptionalFeatureDisplayContrast": [],
        "IOptionalFeatureMountingOrientation": [],
    }

    def __init__(self, connection):
        super().__init__(connection)

        self.updateState = DeviceUpdateState.UP_TO_DATE
        self.availableFirmwareVersion = None
        self.firmwareVersionInteger = (
            0  # firmwareVersion = A.B.C -> firmwareVersionInteger ((A<<16)|(B<<8)|C)
        )
        self.unreach = False
        self.lowBat = False
        self.routerModuleSupported = False
        self.routerModuleEnabled = False
        self.modelId = 0
        self.oem = ""
        self.manufacturerCode = 0
        self.serializedGlobalTradeItemNumber = ""
        self.rssiDeviceValue = 0
        self.rssiPeerValue = 0
        self.dutyCycle = False
        self.configPending = False

        self._baseChannel = "DEVICE_BASE"

        self.deviceOverheated = False
        self.deviceOverloaded = False
        self.deviceUndervoltage = False
        self.temperatureOutOfRange = False
        self.coProFaulty = False
        self.coProRestartNeeded = False
        self.coProUpdateFailure = False
        self.busConfigMismatch = False
        self.shortCircuitDataLine = False
        self.powerShortCircuit = False
        self.deviceUndervoltage = False
        self.devicePowerFailureDetected = False
        self.deviceIdentifySupported = (
            False  # just placeholder at the moment the feature doesn't set any values
        )

    def from_json(self, js):
        super().from_json(js)

        self.updateState = DeviceUpdateState.from_str(js["updateState"])
        self.firmwareVersionInteger = js["firmwareVersionInteger"]
        self.availableFirmwareVersion = js["availableFirmwareVersion"]
        self.modelId = js["modelId"]
        self.oem = js["oem"]
        self.manufacturerCode = js["manufacturerCode"]
        self.serializedGlobalTradeItemNumber = js["serializedGlobalTradeItemNumber"]
        self.liveUpdateState = LiveUpdateState.from_str(js["liveUpdateState"])
        c = get_functional_channel(self._baseChannel, js)
        if c:
            self.set_attr_from_dict("lowBat", c)
            self.set_attr_from_dict("unreach", c)
            self.set_attr_from_dict("rssiDeviceValue", c)
            self.set_attr_from_dict("rssiPeerValue", c)
            self.set_attr_from_dict("configPending", c)
            self.set_attr_from_dict("dutyCycle", c)
            self.routerModuleSupported = c["routerModuleSupported"]
            self.routerModuleEnabled = c["routerModuleEnabled"]

            sof = c.get("supportedOptionalFeatures")
            if sof:
                for k, v in sof.items():
                    if v:
                        if k in Device._supportedFeatureAttributeMap:
                            for attribute in Device._supportedFeatureAttributeMap[k]:
                                self.set_attr_from_dict(attribute, c)
                        else:  # pragma: no cover
                            LOGGER.warning(
                                "Optional Device Feature '%s' is not yet supported",
                                k,
                            )

    def __str__(self):
        return f"{self.modelType} {self.label} {self.str_from_attr_map()}"

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


class ExternalDevice(BaseDevice):
    """Represents devices with archtetype EXTERNAL"""

    def __init__(self, connection):
        super().__init__(connection)
        self.hasCustomLabel = None
        self.externalService = ""
        self.supported = None
        self._baseChannel = "EXTERNAL_BASE_CHANNEL"

    def from_json(self, js):
        super().from_json(js)

        self.hasCustomLabel = js["hasCustomLabel"]
        self.externalService = js["externalService"]
        self.supported = js["supported"]


class HomeControlAccessPoint(Device):
    def __init__(self, connection):
        super().__init__(connection)
        self.dutyCycleLevel = 0.0
        self.accessPointPriority = 0
        self.signalBrightness = 0
        self._baseChannel = "ACCESS_CONTROLLER_CHANNEL"

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel(self._baseChannel, js)
        if c:
            self.set_attr_from_dict("dutyCycleLevel", c)
            self.set_attr_from_dict("accessPointPriority", c)
            self.set_attr_from_dict("signalBrightness", c)


class SabotageDevice(Device):
    def __init__(self, connection):
        super().__init__(connection)
        self.sabotage = None
        self._baseChannel = "DEVICE_SABOTAGE"

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel(self._baseChannel, js)
        if c:
            self.set_attr_from_dict("sabotage", c)


class OperationLockableDevice(Device):
    def __init__(self, connection):
        super().__init__(connection)
        self.operationLockActive = None
        self._baseChannel = "DEVICE_OPERATIONLOCK"

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel(self._baseChannel, js)
        if c:
            self.set_attr_from_dict("operationLockActive", c)

    def set_operation_lock(self, operationLock=True):
        data = {"channelIndex": 0, "deviceId": self.id, "operationLock": operationLock}
        return self._restCall("device/configuration/setOperationLock", json.dumps(data))


class HeatingThermostat(OperationLockableDevice):
    """HMIP-eTRV (Radiator Thermostat)"""

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
    """HMIP-eTRV-C (Heating-thermostat compact without display)"""

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


class HeatingThermostatEvo(OperationLockableDevice):
    """HMIP-eTRV-E (Heating-thermostat new evo version)"""

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
    """HMIP-SWDO (Door / Window Contact - optical) / HMIP-SWDO-I (Door / Window Contact Invisible - optical)"""

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


class ShutterContactMagnetic(Device):
    """HMIP-SWDM /  HMIP-SWDM-B2  (Door / Window Contact - magnetic )"""

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


class ShutterContactOpticalPlus(ShutterContact):
    """HmIP-SWDO-PL ( Window / Door Contact – optical, plus )"""


class ContactInterface(SabotageDevice):
    """HMIP-SCI (Contact Interface Sensor)"""

    def __init__(self, connection):
        super().__init__(connection)
        self.windowState = WindowState.CLOSED
        self.eventDelay = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("CONTACT_INTERFACE_CHANNEL", js)
        if c:
            self.windowState = WindowState.from_str(c["windowState"])
            self.eventDelay = c["eventDelay"]

    def __str__(self):
        return "{} windowState({})".format(super().__str__(), self.windowState)


class RotaryHandleSensor(SabotageDevice):
    """HMIP-SRH"""

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
    """HMIP-STHO (Temperature and Humidity Sensor outdoor)"""

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
    """HMIP-STH (Temperature and Humidity Sensor without display - indoor)"""

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
    """HMIP-STHD (Temperature and Humidity Sensor with display - indoor)"""

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
    """HMIP-WTH, HMIP-WTH-2 (Wall Thermostat with Humidity Sensor) / HMIP-BWTH (Brand Wall Thermostat with Humidity Sensor)"""

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL", js)
        if c:
            self.temperatureOffset = c["temperatureOffset"]
            self.display = ClimateControlDisplay.from_str(c["display"])
            self.actualTemperature = c["actualTemperature"]
            self.humidity = c["humidity"]
            self.setPointTemperature = c["setPointTemperature"]


class RoomControlDevice(WallMountedThermostatPro):
    """ALPHA-IP-RBG    (Alpha IP Wall Thermostat Display)"""

    pass


class RoomControlDeviceAnalog(Device):
    """ALPHA-IP-RBGa   (ALpha IP Wall Thermostat Display analog)"""

    def __init__(self, connection):
        super().__init__(connection)
        self.actualTemperature = 0.0
        self.setPointTemperature = 0.0
        self.temperatureOffset = 0.0

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("ANALOG_ROOM_CONTROL_CHANNEL", js)
        if c:
            self.set_attr_from_dict("actualTemperature", c)
            self.set_attr_from_dict("setPointTemperature", c)
            self.set_attr_from_dict("temperatureOffset", c)


class WallMountedThermostatBasicHumidity(WallMountedThermostatPro):
    """HMIP-WTH-B (Wall Thermostat – basic)"""

    pass


class SmokeDetector(Device):
    """HMIP-SWSD (Smoke Alarm with Q label)"""

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
    """HMIP-FAL230-C6 (Floor Heating Actuator - 6 channels, 230 V)"""

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
    """HMIP-FAL24-C10  (Floor Heating Actuator – 10x channels, 24V)"""


class FloorTerminalBlock12(Device):
    """HMIP-FALMOT-C12 (Floor Heating Actuator – 12x channels, motorised)"""

    def __init__(self, connection):
        super().__init__(connection)
        self.frostProtectionTemperature = 0.0
        self.valveProtectionDuration = 0
        self.valveProtectionSwitchingInterval = 20
        self.coolingEmergencyValue = 0
        self.minimumFloorHeatingValvePosition = 0.0
        self.pulseWidthModulationAtLowFloorHeatingValvePositionEnabled = False

        self._baseChannel = "DEVICE_BASE_FLOOR_HEATING"

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DEVICE_BASE_FLOOR_HEATING", js)
        if c:
            self.set_attr_from_dict("coolingEmergencyValue", c)
            self.set_attr_from_dict("frostProtectionTemperature", c)
            self.set_attr_from_dict("valveProtectionDuration", c)
            self.set_attr_from_dict("valveProtectionSwitchingInterval", c)

    def set_minimum_floor_heating_valve_position(
        self, minimumFloorHeatingValvePosition: float
    ):
        """sets the minimum floot heating valve position

        Args:
            minimumFloorHeatingValvePosition(float): the minimum valve position. must be between 0.0 and 1.0

        Returns:
            the result of the _restCall
        """
        data = {
            "channelIndex": 0,
            "deviceId": self.id,
            "minimumFloorHeatingValvePosition": minimumFloorHeatingValvePosition,
        }
        return self._restCall(
            "device/configuration/setMinimumFloorHeatingValvePosition",
            body=json.dumps(data),
        )


class WiredFloorTerminalBlock12(FloorTerminalBlock12):
    """Implementation of HmIPW-FALMOT-C12"""


class Switch(Device):
    """Generic Switch class"""

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
    """HMIP-PS (Pluggable Switch), HMIP-PCBS (Switch Circuit Board - 1 channel)"""


class PrintedCircuitBoardSwitchBattery(Switch):
    """HMIP-PCBS-BAT (Printed Circuit Board Switch Battery)"""


class PrintedCircuitBoardSwitch2(Switch):
    """HMIP-PCBS2 (Switch Circuit Board - 2x channels)"""


class OpenCollector8Module(Switch):
    """HMIP-MOD-OC8 ( Open Collector Module )"""


class HeatingSwitch2(Switch):
    """HMIP-WHS2 (Switch Actuator for heating systems – 2x channels)"""


class WiredInputSwitch6(Switch):
    """HmIPW-FIO6"""


class WiredSwitch8(Switch):
    """HMIPW-DRS8 (Homematic IP Wired Switch Actuator – 8x channels)"""


class WiredSwitch4(Switch):
    """HMIPW-DRS4 (Homematic IP Wired Switch Actuator – 4x channels)"""


class DinRailSwitch4(Switch):
    """HMIP-DRSI4 (Homematic IP Switch Actuator for DIN rail mount – 4x channels)"""


class BrandSwitch2(Switch):
    """ELV-SH-BS2 (ELV Smart Home ARR-Bausatz Schaltaktor für Markenschalter – 2-fach powered by Homematic IP)"""


class SwitchMeasuring(Switch):
    """Generic class for Switch and Meter"""

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
    """HMIP-MIOB (Multi IO Box for floor heating & cooling)"""

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
    """HMIP-BSL (Switch Actuator for brand switches – with signal lamp)"""

    def __init__(self, connection):
        super().__init__(connection)
        #:int:the channel number for the top light
        self.topLightChannelIndex = 2
        #:int:the channel number for the bottom light
        self.bottomLightChannelIndex = 3

    def __str__(self):
        top = self.functionalChannels[self.topLightChannelIndex]
        bottom = self.functionalChannels[self.bottomLightChannelIndex]
        return (
            "{} topDimLevel({}) topColor({}) bottomDimLevel({}) bottomColor({})".format(
                super().__str__(),
                top.dimLevel,
                top.simpleRGBColorState,
                bottom.dimLevel,
                bottom.simpleRGBColorState,
            )
        )

    def set_rgb_dim_level(self, channelIndex: int, rgb: RGBColorState, dimLevel: float):
        """sets the color and dimlevel of the lamp

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
        """sets the color and dimlevel of the lamp

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
    """HMIP-PSM (Pluggable Switch and Meter)"""


class BrandSwitchMeasuring(SwitchMeasuring):
    """HMIP-BSM (Brand Switch and Meter)"""


class FullFlushSwitchMeasuring(SwitchMeasuring):
    """HMIP-FSM, HMIP-FSM16 (Full flush Switch and Meter)"""


class PushButton(Device):
    """HMIP-WRC2 (Wall-mount Remote Control - 2-button)"""


class PushButton6(PushButton):
    """HMIP-WRC6 (Wall-mount Remote Control - 6-button)"""


class PushButtonFlat(PushButton):
    """HmIP-WRCC2 (Wall-mount Remote Control – flat)"""


class BrandPushButton(PushButton):
    """HMIP-BRC2 (Remote Control for brand switches – 2x channels)"""


class KeyRemoteControl4(PushButton):
    """HMIP-KRC4 (Key Ring Remote Control - 4 buttons)"""


class RemoteControl8(PushButton):
    """HMIP-RC8 (Remote Control - 8 buttons)"""


class RemoteControl8Module(RemoteControl8):
    """HMIP-MOD-RC8 (Open Collector Module Sender - 8x)"""


class AlarmSirenIndoor(SabotageDevice):
    """HMIP-ASIR (Alarm Siren)"""

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("ALARM_SIREN_CHANNEL", js)
        if c:
            # The ALARM_SIREN_CHANNEL doesn't have any values yet.
            pass


class AlarmSirenOutdoor(AlarmSirenIndoor):
    """HMIP-ASIR-O (Alarm Siren Outdoor)"""

    def __init__(self, connection):
        super().__init__(connection)
        self.badBatteryHealth = False
        self._baseChannel = "DEVICE_RECHARGEABLE_WITH_SABOTAGE"

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DEVICE_RECHARGEABLE_WITH_SABOTAGE", js)
        if c:
            self.set_attr_from_dict("badBatteryHealth", c)


class MotionDetectorIndoor(SabotageDevice):
    """HMIP-SMI (Motion Detector with Brightness Sensor - indoor)"""

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
    """HMIP-SMO-A (Motion Detector with Brightness Sensor - outdoor)"""

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
            self.set_attr_from_dict("motionDetected", c)
            self.set_attr_from_dict("illumination", c)
            self.set_attr_from_dict("motionBufferActive", c)
            self.set_attr_from_dict("motionDetectionSendInterval", c)
            self.set_attr_from_dict("numberOfBrightnessMeasurements", c)
            self.set_attr_from_dict("currentIllumination", c)


class MotionDetectorPushButton(MotionDetectorOutdoor):
    """HMIP-SMI55 (Motion Detector with Brightness Sensor and Remote Control - 2-button)"""

    def __init__(self, connection):
        super().__init__(connection)
        self._baseChannel = "DEVICE_PERMANENT_FULL_RX"
        self.permanentFullRx = False

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DEVICE_PERMANENT_FULL_RX", js)
        if c:
            self.set_attr_from_dict("permanentFullRx", c)


class WiredMotionDetectorPushButton(MotionDetectorOutdoor):
    """HmIPW-SMI55"""


class PresenceDetectorIndoor(SabotageDevice):
    """HMIP-SPI (Presence Sensor - indoor)"""

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
    """HMIP-SPDR (Passage Detector)"""

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
    """HMIP-KRCA (Key Ring Remote Control - alarm)"""


class Shutter(Device):
    """Base class for shutter devices"""

    def set_shutter_level(self, level=0.0, channelIndex=1):
        """sets the shutter level

        Args:
            level(float): the new level of the shutter. 0.0 = open, 1.0 = closed
            channelIndex(int): the channel to control
        Returns:
            the result of the _restCall
        """
        data = {
            "channelIndex": channelIndex,
            "deviceId": self.id,
            "shutterLevel": level,
        }
        return self._restCall("device/control/setShutterLevel", body=json.dumps(data))

    def set_shutter_stop(self, channelIndex=1):
        """stops the current shutter operation

        Args:
            channelIndex(int): the channel to control
        Returns:
            the result of the _restCall
        """
        data = {"channelIndex": channelIndex, "deviceId": self.id}
        return self._restCall("device/control/stop", body=json.dumps(data))


class Blind(Shutter):
    """Base class for blind devices"""

    def set_slats_level(self, slatsLevel=0.0, shutterLevel=None, channelIndex=1):
        """sets the slats and shutter level

        Args:
            slatsLevel(float): the new level of the slats. 0.0 = open, 1.0 = closed,
            shutterLevel(float): the new level of the shutter. 0.0 = open, 1.0 = closed, None = use the current value
            channelIndex(int): the channel to control
        Returns:
            the result of the _restCall
        """
        if shutterLevel is None:
            shutterLevel = self.functionalChannels[channelIndex].shutterLevel

        data = {
            "channelIndex": channelIndex,
            "deviceId": self.id,
            "slatsLevel": slatsLevel,
            "shutterLevel": shutterLevel,
        }
        return self._restCall("device/control/setSlatsLevel", json.dumps(data))


class FullFlushShutter(Shutter):
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


class FullFlushBlind(FullFlushShutter, Blind):
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

    def __str__(self):
        return "{} slatsLevel({}) blindModeActive({})".format(
            super().__str__(), self.slatsLevel, self.blindModeActive
        )


class BrandBlind(FullFlushBlind):
    """HMIP-BBL (Blind Actuator for brand switches)"""


class DinRailBlind4(Blind):
    """HmIP-DRBLI4 (Blind Actuator for DIN rail mount – 4 channels)"""


class WiredDinRailBlind4(Blind):
    """HmIPW-DRBL4"""


class WiredPushButton(PushButton):
    """HmIPW-WRC6 and HmIPW-WRC2"""


class BlindModule(Device):
    """HMIP-HDM1 (Hunter Douglas & erfal window blinds)"""

    def __init__(self, connection):
        super().__init__(connection)
        self.automationDriveSpeed = DriveSpeed.CREEP_SPEED
        self.manualDriveSpeed = DriveSpeed.CREEP_SPEED
        self.favoritePrimaryShadingPosition = 0.0
        self.favoriteSecondaryShadingPosition = 0.0
        self.primaryShadingLevel = 0.0
        self.secondaryShadingLevel = 0.0
        self.previousPrimaryShadingLevel = 0.0
        self.previousSecondaryShadingLevel = 0.0
        self.identifyOemSupported = False
        self.productId = 0
        self.primaryCloseAdjustable = False
        self.primaryOpenAdjustable = False
        self.primaryShadingStateType = ShadingStateType.NOT_EXISTENT
        self.primaryCloseAdjustable = False
        self.primaryOpenAdjustable = False
        self.primaryShadingStateType = ShadingStateType.NOT_EXISTENT
        self.profileMode = ProfileMode.MANUAL
        self.userDesiredProfileMode = ProfileMode.MANUAL
        self.processing = False
        self.shadingDriveVersion = None
        self.shadingPackagePosition = ShadingPackagePosition.NOT_USED
        self.shadingPositionAdjustmentActive = None
        self.shadingPositionAdjustmentClientId = None

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("SHADING_CHANNEL", js)
        if c:
            self.set_attr_from_dict("automationDriveSpeed", c, DriveSpeed)
            self.set_attr_from_dict("manualDriveSpeed", c, DriveSpeed)

            self.set_attr_from_dict("favoritePrimaryShadingPosition", c)
            self.set_attr_from_dict("favoriteSecondaryShadingPosition", c)

            self.set_attr_from_dict("primaryCloseAdjustable", c)
            self.set_attr_from_dict("primaryOpenAdjustable", c)
            self.set_attr_from_dict("primaryShadingStateType", c, ShadingStateType)
            self.set_attr_from_dict("secondaryCloseAdjustable", c)
            self.set_attr_from_dict("secondaryOpenAdjustable", c)
            self.set_attr_from_dict("secondaryShadingStateType", c, ShadingStateType)

            self.set_attr_from_dict("primaryShadingLevel", c)
            self.set_attr_from_dict("secondaryShadingLevel", c)

            self.set_attr_from_dict("previousPrimaryShadingLevel", c)
            self.set_attr_from_dict("previousSecondaryShadingLevel", c)

            self.set_attr_from_dict("identifyOemSupported", c)
            self.set_attr_from_dict("productId", c)

            self.set_attr_from_dict("profileMode", c, ProfileMode)
            self.set_attr_from_dict("userDesiredProfileMode", c, ProfileMode)

            self.set_attr_from_dict("shadingDriveVersion", c)
            self.set_attr_from_dict("shadingPackagePosition", c, ShadingPackagePosition)
            self.set_attr_from_dict("shadingPositionAdjustmentActive", c)
            self.set_attr_from_dict("shadingPositionAdjustmentClientId", c)

    def set_primary_shading_level(self, primaryShadingLevel: float):
        data = {
            "channelIndex": 1,
            "deviceId": self.id,
            "primaryShadingLevel": primaryShadingLevel,
        }
        return self._restCall("device/control/setPrimaryShadingLevel", json.dumps(data))

    def set_secondary_shading_level(
        self, primaryShadingLevel: float, secondaryShadingLevel: float
    ):
        data = {
            "channelIndex": 1,
            "deviceId": self.id,
            "primaryShadingLevel": primaryShadingLevel,
            "secondaryShadingLevel": secondaryShadingLevel,
        }
        return self._restCall(
            "device/control/setSecondaryShadingLevel", json.dumps(data)
        )

    def stop(self):
        """stops the current operation
        Returns:
            the result of the _restCall
        """
        data = {"channelIndex": 1, "deviceId": self.id}
        return self._restCall("device/control/stop", body=json.dumps(data))


class LightSensor(Device):
    """HMIP-SLO (Light Sensor outdoor)"""

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

    def set_dim_level(self, dimLevel=0.0, channelIndex=1):
        data = {"channelIndex": channelIndex, "deviceId": self.id, "dimLevel": dimLevel}
        return self._restCall("device/control/setDimLevel", json.dumps(data))


class PluggableDimmer(Dimmer):
    """HMIP-PDT Pluggable Dimmer"""


class BrandDimmer(Dimmer):
    """HMIP-BDT Brand Dimmer"""


class FullFlushDimmer(Dimmer):
    """HMIP-FDT Dimming Actuator flush-mount"""


class WiredDimmer3(Dimmer):
    """HMIPW-DRD3 (Homematic IP Wired Dimming Actuator – 3x channels)"""


class DinRailDimmer3(Dimmer):
    """HMIP-DRDI3 (Dimming Actuator Inbound 230V – 3x channels, 200W per channel) electrical DIN rail"""

    def __init__(self, connection):
        super().__init__(connection)
        self.c1dimLevel = 0.0
        self.c2dimLevel = 0.0
        self.c3dimLevel = 0.0

    def from_json(self, js):
        super().from_json(js)
        channels = get_functional_channels("MULTI_MODE_INPUT_DIMMER_CHANNEL", js)
        if channels:
            self.c1dimLevel = channels[0]["dimLevel"]
            self.dimLevel = self.c1dimLevel
            self.c2dimLevel = channels[1]["dimLevel"]
            self.c3dimLevel = channels[2]["dimLevel"]

    def __str__(self):
        return "{} c1DimLevel({}) c2DimLevel({}) c3DimLevel({})".format(
            super().__str__(), self.c1dimLevel, self.c2dimLevel, self.c3dimLevel
        )


class WeatherSensor(Device):
    """HMIP-SWO-B"""

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
    """HMIP-SWO-PL"""

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
    """HMIP-SWO-PR"""

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
    """HMIP-SWD ( Water Sensor )"""

    def __init__(self, connection):
        super().__init__(connection)
        self.incorrectPositioned = False
        self.acousticAlarmSignal = AcousticAlarmSignal.DISABLE_ACOUSTIC_SIGNAL
        self.acousticAlarmTiming = AcousticAlarmTiming.PERMANENT
        self.acousticWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.inAppWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.moistureDetected = False
        self.sirenWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
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
    """HMIP-FCI1 (Contact Interface flush-mount – 1 channel)"""

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
        return (
            "{} binaryBehaviorType({}) multiModeInputMode({}) windowState({})".format(
                super().__str__(),
                self.binaryBehaviorType,
                self.multiModeInputMode,
                self.windowState,
            )
        )


class FullFlushContactInterface6(Device):
    """HMIP-FCI6 (Contact Interface flush-mount – 6 channels)"""


class WiredInput32(FullFlushContactInterface):
    """HMIPW-DRI32 (Homematic IP Wired Inbound module – 32x channels)"""


class FullFlushInputSwitch(Switch):
    """HMIP-FSI16 (Switch Actuator with Push-button Input 230V, 16A)"""

    def __init__(self, connection):
        super().__init__(connection)
        self.binaryBehaviorType = BinaryBehaviorType.NORMALLY_OPEN
        self.multiModeInputMode = MultiModeInputMode.SWITCH_BEHAVIOR
        self.on = False
        self.profileMode = ProfileMode.MANUAL
        self.userDesiredProfileMode = ProfileMode.MANUAL

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("MULTI_MODE_INPUT_SWITCH_CHANNEL", js)
        if c:
            self.set_attr_from_dict("binaryBehaviorType", c, BinaryBehaviorType)
            self.set_attr_from_dict("multiModeInputMode", c, MultiModeInputMode)
            self.set_attr_from_dict("on", c)
            self.set_attr_from_dict("profileMode", c, ProfileMode)
            self.set_attr_from_dict("userDesiredProfileMode", c, ProfileMode)


class DinRailSwitch(FullFlushInputSwitch):
    """HMIP-DRSI1 (Switch Actuator for DIN rail mount – 1x channel)"""


class AccelerationSensor(Device):
    """HMIP-SAM (Contact Interface flush-mount – 1 channel)"""

    def __init__(self, connection):
        super().__init__(connection)
        #:float:
        self.accelerationSensorEventFilterPeriod = 100.0
        #:AccelerationSensorMode:
        self.accelerationSensorMode = AccelerationSensorMode.ANY_MOTION
        #:AccelerationSensorNeutralPosition:
        self.accelerationSensorNeutralPosition = (
            AccelerationSensorNeutralPosition.HORIZONTAL
        )
        #:AccelerationSensorSensitivity:
        self.accelerationSensorSensitivity = (
            AccelerationSensorSensitivity.SENSOR_RANGE_2G
        )
        #:int:
        self.accelerationSensorTriggerAngle = 0
        #:bool:
        self.accelerationSensorTriggered = False
        #:NotificationSoundType:
        self.notificationSoundTypeHighToLow = NotificationSoundType.SOUND_NO_SOUND
        #:NotificationSoundType:
        self.notificationSoundTypeLowToHigh = NotificationSoundType.SOUND_NO_SOUND

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("ACCELERATION_SENSOR_CHANNEL", js)
        if c:
            self.set_attr_from_dict("accelerationSensorEventFilterPeriod", c)
            self.set_attr_from_dict("accelerationSensorMode", c, AccelerationSensorMode)
            self.set_attr_from_dict(
                "accelerationSensorNeutralPosition",
                c,
                AccelerationSensorNeutralPosition,
            )
            self.set_attr_from_dict(
                "accelerationSensorSensitivity", c, AccelerationSensorSensitivity
            )
            self.set_attr_from_dict("accelerationSensorTriggerAngle", c)
            self.set_attr_from_dict("accelerationSensorTriggered", c)
            self.set_attr_from_dict(
                "notificationSoundTypeHighToLow", c, NotificationSoundType
            )
            self.set_attr_from_dict(
                "notificationSoundTypeLowToHigh", c, NotificationSoundType
            )

    def set_acceleration_sensor_mode(
        self, mode: AccelerationSensorMode, channelIndex=1
    ):
        data = {
            "channelIndex": channelIndex,
            "deviceId": self.id,
            "accelerationSensorMode": str(mode),
        }
        return self._restCall(
            "device/configuration/setAccelerationSensorMode", json.dumps(data)
        )

    def set_acceleration_sensor_neutral_position(
        self, neutralPosition: AccelerationSensorNeutralPosition, channelIndex=1
    ):
        data = {
            "channelIndex": channelIndex,
            "deviceId": self.id,
            "accelerationSensorNeutralPosition": str(neutralPosition),
        }
        return self._restCall(
            "device/configuration/setAccelerationSensorNeutralPosition",
            json.dumps(data),
        )

    def set_acceleration_sensor_sensitivity(
        self, sensitivity: AccelerationSensorSensitivity, channelIndex=1
    ):
        data = {
            "channelIndex": channelIndex,
            "deviceId": self.id,
            "accelerationSensorSensitivity": str(sensitivity),
        }
        return self._restCall(
            "device/configuration/setAccelerationSensorSensitivity", json.dumps(data)
        )

    def set_acceleration_sensor_trigger_angle(self, angle: int, channelIndex=1):
        data = {
            "channelIndex": channelIndex,
            "deviceId": self.id,
            "accelerationSensorTriggerAngle": angle,
        }
        return self._restCall(
            "device/configuration/setAccelerationSensorTriggerAngle", json.dumps(data)
        )

    def set_acceleration_sensor_event_filter_period(
        self, period: float, channelIndex=1
    ):
        data = {
            "channelIndex": channelIndex,
            "deviceId": self.id,
            "accelerationSensorEventFilterPeriod": period,
        }
        return self._restCall(
            "device/configuration/setAccelerationSensorEventFilterPeriod",
            json.dumps(data),
        )

    def set_notification_sound_type(
        self, soundType: NotificationSoundType, isHighToLow: bool, channelIndex=1
    ):
        data = {
            "channelIndex": channelIndex,
            "deviceId": self.id,
            "notificationSoundType": str(soundType),
            "isHighToLow": isHighToLow,
        }
        return self._restCall(
            "device/configuration/setNotificationSoundType", json.dumps(data)
        )


class DoorModule(Device):
    """Generic class for a door module"""

    def __init__(self, connection):
        super().__init__(connection)
        self.doorState = DoorState.POSITION_UNKNOWN
        self.on = False
        self.processing = False
        self.ventilationPositionSupported = False

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DOOR_CHANNEL", js)
        if c:
            self.set_attr_from_dict("doorState", c, DoorState)
            self.set_attr_from_dict("on", c)
            self.set_attr_from_dict("processing", c)
            self.set_attr_from_dict("ventilationPositionSupported", c)

    def send_door_command(self, doorCommand=DoorCommand.STOP):
        data = {"channelIndex": 1, "deviceId": self.id, "doorCommand": doorCommand}
        return self._restCall("device/control/sendDoorCommand", json.dumps(data))


class GarageDoorModuleTormatic(DoorModule):
    """HMIP-MOD-TM (Garage Door Module Tormatic)"""


class HoermannDrivesModule(DoorModule):
    """HMIP-MOD-HO (Garage Door Module for Hörmann)"""


class PluggableMainsFailureSurveillance(Device):
    """HMIP-PMFS (Plugable Power Supply Monitoring)"""

    def __init__(self, connection):
        super().__init__(connection)
        self.powerMainsFailure = False
        self.genericAlarmSignal = AlarmSignalType.NO_ALARM

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("MAINS_FAILURE_CHANNEL", js)
        if c:
            self.set_attr_from_dict("powerMainsFailure", c)
            self.set_attr_from_dict("genericAlarmSignal", c, AlarmSignalType)


class WallMountedGarageDoorController(Device):
    """HmIP-WGC Wall mounted Garage Door Controller"""

    def __init__(self, connection):
        super().__init__(connection)
        self.impulseDuration = 0
        self.processing = False

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("IMPULSE_OUTPUT_CHANNEL", js)
        if c:
            self.set_attr_from_dict("impulseDuration", c)
            self.set_attr_from_dict("processing", c)

    def send_start_impulse(self, channelIndex=2):
        """Toggle Wall mounted Garage Door Controller."""
        data = {"channelIndex": channelIndex, "deviceId": self.id}
        return self._restCall("device/control/startImpulse", body=json.dumps(data))


class TiltVibrationSensor(Device):
    """HMIP-STV (Inclination and vibration Sensor)"""

    def __init__(self, connection):
        super().__init__(connection)
        #:float:
        self.accelerationSensorEventFilterPeriod = 100.0
        #:AccelerationSensorMode:
        self.accelerationSensorMode = AccelerationSensorMode.ANY_MOTION
        #:AccelerationSensorSensitivity:
        self.accelerationSensorSensitivity = (
            AccelerationSensorSensitivity.SENSOR_RANGE_2G
        )
        #:int:
        self.accelerationSensorTriggerAngle = 0
        #:bool:
        self.accelerationSensorTriggered = False

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("TILT_VIBRATION_SENSOR_CHANNEL", js)
        if c:
            self.set_attr_from_dict("accelerationSensorEventFilterPeriod", c)
            self.set_attr_from_dict("accelerationSensorMode", c, AccelerationSensorMode)
            self.set_attr_from_dict(
                "accelerationSensorSensitivity", c, AccelerationSensorSensitivity
            )
            self.set_attr_from_dict("accelerationSensorTriggerAngle", c)
            self.set_attr_from_dict("accelerationSensorTriggered", c)

    def set_acceleration_sensor_mode(
        self, mode: AccelerationSensorMode, channelIndex=1
    ):
        data = {
            "channelIndex": channelIndex,
            "deviceId": self.id,
            "accelerationSensorMode": str(mode),
        }
        return self._restCall(
            "device/configuration/setAccelerationSensorMode", json.dumps(data)
        )

    def set_acceleration_sensor_sensitivity(
        self, sensitivity: AccelerationSensorSensitivity, channelIndex=1
    ):
        data = {
            "channelIndex": channelIndex,
            "deviceId": self.id,
            "accelerationSensorSensitivity": str(sensitivity),
        }
        return self._restCall(
            "device/configuration/setAccelerationSensorSensitivity", json.dumps(data)
        )

    def set_acceleration_sensor_trigger_angle(self, angle: int, channelIndex=1):
        data = {
            "channelIndex": channelIndex,
            "deviceId": self.id,
            "accelerationSensorTriggerAngle": angle,
        }
        return self._restCall(
            "device/configuration/setAccelerationSensorTriggerAngle", json.dumps(data)
        )

    def set_acceleration_sensor_event_filter_period(
        self, period: float, channelIndex=1
    ):
        data = {
            "channelIndex": channelIndex,
            "deviceId": self.id,
            "accelerationSensorEventFilterPeriod": period,
        }
        return self._restCall(
            "device/configuration/setAccelerationSensorEventFilterPeriod",
            json.dumps(data),
        )


class RainSensor(Device):
    """HMIP-SRD (Rain Sensor)"""

    def __init__(self, connection):
        super().__init__(connection)
        #:bool:
        self.raining = False
        #:float:
        self.rainSensorSensitivity = 0.0

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("RAIN_DETECTION_CHANNEL", js)
        if c:
            self.set_attr_from_dict("rainSensorSensitivity", c)
            self.set_attr_from_dict("raining", c)


class TemperatureDifferenceSensor2(Device):
    """HmIP-STE2-PCB (Temperature Difference Sensors - 2x sensors)"""

    def __init__(self, connection):
        super().__init__(connection)
        #:float:
        self.temperatureExternalDelta = 0.0
        #:float:
        self.temperatureExternalOne = 0.0
        #:float:
        self.temperatureExternalTwo = 0.0

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("TEMPERATURE_SENSOR_2_EXTERNAL_DELTA_CHANNEL", js)
        if c:
            self.set_attr_from_dict("temperatureExternalDelta", c)
            self.set_attr_from_dict("temperatureExternalOne", c)
            self.set_attr_from_dict("temperatureExternalTwo", c)


class DoorLockDrive(Device):
    """HmIP-DLD"""

    def __init__(self, connection):
        super().__init__(connection)
        self.autoRelockDelay = False
        self.doorHandleType = "UNKNOWN"
        self.doorLockDirection = False
        self.doorLockNeutralPosition = False
        self.doorLockTurns = False
        self.lockState = LockState.UNLOCKED
        self.motorState = MotorState.STOPPED

        self.door_lock_channel = -1

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DOOR_LOCK_CHANNEL", js)
        if c:
            self.set_attr_from_dict("autoRelockDelay", c)
            self.set_attr_from_dict("doorHandleType", c)
            self.set_attr_from_dict("doorLockDirection", c)
            self.set_attr_from_dict("doorLockNeutralPosition", c)
            self.set_attr_from_dict("doorLockTurns", c)
            self.set_attr_from_dict("lockState", c, LockState)
            self.set_attr_from_dict("motorState", c, MotorState)
            self.door_lock_channel = c["index"]

    def set_lock_state(self, doorLockState: LockState, pin="", channelIndex=1):
        """sets the door lock state

        Args:
            doorLockState(float): the state of the door. See LockState from base/enums.py
            pin(string): Pin, if specified.
            channelIndex(int): the channel to control. Normally the channel from DOOR_LOCK_CHANNEL is used.
        Returns:
            the result of the _restCall
        """
        if channelIndex == 1:
            channelIndex = self.door_lock_channel

        data = {
            "deviceId": self.id,
            "channelIndex": channelIndex,
            "authorizationPin": pin,
            "targetLockState": doorLockState,
        }
        return self._restCall("device/control/setLockState", json.dumps(data))


class DoorLockSensor(Device):
    """HmIP-DLS"""

    def __init__(self, connection):
        super().__init__(connection)
        self.doorLockDirection = ""
        self.doorLockNeutralPosition = ""
        self.doorLockTurns = 0
        self.lockState = LockState.OPEN

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("DOOR_LOCK_SENSOR_CHANNEL", js)
        if c:

            self.set_attr_from_dict("doorLockDirection", c)
            self.set_attr_from_dict("doorLockNeutralPosition", c)
            self.set_attr_from_dict("doorLockTurns", c)
            self.set_attr_from_dict("lockState", c, LockState)
            self.door_lock_channel = c["index"]
