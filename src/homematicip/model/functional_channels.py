
#
#
# @RegisterFunctionalChannel("DEVICE_BASE")
# class DeviceBaseChannel(FunctionalChannel):
#     """this is the representative of the DEVICE_BASE channel"""
#
#     coProFaulty: Optional[bool] = None
#     coProRestartNeeded: Optional[bool] = None
#     coProUpdateFailure: Optional[bool] = None
#     configPending: Optional[bool] = None
#     deviceOverheated: Optional[bool] = None
#     deviceOverloaded: Optional[bool] = None
#     deviceUndervoltage: Optional[bool] = None
#     dutyCycle: Optional[bool] = None
#     lowBat: Optional[bool] = None
#     routerModuleEnabled: Optional[bool] = None
#     routerModuleSupported: Optional[bool] = None
#     rssiDeviceValue: Optional[int] = None
#     rssiPeerValue: Optional[int] = None
#     temperatureOutOfRange: Optional[bool] = None
#     unreach: Optional[bool] = None
#
#
# @RegisterFunctionalChannel("SWITCH_CHANNEL")
# class SwitchChannel(FunctionalChannel):
#     """this is the representative of the SWITCH_CHANNEL channel"""
#
#     on: Optional[bool] = False
#     powerUpSwitchState: Optional[str] = ""
#     profileMode: Optional[str] = None
#     userDesiredProfileMode: Optional[str] = None
#
#     def set_switch_state(self, on=True):
#         data = {"channelIndex": self.index, "deviceId": self.device.id, "on": on}
#         return self._rest_call("device/control/setSwitchState", body=json.dumps(data))
#
#     def turn_on(self):
#         return self.set_switch_state(True)
#
#     def turn_off(self):
#         return self.set_switch_state(False)
#
#     async def async_set_switch_state(self, on=True):
#         return await self._connection.api_call(*self.set_switch_state(on))
#
#     async def async_turn_on(self):
#         return await self.async_set_switch_state(True)
#
#     async def async_turn_off(self):
#         return await self.async_set_switch_state(False)
#
#
# @RegisterFunctionalChannel("ACCELERATION_SENSOR_CHANNEL")
# class AccelerationSensorChannel(FunctionalChannel):
#     """this is the representative of the ACCELERATION_SENSOR_CHANNEL channel"""
#
#     accelerationSensorEventFilterPeriod: Optional[float] = 100.0
#     accelerationSensorMode: Optional[AccelerationSensorMode] = None
#     accelerationSensorNeutralPosition: Optional[AccelerationSensorNeutralPosition] = None
#     accelerationSensorSensitivity: Optional[AccelerationSensorSensitivity] = None
#     accelerationSensorTriggerAngle: Optional[int] = 0
#     accelerationSensorTriggered: Optional[bool] = False
#     notificationSoundTypeHighToLow: Optional[NotificationSoundType] = None
#     notificationSoundTypeLowToHigh: Optional[NotificationSoundType] = None
#
#     def set_acceleration_sensor_mode(self, mode: AccelerationSensorMode):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "accelerationSensorMode": str(mode),
#         }
#         return self._rest_call(
#             "device/configuration/setAccelerationSensorMode", json.dumps(data)
#         )
#
#     async def async_set_acceleration_sensor_mode(self, mode):
#         return await self._connection.api_call(*self.set_acceleration_sensor_mode(mode))
#
#     def set_acceleration_sensor_neutral_position(
#             self, neutralPosition: AccelerationSensorNeutralPosition
#     ):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "accelerationSensorNeutralPosition": str(neutralPosition),
#         }
#         return self._rest_call(
#             "device/configuration/setAccelerationSensorNeutralPosition",
#             json.dumps(data),
#         )
#
#     async def async_set_acceleration_sensor_neutral_position(
#             self, neutralPosition: AccelerationSensorNeutralPosition
#     ):
#         return await self._connection.api_call(
#             *self.set_acceleration_sensor_neutral_position(neutralPosition)
#         )
#
#     def set_acceleration_sensor_sensitivity(
#             self, sensitivity: AccelerationSensorSensitivity
#     ):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "accelerationSensorSensitivity": str(sensitivity),
#         }
#         return self._rest_call(
#             "device/configuration/setAccelerationSensorSensitivity", json.dumps(data)
#         )
#
#     async def async_set_acceleration_sensor_sensitivity(
#             self, sensitivity: AccelerationSensorSensitivity
#     ):
#         return await self._connection.api_call(
#             *self.set_acceleration_sensor_sensitivity(sensitivity)
#         )
#
#     def set_acceleration_sensor_trigger_angle(self, angle: int):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "accelerationSensorTriggerAngle": angle,
#         }
#         return self._rest_call(
#             "device/configuration/setAccelerationSensorTriggerAngle", json.dumps(data)
#         )
#
#     async def async_set_acceleration_sensor_trigger_angle(self, angle: int):
#         return await self._connection.api_call(
#             *self.set_acceleration_sensor_trigger_angle(angle)
#         )
#
#     def set_acceleration_sensor_event_filter_period(self, period: float):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "accelerationSensorEventFilterPeriod": period,
#         }
#         return self._rest_call(
#             "device/configuration/setAccelerationSensorEventFilterPeriod",
#             json.dumps(data),
#         )
#
#     async def async_set_acceleration_sensor_event_filter_period(self, period: float):
#         return await self._connection.api_call(
#             *self.set_acceleration_sensor_event_filter_period(period)
#         )
#
#     def set_notification_sound_type(
#             self, soundType: NotificationSoundType, isHighToLow: bool
#     ):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "notificationSoundType": str(soundType),
#             "isHighToLow": isHighToLow,
#         }
#         return self._rest_call(
#             "device/configuration/setNotificationSoundType", json.dumps(data)
#         )
#
#     async def async_set_notification_sound_type(
#             self, soundType: NotificationSoundType, isHighToLow: bool
#     ):
#         return await self._connection.api_call(
#             *self.set_notification_sound_type(soundType, isHighToLow)
#         )
#
#
# @RegisterFunctionalChannel("BLIND_CHANNEL")
# class BlindChannel(FunctionalChannel):
#     """this is the representative of the BLIND_CHANNEL channel"""
#
#     blindModeActive: Optional[bool] = False
#     bottomToTopReferenceTime: Optional[float] = 0.0
#     changeOverDelay: Optional[float] = 0.0
#     delayCompensationValue: Optional[float] = 0.0
#     endpositionAutoDetectionEnabled: Optional[bool] = False
#     previousShutterLevel: Optional[float] = None
#     previousSlatsLevel: Optional[float] = None
#     processing: Optional[bool] = None
#     profileMode: Optional[str] = None
#     shutterLevel: Optional[float] = 0.0
#     selfCalibrationInProgress: Optional[bool] = None
#     supportingDelayCompensation: Optional[bool] = None
#     supportingEndpositionAutoDetection: Optional[bool] = None
#     supportingSelfCalibration: Optional[bool] = None
#     slatsLevel: Optional[float] = 0.0
#     slatsReferenceTime: Optional[float] = 0.0
#     topToBottomReferenceTime: Optional[float] = 0.0
#     userDesiredProfileMode: Optional[str] = None
#
#     def set_slats_level(self, slats_level=0.0, shutter_level=None):
#         """sets the slats and shutter level
#
#         Args:
#             slats_level(float): the new level of the slats. 0.0 = open, 1.0 = closed,
#             shutter_level(float): the new level of the shutter. 0.0 = open, 1.0 = closed, None = use the current value
#         Returns:
#             the result of the _restCall
#         """
#         if shutter_level is None:
#             shutter_level = self.shutterLevel
#
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "slatsLevel": slats_level,
#             "shutterLevel": shutter_level,
#         }
#         return self._rest_call("device/control/setSlatsLevel", json.dumps(data))
#
#     async def async_set_slats_level(self, slats_level=0.0, shutter_level=None):
#         return await self._connection.api_call(
#             *self.set_slats_level(slats_level, shutter_level)
#         )
#
#     def set_shutter_level(self, level=0.0):
#         """sets the shutter level
#
#         Args:
#             level(float): the new level of the shutter. 0.0 = open, 1.0 = closed
#         Returns:
#             the result of the _restCall
#         """
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "shutterLevel": level,
#         }
#         return self._rest_call("device/control/setShutterLevel", body=json.dumps(data))
#
#     async def async_set_shutter_level(self, level=0.0):
#         return await self._connection.api_call(*self.set_shutter_level(level))
#
#     def stop(self):
#         """stops the current shutter operation
#
#         Returns:
#             the result of the _restCall
#         """
#         self.set_shutter_stop()
#
#     async def async_stop(self):
#         return self.async_set_shutter_stop()
#
#     def set_shutter_stop(self):
#         """stops the current operation
#         Returns:
#             the result of the _restCall
#         """
#         data = {"channelIndex": self.index, "deviceId": self.device.id}
#         return self._rest_call("device/control/stop", body=json.dumps(data))
#
#     async def async_set_shutter_stop(self):
#         return await self._connection.api_call(*self.stop())
#
#
# @RegisterFunctionalChannel("DEVICE_BASE_FLOOR_HEATING")
# class DeviceBaseFloorHeatingChannel(DeviceBaseChannel):
#     """this is the representative of the DEVICE_BASE_FLOOR_HEATING channel"""
#
#     coolingEmergencyValue: Optional[int] = 0
#     frostProtectionTemperature: Optional[float] = 0.0
#     heatingEmergencyValue: Optional[float] = 0.0
#     minimumFloorHeatingValvePosition: Optional[float] = 0.0
#     temperatureOutOfRange: Optional[bool] = False
#     valveProtectionDuration: Optional[int] = 0
#     valveProtectionSwitchingInterval: Optional[int] = 20
#
#     def set_minimum_floor_heating_valve_position(
#             self, minimumFloorHeatingValvePosition: float
#     ):
#         """sets the minimum floot heating valve position
#
#         Args:
#             minimumFloorHeatingValvePosition(float): the minimum valve position. must be between 0.0 and 1.0
#
#         Returns:
#             the result of the _restCall
#         """
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "minimumFloorHeatingValvePosition": minimumFloorHeatingValvePosition,
#         }
#         return self._rest_call(
#             "device/configuration/setMinimumFloorHeatingValvePosition",
#             body=json.dumps(data),
#         )
#
#     async def async_set_minimum_floor_heating_valve_position(
#             self, minimumFloorHeatingValvePosition: float
#     ):
#         return await self._connection.api_call(
#             *self.set_minimum_floor_heating_valve_position(
#                 minimumFloorHeatingValvePosition
#             )
#         )
#
#
# @RegisterFunctionalChannel("DEVICE_OPERATIONLOCK")
# class DeviceOperationLockChannel(DeviceBaseChannel):
#     """this is the representative of the DEVICE_OPERATIONLOCK channel"""
#
#     operationLockActive: Optional[bool] = False
#
#     def set_operation_lock(self, operationLock=True):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "operationLock": operationLock,
#         }
#         return self._rest_call(
#             "device/configuration/setOperationLock", json.dumps(data)
#         )
#
#     async def async_set_operation_lock(self, operationLock=True):
#         return await self._connection.api_call(*self.set_operation_lock(operationLock))
#
#
# @RegisterFunctionalChannel("DEVICE_OPERATIONLOCK_WITH_SABOTAGE")
# class DeviceOperationLockChannelWithSabotage(DeviceOperationLockChannel):
#     """this is the representation of the DeviceOperationLockChannelWithSabotage channel"""
#
#     pass
#
#
# @RegisterFunctionalChannel("DIMMER_CHANNEL")
# class DimmerChannel(FunctionalChannel):
#     """this is the representative of the DIMMER_CHANNEL channel"""
#
#     dimLevel: Optional[float] = 0
#     profileMode: Optional[str] = None
#     userDesiredProfileMode: Optional[str] = None
#
#     def set_dim_level(self, dim_level=0.0):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "dimLevel": dim_level,
#         }
#         return self._rest_call("device/control/setDimLevel", json.dumps(data))
#
#     async def async_set_dim_level(self, dim_level=0.0):
#         return await self._connection.api_call(*self.set_dim_level(dim_level))
#
#
# @RegisterFunctionalChannel("DOOR_CHANNEL")
# class DoorChannel(FunctionalChannel):
#     """this is the representative of the DoorChannel channel"""
#
#     doorState: DoorState = DoorState.POSITION_UNKNOWN
#     on: Optional[bool] = False
#     processing: Optional[bool] = False
#     ventilationPositionSupported: Optional[bool] = True
#
#     def send_door_command(self, door_command=DoorCommand.STOP):
#         print(
#             f"Device: {self.device.id}; Channel: {self.index}; Command: {door_command}"
#         )
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "doorCommand": door_command,
#         }
#         return self._rest_call("device/control/sendDoorCommand", json.dumps(data))
#
#     async def async_send_door_command(self, door_command=DoorCommand.STOP):
#         return await self._connection.api_call(*self.send_door_command(door_command))
#
#
# @RegisterFunctionalChannel("DOOR_LOCK_CHANNEL")
# class DoorLockChannel(FunctionalChannel):
#     """This respresents of the DoorLockChannel"""
#
#     autoRelockDelay: Optional[float] = None
#     doorHandleType: Optional[str] = "UNKNOWN"
#     doorLockDirection: Optional[str] = None
#     doorLockNeutralPosition: Optional[str] = None
#     doorLockTurns: Optional[int] = None
#     lockState: Optional[LockState] = LockState.UNLOCKED
#     motorState: Optional[MotorState] = MotorState.STOPPED
#
#     def set_lock_state(self, door_lock_state: LockState, pin=""):
#         """sets the door lock state
#
#         Args:
#             door_lock_state(LockState): the state of the door. See LockState from base/enums.py
#             pin(string): Pin, if specified.
#         Returns:
#             the result of the _restCall
#         """
#         data = {
#             "deviceId": self.device.id,
#             "channelIndex": self.index,
#             "authorizationPin": pin,
#             "targetLockState": door_lock_state,
#         }
#         return self._rest_call("device/control/setLockState", json.dumps(data))
#
#     async def async_set_lock_state(self, door_lock_state: LockState, pin=""):
#         """sets the door lock state
#
#         Args:
#             door_lock_state(float): the state of the door. See LockState from base/enums.py
#             pin(string): Pin, if specified.
#         Returns:
#             the result of the _restCall
#         """
#         return await self._connection.api_call(*self.set_lock_state(door_lock_state, pin))
#
#
# @RegisterFunctionalChannel("ENERGY_SENSORS_INTERFACE_CHANNEL")
# class EnergySensorInterfaceChannel(FunctionalChannel):
#     """EnergySensorInterfaceChannel"""
#
#     connectedEnergySensorType: Optional[str] = None
#     currentGasFlow: Optional[float] = None
#     currentPowerConsumption: Optional[float] = None
#     energyCounterOne: Optional[float] = 0.0
#     energyCounterOneType: Optional[str] = ""
#     energyCounterTwo: Optional[float] = 0.0
#     energyCounterTwoType: Optional[str] = ""
#     energyCounterThree: Optional[float] = 0.0
#     energyCounterThreeType: Optional[str] = ""
#     gasVolume: Optional[float] = None
#     gasVolumePerImpulse: Optional[float] = None
#     impulsesPerKWH: Optional[float] = None
#
#
# @RegisterFunctionalChannel("IMPULSE_OUTPUT_CHANNEL")
# class ImpulseOutputChannel(FunctionalChannel):
#     """this is the representation of the IMPULSE_OUTPUT_CHANNEL"""
#
#     impulseDuration: Optional[float] = 0.0
#     processing: Optional[bool] = False
#
#     def send_start_impulse(self):
#         """Toggle Wall mounted Garage Door Controller."""
#         data = {"channelIndex": self.index, "deviceId": self.device.id}
#         return self._rest_call("device/control/startImpulse", body=json.dumps(data))
#
#     async def async_send_start_impulse(self):
#         return await self._connection.api_call(*self.send_start_impulse())
#
#
# @RegisterFunctionalChannel("MULTI_MODE_INPUT_CHANNEL")
# class MultiModeInputChannel(FunctionalChannel):
#     """this is the representative of the MULTI_MODE_INPUT_CHANNEL channel"""
#
#     binaryBehaviorType: Optional[BinaryBehaviorType] = BinaryBehaviorType.NORMALLY_OPEN
#     multiModeInputMode: Optional[MultiModeInputMode] = MultiModeInputMode.BINARY_BEHAVIOR
#     windowState: Optional[WindowState] = WindowState.OPEN
#     doorBellSensorEventTimestamp: Optional[int] = None
#     corrosionPreventionActive: Optional[bool] = None
#
#
# @RegisterFunctionalChannel("MULTI_MODE_INPUT_DIMMER_CHANNEL")
# class MultiModeInputDimmerChannel(DimmerChannel):
#     """this is the representative of the MULTI_MODE_INPUT_DIMMER_CHANNEL channel"""
#
#     binaryBehaviorType: Optional[BinaryBehaviorType] = BinaryBehaviorType.NORMALLY_CLOSE
#     dimLevel: Optional[float] = None
#     multiModeInputMode: Optional[MultiModeInputMode] = MultiModeInputMode.KEY_BEHAVIOR
#     on: Optional[bool] = False
#     profileMode: Optional[ProfileMode] = ProfileMode.AUTOMATIC
#     userDesiredProfileMode: Optional[ProfileMode] = ProfileMode.AUTOMATIC
#
#
# @RegisterFunctionalChannel("MULTI_MODE_INPUT_SWITCH_CHANNEL")
# class MultiModeInputSwitchChannel(SwitchChannel):
#     """this is the representative of the MULTI_MODE_INPUT_SWITCH_CHANNEL channel"""
#
#     pass
#
#
# @RegisterFunctionalChannel("NOTIFICATION_LIGHT_CHANNEL")
# class NotificationLightChannel(DimmerChannel):
#     """this is the representative of the NOTIFICATION_LIGHT_CHANNEL channel"""
#
#     on: Optional[bool] = False
#     simpleRGBColorState: Optional[RGBColorState] = RGBColorState.BLACK
#
#     def set_rgb_dim_level(self, rgb: RGBColorState, dim_level: float):
#         """sets the color and dimlevel of the lamp
#
#         Args:
#             rgb(RGBColorState): the color of the lSamp
#             dim_level(float): the dimLevel of the lamp. 0.0 = off, 1.0 = MAX
#
#         Returns:
#             the result of the _restCall
#         """
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "simpleRGBColorState": rgb,
#             "dimLevel": dim_level,
#         }
#         return self._rest_call(
#             "device/control/setSimpleRGBColorDimLevel", body=json.dumps(data)
#         )
#
#     async def async_set_rgb_dim_level(self, rgb: RGBColorState, dim_level: float):
#         return await self._connection.api_call(*self.set_rgb_dim_level(rgb, dim_level))
#
#     def set_rgb_dim_level_with_time(
#             self,
#             rgb: RGBColorState,
#             dim_level: float,
#             on_time: float,
#             ramp_time: float,
#     ):
#         """sets the color and dimlevel of the lamp
#
#         Args:
#             rgb(RGBColorState): the color of the lamp
#             dim_level(float): the dimLevel of the lamp. 0.0 = off, 1.0 = MAX
#             on_time(float):
#             ramp_time(float):
#         Returns:
#             the result of the _restCall
#         """
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "simpleRGBColorState": rgb,
#             "dimLevel": dim_level,
#             "onTime": on_time,
#             "rampTime": ramp_time,
#         }
#         return self._rest_call(
#             "device/control/setSimpleRGBColorDimLevelWithTime", body=json.dumps(data)
#         )
#
#     async def async_set_rgb_dim_level_with_time(
#             self,
#             rgb: RGBColorState,
#             dimLevel: float,
#             onTime: float,
#             rampTime: float,
#     ):
#         return await self._connection.api_call(
#             *self.set_rgb_dim_level_with_time(rgb, dimLevel, onTime, rampTime)
#         )
#
#
# @RegisterFunctionalChannel("SHADING_CHANNEL")
# class ShadingChannel(FunctionalChannel):
#     """this is the representative of the SHADING_CHANNEL channel"""
#
#     automationDriveSpeed: Optional[DriveSpeed] = DriveSpeed.CREEP_SPEED
#     manualDriveSpeed: Optional[DriveSpeed] = DriveSpeed.CREEP_SPEED
#     favoritePrimaryShadingPosition: Optional[float] = 0.0
#     favoriteSecondaryShadingPosition: Optional[float] = 0.0
#     primaryShadingLevel: Optional[float] = 0.0
#     secondaryShadingLevel: Optional[float] = 0.0
#     previousPrimaryShadingLevel: Optional[float] = 0.0
#     previousSecondaryShadingLevel: Optional[float] = 0.0
#     identifyOemSupported: Optional[bool] = False
#     productId: Optional[int] = 0
#     primaryCloseAdjustable: Optional[bool] = False
#     primaryOpenAdjustable: Optional[bool] = False
#     primaryShadingStateType: Optional[ShadingStateType] = ShadingStateType.NOT_EXISTENT
#     profileMode: Optional[ProfileMode] = ProfileMode.MANUAL
#     userDesiredProfileMode: Optional[ProfileMode] = ProfileMode.MANUAL
#     processing: Optional[bool] = False
#     shadingDriveVersion: Optional[str] = None
#     shadingPackagePosition: Optional[ShadingPackagePosition] = ShadingPackagePosition.NOT_USED
#     shadingPositionAdjustmentActive: Optional[bool] = None
#     shadingPositionAdjustmentClientId: Optional[str] = None
#
#     def set_primary_shading_level(self, primaryShadingLevel: float):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "primaryShadingLevel": primaryShadingLevel,
#         }
#         return self._rest_call(
#             "device/control/setPrimaryShadingLevel", json.dumps(data)
#         )
#
#     async def async_set_primary_shading_level(self, primaryShadingLevel: float):
#         return await self._connection.api_call(
#             *self.set_primary_shading_level(primaryShadingLevel)
#         )
#
#     def set_secondary_shading_level(
#             self, primaryShadingLevel: float, secondaryShadingLevel: float
#     ):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "primaryShadingLevel": primaryShadingLevel,
#             "secondaryShadingLevel": secondaryShadingLevel,
#         }
#         return self._rest_call(
#             "device/control/setSecondaryShadingLevel", json.dumps(data)
#         )
#
#     async def async_set_secondary_shading_level(
#             self, primaryShadingLevel: float, secondaryShadingLevel: float
#     ):
#         return await self._connection.api_call(
#             *self.set_secondary_shading_level(
#                 primaryShadingLevel, secondaryShadingLevel
#             )
#         )
#
#     def set_shutter_stop(self):
#         """stops the current operation
#         Returns:
#             the result of the _restCall
#         """
#         data = {"channelIndex": self.index, "deviceId": self.device.id}
#         return self._rest_call("device/control/stop", body=json.dumps(data))
#
#     async def async_set_shutter_stop(self):
#         return await self._connection.api_call(*self.stop())
#
#
# @RegisterFunctionalChannel("SHUTTER_CHANNEL")
# class ShutterChannel(FunctionalChannel):
#     """this is the representative of the SHUTTER_CHANNEL channel"""
#
#     shutterLevel: Optional[int] = 0
#     changeOverDelay: Optional[float] = 0.0
#     bottomToTopReferenceTime: Optional[float] = 0.0
#     topToBottomReferenceTime: Optional[float] = 0.0
#     delayCompensationValue: Optional[float] = 0
#     endpositionAutoDetectionEnabled: Optional[bool] = False
#     previousShutterLevel: Optional[int] = None
#     processing: Optional[bool] = False
#     profileMode: Optional[str] = "AUTOMATIC"
#     selfCalibrationInProgress: Optional[bool] = None
#     supportingDelayCompensation: Optional[bool] = False
#     supportingEndpositionAutoDetection: Optional[bool] = False
#     supportingSelfCalibration: Optional[bool] = False
#     userDesiredProfileMode: Optional[str] = "AUTOMATIC"
#
#     def set_shutter_stop(self):
#         """stops the current shutter operation
#
#         Returns:
#             the result of the _restCall
#         """
#         data = {"channelIndex": self.index, "deviceId": self.device.id}
#         return self._rest_call("device/control/stop", body=json.dumps(data))
#
#     async def async_set_shutter_stop(self):
#         return await self._connection.api_call(*self.set_shutter_stop())
#
#     def set_shutter_level(self, level=0.0):
#         """sets the shutter level
#
#         Args:
#             level(float): the new level of the shutter. 0.0 = open, 1.0 = closed
#         Returns:
#             the result of the _restCall
#         """
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "shutterLevel": level,
#         }
#         return self._rest_call("device/control/setShutterLevel", body=json.dumps(data))
#
#     async def async_set_shutter_level(self, level=0.0):
#         return await self._connection.api_call(*self.set_shutter_level(level))

#
# @RegisterFunctionalChannel("SWITCH_MEASURING_CHANNEL")
# class SwitchMeasuringChannel(SwitchChannel):
#     """this is the representative of the SWITCH_MEASURING_CHANNEL channel"""
#
#     energyCounter: float = 0.0
#     currentPowerConsumption: float = 0.0
#
#     def reset_energy_counter(self):
#         data = {"channelIndex": self.index, "deviceId": self.device.id}
#         return self._rest_call(
#             "device/control/resetEnergyCounter", body=json.dumps(data)
#         )
#
#     async def async_reset_energy_counter(self):
#         return await self._connection.api_call(*self.reset_energy_counter())
#
#
# @RegisterFunctionalChannel("TILT_VIBRATION_SENSOR_CHANNEL")
# class TiltVibrationSensorChannel(FunctionalChannel):
#     """this is the representative of the TILT_VIBRATION_SENSOR_CHANNEL channel"""
#
#     accelerationSensorEventFilterPeriod: float = 100.0
#     accelerationSensorMode: float = AccelerationSensorMode.ANY_MOTION
#     accelerationSensorSensitivity: AccelerationSensorSensitivity = (
#         AccelerationSensorSensitivity.SENSOR_RANGE_2G
#     )
#     accelerationSensorNeutralPosition: str = None
#     accelerationSensorTriggerAngle: int = 0
#     accelerationSensorTriggered: Optional[bool] = False
#
#     def set_acceleration_sensor_mode(self, mode: AccelerationSensorMode):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "accelerationSensorMode": str(mode),
#         }
#         return self._rest_call(
#             "device/configuration/setAccelerationSensorMode", json.dumps(data)
#         )
#
#     async def async_set_acceleration_sensor_mode(self, mode: AccelerationSensorMode):
#         return await self._connection.api_call(*self.set_acceleration_sensor_mode(mode))
#
#     def set_acceleration_sensor_sensitivity(
#             self, sensitivity: AccelerationSensorSensitivity
#     ):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "accelerationSensorSensitivity": str(sensitivity),
#         }
#         return self._rest_call(
#             "device/configuration/setAccelerationSensorSensitivity", json.dumps(data)
#         )
#
#     async def async_set_acceleration_sensor_sensitivity(
#             self, sensitivity: AccelerationSensorSensitivity
#     ):
#         return await self._connection.api_call(
#             *self.set_acceleration_sensor_sensitivity(sensitivity)
#         )
#
#     def set_acceleration_sensor_trigger_angle(self, angle: int):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "accelerationSensorTriggerAngle": angle,
#         }
#         return self._rest_call(
#             "device/configuration/setAccelerationSensorTriggerAngle", json.dumps(data)
#         )
#
#     async def async_set_acceleration_sensor_trigger_angle(self, angle: int):
#         return await self._connection.api_call(
#             *self.set_acceleration_sensor_trigger_angle(angle)
#         )
#
#     def set_acceleration_sensor_event_filter_period(self, period: float):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "accelerationSensorEventFilterPeriod": period,
#         }
#         return self._rest_call(
#             "device/configuration/setAccelerationSensorEventFilterPeriod",
#             json.dumps(data),
#         )
#
#     async def async_set_acceleration_sensor_event_filter_period(self, period: float):
#         return await self._connection.api_call(
#             *self.set_acceleration_sensor_event_filter_period(period)
#         )
#
#
# @RegisterFunctionalChannel("WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL")
# class WallMountedThermostatProChannel(FunctionalChannel):
#     """this is the representative of the WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL channel"""
#
#     display: ClimateControlDisplay = ClimateControlDisplay.ACTUAL
#     setPointTemperature: float = 0
#     temperatureOffset: float = 0
#     actualTemperature: float = 0
#     humidity: int = 0
#     vaporAmount: float = 0.0
#
#     def set_display(
#             self, display: ClimateControlDisplay = ClimateControlDisplay.ACTUAL
#     ):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "display": str(display),
#         }
#         return self._rest_call(
#             "device/configuration/setClimateControlDisplay", json.dumps(data)
#         )
#
#     async def async_set_display(
#             self, display: ClimateControlDisplay = ClimateControlDisplay.ACTUAL
#     ):
#         return await self._connection.api_call(*self.set_display(display))
#
#
# @RegisterFunctionalChannel("WATER_SENSOR_CHANNEL")
# class WaterSensorChannel(FunctionalChannel):
#     """this is the representative of the WATER_SENSOR_CHANNEL channel"""
#
#     acousticAlarmSignal: AcousticAlarmSignal = (
#         AcousticAlarmSignal.DISABLE_ACOUSTIC_SIGNAL
#     )
#     acousticAlarmTiming: AcousticAlarmTiming = AcousticAlarmTiming.PERMANENT
#     acousticWaterAlarmTrigger: WaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
#     inAppWaterAlarmTrigger: WaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
#     moistureDetected: Optional[bool] = False
#     sirenWaterAlarmTrigger: WaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
#     waterlevelDetected: Optional[bool] = False
#
#     def set_acoustic_alarm_signal(self, acousticAlarmSignal: AcousticAlarmSignal):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "acousticAlarmSignal": str(acousticAlarmSignal),
#         }
#         return self._rest_call(
#             "device/configuration/setAcousticAlarmSignal", json.dumps(data)
#         )
#
#     async def async_set_acoustic_alarm_signal(
#             self, acousticAlarmSignal: AcousticAlarmSignal
#     ):
#         return await self._connection.api_call(
#             *self.set_acoustic_alarm_signal(acousticAlarmSignal)
#         )
#
#     def set_acoustic_alarm_timing(self, acousticAlarmTiming: AcousticAlarmTiming):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "acousticAlarmTiming": str(acousticAlarmTiming),
#         }
#         return self._rest_call(
#             "device/configuration/setAcousticAlarmTiming", json.dumps(data)
#         )
#
#     async def async_set_acoustic_alarm_timing(
#             self, acousticAlarmTiming: AcousticAlarmTiming
#     ):
#         return await self._connection.api_call(
#             *self.set_acoustic_alarm_timing(acousticAlarmTiming)
#         )
#
#     def set_acoustic_water_alarm_trigger(
#             self, acousticWaterAlarmTrigger: WaterAlarmTrigger
#     ):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "acousticWaterAlarmTrigger": str(acousticWaterAlarmTrigger),
#         }
#         return self._rest_call(
#             "device/configuration/setAcousticWaterAlarmTrigger", json.dumps(data)
#         )
#
#     async def async_set_acoustic_water_alarm_trigger(
#             self, acousticWaterAlarmTrigger: WaterAlarmTrigger
#     ):
#         return await self._connection.api_call(
#             *self.set_acoustic_water_alarm_trigger(acousticWaterAlarmTrigger)
#         )
#
#     def set_inapp_water_alarm_trigger(self, inAppWaterAlarmTrigger: WaterAlarmTrigger):
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "inAppWaterAlarmTrigger": str(inAppWaterAlarmTrigger),
#         }
#         return self._rest_call(
#             "device/configuration/setInAppWaterAlarmTrigger", json.dumps(data)
#         )
#
#     async def async_set_inapp_water_alarm_trigger(
#             self, inAppWaterAlarmTrigger: WaterAlarmTrigger
#     ):
#         return await self._connection.api_call(
#             *self.set_inapp_water_alarm_trigger(inAppWaterAlarmTrigger)
#         )
#
#     def set_siren_water_alarm_trigger(self, sirenWaterAlarmTrigger: WaterAlarmTrigger):
#         LOGGER.warning(
#             "set_siren_water_alarm_trigger is currently not available in the HMIP App. It might not be available in the cloud yet"
#         )
#         data = {
#             "channelIndex": self.index,
#             "deviceId": self.device.id,
#             "sirenWaterAlarmTrigger": str(sirenWaterAlarmTrigger),
#         }
#         return self._rest_call(
#             "device/configuration/setSirenWaterAlarmTrigger", json.dumps(data)
#         )
#
#     async def async_set_siren_water_alarm_trigger(
#             self, sirenWaterAlarmTrigger: WaterAlarmTrigger
#     ):
#         return await self._connection.api_call(
#             *self.set_siren_water_alarm_trigger(sirenWaterAlarmTrigger)
#         )
#
#
# @RegisterFunctionalChannel("ACCESS_CONTROLLER_CHANNEL")
# class AccessControllerChannel(DeviceBaseChannel):
#     """this is the representative of the ACCESS_CONTROLLER_CHANNEL channel"""
#
#     dutyCycleLevel: float = 0.0
#     accessPointPriority: int = 0
#     signalBrightness: float = 0
#     filteredMulticastRoutingEnabled: Optional[bool] = None
#
#
# @RegisterFunctionalChannel("DEVICE_SABOTAGE")
# class DeviceSabotageChannel(DeviceBaseChannel):
#     """this is the representative of the DEVICE_SABOTAGE channel"""
#
#     sabotage: Optional[bool] = False
#
#
# @RegisterFunctionalChannel("DEVICE_INCORRECT_POSITIONED")
# class DeviceIncorrectPositionedChannel(DeviceBaseChannel):
#     """this is the representative of the DEVICE_INCORRECT_POSITIONED channel"""
#
#     incorrectPositioned: Optional[bool] = False
#
#
# @RegisterFunctionalChannel("DEVICE_PERMANENT_FULL_RX")
# class DevicePermanentFullRxChannel(DeviceBaseChannel):
#     """this is the representative of the DEVICE_PERMANENT_FULL_RX channel"""
#
#     permanentFullRx: Optional[bool] = False
#
#
# @RegisterFunctionalChannel("ACCESS_AUTHORIZATION_CHANNEL")
# class AccessAuthorizationChannel(FunctionalChannel):
#     """this represents ACCESS_AUTHORIZATION_CHANNEL channel"""
#
#     authorized: Optional[bool] = False
#
#
# @RegisterFunctionalChannel("HEATING_THERMOSTAT_CHANNEL")
# class HeatingThermostatChannel(FunctionalChannel):
#     """this is the representative of the HEATING_THERMOSTAT_CHANNEL channel"""
#
#     temperatureOffset: float = 0.0
#     valvePosition: float = 0.0
#     valveState: ValveState = ValveState.ERROR_POSITION
#     setPointTemperature: float = 0.0
#     valveActualTemperature: float = 0.0
#     automaticValveAdaptionNeeded: Optional[bool] = False
#
#
# @RegisterFunctionalChannel("SHUTTER_CONTACT_CHANNEL")
# class ShutterContactChannel(FunctionalChannel):
#     """this is the representative of the SHUTTER_CONTACT_CHANNEL channel"""
#
#     windowState: WindowState = WindowState.CLOSED
#     eventDelay: int = None
#
#
# @RegisterFunctionalChannel("ROTARY_HANDLE_SENSOR")
# class RotaryHandleChannel(ShutterContactChannel):
#     """this is the representative of the ROTARY_HANDLE_CHANNEL channel"""
#
#
# @RegisterFunctionalChannel("CONTACT_INTERFACE_CHANNEL")
# class ContactInterfaceChannel(ShutterContactChannel):
#     """this is the representative of the CONTACT_INTERFACE_CHANNEL channel"""
#
#     alarmContactType: AlarmContactType = AlarmContactType.WINDOW_DOOR_CONTACT
#     contactType: ContactType = ContactType.NORMALLY_CLOSE
#
#
# @RegisterFunctionalChannel("CLIMATE_SENSOR_CHANNEL")
# class ClimateSensorChannel(FunctionalChannel):
#     """this is the representative of the CLIMATE_SENSOR_CHANNEL channel"""
#
#     actualTemperature: float = 0
#     humidity: int = 0
#     vaporAmount: float = 0.0
#
#
# @RegisterFunctionalChannel("DOOR_LOCK_SENSOR_CHANNEL")
# class DoorLockSensorChannel(FunctionalChannel):
#     """This respresents of the DoorLockSensorChannel"""
#
#     doorLockDirection: Optional[bool] = False
#     doorLockNeutralPosition: Optional[bool] = False
#     doorLockTurns: Optional[bool] = False
#     lockState: LockState = LockState.UNLOCKED
#
#
# @RegisterFunctionalChannel("WALL_MOUNTED_THERMOSTAT_WITHOUT_DISPLAY_CHANNEL")
# class WallMountedThermostatWithoutDisplayChannel(ClimateSensorChannel):
#     """this is the representative of the WALL_MOUNTED_THERMOSTAT_WITHOUT_DISPLAY_CHANNEL channel"""
#
#     temperatureOffset: float = 0
#
#
# @RegisterFunctionalChannel("ANALOG_ROOM_CONTROL_CHANNEL")
# class AnalogRoomControlChannel(FunctionalChannel):
#     """this is the representative of the ANALOG_ROOM_CONTROL_CHANNEL channel"""
#
#     actualTemperature: float = 0
#     setPointTemperature: float = 0
#     temperatureOffset: float = 0
#
#
# @RegisterFunctionalChannel("SMOKE_DETECTOR_CHANNEL")
# class SmokeDetectorChannel(FunctionalChannel):
#     """this is the representative of the SMOKE_DETECTOR_CHANNEL channel"""
#
#     smokeDetectorAlarmType: SmokeDetectorAlarmType = SmokeDetectorAlarmType.IDLE_OFF
#
#
# @RegisterFunctionalChannel("DEVICE_GLOBAL_PUMP_CONTROL")
# class DeviceGlobalPumpControlChannel(DeviceBaseChannel):
#     """this is the representative of the DEVICE_GLOBAL_PUMP_CONTROL channel"""
#
#     globalPumpControl: Optional[bool] = False
#     heatingValveType: HeatingValveType = HeatingValveType.NORMALLY_CLOSE
#     heatingLoadType: HeatingLoadType = HeatingLoadType.LOAD_BALANCING
#     frostProtectionTemperature: float = 0.0
#     heatingEmergencyValue: float = 0.0
#     valveProtectionDuration: float = 0
#     valveProtectionSwitchingInterval: int = 20
#     coolingEmergencyValue: float = 0
#
#
# @RegisterFunctionalChannel("MOTION_DETECTION_CHANNEL")
# class MotionDetectionChannel(FunctionalChannel):
#     """this is the representative of the MOTION_DETECTION_CHANNEL channel"""
#
#     motionDetected: Optional[bool] = False
#     presenceDetected: Optional[bool] = False
#     currentIllumination: float = None
#     illumination: float = 0
#     motionBufferActive: Optional[bool] = False
#     motionDetectionSendInterval: MotionDetectionSendInterval = (
#         MotionDetectionSendInterval.SECONDS_30
#     )
#     numberOfBrightnessMeasurements: int = 0
#
#
# @RegisterFunctionalChannel("PRESENCE_DETECTION_CHANNEL")
# class PresenceDetectionChannel(FunctionalChannel):
#     """this is the representative of the PRESENCE_DETECTION_CHANNEL channel"""
#
#     presenceDetected: Optional[bool] = False
#     currentIllumination: float = None
#     illumination: float = 0
#     motionBufferActive: Optional[bool] = False
#     motionDetectionSendInterval: MotionDetectionSendInterval = (
#         MotionDetectionSendInterval.SECONDS_30
#     )
#     numberOfBrightnessMeasurements: int = 0
#
#
# @RegisterFunctionalChannel("MULTI_MODE_INPUT_BLIND_CHANNEL")
# class MultiModeInputBlindChannel(BlindChannel):
#     """this is the representative of the MULTI_MODE_INPUT_BLIND_CHANNEL channel"""
#
#     binaryBehaviorType: BinaryBehaviorType = BinaryBehaviorType.NORMALLY_CLOSE
#     multiModeInputMode: MultiModeInputMode = MultiModeInputMode.KEY_BEHAVIOR
#     favoritePrimaryShadingPosition: float = 0.0
#     favoriteSecondaryShadingPosition: float = 0.0
#
#
# @RegisterFunctionalChannel("WEATHER_SENSOR_CHANNEL")
# class WeatherSensorChannel(FunctionalChannel):
#     """this is the representative of the WEATHER_SENSOR_CHANNEL channel"""
#
#     actualTemperature: float = 0
#     humidity: float = 0
#     vaporAmount: float = 0.0
#     illumination: float = 0
#     illuminationThresholdSunshine: float = 0
#     storm: Optional[bool] = False
#     sunshine: Optional[bool] = False
#     todaySunshineDuration: float = 0
#     totalSunshineDuration: float = 0
#     windSpeed: float = 0
#     windValueType: WindValueType = WindValueType.AVERAGE_VALUE
#     yesterdaySunshineDuration: float = 0
#
#
# @RegisterFunctionalChannel("WEATHER_SENSOR_PLUS_CHANNEL")
# class WeatherSensorPlusChannel(WeatherSensorChannel):
#     """this is the representative of the WEATHER_SENSOR_PLUS_CHANNEL channel"""
#
#     raining: Optional[bool] = False
#     todayRainCounter: float = 0
#     totalRainCounter: float = 0
#     yesterdayRainCounter: float = 0
#
#
# @RegisterFunctionalChannel("WEATHER_SENSOR_PRO_CHANNEL")
# class WeatherSensorProChannel(WeatherSensorPlusChannel):
#     """this is the representative of the WEATHER_SENSOR_PRO_CHANNEL channel"""
#
#     weathervaneAlignmentNeeded: Optional[bool] = False
#     windDirection: float = 0
#     windDirectionVariation: float = 0
#
#
# @RegisterFunctionalChannel("SINGLE_KEY_CHANNEL")
# class SingleKeyChannel(FunctionalChannel):
#     """this is the representative of the SINGLE_KEY_CHANNEL channel"""
#
#     acousticSendStateEnabled: Optional[bool] = None
#     actionParameter: str = None
#     doorBellSensorEventTimestamp: int = None
#     doublePressTime: float = None
#
#
# @RegisterFunctionalChannel("ALARM_SIREN_CHANNEL")
# class AlarmSirenChannel(FunctionalChannel):
#     """this is the representative of the ALARM_SIREN_CHANNEL channel"""
#
#     pass
#
#
# @RegisterFunctionalChannel("FLOOR_TERMINAL_BLOCK_CHANNEL")
# class FloorTeminalBlockChannel(FunctionalChannel):
#     """this is the representative of the FLOOR_TERMINAL_BLOCK_CHANNEL channel"""
#
#     pass
#
#
# @RegisterFunctionalChannel("FLOOR_TERMINAL_BLOCK_LOCAL_PUMP_CHANNEL")
# class FloorTerminalBlockLocalPumpChannel(FunctionalChannel):
#     """this is the representative of the FLOOR_TERMINAL_BLOCK_LOCAL_PUMP_CHANNEL  channel"""
#
#     pumpFollowUpTime: int = 0
#     pumpLeadTime: int = 0
#     pumpProtectionDuration: int = 0
#     pumpProtectionSwitchingInterval: int = 20
#
#
# @RegisterFunctionalChannel("HEAT_DEMAND_CHANNEL")
# class HeatDemandChannel(FunctionalChannel):
#     """this is the representative of the HEAT_DEMAND_CHANNEL channel"""
#
#
# @RegisterFunctionalChannel("DEHUMIDIFIER_DEMAND_CHANNEL")
# class DehumidifierDemandChannel(FunctionalChannel):
#     """this is the representative of the DEHUMIDIFIER_DEMAND_CHANNEL channel"""
#
#
# @RegisterFunctionalChannel("PASSAGE_DETECTOR_CHANNEL")
# class PassageDetectorChannel(FunctionalChannel):
#     """this is the representative of the PASSAGE_DETECTOR_CHANNEL channel"""
#
#     leftCounter: int = 0
#     leftRightCounterDelta: int = 0
#     passageBlindtime: float = 0.0
#     passageDirection: PassageDirection = PassageDirection.RIGHT
#     passageSensorSensitivity: float = 0.0
#     passageTimeout: float = 0.0
#     rightCounter: int = 0
#
#
# @RegisterFunctionalChannel("INTERNAL_SWITCH_CHANNEL")
# class InternalSwitchChannel(FunctionalChannel):
#     """this is the representative of the INTERNAL_SWITCH_CHANNEL channel"""
#
#     frostProtectionTemperature: float = 0
#     heatingValveType: HeatingValveType = HeatingValveType.NORMALLY_CLOSE
#     internalSwitchOutputEnabled: Optional[bool] = False
#     valveProtectionDuration: int = 0
#     valveProtectionSwitchingInterval: int = 0
#
#
# @RegisterFunctionalChannel("LIGHT_SENSOR_CHANNEL")
# class LightSensorChannel(FunctionalChannel):
#     """this is the representative of the LIGHT_SENSOR_CHANNEL channel"""
#
#     averageIllumination: float = 0.0
#     currentIllumination: float = 0.0
#     highestIllumination: float = 0.0
#     lowestIllumination: float = 0.0
#
#
# @RegisterFunctionalChannel("GENERIC_INPUT_CHANNEL")
# class GenericInputChannel(FunctionalChannel):
#     """this is the representative of the GENERIC_INPUT_CHANNEL channel"""
#
#
# @RegisterFunctionalChannel("ANALOG_OUTPUT_CHANNEL")
# class AnalogOutputChannel(FunctionalChannel):
#     """this is the representative of the ANALOG_OUTPUT_CHANNEL channel"""
#
#     analogOutputLevel: float = 0.0
#
#
# @RegisterFunctionalChannel("DEVICE_RECHARGEABLE_WITH_SABOTAGE")
# class DeviceRechargeableWithSabotage(DeviceSabotageChannel):
#     """this is the representative of the DEVICE_RECHARGEABLE_WITH_SABOTAGE channel"""
#
#     badBatteryHealth: Optional[bool] = False
#
#
# @RegisterFunctionalChannel("FLOOR_TERMINAL_BLOCK_MECHANIC_CHANNEL")
# class FloorTerminalBlockMechanicChannel(FunctionalChannel):
#     """this is the representative of the class FLOOR_TERMINAL_BLOCK_MECHANIC_CHANNEL(FunctionalChannel) channel"""
#
#     valveState: ValveState = ValveState.ADAPTION_DONE
#     valvePosition: float = 0.0
#
#
# @RegisterFunctionalChannel("CHANGE_OVER_CHANNEL")
# class ChangeOverChannel(FunctionalChannel):
#     """this is the representative of the CHANGE_OVER_CHANNEL channel"""
#
#
# @RegisterFunctionalChannel("MAINS_FAILURE_CHANNEL")
# class MainsFailureChannel(FunctionalChannel):
#     """this is the representative of the MAINS_FAILURE_CHANNEL channel"""
#
#     powerMainsFailure: Optional[bool] = False
#     genericAlarmSignal: AlarmSignalType = AlarmSignalType.NO_ALARM
#
#
# @RegisterFunctionalChannel("RAIN_DETECTION_CHANNEL")
# class RainDetectionChannel(FunctionalChannel):
#     """this is the representative of the TILT_VIBRATION_SENSOR_CHANNEL channel"""
#
#     rainSensorSensitivity: int = 0
#     raining: Optional[bool] = False
#
#
# @RegisterFunctionalChannel("TEMPERATURE_SENSOR_2_EXTERNAL_DELTA_CHANNEL")
# class TemperatureDifferenceSensor2Channel(FunctionalChannel):
#     """this is the representative of the TEMPERATURE_SENSOR_2_EXTERNAL_DELTA_CHANNEL channel"""
#
#     temperatureExternalDelta: float = 0.0
#     temperatureExternalOne: float = 0.0
#     temperatureExternalTwo: float = 0.0
#
#
# @RegisterFunctionalChannel("EXTERNAL_BASE_CHANNEL")
# class ExternalBaseChannel(FunctionalChannel):
#     """this represents the EXTERNAL_BASE_CHANNEL function-channel for external devices"""
#
#     pass
#
#
# @RegisterFunctionalChannel("EXTERNAL_UNIVERSAL_LIGHT_CHANNEL")
# class ExternalUniversalLightChannel(FunctionalChannel):
#     """this represents the EXTERNAL_UNIVERSAL_LIGHT_CHANNEL function-channel for external devices"""
#
#     colorTemperature: int = 0
#     dimLevel: float = 0.0
#     hue: int = None
#     maximumColorTemperature: int = 0
#     minimalColorTemperature: int = 0
#     on: Optional[bool] = None
#     saturationLevel: float = None
#
#
# @RegisterFunctionalChannel("OPTICAL_SIGNAL_CHANNEL")
# class OpticalSignalChannel(FunctionalChannel):
#     """this class represents the OPTICAL_SIGNAL_CHANNEL"""
#
#     dimLevel: int = -1
#     on: Optional[bool] = None
#     opticalSignalBehaviour: str = None
#     powerUpSwitchState: Optional[bool] = None
#     simpleRGBColorState: str = None
#     userDesiredProfileMode: str = None
#
#
# @RegisterFunctionalChannel("CARBON_DIOXIDE_SENSOR_CHANNEL")
# class CarbonDioxideSensorChannel(FunctionalChannel):
#     """Representation of the CarbonDioxideSensorChannel Channel"""
#
#     actualTemperature: float = None
#     carbonDioxideConcentration: float = None
#     carbonDioxideVisualisationEnabled: Optional[bool] = None
#     humidity: float = None
#     vaporAmount: float = None
#
#
# @RegisterFunctionalChannel("ACCESS_CONTROLLER_WIRED_CHANNEL")
# class AccessControllerWiredChannel(DeviceBaseChannel):
#     """this is the representative of the ACCESS_CONTROLLER_WIRED_CHANNEL channel"""
#
#     accessPointPriority: Optional[bool] = None
#     busConfigMismatch: Optional[bool] = None
#     busMode: str = None
#     controlsMountingOrientation: str = None
#     deviceCommunicationError: Optional[bool] = None
#     deviceDriveError: Optional[bool] = None
#     deviceDriveModeError: Optional[bool] = None
#     deviceOperationMode: str = None
#     devicePowerFailureDetected: Optional[bool] = None
#     displayContrast: float = None
#     index: int = None
#     label: str = None
#     lockJammed: Optional[bool] = None
#     mountingOrientation: str = None
#     multicastRoutingEnabled: Optional[bool] = None
#     particulateMatterSensorCommunicationError: Optional[bool] = None
#     particulateMatterSensorError: Optional[bool] = None
#     powerShortCircuit: Optional[bool] = None
#     powerSupplyCurrent: float = None
#     profilePeriodLimitReached: Optional[bool] = None
#     shortCircuitDataLine: Optional[bool] = None
#     signalBrightness: float = 0.0
#
#
# @RegisterFunctionalChannel("OPTICAL_SIGNAL_GROUP_CHANNEL")
# class OpticalSignalGroupChannel(FunctionalChannel):
#     """this class represents the OPTICAL_SIGNAL_GROUP_CHANNEL"""
#
#     dimLevel: int = -1
#     on: Optional[bool] = None
#     opticalSignalBehaviour: str = None
#     powerUpSwitchState: Optional[bool] = None
#     profileMode: str = None
#     simpleRGBColorState: str = None
#     userDesiredProfileMode: str = None
#
#
# @RegisterFunctionalChannel("UNIVERSAL_LIGHT_CHANNEL")
# class UniversalLightChannel(FunctionalChannel):
#     """Represents Universal Light Channel."""
#
#     channelRole: str = None
#     colorTemperature: int = None
#     controlGearFailure: str = None
#     dim2WarmActive: Optional[bool] = None
#     dimLevel: float = None
#     hardwareColorTemperatureColdWhite: int = None
#     hardwareColorTemperatureWarmWhite: int = None
#     hue: Optional[bool] = None
#     humanCentricLightActive: Optional[bool] = None
#     lampFailure: Optional[bool] = None
#     lightSceneId: int = None
#     limitFailure: Any = None
#     maximumColorTemperature: int = None
#     minimalColorTemperature: int = None
#     on: Optional[bool] = None
#     onMinLevel: float = None
#     profileMode: ProfileMode = None
#     saturationLevel: float = None
#
#
# @RegisterFunctionalChannel("UNIVERSAL_LIGHT_GROUP_CHANNEL")
# class UniversalLightChannelGroup(UniversalLightChannel):
#     """Universal-Light-Channel-Group."""
#
#     channelSelections: list = []
