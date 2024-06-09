from homematicip.action.action import Action
from homematicip.action.registry import ActionTarget
from homematicip.connection.rest_connection import RestConnection
from homematicip.model.enums import AccelerationSensorMode, AccelerationSensorNeutralPosition, \
    AccelerationSensorSensitivity, NotificationSoundType, DoorCommand, LockState, RGBColorState, ClimateControlDisplay, \
    AcousticAlarmSignal, AcousticAlarmTiming, WaterAlarmTrigger, OpticalSignalBehaviour
from homematicip.model.model_components import FunctionalChannel
from homematicip.runner import Runner


@Action.allowed_types('BLIND_CHANNEL', 'MULTI_MODE_INPUT_BLIND_CHANNEL')
@Action.cli_commands("set_slats_level")
@Action.target_type(ActionTarget.FUNCTIONAL_CHANNEL)
async def async_set_slats_level_fc(rest_connection: RestConnection, fc: FunctionalChannel, slats_level: float,
                                   shutter_level: float = None):
    if shutter_level is None:
        shutter_level = fc.shutterLevel
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "slatsLevel": slats_level,
        "shutterLevel": shutter_level
    }
    return await rest_connection.async_post("device/control/setSlatsLevel", data)


@Action.allowed_types('BLIND_CHANNEL', 'MULTI_MODE_INPUT_BLIND_CHANNEL', 'SHUTTER_CHANNEL')
@Action.cli_commands("set_shutter_level")
@Action.target_type(ActionTarget.FUNCTIONAL_CHANNEL)
async def async_set_shutter_level_fc(rest_connection: RestConnection, fc: FunctionalChannel, shutter_level: float):
    data = {"channelIndex": fc.index, "deviceId": fc.deviceId, "shutterLevel": shutter_level}
    return await rest_connection.async_post("device/control/setShutterLevel", data)


@Action.allowed_types('BLIND_CHANNEL', 'MULTI_MODE_INPUT_BLIND_CHANNEL', 'SHUTTER_CHANNEL', 'SHADING_CHANNEL')
@Action.cli_commands("set_shutter_stop")
@Action.target_type(ActionTarget.FUNCTIONAL_CHANNEL)
async def async_set_shutter_stop_fc(rest_connection: RestConnection, fc: FunctionalChannel):
    data = {"channelIndex": fc.index, "deviceId": fc.deviceId}
    return await rest_connection.async_post("device/control/stop", data)


@Action.allowed_types('SWITCH_CHANNEL',
                      'MULTI_MODE_INPUT_SWITCH_CHANNEL',
                      'SWITCH_MEASURING_CHANNEL',
                      'OPTICAL_SIGNAL_CHANNEL')
@Action.cli_commands("set_switch_state", "turn_on", "turn_off")
@Action.target_type(ActionTarget.FUNCTIONAL_CHANNEL)
async def async_set_switch_state_fc(rest_connection: RestConnection, fc: FunctionalChannel, on: bool):
    data = {"channelIndex": fc.index, "deviceId": fc.deviceId, "on": on}
    return await rest_connection.async_post("device/control/setSwitchState", data)


@Action.allowed_types('IMPULSE_OUTPUT_CHANNEL')
@Action.cli_commands("toggle_garage_door")
@Action.target_type(ActionTarget.FUNCTIONAL_CHANNEL)
async def async_start_impulse_fc(rest_connection: RestConnection, fc: FunctionalChannel):
    """Toggle Wall mounted Garage Door Controller."""
    data = {"channelIndex": fc.index, "deviceId": fc.deviceId}
    return await rest_connection.async_post("device/control/startImpulse", data)


@Action.allowed_types("DIMMER_CHANNEL", "MULTI_MODE_INPUT_DIMMER_CHANNEL", "NOTIFICATION_LIGHT_CHANNEL")
@Action.cli_commands("set_dim_level")
@Action.target_type(ActionTarget.FUNCTIONAL_CHANNEL)
async def async_set_dim_level_fc(rest_connection: RestConnection, fc: FunctionalChannel, dim_level: float):
    data = {"channelIndex": fc.index, "deviceId": fc.deviceId, "dimLevel": dim_level}
    return await rest_connection.async_post("device/control/setDimLevel", data)


@Action.allowed_types("ACCELERATION_SENSOR_CHANNEL", "TILT_VIBRATION_SENSOR")
@Action.target_type(ActionTarget.FUNCTIONAL_CHANNEL)
async def async_set_acceleration_sensor_mode_action_fc(rest_connection: RestConnection, fc: FunctionalChannel,
                                                       mode: AccelerationSensorMode):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "accelerationSensorMode": mode.value,
    }
    return await rest_connection.async_post("device/configuration/setAccelerationSensorMode", data)


@Action.allowed_types("ACCELERATION_SENSOR_CHANNEL", "TILT_VIBRATION_SENSOR")
async def async_set_acceleration_sensor_neutral_position_fc(rest_connection: RestConnection, fc: FunctionalChannel,
                                                            neutral_position: AccelerationSensorNeutralPosition):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "accelerationSensorNeutralPosition": neutral_position.value
    }
    return await rest_connection.async_post("device/configuration/setAccelerationSensorNeutralPosition", data)


@Action.allowed_types("ACCELERATION_SENSOR_CHANNEL", "TILT_VIBRATION_SENSOR")
async def async_set_acceleration_sensor_sensitivity_fc(rest_connection: RestConnection, fc: FunctionalChannel,
                                                       sensitivity: AccelerationSensorSensitivity):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "accelerationSensorSensitivity": str(sensitivity),
    }
    return await rest_connection.async_post("device/configuration/setAccelerationSensorSensitivity", data)


@Action.allowed_types("ACCELERATION_SENSOR_CHANNEL", "TILT_VIBRATION_SENSOR")
async def async_set_acceleration_sensor_trigger_angle_fc(rest_connection: RestConnection, fc: FunctionalChannel,
                                                         angle: int):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "accelerationSensorTriggerAngle": angle
    }
    return await rest_connection.async_post("device/configuration/setAccelerationSensorTriggerAngle", data)


@Action.allowed_types("ACCELERATION_SENSOR_CHANNEL", "TILT_VIBRATION_SENSOR")
async def async_set_acceleration_sensor_event_filter_period_fc(rest_connection: RestConnection, fc: FunctionalChannel,
                                                               period: float):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "accelerationSensorEventFilterPeriod": period
    }
    return await rest_connection.async_post("device/configuration/setAccelerationSensorEventFilterPeriod", data)


@Action.allowed_types("ACCELERATION_SENSOR_CHANNEL")
async def async_set_notification_sound_type_fc(rest_connection: RestConnection, fc: FunctionalChannel,
                                               sound_type: NotificationSoundType,
                                               is_high_to_low: bool):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "notificationSoundType": sound_type.value,
        "isHighToLow": is_high_to_low
    }
    return await rest_connection.async_post("device/configuration/setNotificationSoundType", data)


@Action.allowed_types("DEVICE_BASE_FLOOR_HEATING")
async def async_set_minimum_floor_heating_valve_position_fc(rest_connection: RestConnection, fc: FunctionalChannel,
                                                            position: float):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "minimumFloorHeatingValvePosition": position
    }
    return await rest_connection.async_post("device/configuration/setMinimumFloorHeatingValvePosition", data)


@Action.allowed_types("DEVICE_OPERATIONLOCK", "DEVICE_OPERATIONLOCK_WITH_SABOTAGE")
async def async_set_operation_lock_fc(rest_connection: RestConnection, fc: FunctionalChannel, operation_lock: bool):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "operationLock": operation_lock
    }
    return await rest_connection.async_post("device/configuration/setOperationLock", data)


@Action.allowed_types("DOOR_CHANNEL")
async def async_send_door_command_fc(rest_connection: RestConnection, fc: FunctionalChannel, door_command: DoorCommand):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "doorCommand": door_command.value,
    }
    return await rest_connection.async_post("device/control/sendDoorCommand", data)


@Action.allowed_types("DOOR_LOCK_CHANNEL")
async def async_set_door_state_fc(rest_connection: RestConnection, fc: FunctionalChannel, lock_state: LockState,
                                  pin: str = None):
    data = {
        "deviceId": fc.deviceId,
        "channelIndex": fc.index,
        "authorizationPin": pin,
        "targetLockState": lock_state.value,
    }
    return await rest_connection.async_post("device/control/setLockState", data)


@Action.allowed_types("NOTIFICATION_LIGHT_CHANNEL", "OPTICAL_SIGNAL_CHANNEL")
async def async_set_optical_signal_fc(
        rest_connection: RestConnection,
        fc: FunctionalChannel,
        optical_signal_behaviour: OpticalSignalBehaviour,
        rgb: RGBColorState,
        dim_level=1.01,
):
    """sets the signal type for the leds

    Args:
        rest_connection(RestConnection): The rest connection
        fc(FunctionalChannel): The functional channel the action should be executed on
        optical_signal_behaviour(OpticalSignalBehaviour): LED signal behaviour
        rgb(RGBColorState): Color
        dim_level(float): usally 1.01. Use set_dim_level instead

    Returns:
        Result of the rest call

    """
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "dimLevel": dim_level,
        "opticalSignalBehaviour": optical_signal_behaviour.value,
        "simpleRGBColorState": rgb.value,
    }
    return await rest_connection.async_post("device/control/setOpticalSignal", data)


@Action.allowed_types("NOTIFICATION_LIGHT_CHANNEL")
async def async_set_rgb_dim_level_fc(rest_connection: RestConnection, fc: FunctionalChannel, rgb: RGBColorState,
                                     dim_level: float):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "simpleRGBColorState": rgb.value,
        "dimLevel": dim_level,
    }
    return await rest_connection.async_post("device/control/setSimpleRGBColorDimLevel", data)


@Action.allowed_types("NOTIFICATION_LIGHT_CHANNEL")
async def async_set_rgb_dim_level_with_time_fc(
        rest_connection: RestConnection,
        fc: FunctionalChannel,
        rgb: RGBColorState,
        dim_level: float,
        on_time: float,
        ramp_time: float,
):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "simpleRGBColorState": rgb.value,
        "dimLevel": dim_level,
        "onTime": on_time,
        "rampTime": ramp_time,
    }
    return await rest_connection.async_post("device/control/setSimpleRGBColorDimLevelWithTime", data)


@Action.allowed_types("SHADING_CHANNEL")
async def async_set_primary_shading_level_fc(rest_connection: RestConnection, fc: FunctionalChannel,
                                             primary_shading_level: float):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "primaryShadingLevel": primary_shading_level,
    }
    return await rest_connection.async_post("device/control/setPrimaryShadingLevel", data)


@Action.allowed_types("SHADING_CHANNEL")
async def async_set_secondary_shading_level_fc(rest_connection: RestConnection, fc: FunctionalChannel,
                                               primary_shading_level: float,
                                               secondary_shading_level: float):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "primaryShadingLevel": primary_shading_level,
        "secondaryShadingLevel": secondary_shading_level,
    }
    return await rest_connection.async_post("device/control/setSecondaryShadingLevel", data)


@Action.allowed_types("SWITCH_MEASURING_CHANNEL")
async def async_reset_energy_counter_fc(rest_connection: RestConnection, fc: FunctionalChannel):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId
    }
    return await rest_connection.async_post("device/control/resetEnergyCounter", data)


@Action.allowed_types("WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL")
@Action.cli_commands("set_display")
@Action.target_type(ActionTarget.FUNCTIONAL_CHANNEL)
async def async_set_display_fc(rest_connection: RestConnection, fc: FunctionalChannel, display: ClimateControlDisplay):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "display": display.value,
    }
    return await rest_connection.async_post("device/configuration/setClimateControlDisplay", data)


@Action.allowed_types("WATER_SENSOR_CHANNEL")
async def async_set_acoustic_alarm_signal_fc(rest_connection: RestConnection, fc: FunctionalChannel,
                                             acoustic_alarm_signal: AcousticAlarmSignal):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "acousticAlarmSignal": acoustic_alarm_signal.value,
    }
    return await rest_connection.async_post("device/configuration/setAcousticAlarmSignal", data)


@Action.allowed_types("WATER_SENSOR_CHANNEL")
async def async_set_acoustic_alarm_timing_fc(rest_connection: RestConnection, fc: FunctionalChannel,
                                             acoustic_alarm_timing: AcousticAlarmTiming):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "acousticAlarmTiming": acoustic_alarm_timing.value,
    }
    return await rest_connection.async_post("device/configuration/setAcousticAlarmTiming", data)


@Action.allowed_types("WATER_SENSOR_CHANNEL")
async def async_set_acoustic_water_alarm_trigger_fc(rest_connection: RestConnection, fc: FunctionalChannel,
                                                    acoustic_water_alarm_trigger: WaterAlarmTrigger):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "acousticWaterAlarmTrigger": acoustic_water_alarm_trigger.value,
    }
    return await rest_connection.async_post("device/configuration/setAcousticWaterAlarmTrigger", data)


@Action.allowed_types("WATER_SENSOR_CHANNEL")
async def async_set_inapp_water_alarm_trigger_fc(rest_connection: RestConnection, fc: FunctionalChannel,
                                                 inapp_water_alarm_trigger: WaterAlarmTrigger):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "inAppWaterAlarmTrigger": inapp_water_alarm_trigger.value,
    }
    return await rest_connection.async_post("device/configuration/setInAppWaterAlarmTrigger", data)


@Action.allowed_types("WATER_SENSOR_CHANNEL")
async def async_set_siren_water_alarm_trigger_fc(rest_connection: RestConnection, fc: FunctionalChannel,
                                                 siren_water_alarm_trigger: WaterAlarmTrigger):
    data = {
        "channelIndex": fc.index,
        "deviceId": fc.deviceId,
        "sirenWaterAlarmTrigger": siren_water_alarm_trigger.value,
    }
    return await rest_connection.async_post("device/configuration/setSirenWaterAlarmTrigger", data)
