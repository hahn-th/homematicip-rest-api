from homematicip.action.action import Action
from homematicip.model.enums import AccelerationSensorMode, AccelerationSensorNeutralPosition, \
    AccelerationSensorSensitivity, NotificationSoundType
from homematicip.model.functional_channels import FunctionalChannel
from homematicip.runner import Runner


@Action.allowed_types('BLIND_CHANNEL', 'MULTI_MODE_INPUT_BLIND_CHANNEL')
async def action_set_slats_level(runner: Runner, fc: FunctionalChannel, slats_level: float,
                                 shutter_level: float = None):
    if shutter_level is None:
        shutter_level = fc.shutterLevel
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "slatsLevel": slats_level,
        "shutterLevel": shutter_level
    }
    return await runner.rest_connection.async_post("device/control/setSlatsLevel", data)


@Action.allowed_types('BLIND_CHANNEL', 'MULTI_MODE_INPUT_BLIND_CHANNEL', 'SHUTTER_CHANNEL')
async def action_set_shutter_level(runner: Runner, fc: FunctionalChannel, shutter_level: float):
    data = {"channelIndex": fc.index, "deviceId": fc.deviceId, "shutterLevel": shutter_level}
    return await runner.rest_connection.async_post("device/control/setShutterLevel", data)


@Action.allowed_types('SWITCH_CHANNEL',
                      'MULTI_MODE_INPUT_SWITCH_CHANNEL',
                      'SWITCH_MEASURING_CHANNEL')
async def action_set_switch_state(runner: Runner, fc: FunctionalChannel, on: bool):
    data = {"channelIndex": fc.index, "deviceId": fc.deviceId, "on": on}
    return await runner.rest_connection.async_post("device/control/setSwitchState", data)


@Action.allowed_types('IMPULSE_OUTPUT_CHANNEL')
async def action_start_impulse(runner: Runner, fc: FunctionalChannel):
    """Toggle Wall mounted Garage Door Controller."""
    data = {"channelIndex": fc.index, "deviceId": fc.deviceId}
    return await runner.rest_connection.async_post("device/control/startImpulse", data)


@Action.allowed_types("DIMMER_CHANNEL")
async def action_set_dim_level(runner: Runner, fc: FunctionalChannel, dim_level: float):
    data = {"channelIndex": fc.index, "deviceId": fc.deviceId, "dimLevel": dim_level}
    return await runner.rest_connection.async_post("device/control/setDimLevel", data)


@Action.allowed_types("ACCELERATION_SENSOR_CHANNEL", "TILT_VIBRATION_SENSOR")
async def set_acceleration_sensor_mode_action(runner: Runner, fc: FunctionalChannel, mode: AccelerationSensorMode):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "accelerationSensorMode": str(mode),
    }
    return await runner.rest_connection.async_post("device/configuration/setAccelerationSensorMode", data)


@Action.allowed_types("ACCELERATION_SENSOR_CHANNEL", "TILT_VIBRATION_SENSOR")
async def set_acceleration_sensor_neutral_position(runner: Runner, fc: FunctionalChannel,
                                                   neutral_position: AccelerationSensorNeutralPosition):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "accelerationSensorNeutralPosition": str(neutral_position)
    }
    return await runner.rest_connection.async_post("device/configuration/setAccelerationSensorNeutralPosition", data)


@Action.allowed_types("ACCELERATION_SENSOR_CHANNEL", "TILT_VIBRATION_SENSOR")
async def set_acceleration_sensor_sensitivity(runner: Runner, fc: FunctionalChannel,
                                              sensitivity: AccelerationSensorSensitivity):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "accelerationSensorSensitivity": str(sensitivity),
    }
    return await runner.rest_connection.async_post("device/configuration/setAccelerationSensorSensitivity", data)


@Action.allowed_types("ACCELERATION_SENSOR_CHANNEL", "TILT_VIBRATION_SENSOR")
async def set_acceleration_sensor_trigger_angle(runner: Runner, fc: FunctionalChannel, angle: int):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "accelerationSensorTriggerAngle": angle
    }
    return await runner.rest_connection.async_post("device/configuration/setAccelerationSensorTriggerAngle", data)


@Action.allowed_types("ACCELERATION_SENSOR_CHANNEL", "TILT_VIBRATION_SENSOR")
async def set_acceleration_sensor_event_filter_period(runner: Runner, fc: FunctionalChannel, period: float):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "accelerationSensorEventFilterPeriod": period
    }
    return await runner.rest_connection.async_post("device/configuration/setAccelerationSensorEventFilterPeriod", data)


@Action.allowed_types("ACCELERATION_SENSOR_CHANNEL")
async def set_notification_sound_type(runner: Runner, fc: FunctionalChannel, sound_type: NotificationSoundType,
                                      is_high_to_low: bool):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "notificationSoundType": str(sound_type),
        "isHighToLow": is_high_to_low
    }
    return await runner.rest_connection.async_post("device/configuration/setNotificationSoundType", data)


@Action.allowed_types("DEVICE_BASE_FLOOR_HEATING")
async def set_minimum_floor_heating_valve_position(runner: Runner, fc: FunctionalChannel, position: float):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "minimumFloorHeatingValvePosition": position
    }
    return await runner.rest_connection.async_post("device/configuration/setMinimumFloorHeatingValvePosition", data)


@Action.allowed_types("DEVICE_OPERATIONLOCK", "DEVICE_OPERATIONLOCK_WITH_SABOTAGE")
async def set_operation_lock(runner: Runner, fc: FunctionalChannel, operation_lock: bool):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "operationLock": operation_lock
    }
    return await runner.rest_connection.async_post("device/configuration/setOperationLock", data)
