import json
from typing import Any, Iterable

from homematicip.base.enums import *
from homematicip.base.homematicip_object import HomeMaticIPObject
from homematicip.group import Group

LOGGER = logging.getLogger(__name__)


class FunctionalChannel(HomeMaticIPObject):
    """this is the base class for the functional channels"""

    def __init__(self, device, connection):
        super().__init__(connection)
        self.index = -1
        self.groupIndex = -1
        self.label = ""
        self.groupIndex = -1
        self.functionalChannelType:str = ""
        self.groups = Iterable[Group]
        self.device = device

        # we don't need a connection in this object (at the moment)
        self._connection = None

    def from_json(self, js, groups: Iterable[Group]):
        """this function will load the functional channel object
        from a json object and the given groups

        Args:
            js(dict): the json object
            groups(Iterable[Group]): the groups for referencing
        """
        self._connection = self.device._connection
        self.index = js["index"]
        self.groupIndex = js["groupIndex"]
        self.label = js["label"]
        self.functionalChannelType = FunctionalChannelType.from_str(
            js["functionalChannelType"], js["functionalChannelType"]
        )
        self.groups = []
        for id in js["groups"]:
            for g in groups:
                if g.id == id:
                    self.groups.append(g)
                    break

        super().from_json(js)

    def __str__(self):
        return "{} {} Index({})".format(
            self.functionalChannelType,
            self.label if self.label else "unknown",
            self.index,
        )


class DeviceBaseChannel(FunctionalChannel):
    """this is the representative of the DEVICE_BASE channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.unreach = None
        self.lowBat = None
        self.routerModuleSupported = False
        self.routerModuleEnabled = False
        self.rssiDeviceValue = 0
        self.rssiPeerValue = 0
        self.dutyCycle = False
        self.configPending = False
        self.coProFaulty = None
        self.coProRestartNeeded = None
        self.coProUpdateFailure = None
        self.deviceOverheated = None
        self.deviceOverloaded = None
        self.deviceUndervoltage = None
        self.temperatureOutOfRange = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.unreach = js["unreach"]
        self.lowBat = js["lowBat"]
        self.routerModuleSupported = js["routerModuleSupported"]
        self.routerModuleEnabled = js["routerModuleEnabled"]
        self.rssiDeviceValue = js["rssiDeviceValue"]
        self.rssiPeerValue = js["rssiPeerValue"]
        self.dutyCycle = js["dutyCycle"]
        self.configPending = js["configPending"]
        sof = js["supportedOptionalFeatures"]
        if sof:
            if sof["IFeatureDeviceCoProError"]:
                self.coProFaulty = js["coProFaulty"]
            if sof["IFeatureDeviceCoProRestart"]:
                self.coProRestartNeeded = js["coProRestartNeeded"]
            if sof["IFeatureDeviceCoProUpdate"]:
                self.coProUpdateFailure = js["coProUpdateFailure"]
            if sof["IFeatureDeviceOverheated"]:
                self.deviceOverheated = js["deviceOverheated"]
            if sof["IFeatureDeviceOverloaded"]:
                self.deviceOverloaded = js["deviceOverloaded"]
            if sof["IFeatureDeviceTemperatureOutOfRange"]:
                self.temperatureOutOfRange = js["temperatureOutOfRange"]
            if sof["IFeatureDeviceUndervoltage"]:
                self.deviceUndervoltage = js["deviceUndervoltage"]


class SwitchChannel(FunctionalChannel):
    """this is the representative of the SWITCH_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.on = False
        self.powerUpSwitchState = ""
        self.profileMode = None
        self.userDesiredProfileMode = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.on = js["on"]
        self.powerUpSwitchState = (
            js["powerUpSwitchState"] if "powerUpSwitchState" in js else ""
        )
        self.profileMode = js["profileMode"]
        self.userDesiredProfileMode = js["userDesiredProfileMode"]

    def set_switch_state(self, on=True):
        data = {"channelIndex": self.index, "deviceId": self.device.id, "on": on}
        return self._rest_call("device/control/setSwitchState", body=json.dumps(data))

    def turn_on(self):
        return self.set_switch_state(True)

    def turn_off(self):
        return self.set_switch_state(False)

    async def async_set_switch_state(self, on=True):
        return await self._connection.api_call(*self.set_switch_state(on))

    async def async_turn_on(self):
        return await self.async_set_switch_state(True)

    async def async_turn_off(self):
        return await self.async_set_switch_state(False)


class AccelerationSensorChannel(FunctionalChannel):
    """this is the representative of the ACCELERATION_SENSOR_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
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

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("accelerationSensorEventFilterPeriod", js)
        self.set_attr_from_dict("accelerationSensorMode", js, AccelerationSensorMode)
        self.set_attr_from_dict(
            "accelerationSensorNeutralPosition", js, AccelerationSensorNeutralPosition
        )
        self.set_attr_from_dict(
            "accelerationSensorSensitivity", js, AccelerationSensorSensitivity
        )
        self.set_attr_from_dict("accelerationSensorTriggerAngle", js)
        self.set_attr_from_dict("accelerationSensorTriggered", js)
        self.set_attr_from_dict(
            "notificationSoundTypeHighToLow", js, NotificationSoundType
        )
        self.set_attr_from_dict(
            "notificationSoundTypeLowToHigh", js, NotificationSoundType
        )

    def set_acceleration_sensor_mode(self, mode: AccelerationSensorMode):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "accelerationSensorMode": str(mode),
        }
        return self._rest_call(
            "device/configuration/setAccelerationSensorMode", json.dumps(data)
        )

    async def async_set_acceleration_sensor_mode(self, mode):
        return await self._connection.api_call(*self.set_acceleration_sensor_mode(mode))

    def set_acceleration_sensor_neutral_position(
        self, neutralPosition: AccelerationSensorNeutralPosition
    ):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "accelerationSensorNeutralPosition": str(neutralPosition),
        }
        return self._rest_call(
            "device/configuration/setAccelerationSensorNeutralPosition",
            json.dumps(data),
        )

    async def async_set_acceleration_sensor_neutral_position(
        self, neutralPosition: AccelerationSensorNeutralPosition
    ):
        return await self._connection.api_call(
            *self.set_acceleration_sensor_neutral_position(neutralPosition)
        )

    def set_acceleration_sensor_sensitivity(
        self, sensitivity: AccelerationSensorSensitivity
    ):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "accelerationSensorSensitivity": str(sensitivity),
        }
        return self._rest_call(
            "device/configuration/setAccelerationSensorSensitivity", json.dumps(data)
        )

    async def async_set_acceleration_sensor_sensitivity(
        self, sensitivity: AccelerationSensorSensitivity
    ):
        return await self._connection.api_call(
            *self.set_acceleration_sensor_sensitivity(sensitivity)
        )

    def set_acceleration_sensor_trigger_angle(self, angle: int):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "accelerationSensorTriggerAngle": angle,
        }
        return self._rest_call(
            "device/configuration/setAccelerationSensorTriggerAngle", json.dumps(data)
        )

    async def async_set_acceleration_sensor_trigger_angle(self, angle: int):
        return await self._connection.api_call(
            *self.set_acceleration_sensor_trigger_angle(angle)
        )

    def set_acceleration_sensor_event_filter_period(self, period: float):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "accelerationSensorEventFilterPeriod": period,
        }
        return self._rest_call(
            "device/configuration/setAccelerationSensorEventFilterPeriod",
            json.dumps(data),
        )

    async def async_set_acceleration_sensor_event_filter_period(self, period: float):
        return await self._connection.api_call(
            *self.set_acceleration_sensor_event_filter_period(period)
        )

    def set_notification_sound_type(
        self, soundType: NotificationSoundType, isHighToLow: bool
    ):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "notificationSoundType": str(soundType),
            "isHighToLow": isHighToLow,
        }
        return self._rest_call(
            "device/configuration/setNotificationSoundType", json.dumps(data)
        )

    async def async_set_notification_sound_type(
        self, soundType: NotificationSoundType, isHighToLow: bool
    ):
        return await self._connection.api_call(
            *self.set_notification_sound_type(soundType, isHighToLow)
        )


class BlindChannel(FunctionalChannel):
    """this is the representative of the BLIND_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.blindModeActive = False
        self.bottomToTopReferenceTime = 0.0
        self.changeOverDelay = 0.0
        self.delayCompensationValue = 0.0
        self.endpositionAutoDetectionEnabled = False
        self.previousShutterLevel = None
        self.previousSlatsLevel = None
        self.processing = None
        self.profileMode = None
        self.shutterLevel = 0.0
        self.selfCalibrationInProgress = None
        self.supportingDelayCompensation = None
        self.supportingEndpositionAutoDetection = None
        self.supportingSelfCalibration = None
        self.slatsLevel = 0.0
        self.slatsReferenceTime = 0.0
        self.topToBottomReferenceTime = 0.0
        self.userDesiredProfileMode = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)

        self.blindModeActive = js["blindModeActive"]
        self.bottomToTopReferenceTime = js["bottomToTopReferenceTime"]
        self.changeOverDelay = js["changeOverDelay"]
        self.delayCompensationValue = js["delayCompensationValue"]
        self.endpositionAutoDetectionEnabled = js["endpositionAutoDetectionEnabled"]
        self.previousShutterLevel = js["previousShutterLevel"]
        self.previousSlatsLevel = js["previousSlatsLevel"]
        self.processing = js["processing"]
        self.profileMode = js["profileMode"]
        self.shutterLevel = js["shutterLevel"]
        self.slatsLevel = js["slatsLevel"]
        self.selfCalibrationInProgress = js["selfCalibrationInProgress"]
        self.supportingDelayCompensation = js["supportingDelayCompensation"]
        self.supportingEndpositionAutoDetection = js[
            "supportingEndpositionAutoDetection"
        ]
        self.supportingSelfCalibration = js["supportingSelfCalibration"]
        self.slatsReferenceTime = js["slatsReferenceTime"]
        self.topToBottomReferenceTime = js["topToBottomReferenceTime"]
        self.userDesiredProfileMode = js["userDesiredProfileMode"]

    def set_slats_level(self, slatsLevel=0.0, shutterLevel=None):
        """sets the slats and shutter level

        Args:
            slatsLevel(float): the new level of the slats. 0.0 = open, 1.0 = closed,
            shutterLevel(float): the new level of the shutter. 0.0 = open, 1.0 = closed, None = use the current value
            channelIndex(int): the channel to control
        Returns:
            the result of the _restCall
        """
        if shutterLevel is None:
            shutterLevel = self.shutterLevel

        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "slatsLevel": slatsLevel,
            "shutterLevel": shutterLevel,
        }
        return self._rest_call("device/control/setSlatsLevel", json.dumps(data))

    async def async_set_slats_level(self, slatsLevel=0.0, shutterLevel=None):
        return await self._connection.api_call(
            *self.set_slats_level(slatsLevel, shutterLevel)
        )

    def set_shutter_level(self, level=0.0):
        """sets the shutter level

        Args:
            level(float): the new level of the shutter. 0.0 = open, 1.0 = closed
            channelIndex(int): the channel to control
        Returns:
            the result of the _restCall
        """
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "shutterLevel": level,
        }
        return self._rest_call("device/control/setShutterLevel", body=json.dumps(data))

    async def async_set_shutter_level(self, level=0.0):
        return await self._connection.api_call(*self.set_shutter_level(level))

    def stop(self):
        """stops the current shutter operation

        Returns:
            the result of the _restCall
        """
        self.set_shutter_stop()

    async def async_stop(self):
        return self.async_set_shutter_stop()

    def set_shutter_stop(self):
        """stops the current operation
        Returns:
            the result of the _restCall
        """
        data = {"channelIndex": self.index, "deviceId": self.device.id}
        return self._rest_call("device/control/stop", body=json.dumps(data))

    async def async_set_shutter_stop(self):
        return await self._connection.api_call(*self.stop())


class DeviceBaseFloorHeatingChannel(DeviceBaseChannel):
    """this is the representative of the DEVICE_BASE_FLOOR_HEATING channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.coolingEmergencyValue = 0
        self.frostProtectionTemperature = 0.0
        self.heatingEmergencyValue = 0.0
        self.minimumFloorHeatingValvePosition = 0.0
        self.temperatureOutOfRange = False
        self.valveProtectionDuration = 0
        self.valveProtectionSwitchingInterval = 20

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("coolingEmergencyValue", js)
        self.set_attr_from_dict("frostProtectionTemperature", js)
        self.set_attr_from_dict("heatingEmergencyValue", js)
        self.set_attr_from_dict("minimumFloorHeatingValvePosition", js)
        self.set_attr_from_dict("temperatureOutOfRange", js)
        self.set_attr_from_dict("valveProtectionDuration", js)
        self.set_attr_from_dict("valveProtectionSwitchingInterval", js)

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
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "minimumFloorHeatingValvePosition": minimumFloorHeatingValvePosition,
        }
        return self._rest_call(
            "device/configuration/setMinimumFloorHeatingValvePosition",
            body=json.dumps(data),
        )

    async def async_set_minimum_floor_heating_valve_position(
        self, minimumFloorHeatingValvePosition: float
    ):
        return await self._connection.api_call(
            *self.set_minimum_floor_heating_valve_position(
                minimumFloorHeatingValvePosition
            )
        )


class DeviceOperationLockChannel(DeviceBaseChannel):
    """this is the representative of the DEVICE_OPERATIONLOCK channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.operationLockActive = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.operationLockActive = js["operationLockActive"]

    def set_operation_lock(self, operationLock=True):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "operationLock": operationLock,
        }
        return self._rest_call("device/configuration/setOperationLock", json.dumps(data))

    async def async_set_operation_lock(self, operationLock=True):
        return await self._connection.api_call(*self.set_operation_lock(operationLock))


class DeviceOperationLockChannelWithSabotage(DeviceOperationLockChannel):
    """this is the representation of the DeviceOperationLockChannelWithSabotage channel"""

    pass


class DeviceOperationLockChannelWithSabotage(DeviceOperationLockChannel):
    """this is the representation of the DeviceOperationLockChannelWithSabotage channel"""

    pass


class DimmerChannel(FunctionalChannel):
    """this is the representative of the DIMMER_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.dimLevel = 0
        self.profileMode = None
        self.userDesiredProfileMode = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.dimLevel = js["dimLevel"]
        self.profileMode = js["profileMode"]
        self.userDesiredProfileMode = js["userDesiredProfileMode"]

    def set_dim_level(self, dimLevel=0.0):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "dimLevel": dimLevel,
        }
        return self._rest_call("device/control/setDimLevel", json.dumps(data))

    async def async_set_dim_level(self, dimLevel=0.0):
        return await self._connection.api_call(*self.set_dim_level(dimLevel))


class DoorChannel(FunctionalChannel):
    """this is the representative of the DoorChannel channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.doorState = DoorState.POSITION_UNKNOWN
        self.on = False
        self.processing = False
        self.ventilationPositionSupported = True

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.doorState = js["doorState"]
        self.on = js["on"]
        self.processing = js["processing"]
        self.ventilationPositionSupported = js["ventilationPositionSupported"]

    def send_door_command(self, doorCommand=DoorCommand.STOP):
        print(
            f"Device: {self.device.id}; Channel: {self.index}; Command: {doorCommand}"
        )
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "doorCommand": doorCommand,
        }
        return self._rest_call("device/control/sendDoorCommand", json.dumps(data))

    async def async_send_door_command(self, doorCommand=DoorCommand.STOP):
        return await self._connection.api_call(*self.send_door_command(doorCommand))


class DoorLockChannel(FunctionalChannel):
    """This respresents of the DoorLockChannel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.autoRelockDelay = False
        self.doorHandleType = "UNKNOWN"
        self.doorLockDirection = False
        self.doorLockNeutralPosition = False
        self.doorLockTurns = False
        self.lockState = LockState.UNLOCKED
        self.motorState = MotorState.STOPPED

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)

        self.autoRelockDelay = js["autoRelockDelay"]
        self.doorHandleType = js["doorHandleType"]
        self.doorLockDirection = js["doorLockDirection"]
        self.doorLockNeutralPosition = js["doorLockNeutralPosition"]
        self.doorLockTurns = js["doorLockTurns"]
        self.lockState = LockState.from_str(js["lockState"])
        self.motorState = MotorState.from_str(js["motorState"])

    def set_lock_state(self, doorLockState: LockState, pin=""):
        """sets the door lock state

        Args:
            doorLockState(float): the state of the door. See LockState from base/enums.py
            pin(string): Pin, if specified.
            channelIndex(int): the channel to control. Normally the channel from DOOR_LOCK_CHANNEL is used.
        Returns:
            the result of the _restCall
        """
        data = {
            "deviceId": self.device.id,
            "channelIndex": self.index,
            "authorizationPin": pin,
            "targetLockState": doorLockState,
        }
        return self._rest_call("device/control/setLockState", json.dumps(data))

    async def async_set_lock_state(self, doorLockState: LockState, pin=""):
        """sets the door lock state

        Args:
            doorLockState(float): the state of the door. See LockState from base/enums.py
            pin(string): Pin, if specified.
            channelIndex(int): the channel to control. Normally the channel from DOOR_LOCK_CHANNEL is used.
        Returns:
            the result of the _restCall
        """
        return await self._connection.api_call(*self.set_lock_state(doorLockState, pin))


class EnergySensorInterfaceChannel(FunctionalChannel):
    """EnergySensorInterfaceChannel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.connectedEnergySensorType = None
        self.currentGasFlow = None
        self.currentPowerConsumption = None
        self.energyCounterOne = 0.0
        self.energyCounterOneType = ""
        self.energyCounterThree = 0.0
        self.energyCounterThreeType = ""
        self.energyCounterTwo = 0.0
        self.energyCounterTwoType = ""
        self.gasVolume = None
        self.gasVolumePerImpulse = None
        self.impulsesPerKWH = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.connectedEnergySensorType = js["connectedEnergySensorType"]
        self.currentGasFlow = js["currentGasFlow"]
        self.currentPowerConsumption = js["currentPowerConsumption"]
        self.energyCounterOne = js["energyCounterOne"]
        self.energyCounterOneType = js["energyCounterOneType"]
        self.energyCounterThree = js["energyCounterThree"]
        self.energyCounterThreeType = js["energyCounterThreeType"]
        self.energyCounterTwo = js["energyCounterTwo"]
        self.energyCounterTwoType = js["energyCounterTwoType"]
        self.gasVolume = js["gasVolume"]
        self.gasVolumePerImpulse = js["gasVolumePerImpulse"]
        self.impulsesPerKWH = js["impulsesPerKWH"]


class ImpulseOutputChannel(FunctionalChannel):
    """this is the representation of the IMPULSE_OUTPUT_CHANNEL"""

    def __init__(self, device, connection):
        super().__init__(device, connection)

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.impulseDuration = js["impulseDuration"]
        self.processing = js["processing"]

    def send_start_impulse(self):
        """Toggle Wall mounted Garage Door Controller."""
        data = {"channelIndex": self.index, "deviceId": self.device.id}
        return self._rest_call("device/control/startImpulse", body=json.dumps(data))

    async def async_send_start_impulse(self):
        return await self._connection.api_call(*self.send_start_impulse())


class MultiModeInputChannel(FunctionalChannel):
    """this is the representative of the MULTI_MODE_INPUT_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.binaryBehaviorType = BinaryBehaviorType.NORMALLY_OPEN
        self.multiModeInputMode = MultiModeInputMode.BINARY_BEHAVIOR
        self.windowState = WindowState.OPEN
        self.doorBellSensorEventTimestamp = None
        self.corrosionPreventionActive = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("binaryBehaviorType", js, BinaryBehaviorType)
        self.set_attr_from_dict("channelRole", js)
        self.set_attr_from_dict("multiModeInputMode", js, MultiModeInputMode)
        self.set_attr_from_dict("windowState", js, WindowState)
        self.set_attr_from_dict("doorBellSensorEventTimestamp", js)
        self.set_attr_from_dict("corrosionPreventionActive", js)

    def __str__(self):
        return "{} binaryBehaviorType({}) channelRole({}) multiModeInputMode({}) windowState({}) doorBellSensorEventTimestamp({}) corrosionPreventionActive({})".format(
            super().__str__(),
            self.binaryBehaviorType,
            self.channelRole,
            self.multiModeInputMode,
            self.windowState,
            self.doorBellSensorEventTimestamp,
            self.corrosionPreventionActive,
        )


class MultiModeInputDimmerChannel(DimmerChannel):
    """this is the representative of the MULTI_MODE_INPUT_DIMMER_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.binaryBehaviorType = BinaryBehaviorType.NORMALLY_CLOSE
        self.dimLevel = 0
        self.multiModeInputMode = MultiModeInputMode.KEY_BEHAVIOR
        self.on = False
        self.profileMode = ProfileMode.AUTOMATIC
        self.userDesiredProfileMode = ProfileMode.AUTOMATIC

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("binaryBehaviorType", js, BinaryBehaviorType)
        self.set_attr_from_dict("dimLevel", js)
        self.set_attr_from_dict("multiModeInputMode", js, MultiModeInputMode)
        self.set_attr_from_dict("on", js)
        self.set_attr_from_dict("profileMode", js, ProfileMode)
        self.set_attr_from_dict("userDesiredProfileMode", js, ProfileMode)


class MultiModeInputSwitchChannel(SwitchChannel):
    """this is the representative of the MULTI_MODE_INPUT_SWITCH_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.binaryBehaviorType = BinaryBehaviorType.NORMALLY_OPEN
        self.multiModeInputMode = MultiModeInputMode.SWITCH_BEHAVIOR
        self.on = False
        self.profileMode = ProfileMode.MANUAL
        self.userDesiredProfileMode = ProfileMode.MANUAL

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("binaryBehaviorType", js, BinaryBehaviorType)
        self.set_attr_from_dict("multiModeInputMode", js, MultiModeInputMode)
        self.set_attr_from_dict("on", js)
        self.set_attr_from_dict("profileMode", js, ProfileMode)
        self.set_attr_from_dict("userDesiredProfileMode", js, ProfileMode)


class NotificationLightChannel(DimmerChannel, SwitchChannel):
    """this is the representative of the NOTIFICATION_LIGHT_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        #:boolean: is the light turned on?
        self.on = False
        #:RGBColorState:the color of the light
        self.simpleRGBColorState = RGBColorState.BLACK


    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.on = js["on"]
        self.simpleRGBColorState = RGBColorState.from_str(js["simpleRGBColorState"])

        if "opticalSignalBehaviour" in js:
            self.opticalSignalBehaviour = OpticalSignalBehaviour.from_str(js["opticalSignalBehaviour"])


    def set_optical_signal(
        self,
        opticalSignalBehaviour: OpticalSignalBehaviour,
        rgb: RGBColorState,
        dimLevel=1.01,
    ):
        """sets the signal type for the leds

        Args:
            opticalSignalBehaviour(OpticalSignalBehaviour): LED signal behaviour
            rgb(RGBColorState): Color
            dimLevel(float): usally 1.01. Use set_dim_level instead

        Returns:
            Result of the _restCall

        """
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "dimLevel": dimLevel,
            "opticalSignalBehaviour": opticalSignalBehaviour,
            "simpleRGBColorState": rgb,
        }
        return self._rest_call("device/control/setOpticalSignal", body=json.dumps(data))
    
    async def async_set_optical_signal(
        self,
        opticalSignalBehaviour: OpticalSignalBehaviour,
        rgb: RGBColorState,
        dimLevel=1.01,
    ):
        return await self._connection.api_call(
            *self.set_optical_signal(opticalSignalBehaviour, rgb, dimLevel)
        )
    
    def set_rgb_dim_level(self, rgb: RGBColorState, dimLevel: float):
        """sets the color and dimlevel of the lamp

        Args:
            channelIndex(int): the channelIndex of the lamp. Use self.topLightChannelIndex or self.bottomLightChannelIndex
            rgb(RGBColorState): the color of the lamp
            dimLevel(float): the dimLevel of the lamp. 0.0 = off, 1.0 = MAX

        Returns:
            the result of the _restCall
        """
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "simpleRGBColorState": rgb,
            "dimLevel": dimLevel,
        }
        return self._rest_call(
            "device/control/setSimpleRGBColorDimLevel", body=json.dumps(data)
        )

    async def async_set_rgb_dim_level(self, rgb: RGBColorState, dimLevel: float):
        return await self._connection.api_call(*self.set_rgb_dim_level(rgb, dimLevel))

    def set_rgb_dim_level_with_time(
        self,
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
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "simpleRGBColorState": rgb,
            "dimLevel": dimLevel,
            "onTime": onTime,
            "rampTime": rampTime,
        }
        return self._rest_call(
            "device/control/setSimpleRGBColorDimLevelWithTime", body=json.dumps(data)
        )

    async def async_set_rgb_dim_level_with_time(
        self,
        rgb: RGBColorState,
        dimLevel: float,
        onTime: float,
        rampTime: float,
    ):
        return await self._connection.api_call(
            *self.set_rgb_dim_level_with_time(rgb, dimLevel, onTime, rampTime)
        )


class ShadingChannel(FunctionalChannel):
    """this is the representative of the SHADING_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
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

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)

        self.set_attr_from_dict("automationDriveSpeed", js, DriveSpeed)
        self.set_attr_from_dict("manualDriveSpeed", js, DriveSpeed)

        self.set_attr_from_dict("favoritePrimaryShadingPosition", js)
        self.set_attr_from_dict("favoriteSecondaryShadingPosition", js)

        self.set_attr_from_dict("primaryCloseAdjustable", js)
        self.set_attr_from_dict("primaryOpenAdjustable", js)
        self.set_attr_from_dict("primaryShadingStateType", js, ShadingStateType)
        self.set_attr_from_dict("secondaryCloseAdjustable", js)
        self.set_attr_from_dict("secondaryOpenAdjustable", js)
        self.set_attr_from_dict("secondaryShadingStateType", js, ShadingStateType)

        self.set_attr_from_dict("primaryShadingLevel", js)
        self.set_attr_from_dict("secondaryShadingLevel", js)

        self.set_attr_from_dict("previousPrimaryShadingLevel", js)
        self.set_attr_from_dict("previousSecondaryShadingLevel", js)

        self.set_attr_from_dict("identifyOemSupported", js)
        self.set_attr_from_dict("productId", js)

        self.set_attr_from_dict("profileMode", js, ProfileMode)
        self.set_attr_from_dict("userDesiredProfileMode", js, ProfileMode)

        self.set_attr_from_dict("shadingDriveVersion", js)
        self.set_attr_from_dict("shadingPackagePosition", js, ShadingPackagePosition)
        self.set_attr_from_dict("shadingPositionAdjustmentActive", js)
        self.set_attr_from_dict("shadingPositionAdjustmentClientId", js)

    def set_primary_shading_level(self, primaryShadingLevel: float):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "primaryShadingLevel": primaryShadingLevel,
        }
        return self._rest_call("device/control/setPrimaryShadingLevel", json.dumps(data))

    async def async_set_primary_shading_level(self, primaryShadingLevel: float):
        return await self._connection.api_call(
            *self.set_primary_shading_level(primaryShadingLevel)
        )

    def set_secondary_shading_level(
        self, primaryShadingLevel: float, secondaryShadingLevel: float
    ):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "primaryShadingLevel": primaryShadingLevel,
            "secondaryShadingLevel": secondaryShadingLevel,
        }
        return self._rest_call(
            "device/control/setSecondaryShadingLevel", json.dumps(data)
        )

    async def async_set_secondary_shading_level(
        self, primaryShadingLevel: float, secondaryShadingLevel: float
    ):
        return await self._connection.api_call(
            *self.set_secondary_shading_level(
                primaryShadingLevel, secondaryShadingLevel
            )
        )

    def set_shutter_stop(self):
        """stops the current operation
        Returns:
            the result of the _restCall
        """
        data = {"channelIndex": self.index, "deviceId": self.device.id}
        return self._rest_call("device/control/stop", body=json.dumps(data))

    async def async_set_shutter_stop(self):
        return await self._connection.api_call(*self.stop())


class ShutterChannel(FunctionalChannel):
    """this is the representative of the SHUTTER_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
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

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.shutterLevel = js["shutterLevel"]
        self.changeOverDelay = js["changeOverDelay"]
        self.delayCompensationValue = js["delayCompensationValue"]
        self.bottomToTopReferenceTime = js["bottomToTopReferenceTime"]
        self.topToBottomReferenceTime = js["topToBottomReferenceTime"]
        self.endpositionAutoDetectionEnabled = js["endpositionAutoDetectionEnabled"]
        self.previousShutterLevel = js["previousShutterLevel"]
        self.processing = js["processing"]
        self.profileMode = js["profileMode"]
        self.selfCalibrationInProgress = js["selfCalibrationInProgress"]
        self.supportingDelayCompensation = js["supportingDelayCompensation"]
        self.supportingEndpositionAutoDetection = js[
            "supportingEndpositionAutoDetection"
        ]
        self.supportingSelfCalibration = js["supportingSelfCalibration"]
        self.userDesiredProfileMode = js["userDesiredProfileMode"]

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
        return self._rest_call("device/control/setShutterLevel", body=json.dumps(data))

    def set_shutter_stop(self):
        """stops the current shutter operation

        Args:
            channelIndex(int): the channel to control
        Returns:
            the result of the _restCall
        """
        data = {"channelIndex": self.index, "deviceId": self.device.id}
        return self._rest_call("device/control/stop", body=json.dumps(data))

    async def async_set_shutter_stop(self):
        return await self._connection.api_call(*self.set_shutter_stop())

    def set_shutter_level(self, level=0.0):
        """sets the shutter level

        Args:
            level(float): the new level of the shutter. 0.0 = open, 1.0 = closed
        Returns:
            the result of the _restCall
        """
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "shutterLevel": level,
        }
        return self._rest_call("device/control/setShutterLevel", body=json.dumps(data))

    async def async_set_shutter_level(self, level=0.0):
        return await self._connection.api_call(*self.set_shutter_level(level))


class SwitchMeasuringChannel(SwitchChannel):
    """this is the representative of the SWITCH_MEASURING_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.energyCounter = 0
        self.currentPowerConsumption = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.energyCounter = js["energyCounter"]
        self.currentPowerConsumption = js["currentPowerConsumption"]

    def reset_energy_counter(self):
        data = {"channelIndex": self.index, "deviceId": self.device.id}
        return self._rest_call(
            "device/control/resetEnergyCounter", body=json.dumps(data)
        )

    async def async_reset_energy_counter(self):
        return await self._connection.api_call(*self.reset_energy_counter())


class TiltVibrationSensorChannel(FunctionalChannel):
    """this is the representative of the TILT_VIBRATION_SENSOR_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        #:float:
        self.accelerationSensorEventFilterPeriod = 100.0
        #:AccelerationSensorMode:
        self.accelerationSensorMode = AccelerationSensorMode.ANY_MOTION
        #:AccelerationSensorSensitivity:
        self.accelerationSensorSensitivity = (
            AccelerationSensorSensitivity.SENSOR_RANGE_2G
        )
        self.accelerationSensorNeutralPosition = None
        #:int:
        self.accelerationSensorTriggerAngle = 0
        #:bool:
        self.accelerationSensorTriggered = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict(
            "accelerationSensorNeutralPosition", js, AccelerationSensorNeutralPosition
        )
        self.set_attr_from_dict("accelerationSensorEventFilterPeriod", js)
        self.set_attr_from_dict("accelerationSensorMode", js, AccelerationSensorMode)
        self.set_attr_from_dict(
            "accelerationSensorSensitivity", js, AccelerationSensorSensitivity
        )
        self.set_attr_from_dict("accelerationSensorTriggerAngle", js)
        self.set_attr_from_dict("accelerationSensorTriggered", js)

    def set_acceleration_sensor_mode(self, mode: AccelerationSensorMode):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "accelerationSensorMode": str(mode),
        }
        return self._rest_call(
            "device/configuration/setAccelerationSensorMode", json.dumps(data)
        )

    async def async_set_acceleration_sensor_mode(self, mode: AccelerationSensorMode):
        return await self._connection.api_call(*self.set_acceleration_sensor_mode(mode))

    def set_acceleration_sensor_sensitivity(
        self, sensitivity: AccelerationSensorSensitivity
    ):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "accelerationSensorSensitivity": str(sensitivity),
        }
        return self._rest_call(
            "device/configuration/setAccelerationSensorSensitivity", json.dumps(data)
        )

    async def async_set_acceleration_sensor_sensitivity(
        self, sensitivity: AccelerationSensorSensitivity
    ):
        return await self._connection.api_call(
            *self.set_acceleration_sensor_sensitivity(sensitivity)
        )

    def set_acceleration_sensor_trigger_angle(self, angle: int):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "accelerationSensorTriggerAngle": angle,
        }
        return self._rest_call(
            "device/configuration/setAccelerationSensorTriggerAngle", json.dumps(data)
        )

    async def async_set_acceleration_sensor_trigger_angle(self, angle: int):
        return await self._connection.api_call(
            *self.set_acceleration_sensor_trigger_angle(angle)
        )

    def set_acceleration_sensor_event_filter_period(self, period: float):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "accelerationSensorEventFilterPeriod": period,
        }
        return self._rest_call(
            "device/configuration/setAccelerationSensorEventFilterPeriod",
            json.dumps(data),
        )

    async def async_set_acceleration_sensor_event_filter_period(self, period: float):
        return await self._connection.api_call(
            *self.set_acceleration_sensor_event_filter_period(period)
        )


class WallMountedThermostatProChannel(FunctionalChannel):
    """this is the representative of the WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.display = ClimateControlDisplay.ACTUAL
        self.setPointTemperature = 0
        self.temperatureOffset = 0
        self.actualTemperature = 0
        self.humidity = 0
        self.vaporAmount = 0.0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.temperatureOffset = js["temperatureOffset"]
        self.setPointTemperature = js["setPointTemperature"]
        self.display = ClimateControlDisplay.from_str(js["display"])
        self.actualTemperature = js["actualTemperature"]
        self.humidity = js["humidity"]
        self.vaporAmount = js["vaporAmount"]

    def set_display(
        self, display: ClimateControlDisplay = ClimateControlDisplay.ACTUAL
    ):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "display": str(display),
        }
        return self._rest_call(
            "device/configuration/setClimateControlDisplay", json.dumps(data)
        )

    async def async_set_display(
        self, display: ClimateControlDisplay = ClimateControlDisplay.ACTUAL
    ):
        return await self._connection.api_call(*self.set_display(display))


class WaterSensorChannel(FunctionalChannel):
    """this is the representative of the WATER_SENSOR_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)

        self.acousticAlarmSignal = AcousticAlarmSignal.DISABLE_ACOUSTIC_SIGNAL
        self.acousticAlarmTiming = AcousticAlarmTiming.PERMANENT
        self.acousticWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.inAppWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.moistureDetected = False
        self.sirenWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.waterlevelDetected = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.acousticAlarmSignal = AcousticAlarmSignal.from_str(
            js["acousticAlarmSignal"]
        )
        self.acousticAlarmTiming = AcousticAlarmTiming.from_str(
            js["acousticAlarmTiming"]
        )
        self.acousticWaterAlarmTrigger = WaterAlarmTrigger.from_str(
            js["acousticWaterAlarmTrigger"]
        )
        self.inAppWaterAlarmTrigger = WaterAlarmTrigger.from_str(
            js["inAppWaterAlarmTrigger"]
        )
        self.moistureDetected = js["moistureDetected"]
        self.sirenWaterAlarmTrigger = WaterAlarmTrigger.from_str(
            js["sirenWaterAlarmTrigger"]
        )
        self.waterlevelDetected = js["waterlevelDetected"]

    def set_acoustic_alarm_signal(self, acousticAlarmSignal: AcousticAlarmSignal):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "acousticAlarmSignal": str(acousticAlarmSignal),
        }
        return self._rest_call(
            "device/configuration/setAcousticAlarmSignal", json.dumps(data)
        )

    async def async_set_acoustic_alarm_signal(
        self, acousticAlarmSignal: AcousticAlarmSignal
    ):
        return await self._connection.api_call(
            *self.set_acoustic_alarm_signal(acousticAlarmSignal)
        )

    def set_acoustic_alarm_timing(self, acousticAlarmTiming: AcousticAlarmTiming):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "acousticAlarmTiming": str(acousticAlarmTiming),
        }
        return self._rest_call(
            "device/configuration/setAcousticAlarmTiming", json.dumps(data)
        )

    async def async_set_acoustic_alarm_timing(
        self, acousticAlarmTiming: AcousticAlarmTiming
    ):
        return await self._connection.api_call(
            *self.set_acoustic_alarm_timing(acousticAlarmTiming)
        )

    def set_acoustic_water_alarm_trigger(
        self, acousticWaterAlarmTrigger: WaterAlarmTrigger
    ):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "acousticWaterAlarmTrigger": str(acousticWaterAlarmTrigger),
        }
        return self._rest_call(
            "device/configuration/setAcousticWaterAlarmTrigger", json.dumps(data)
        )

    async def async_set_acoustic_water_alarm_trigger(
        self, acousticWaterAlarmTrigger: WaterAlarmTrigger
    ):
        return await self._connection.api_call(
            *self.set_acoustic_water_alarm_trigger(acousticWaterAlarmTrigger)
        )

    def set_inapp_water_alarm_trigger(self, inAppWaterAlarmTrigger: WaterAlarmTrigger):
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "inAppWaterAlarmTrigger": str(inAppWaterAlarmTrigger),
        }
        return self._rest_call(
            "device/configuration/setInAppWaterAlarmTrigger", json.dumps(data)
        )

    async def async_set_inapp_water_alarm_trigger(
        self, inAppWaterAlarmTrigger: WaterAlarmTrigger
    ):
        return await self._connection.api_call(
            *self.set_inapp_water_alarm_trigger(inAppWaterAlarmTrigger)
        )

    def set_siren_water_alarm_trigger(self, sirenWaterAlarmTrigger: WaterAlarmTrigger):
        LOGGER.warning(
            "set_siren_water_alarm_trigger is currently not available in the HMIP App. It might not be available in the cloud yet"
        )
        data = {
            "channelIndex": self.index,
            "deviceId": self.device.id,
            "sirenWaterAlarmTrigger": str(sirenWaterAlarmTrigger),
        }
        return self._rest_call(
            "device/configuration/setSirenWaterAlarmTrigger", json.dumps(data)
        )

    async def async_set_siren_water_alarm_trigger(
        self, sirenWaterAlarmTrigger: WaterAlarmTrigger
    ):
        return await self._connection.api_call(
            *self.set_siren_water_alarm_trigger(sirenWaterAlarmTrigger)
        )


#################
#################
#################


class AccessControllerChannel(DeviceBaseChannel):
    """this is the representative of the ACCESS_CONTROLLER_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.dutyCycleLevel = 0.0
        self.accessPointPriority = 0
        self.signalBrightness = 0
        self.filteredMulticastRoutingEnabled = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("dutyCycleLevel", js)
        self.set_attr_from_dict("accessPointPriority", js)
        self.set_attr_from_dict("signalBrightness", js)
        self.set_attr_from_dict("filteredMulticastRoutingEnabled", js)


class DeviceSabotageChannel(DeviceBaseChannel):
    """this is the representative of the DEVICE_SABOTAGE channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.sabotage = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.sabotage = js["sabotage"]


class DeviceIncorrectPositionedChannel(DeviceBaseChannel):
    """this is the representative of the DEVICE_INCORRECT_POSITIONED channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.incorrectPositioned = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.incorrectPositioned = js["incorrectPositioned"]


class DevicePermanentFullRxChannel(DeviceBaseChannel):
    """this is the representative of the DEVICE_PERMANENT_FULL_RX channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.permanentFullRx = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.permanentFullRx = js["permanentFullRx"]


class AccessAuthorizationChannel(FunctionalChannel):
    """this represents ACCESS_AUTHORIZATION_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.authorized = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.authorized = js["authorized"]


class HeatingThermostatChannel(FunctionalChannel):
    """this is the representative of the HEATING_THERMOSTAT_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
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

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.temperatureOffset = js["temperatureOffset"]
        self.valvePosition = js["valvePosition"]
        self.valveState = ValveState.from_str(js["valveState"])
        self.setPointTemperature = js["setPointTemperature"]
        self.valveActualTemperature = js["valveActualTemperature"]


class ShutterContactChannel(FunctionalChannel):
    """this is the representative of the SHUTTER_CONTACT_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.windowState = WindowState.CLOSED
        self.eventDelay = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.windowState = WindowState.from_str(js["windowState"])
        self.eventDelay = js["eventDelay"]


class RotaryHandleChannel(ShutterContactChannel):
    """this is the representative of the ROTARY_HANDLE_CHANNEL channel"""


class ContactInterfaceChannel(ShutterContactChannel):
    """this is the representative of the CONTACT_INTERFACE_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.alarmContactType = AlarmContactType.WINDOW_DOOR_CONTACT
        self.contactType = ContactType.NORMALLY_CLOSE

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.alarmContactType = AlarmContactType.from_str(js["alarmContactType"])
        self.contactType = ContactType.from_str(js["contactType"])


class ClimateSensorChannel(FunctionalChannel):
    """this is the representative of the CLIMATE_SENSOR_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.actualTemperature = 0
        self.humidity = 0
        self.vaporAmount = 0.0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.actualTemperature = js["actualTemperature"]
        self.humidity = js["humidity"]
        self.vaporAmount = js["vaporAmount"]


class DoorLockSensorChannel(FunctionalChannel):
    """This respresents of the DoorLockSensorChannel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.doorLockDirection = False
        self.doorLockNeutralPosition = False
        self.doorLockTurns = False
        self.lockState = LockState.UNLOCKED

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.doorLockDirection = js["doorLockDirection"]
        self.doorLockNeutralPosition = js["doorLockNeutralPosition"]
        self.doorLockTurns = js["doorLockTurns"]
        self.lockState = LockState.from_str(js["lockState"])


class WallMountedThermostatWithoutDisplayChannel(ClimateSensorChannel):
    """this is the representative of the WALL_MOUNTED_THERMOSTAT_WITHOUT_DISPLAY_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.temperatureOffset = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.temperatureOffset = js["temperatureOffset"]


class AnalogRoomControlChannel(FunctionalChannel):
    """this is the representative of the ANALOG_ROOM_CONTROL_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.actualTemperature = 0
        self.setPointTemperature = 0
        self.temperatureOffset = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("actualTemperature", js)
        self.set_attr_from_dict("setPointTemperature", js)
        self.set_attr_from_dict("temperatureOffset", js)


class SmokeDetectorChannel(FunctionalChannel):
    """this is the representative of the SMOKE_DETECTOR_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.smokeDetectorAlarmType = SmokeDetectorAlarmType.IDLE_OFF

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.smokeDetectorAlarmType = SmokeDetectorAlarmType.from_str(
            js["smokeDetectorAlarmType"]
        )


class DeviceGlobalPumpControlChannel(DeviceBaseChannel):
    """this is the representative of the DEVICE_GLOBAL_PUMP_CONTROL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.globalPumpControl = False
        self.heatingValveType = HeatingValveType.NORMALLY_CLOSE
        self.heatingLoadType = HeatingLoadType.LOAD_BALANCING
        self.frostProtectionTemperature = 0.0
        self.heatingEmergencyValue = 0.0
        self.valveProtectionDuration = 0
        self.valveProtectionSwitchingInterval = 20
        self.coolingEmergencyValue = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.globalPumpControl = js["globalPumpControl"]
        self.heatingValveType = HeatingValveType.from_str(js["heatingValveType"])
        self.heatingLoadType = HeatingLoadType.from_str(js["heatingLoadType"])
        self.coolingEmergencyValue = js["coolingEmergencyValue"]

        self.frostProtectionTemperature = js["frostProtectionTemperature"]
        self.heatingEmergencyValue = js["heatingEmergencyValue"]
        self.valveProtectionDuration = js["valveProtectionDuration"]
        self.valveProtectionSwitchingInterval = js["valveProtectionSwitchingInterval"]


class MotionDetectionChannel(FunctionalChannel):
    """this is the representative of the MOTION_DETECTION_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.currentIllumination = None
        self.motionDetected = None
        self.illumination = None
        self.motionBufferActive = False
        self.motionDetected = False
        self.motionDetectionSendInterval = MotionDetectionSendInterval.SECONDS_30
        self.numberOfBrightnessMeasurements = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.motionDetected = js["motionDetected"]
        self.illumination = js["illumination"]
        self.motionBufferActive = js["motionBufferActive"]
        self.motionDetected = js["motionDetected"]
        self.motionDetectionSendInterval = MotionDetectionSendInterval.from_str(
            js["motionDetectionSendInterval"]
        )
        self.numberOfBrightnessMeasurements = js["numberOfBrightnessMeasurements"]
        self.currentIllumination = js["currentIllumination"]


class PresenceDetectionChannel(FunctionalChannel):
    """this is the representative of the PRESENCE_DETECTION_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.presenceDetected = False
        self.currentIllumination = None
        self.illumination = 0
        self.motionBufferActive = False
        self.motionDetectionSendInterval = MotionDetectionSendInterval.SECONDS_30
        self.numberOfBrightnessMeasurements = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.presenceDetected = js["presenceDetected"]
        self.currentIllumination = js["currentIllumination"]
        self.illumination = js["illumination"]
        self.motionBufferActive = js["motionBufferActive"]
        self.motionDetectionSendInterval = MotionDetectionSendInterval.from_str(
            js["motionDetectionSendInterval"]
        )
        self.numberOfBrightnessMeasurements = js["numberOfBrightnessMeasurements"]


class MultiModeInputBlindChannel(BlindChannel):
    """this is the representative of the MULTI_MODE_INPUT_BLIND_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.binaryBehaviorType = BinaryBehaviorType.NORMALLY_CLOSE
        self.multiModeInputMode = MultiModeInputMode.KEY_BEHAVIOR
        self.favoritePrimaryShadingPosition = 0.0
        self.favoriteSecondaryShadingPosition = 0.0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)

        self.binaryBehaviorType = BinaryBehaviorType.from_str(js["binaryBehaviorType"])
        self.multiModeInputMode = MultiModeInputMode.from_str(js["multiModeInputMode"])
        self.favoritePrimaryShadingPosition = js["favoritePrimaryShadingPosition"]
        self.favoriteSecondaryShadingPosition = js["favoriteSecondaryShadingPosition"]


class WeatherSensorChannel(FunctionalChannel):
    """this is the representative of the WEATHER_SENSOR_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.actualTemperature = 0
        self.humidity = 0
        self.vaporAmount = 0.0
        self.illumination = 0
        self.illuminationThresholdSunshine = 0
        self.storm = False
        self.sunshine = False
        self.todaySunshineDuration = 0
        self.totalSunshineDuration = 0
        self.windSpeed = 0
        self.windValueType = WindValueType.AVERAGE_VALUE
        self.yesterdaySunshineDuration = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.actualTemperature = js["actualTemperature"]
        self.humidity = js["humidity"]
        self.illumination = js["illumination"]
        self.illuminationThresholdSunshine = js["illuminationThresholdSunshine"]
        self.storm = js["storm"]
        self.sunshine = js["sunshine"]
        self.todaySunshineDuration = js["todaySunshineDuration"]
        self.totalSunshineDuration = js["totalSunshineDuration"]
        self.windSpeed = js["windSpeed"]
        self.windValueType = WindValueType.from_str(js["windValueType"])
        self.yesterdaySunshineDuration = js["yesterdaySunshineDuration"]
        self.vaporAmount = js["vaporAmount"]


class WeatherSensorPlusChannel(WeatherSensorChannel):
    """this is the representative of the WEATHER_SENSOR_PLUS_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.raining = False
        self.todayRainCounter = 0
        self.totalRainCounter = 0
        self.yesterdayRainCounter = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.raining = js["raining"]
        self.todayRainCounter = js["todayRainCounter"]
        self.totalRainCounter = js["totalRainCounter"]
        self.yesterdayRainCounter = js["yesterdayRainCounter"]


class WeatherSensorProChannel(WeatherSensorPlusChannel):
    """this is the representative of the WEATHER_SENSOR_PRO_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.weathervaneAlignmentNeeded = False
        self.windDirection = 0
        self.windDirectionVariation = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.weathervaneAlignmentNeeded = js["weathervaneAlignmentNeeded"]
        self.windDirection = js["windDirection"]
        self.windDirectionVariation = js["windDirectionVariation"]


class SingleKeyChannel(FunctionalChannel):
    """this is the representative of the SINGLE_KEY_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.acousticSendStateEnabled = None
        self.actionParameter = None
        self.doorBellSensorEventTimestamp = None
        self.doublePressTime = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("acousticSendStateEnabled", js)
        self.set_attr_from_dict("actionParameter", js)
        self.set_attr_from_dict("doorBellSensorEventTimestamp", js)
        self.set_attr_from_dict("doublePressTime", js)


class AlarmSirenChannel(FunctionalChannel):
    """this is the representative of the ALARM_SIREN_CHANNEL channel"""


class FloorTeminalBlockChannel(FunctionalChannel):
    """this is the representative of the FLOOR_TERMINAL_BLOCK_CHANNEL channel"""


class FloorTerminalBlockLocalPumpChannel(FunctionalChannel):
    """this is the representative of the FLOOR_TERMINAL_BLOCK_LOCAL_PUMP_CHANNEL  channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.pumpFollowUpTime = 0
        self.pumpLeadTime = 0
        self.pumpProtectionDuration = 0
        self.pumpProtectionSwitchingInterval = 20

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.pumpFollowUpTime = js["pumpFollowUpTime"]
        self.pumpLeadTime = js["pumpLeadTime"]
        self.pumpProtectionDuration = js["pumpProtectionDuration"]
        self.pumpProtectionSwitchingInterval = js["pumpProtectionSwitchingInterval"]


class HeatDemandChannel(FunctionalChannel):
    """this is the representative of the HEAT_DEMAND_CHANNEL channel"""


class DehumidifierDemandChannel(FunctionalChannel):
    """this is the representative of the DEHUMIDIFIER_DEMAND_CHANNEL channel"""


class PassageDetectorChannel(FunctionalChannel):
    """this is the representative of the PASSAGE_DETECTOR_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.leftCounter = 0
        self.leftRightCounterDelta = 0
        self.passageBlindtime = 0.0
        self.passageDirection = PassageDirection.RIGHT
        self.passageSensorSensitivity = 0.0
        self.passageTimeout = 0.0
        self.rightCounter = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.leftCounter = js["leftCounter"]
        self.leftRightCounterDelta = js["leftRightCounterDelta"]
        self.passageBlindtime = js["passageBlindtime"]
        self.passageDirection = PassageDirection.from_str(js["passageDirection"])
        self.passageSensorSensitivity = js["passageSensorSensitivity"]
        self.passageTimeout = js["passageTimeout"]
        self.rightCounter = js["rightCounter"]


class InternalSwitchChannel(FunctionalChannel):
    """this is the representative of the INTERNAL_SWITCH_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.frostProtectionTemperature = 0
        self.heatingValveType = HeatingValveType.NORMALLY_CLOSE
        self.internalSwitchOutputEnabled = False
        self.valveProtectionDuration = 0
        self.valveProtectionSwitchingInterval = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.frostProtectionTemperature = js["frostProtectionTemperature"]
        self.heatingValveType = HeatingValveType.from_str(js["heatingValveType"])
        self.internalSwitchOutputEnabled = js["internalSwitchOutputEnabled"]
        self.valveProtectionDuration = js["valveProtectionDuration"]
        self.valveProtectionSwitchingInterval = js["valveProtectionSwitchingInterval"]

    def __str__(self):
        return "{} frostProtectionTemperature({}) heatingValveType({}) internalSwitchOutputEnabled({}) valveProtectionDuration({}) valveProtectionSwitchingInterval({})".format(
            super().__str__(),
            self.frostProtectionTemperature,
            self.heatingValveType,
            self.internalSwitchOutputEnabled,
            self.valveProtectionDuration,
            self.valveProtectionSwitchingInterval,
        )


class LightSensorChannel(FunctionalChannel):
    """this is the representative of the LIGHT_SENSOR_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        #:float:the average illumination value
        self.averageIllumination = 0.0
        #:float:the current illumination value
        self.currentIllumination = 0.0
        #:float:the highest illumination value
        self.highestIllumination = 0.0
        #:float:the lowest illumination value
        self.lowestIllumination = 0.0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.averageIllumination = js["averageIllumination"]
        self.currentIllumination = js["currentIllumination"]
        self.highestIllumination = js["highestIllumination"]
        self.lowestIllumination = js["lowestIllumination"]


class GenericInputChannel(FunctionalChannel):
    """this is the representative of the GENERIC_INPUT_CHANNEL channel"""


class AnalogOutputChannel(FunctionalChannel):
    """this is the representative of the ANALOG_OUTPUT_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        #:float:the analog output level (Volt?)
        self.analogOutputLevel = 0.0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.analogOutputLevel = js["analogOutputLevel"]


class DeviceRechargeableWithSabotage(DeviceSabotageChannel):
    """this is the representative of the DEVICE_RECHARGEABLE_WITH_SABOTAGE channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        #:bool:is the battery in a bad condition
        self.badBatteryHealth = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("badBatteryHealth", js)


class FloorTerminalBlockMechanicChannel(FunctionalChannel):
    """this is the representative of the class FLOOR_TERMINAL_BLOCK_MECHANIC_CHANNEL(FunctionalChannel) channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        #:ValveState:the current valve state
        self.valveState = ValveState.ADAPTION_DONE
        self.valvePosition = 0.0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("valveState", js, ValveState)
        if "valvePosition" in js:
            self.set_attr_from_dict("valvePosition", js)


class ChangeOverChannel(FunctionalChannel):
    """this is the representative of the CHANGE_OVER_CHANNEL channel"""


class MainsFailureChannel(FunctionalChannel):
    """this is the representative of the MAINS_FAILURE_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.powerMainsFailure = False
        self.genericAlarmSignal = AlarmSignalType.NO_ALARM

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("powerMainsFailure", js)
        self.set_attr_from_dict("genericAlarmSignal", js, AlarmSignalType)


class UniversalActuatorChannel(FunctionalChannel):
    """this is the representative of the UniversalActuatorChannel UNIVERSAL_ACTUATOR_CHANNEL"""

    def __init__(self, device, connection):
        super().__init__(device, connection)

        self.channelRole = None  # String
        self.dimLevel = 0.0
        self.on = True
        self.profileMode = None  # String "AUTOMATIC",
        self.relayMode = None  # "RELAY_INACTIVE"
        self.userDesiredProfileMode = None  # "AUTOMATIC"
        self.ventilationLevel = 0.0  # 0.35,
        self.ventilationState = None  # "VENTILATION"

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.channelRole = js["channelRole"]
        self.dimLevel = js["dimLevel"]
        self.on = js["on"]
        self.profileMode = js["profileMode"]
        self.relayMode = js["relayMode"]
        self.userDesiredProfileMode = js["userDesiredProfileMode"]
        self.ventilationLevel = js["ventilationLevel"]
        self.ventilationState = js["ventilationState"]

    def __str__(self):
        return "{} channelRole({}) dimLevel({}) ventilationLevel({}) ventilationState({}) on({}) profileMode({}) relayMode({})".format(
            super().__str__(),
            self.channelRole,
            self.dimLevel,
            self.ventilationLevel,
            self.ventilationState,
            self.on,
            self.profileMode,
            self.relayMode,
        )
    


class RainDetectionChannel(FunctionalChannel):
    """this is the representative of the TILT_VIBRATION_SENSOR_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        #:float:
        self.rainSensorSensitivity = 0
        #:bool:
        self.raining = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("rainSensorSensitivity", js)
        self.set_attr_from_dict("raining", js)


class TemperatureDifferenceSensor2Channel(FunctionalChannel):
    """this is the representative of the TEMPERATURE_SENSOR_2_EXTERNAL_DELTA_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        #:float:
        self.temperatureExternalDelta = 0.0
        #:float:
        self.temperatureExternalOne = 0.0
        #:float:
        self.temperatureExternalTwo = 0.0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("temperatureExternalDelta", js)
        self.set_attr_from_dict("temperatureExternalOne", js)
        self.set_attr_from_dict("temperatureExternalTwo", js)


class ExternalBaseChannel(FunctionalChannel):
    """this represents the EXTERNAL_BASE_CHANNEL function-channel for external devices"""

    def __init__(self, device, connection):
        super().__init__(device, connection)

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)


class ExternalUniversalLightChannel(FunctionalChannel):
    """this represents the EXTERNAL_UNIVERSAL_LIGHT_CHANNEL function-channel for external devices"""

    def __init__(self, device, connection):
        super().__init__(device, connection)

        self.channelRole = ""
        self.colorTemperature = 0
        self.dimLevel = 0.0
        self.hue = None
        self.maximumColorTemperature = 0
        self.minimalColorTemperature = 0
        self.on = None
        self.saturationLevel = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)

        self.set_attr_from_dict("channelRole", js)
        self.set_attr_from_dict("colorTemperature", js)
        self.set_attr_from_dict("dimLevel", js)
        self.set_attr_from_dict("hue", js)
        self.set_attr_from_dict("maximumColorTemperature", js)
        self.set_attr_from_dict("minimalColorTemperature", js)
        self.set_attr_from_dict("on", js)
        self.set_attr_from_dict("saturationLevel", js)


class OpticalSignalChannel(FunctionalChannel):
    """this class represents the OPTICAL_SIGNAL_CHANNEL"""

    def __init__(self, device, connection):
        super().__init__(device, connection)

        self.dimLevel = -1
        self.on = None
        self.opticalSignalBehaviour = None
        self.powerUpSwitchState = None
        self.profileMode = None
        self.simpleRGBColorState = None
        self.profileMode = None
        self.userDesiredProfileMode = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)

        self.set_attr_from_dict("dimLevel", js)
        self.set_attr_from_dict("on", js)
        self.set_attr_from_dict("opticalSignalBehaviour", js, OpticalSignalBehaviour)
        self.set_attr_from_dict("powerUpSwitchState", js)
        self.set_attr_from_dict("profileMode", js)
        self.simpleRGBColorState = RGBColorState.from_str(js["simpleRGBColorState"])
        self.set_attr_from_dict("userDesiredProfileMode", js)

    def __str__(self):
        return "{} dimLevel({}) on({}) opticalSignalBehaviour({}) powerUpSwitchState({}) profileMode({}) simpleRGBColorState({}) userDesiredProfileMode({})".format(
            super().__str__(),
            self.dimLevel,
            self.on,
            self.opticalSignalBehaviour,
            self.powerUpSwitchState,
            self.profileMode,
            self.simpleRGBColorState,
            self.userDesiredProfileMode,
        )


class CarbonDioxideSensorChannel(FunctionalChannel):
    """Representation of the CarbonDioxideSensorChannel Channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.actualTemperature = None
        self.carbonDioxideConcentration = None
        self.carbonDioxideVisualisationEnabled = None
        self.humidity = None
        self.vaporAmount = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("actualTemperature", js)
        self.set_attr_from_dict("carbonDioxideConcentration", js)
        self.set_attr_from_dict("carbonDioxideVisualisationEnabled", js)
        self.set_attr_from_dict("humidity", js)
        self.set_attr_from_dict("vaporAmount", js)


class AccessControllerWiredChannel(DeviceBaseChannel):
    """this is the representative of the ACCESS_CONTROLLER_WIRED_CHANNEL channel"""

    def __init__(self, device, connection):
        super().__init__(device, connection)
        self.accessPointPriority = None
        self.busConfigMismatch = None
        self.busMode = None
        self.controlsMountingOrientation = None
        self.deviceCommunicationError = None
        self.deviceDriveError = None
        self.deviceDriveModeError = None
        self.deviceOperationMode = None
        self.devicePowerFailureDetected = None
        self.displayContrast = None
        self.index = None
        self.label = None
        self.lockJammed = None
        self.mountingOrientation = None
        self.multicastRoutingEnabled = None
        self.particulateMatterSensorCommunicationError = None
        self.particulateMatterSensorError = None
        self.powerShortCircuit = None
        self.powerSupplyCurrent = None
        self.profilePeriodLimitReached = None
        self.shortCircuitDataLine = None
        self.signalBrightness = 0.0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("accessPointPriority", js)
        self.set_attr_from_dict("busConfigMismatch", js)
        self.set_attr_from_dict("busMode", js)
        self.set_attr_from_dict("controlsMountingOrientation", js)
        self.set_attr_from_dict("deviceCommunicationError", js)
        self.set_attr_from_dict("deviceDriveError", js)
        self.set_attr_from_dict("deviceDriveModeError", js)
        self.set_attr_from_dict("deviceOperationMode", js)
        self.set_attr_from_dict("devicePowerFailureDetected", js)
        self.set_attr_from_dict("displayContrast", js)
        self.set_attr_from_dict("index", js)
        self.set_attr_from_dict("label", js)
        self.set_attr_from_dict("lockJammed", js)
        self.set_attr_from_dict("mountingOrientation", js)
        self.set_attr_from_dict("multicastRoutingEnabled", js)
        self.set_attr_from_dict("particulateMatterSensorCommunicationError", js)
        self.set_attr_from_dict("particulateMatterSensorError", js)
        self.set_attr_from_dict("powerShortCircuit", js)
        self.set_attr_from_dict("powerSupplyCurrent", js)
        self.set_attr_from_dict("profilePeriodLimitReached", js)
        self.set_attr_from_dict("shortCircuitDataLine", js)
        self.set_attr_from_dict("signalBrightness", js)


class OpticalSignalGroupChannel(FunctionalChannel):
    """this class represents the OPTICAL_SIGNAL_GROUP_CHANNEL"""

    def __init__(self, device, connection):
        super().__init__(device, connection)

        self.dimLevel = -1
        self.on = None
        self.opticalSignalBehaviour = None
        self.powerUpSwitchState = None
        self.profileMode = None
        self.simpleRGBColorState = None
        self.profileMode = None
        self.userDesiredProfileMode = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)

        self.set_attr_from_dict("dimLevel", js)
        self.set_attr_from_dict("on", js)
        self.set_attr_from_dict("opticalSignalBehaviour", js, OpticalSignalBehaviour)
        self.set_attr_from_dict("powerUpSwitchState", js)
        self.set_attr_from_dict("profileMode", js)
        self.simpleRGBColorState = RGBColorState.from_str(js["simpleRGBColorState"])
        self.set_attr_from_dict("userDesiredProfileMode", js)

    def __str__(self):
        return "{} dimLevel({}) on({}) opticalSignalBehaviour({}) powerUpSwitchState({}) profileMode({}) simpleRGBColorState({}) userDesiredProfileMode({})".format(
            super().__str__(),
            self.dimLevel,
            self.on,
            self.opticalSignalBehaviour,
            self.powerUpSwitchState,
            self.profileMode,
            self.simpleRGBColorState,
            self.userDesiredProfileMode,
        )


class UniversalLightChannel(FunctionalChannel):
    """Represents Universal Light Channel."""

    def __init__(self, device, connection):
        super().__init__(device, connection)

        self.channelRole: str = None
        self.colorTemperature: int = None
        self.controlGearFailure: str = None
        self.dim2WarmActive: bool = None
        self.dimLevel: float = None
        self.hardwareColorTemperatureColdWhite: int = None
        self.hardwareColorTemperatureWarmWhite: int = None
        self.hue: bool = None
        self.humanCentricLightActive: bool = None
        self.lampFailure: bool = None
        self.lightSceneId: int = None
        self.limitFailure: Any = None
        self.maximumColorTemperature: int = None
        self.minimalColorTemperature: int = None
        self.on: bool = None
        self.onMinLevel: float = None
        self.profileMode: ProfileMode = None
        self.saturationLevel: float = None
        
    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)

        self.set_attr_from_dict("channelRole", js)
        self.set_attr_from_dict("colorTemperature", js)
        self.set_attr_from_dict("controlGearFailure", js)
        self.set_attr_from_dict("dim2WarmActive", js)
        self.set_attr_from_dict("dimLevel", js)
        self.set_attr_from_dict("hardwareColorTemperatureColdWhite", js)
        self.set_attr_from_dict("hardwareColorTemperatureWarmWhite", js)
        self.set_attr_from_dict("hue", js)
        self.set_attr_from_dict("humanCentricLightActive", js)
        self.set_attr_from_dict("lampFailure", js)
        self.set_attr_from_dict("lightSceneId", js)
        self.set_attr_from_dict("limitFailure", js)
        self.set_attr_from_dict("maximumColorTemperature", js)
        self.set_attr_from_dict("minimalColorTemperature", js)
        self.set_attr_from_dict("on", js)
        self.set_attr_from_dict("onMinLevel", js)
        self.set_attr_from_dict("profileMode", js, ProfileMode)
        self.set_attr_from_dict("saturationLevel", js)


class UniversalLightChannelGroup(UniversalLightChannel):
    """Universal-Light-Channel-Group."""


    def __init__(self, device, connection):
        super().__init__(device, connection)
        
        self.channelSelections: list = []

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)

        self.set_attr_from_dict("channelSelections", js)