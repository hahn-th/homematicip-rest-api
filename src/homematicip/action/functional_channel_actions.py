from homematicip.action.action import Action
from homematicip.model.functional_channels import FunctionalChannel
from homematicip.runner import Runner


@Action.allowed_types('BLIND_CHANNEL', 'MULTI_MODE_INPUT_BLIND_CHANNEL')
async def action_set_slats_level(runner: Runner, fc: FunctionalChannel, slats_level: float,
                                 shutter_level: float = None):
    if shutter_level is None:
        shutter_level = fc.shutterLevel
    data = {
        "channelIndex": fc.channelIndex,
        "deviceId": fc.deviceId,
        "slatsLevel": slats_level,
        "shutterLevel": shutter_level
    }
    return await runner.rest_connection.async_post("device/control/setSlatsLevel", data)


@Action.allowed_types('BLIND_CHANNEL', 'MULTI_MODE_INPUT_BLIND_CHANNEL', 'SHUTTER_CHANNEL')
async def action_set_shutter_level(runner: Runner, fc: FunctionalChannel, shutter_level: float):
    data = {"channelIndex": fc.channelIndex, "deviceId": fc.deviceId, "shutterLevel": shutter_level}
    return await runner.rest_connection.async_post("device/control/setShutterLevel", data)


@Action.allowed_types('SWITCH_CHANNEL',
                      'MULTI_MODE_INPUT_SWITCH_CHANNEL',
                      'SWITCH_MEASURING_CHANNEL')
async def action_set_switch_state(runner: Runner, fc: FunctionalChannel, on: bool):
    data = {"channelIndex": fc.channelIndex, "deviceId": fc.deviceId, "on": on}
    return await runner.rest_connection.async_post("device/control/setSwitchState", data)

#
# class SetAccelerationSensorModeAction(AbstractAction):
#     """Set acceleration sensor mode for a functional channel"""
#
#     def get_target_type_names(self) -> list[str]:
#         return ['ACCELERATION_SENSOR_CHANNEL', 'TILT_VIBRATION_SENSOR']
#
#     async def run(self, target: HmipBaseModel, **kwargs):
#         """Set acceleration sensor mode for functional channel. target must be a FunctionalChannel
#
#         Required: mode (AccelerationSensorMode)
#         """
#         mode = kwargs.get("mode")
#
#         if not isinstance(target, FunctionalChannel):
#             raise ValueError("target must be type FunctionalChannel")
#         if not isinstance(mode, AccelerationSensorMode):
#             raise ValueError("mode must be AccelerationSensorMode")
#
#         data = {
#             "channelIndex": target.channelIndex,
#             "deviceId": target.deviceId,
#             "accelerationSensorMode": str(mode),
#         }
#         return await self.connection.async_post("device/configuration/setAccelerationSensorMode", data)
#
#
# class SetAccelerationSensorNeutralPositionAction(AbstractAction):
#     """Set acceleration sensor mode for a functional channel"""
#
#     def get_target_type_names(self) -> list[str]:
#         return ['ACCELERATION_SENSOR_CHANNEL', 'TILT_VIBRATION_SENSOR']
#
#     async def run(self, target: HmipBaseModel, **kwargs):
#         """Set acceleration sensor mode for functional channel. target must be a FunctionalChannel
#
#         Required: neutral_position (AccelerationSensorNeutralPosition)
#         """
#         neutral_position = kwargs.get("neutral_position")
#
#         if not isinstance(target, FunctionalChannel):
#             raise ValueError("target must be type FunctionalChannel")
#         if not isinstance(neutral_position, AccelerationSensorNeutralPosition):
#             raise ValueError("mode must be AccelerationSensorNeutralPosition")
#
#         data = {
#             "channelIndex": target.channelIndex,
#             "deviceId": target.deviceId,
#             "accelerationSensorNeutralPosition": str(neutral_position),
#         }
#         return await self.connection.async_post("device/configuration/setAccelerationSensorNeutralPosition", data)
#
#
# class SetAccelerationSensorSensitivityAction(AbstractAction):
#     """Set acceleration sensor sensitivity for a functional channel"""
#
#     def get_target_type_names(self) -> list[str]:
#         return ['ACCELERATION_SENSOR_CHANNEL', 'TILT_VIBRATION_SENSOR']
#
#     async def run(self, target: HmipBaseModel, **kwargs):
#         """Set acceleration sensor sensitivity for functional channel. target must be a FunctionalChannel
#
#         Required: sensitivity (AccelerationSensorSensitivity)
#         """
#         sensitivity = kwargs.get("sensitivity")
#
#         if not isinstance(target, FunctionalChannel):
#             raise ValueError("target must be type FunctionalChannel")
#         if not isinstance(sensitivity, AccelerationSensorSensitivity):
#             raise ValueError("mode must be AccelerationSensorSensitivity")
#
#         data = {
#             "channelIndex": target.channelIndex,
#             "deviceId": target.deviceId,
#             "accelerationSensorSensitivity": str(sensitivity),
#         }
#         return await self.connection.async_post("device/configuration/setAccelerationSensorSensitivity", data)
#
#
# class SetAccelerationSensorTriggerAngleAction(AbstractAction):
#     """Set acceleration sensor sensitivity for a functional channel"""
#
#     def get_target_type_names(self) -> list[str]:
#         return ['ACCELERATION_SENSOR_CHANNEL', 'TILT_VIBRATION_SENSOR']
#
#     async def run(self, target: HmipBaseModel, **kwargs):
#         """Set acceleration sensor sensitivity for functional channel. target must be a FunctionalChannel
#
#         Required: angle (int)
#         """
#         angle = kwargs.get("angle")
#
#         if not isinstance(target, FunctionalChannel):
#             raise ValueError("target must be type FunctionalChannel")
#         if not isinstance(int, angle):
#             raise ValueError("angle must be integer")
#
#         data = {
#             "channelIndex": target.channelIndex,
#             "deviceId": target.deviceId,
#             "accelerationSensorTriggerAngle": angle
#         }
#         return await self.connection.async_post("device/configuration/setAccelerationSensorTriggerAngle", data)
#
#
# class SetAccelerationSensorEventFilterPeriodAction(AbstractAction):
#     """Set acceleration sensor event filter period for a functional channel"""
#
#     def get_target_type_names(self) -> list[str]:
#         return ['ACCELERATION_SENSOR_CHANNEL', 'TILT_VIBRATION_SENSOR']
#
#     async def run(self, target: HmipBaseModel, **kwargs):
#         """Set acceleration sensor event filter period for a functional channel
#
#         Required: period (float)
#         """
#         period = kwargs.get("period")
#
#         if not isinstance(target, FunctionalChannel):
#             raise ValueError("target must be type FunctionalChannel")
#         if not isinstance(float, period):
#             raise ValueError("period must be float")
#
#         data = {
#             "channelIndex": target.channelIndex,
#             "deviceId": target.deviceId,
#             "accelerationSensorEventFilterPeriod": period
#         }
#         return await self.connection.async_post("device/configuration/setAccelerationSensorEventFilterPeriod", data)
#
#
# class SetNotificationSoundTypeAction(AbstractAction):
#     """Set acceleration sensor event filter period for a functional channel"""
#
#     def get_target_type_names(self) -> list[str]:
#         return ['ACCELERATION_SENSOR_CHANNEL']
#
#     async def run(self, target: HmipBaseModel, **kwargs):
#         """Set acceleration sensor event filter period for a functional channel
#
#         Required: sound_type: NotificationSoundType
#         Required: is_high_to_low: bool
#         """
#         sound_type = kwargs.get("sound_type")
#         is_high_to_low = kwargs.get("is_high_to_low")
#
#         if not isinstance(target, FunctionalChannel):
#             raise ValueError("target must be type FunctionalChannel")
#         if not isinstance(NotificationSoundType, sound_type):
#             raise ValueError("sound_type must be NotificationSoundType")
#         if not isinstance(bool, is_high_to_low):
#             raise ValueError("is_high_to_low must be float")
#
#         data = {
#             "channelIndex": target.channelIndex,
#             "deviceId": target.deviceId,
#             "notificationSoundType": sound_type,
#             "isHighToLow": is_high_to_low
#         }
#         return await self.connection.async_post("device/configuration/setNotificationSoundType", data)
#
#
# class SetMinimumFloorHeatingValvePositionAction(AbstractAction):
#
#     def get_target_type_names(self) -> list[str]:
#         return ['DEVICE_BASE_FLOOR_HEATING']
#
#     async def run(self, target: HmipBaseModel, **kwargs):
#         """Set the minimum floor heating valve position for a device
#
#         Required: minimum_floor_heating_valve_position: float
#         """
#         minimum_floor_heating_valve_position = kwargs.get("minimumFloorHeatingValvePosition")
#
#         if not isinstance(target, FunctionalChannel):
#             raise ValueError("target must be type FunctionalChannel")
#         if not isinstance(float, minimum_floor_heating_valve_position):
#             raise ValueError("minimum_floor_heating_valve_position must be float")
#
#         data = {
#             "channelIndex": target.channelIndex,
#             "deviceId": target.deviceId,
#             "minimumFloorHeatingValvePosition": minimum_floor_heating_valve_position
#         }
#         return await self.connection.async_post("device/configuration/setMinimumFloorHeatingValvePosition", data)
#
#
# class SetOperationLockAction(AbstractAction):
#
#     def get_target_type_names(self) -> list[str]:
#         return ['DEVICE_OPERATIONLOCK', 'DEVICE_OPERATIONLOCK_WITH_SABOTAGE']
#
#     async def run(self, target: HmipBaseModel, **kwargs):
#         """Set the operation lock for a device
#
#         Required: operationLock: bool
#         """
#         operation_lock = kwargs.get("operationLock")
#
#         if not isinstance(target, FunctionalChannel):
#             raise ValueError("target must be type FunctionalChannel")
#         if not isinstance(bool, operation_lock):
#             raise ValueError("operation_lock must be bool")
#
#         data = {
#             "channelIndex": target.channelIndex,
#             "deviceId": target.deviceId,
#             "operationLock": operation_lock
#         }
#         return await self.connection.async_post("device/configuration/setOperationLock", data)


@Action.allowed_types("DIMMER_CHANNEL")
async def action_set_dim_level(runner: Runner, fc: FunctionalChannel, dim_level: float):
    data = {"channelIndex": fc.channelIndex, "deviceId": fc.deviceId, "dimLevel": dim_level}
    return await runner.rest_connection.async_post("device/control/setDimLevel", data)
