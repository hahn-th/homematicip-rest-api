from homematicip.connection.rest_connection import RestConnection


async def reset_energy_counter_async(rest_connection: RestConnection, device_id: str, channel_index: int):
    """
    Reset the energy counter for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id
    }
    return await rest_connection.async_post("device/control/resetEnergyCounter", data)


async def reset_passage_counter_async(rest_connection: RestConnection, device_id: str, channel_index: int):
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id
    }
    return await rest_connection.async_post("device/control/resetPassageCounter", data)


async def reset_water_volume_async(rest_connection: RestConnection, device_id: str, channel_index: int):
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id
    }
    return await rest_connection.async_post("device/control/resetWaterVolume", data)


async def send_door_command_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                  door_command: str):
    """
    Send a door command.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param door_command: The door command as string. Possible values are defined in the DoorCommand enum.
    :type door_command: str
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "doorCommand": door_command,
    }
    return await rest_connection.async_post("device/control/sendDoorCommand", data)


async def set_color_temperature_dim_level_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                                color_temperature: int, dim_level: float):
    """
    Set the color temperature and dim level for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param color_temperature: The desired color temperature in Kelvin. Between 1000 K(Kelvin) to 10000 K
    :type color_temperature: int
    :param dim_level: The desired dim level (0.0 to 1.0).
    :type dim_level: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "colorTemperature": color_temperature,
        "dimLevel": dim_level
    }
    return await rest_connection.async_post("device/control/setColorTemperatureDimLevel", data)


async def set_color_temperature_dim_level_with_time_async(rest_connection: RestConnection, device_id: str,
                                                          channel_index: int,
                                                          color_temperature: int, dim_level: float, on_time: float,
                                                          ramp_time: float):
    """
    Set the color temperature and dim level with time for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param color_temperature: The desired color temperature in Kelvin. Between 1000 K(Kelvin) to 10000 K
    :type color_temperature: int
    :param dim_level: The desired dim level (0.0 to 1.0).
    :type dim_level: float
    :param on_time: The on time in seconds.
    :type on_time: float
    :param ramp_time: The ramp time in seconds.
    :type ramp_time: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "colorTemperature": color_temperature,
        "dimLevel": dim_level,
        "onTime": on_time,
        "rampTime": ramp_time
    }
    return await rest_connection.async_post("device/control/setColorTemperatureDimLevelWithTime", data)


async def set_dim_level_async(rest_connection: RestConnection, device_id: str, channel_index: int, dim_level: float):
    """
    Set the dim level for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param dim_level: The desired dim level.
    :type dim_level: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {"channelIndex": channel_index, "deviceId": device_id, "dimLevel": dim_level}
    return await rest_connection.async_post("device/control/setDimLevel", data)


async def set_dim_level_with_time_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                        dim_level: float, on_time: float, ramp_time: float):
    """
    Set the dim level with time for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param dim_level: The desired dim level.
    :type dim_level: float
    :param on_time: The on time in seconds.
    :type on_time: float
    :param ramp_time: The ramp time in seconds.
    :type ramp_time: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "dimLevel": dim_level,
        "onTime": on_time,
        "rampTime": ramp_time
    }
    return await rest_connection.async_post("device/control/setDimLevelWithTime", data)


async def set_favorite_shading_position(rest_connection: RestConnection, device_id: str, channel_index: int):
    """ Set the favorite shading position for a functional channel.
    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id
    }
    return await rest_connection.async_post("device/control/setFavoriteShadingPosition", data)


async def set_hue_saturation_dim_level_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                             hue: int, saturation_level: float, dim_level: float):
    """
    Set the hue, saturation, and dim level for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param hue: The desired hue (0-360).
    :type hue: int
    :param saturation_level: The desired saturation level (0.0 to 1.0).
    :type saturation_level: float
    :param dim_level: The desired dim level (0.0 to 1.0).
    :type dim_level: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "hue": hue,
        "saturationLevel": saturation_level,
        "dimLevel": dim_level
    }
    return await rest_connection.async_post("device/control/setHueSaturationDimLevel", data)


async def set_hue_saturation_dim_level_with_time_async(rest_connection: RestConnection, device_id: str,
                                                       channel_index: int,
                                                       hue: int, saturation_level: float, dim_level: float,
                                                       on_time: float, ramp_time: float):
    """
    Set the hue, saturation, and dim level with time for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param hue: The desired hue (0-360).
    :type hue: int
    :param saturation_level: The desired saturation level (0.0 to 1.0).
    :type saturation_level: float
    :param dim_level: The desired dim level (0.0 to 1.0).
    :type dim_level: float
    :param on_time: The on time in seconds.
    :type on_time: float
    :param ramp_time: The ramp time in seconds.
    :type ramp_time: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "hue": hue,
        "saturationLevel": saturation_level,
        "dimLevel": dim_level,
        "onTime": on_time,
        "rampTime": ramp_time
    }
    return await rest_connection.async_post("device/control/setHueSaturationDimLevelWithTime", data)


async def set_lock_state_async(rest_connection: RestConnection, device_id: str, channel_index: int, lock_state: str,
                               pin: str = None):
    """
    Set the door lock state.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param lock_state: The lock state as string. Possible values are defined in the LockState enum.
    :type lock_state: str
    :param pin: The authorization pin (optional).
    :type pin: str or None
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "deviceId": device_id,
        "channelIndex": channel_index,
        "authorizationPin": pin,
        "targetLockState": lock_state,
    }
    return await rest_connection.async_post("device/control/setLockState", data)


async def set_motion_detection_active_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                            motion_detection_active: bool):
    """
    Set the motion detection active state for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param motion_detection_active: Whether motion detection is active (True) or not (False).
    :type motion_detection_active: bool
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "motionDetectionActive": motion_detection_active
    }
    return await rest_connection.async_post("device/control/setMotionDetectionActive", data)


async def set_optical_signal_async(
        rest_connection: RestConnection,
        device_id: str,
        channel_index: int,
        optical_signal_behaviour: str,
        rgb: str,
        dim_level=1.01,
):
    """
    Set the signal type for the LEDs.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param optical_signal_behaviour: The optical signal behaviour as string. Possible values are defined in the OpticalSignalBehaviour enum.
    :type optical_signal_behaviour: str
    :param rgb: The RGB color as string. Possible values are defined in the RGBColorState enum.
    :type rgb: str
    :param dim_level: The dim level (usually 1.01). Use set_dim_level instead.
    :type dim_level: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "dimLevel": dim_level,
        "opticalSignalBehaviour": optical_signal_behaviour,
        "simpleRGBColorState": rgb,
    }
    return await rest_connection.async_post("device/control/setOpticalSignal", data)


async def set_optical_signal_with_time_async(
        rest_connection: RestConnection, device_id: str, channel_index: int, optical_signal_behaviour: str,
        simple_rgb_color_state: str, on_time: float, ramp_time: float, dim_level: float = 1.01):
    """
    Set the optical signal with time for a functional channel.
    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param optical_signal_behaviour: The optical signal behaviour as string. Possible values are defined in the OpticalSignalBehaviour enum.
    :type optical_signal_behaviour: str
    :param simple_rgb_color_state: The RGB color as string. Possible values are defined in the RGBColorState enum.
    :type simple_rgb_color_state: str
    :param on_time: The on time in seconds.
    :type on_time: float
    :param ramp_time: The ramp time in seconds.
    :type ramp_time: float
    :param dim_level: The dim level (usually 1.01). Use set_dim_level instead.
    :type dim_level: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "opticalSignalBehaviour": optical_signal_behaviour,
        "simpleRGBColorState": simple_rgb_color_state,
        "onTime": on_time,
        "rampTime": ramp_time,
        "dimLevel": dim_level
    }
    return await rest_connection.async_post("device/control/setOpticalSignalWithTime", data)


async def set_primary_shading_level_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                          primary_shading_level: float):
    """
    Set the primary shading level for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param primary_shading_level: The desired primary shading level.
    :type primary_shading_level: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "primaryShadingLevel": primary_shading_level,
    }
    return await rest_connection.async_post("device/control/setPrimaryShadingLevel", data)


async def set_secondary_shading_level_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                            primary_shading_level: float,
                                            secondary_shading_level: float):
    """
    Set the secondary shading level for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param primary_shading_level: The desired primary shading level.
    :type primary_shading_level: float
    :param secondary_shading_level: The desired secondary shading level.
    :type secondary_shading_level: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "primaryShadingLevel": primary_shading_level,
        "secondaryShadingLevel": secondary_shading_level,
    }
    return await rest_connection.async_post("device/control/setSecondaryShadingLevel", data)


async def set_shutter_level_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                  shutter_level: float):
    """
    Set the shutter level for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param shutter_level: The desired shutter level.
    :type shutter_level: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {"channelIndex": channel_index, "deviceId": device_id, "shutterLevel": shutter_level}
    return await rest_connection.async_post("device/control/setShutterLevel", data)


async def set_simple_rgb_color_dim_level_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                               simple_rgb_color_state: str, dim_level: float):
    """
    Set the simple RGB color and dim level for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param simple_rgb_color_state: The RGB color as string. Possible values are defined in the RGBColorState enum.
    :type simple_rgb_color_state: str
    :param dim_level: The desired dim level (0.0 to 1.0).
    :type dim_level: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "simpleRGBColorState": simple_rgb_color_state,
        "dimLevel": dim_level
    }
    return await rest_connection.async_post("device/control/setSimpleRGBColorDimLevel", data)


async def set_simple_rgb_color_dim_level_with_time_async(
        rest_connection: RestConnection,
        device_id: str,
        channel_index: int,
        simple_rgb_color_state: str,
        dim_level: float,
        on_time: float,
        ramp_time: float
) -> dict:
    """
    Set the RGB color and dim level with on and ramp time for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param simple_rgb_color_state: The RGB color as string. Possible values are defined in the RGBColorState enum.
    :type simple_rgb_color_state: str
    :param dim_level: The desired dim level (0.0 to 1.0).
    :type dim_level: float
    :param on_time: The on time in seconds.
    :type on_time: float
    :param ramp_time: The ramp time in seconds.
    :type ramp_time: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "simpleRGBColorState": simple_rgb_color_state,
        "dimLevel": dim_level,
        "onTime": on_time,
        "rampTime": ramp_time
    }
    return await rest_connection.async_post("device/control/setSimpleRGBColorDimLevelWithTime", data)


async def set_slats_level_async(rest_connection: RestConnection, device_id: str, channel_index: int, slats_level: float,
                                shutter_level: float):
    """
    Set the slats level for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param slats_level: The desired slats level.
    :type slats_level: float
    :param shutter_level: The desired shutter level (optional).
    :type shutter_level: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "slatsLevel": slats_level,
        "shutterLevel": shutter_level
    }
    return await rest_connection.async_post("device/control/setSlatsLevel", data)


async def set_switch_state_async(rest_connection: RestConnection, device_id: str, channel_index: int, on: bool):
    """
    Set the switch state for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param on: The desired switch state (True for ON, False for OFF).
    :type on: bool
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {"channelIndex": channel_index, "deviceId": device_id, "on": on}
    return await rest_connection.async_post("device/control/setSwitchState", data)


async def set_shutter_stop_async(rest_connection: RestConnection, device_id: str, channel_index: int):
    """
    Stop the shutter for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {"channelIndex": channel_index, "deviceId": device_id}
    return await rest_connection.async_post("device/control/stop", data)


async def start_impulse_async(rest_connection: RestConnection, device_id: str, channel_index: int):
    """Toggle Wall mounted Garage Door Controller."""
    data = {"channelIndex": channel_index, "deviceId": device_id}
    return await rest_connection.async_post("device/control/startImpulse", data)


async def set_acceleration_sensor_mode_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                             mode: str):
    """
    Set the mode for the acceleration sensor.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param mode: The mode as string. Possible values are defined in the AccelerationSensorMode enum.
    :type mode: str
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "accelerationSensorMode": mode,
    }
    return await rest_connection.async_post("device/configuration/setAccelerationSensorMode", data)


async def set_acceleration_sensor_neutral_position_async(rest_connection: RestConnection, device_id: str,
                                                         channel_index: int,
                                                         neutral_position: str):
    """
    Set the neutral position for the acceleration sensor.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param neutral_position: The neutral position as string. Possible values are defined in the AccelerationSensorNeutralPosition enum.
    :type neutral_position: str
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "accelerationSensorNeutralPosition": neutral_position
    }
    return await rest_connection.async_post("device/configuration/setAccelerationSensorNeutralPosition", data)


async def set_acceleration_sensor_sensitivity_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                                    sensitivity: str):
    """
    Set the sensitivity for the acceleration sensor.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param sensitivity: The sensitivity as string. Possible values are defined in the AccelerationSensorSensitivity enum.
    :type sensitivity: str
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "accelerationSensorSensitivity": sensitivity,
    }
    return await rest_connection.async_post("device/configuration/setAccelerationSensorSensitivity", data)


async def set_acceleration_sensor_trigger_angle_async(rest_connection: RestConnection, device_id: str,
                                                      channel_index: int,
                                                      angle: int):
    """
    Set the trigger angle for the acceleration sensor.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param angle: The trigger angle in degrees.
    :type angle: int
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "accelerationSensorTriggerAngle": angle
    }
    return await rest_connection.async_post("device/configuration/setAccelerationSensorTriggerAngle", data)


async def set_acceleration_sensor_event_filter_period_async(rest_connection: RestConnection, device_id: str,
                                                            channel_index: int,
                                                            period: float):
    """
    Set the event filter period for the acceleration sensor.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param period: The event filter period in seconds.
    :type period: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "accelerationSensorEventFilterPeriod": period
    }
    return await rest_connection.async_post("device/configuration/setAccelerationSensorEventFilterPeriod", data)


async def set_notification_sound_type_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                            sound_type: str,
                                            is_high_to_low: bool):
    """
    Set the notification sound type.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param sound_type: The sound type as string. Possible values are defined in the AcousticAlarmSignal enum.
    :type sound_type: str
    :param is_high_to_low: Whether the signal is high to low.
    :type is_high_to_low: bool
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "notificationSoundType": sound_type,
        "isHighToLow": is_high_to_low
    }
    return await rest_connection.async_post("device/configuration/setNotificationSoundType", data)


async def set_minimum_floor_heating_valve_position_async(rest_connection: RestConnection,
                                                         device_id: str,
                                                         channel_index: int,
                                                         position: float):
    """
    Set the minimum floor heating valve position.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param position: The desired minimum valve position.
    :type position: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "minimumFloorHeatingValvePosition": position
    }
    return await rest_connection.async_post("device/configuration/setMinimumFloorHeatingValvePosition", data)


async def set_operation_lock_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                   operation_lock: bool):
    """
    Set the operation lock for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param operation_lock: The desired operation lock state (True for locked, False for unlocked).
    :type operation_lock: bool
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "operationLock": operation_lock
    }
    return await rest_connection.async_post("device/configuration/setOperationLock", data)


async def set_watering_switch_state_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                          watering_active: bool):
    """
    Set the watering switch state for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param watering_active: The desired watering state (True for active, False for inactive).
    :type watering_active: bool
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "wateringActive": watering_active
    }
    return await rest_connection.async_post("device/control/setWateringSwitchState", data)


async def set_watering_switch_state_with_time_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                                    watering_active: bool, watering_time: float):
    """
    Set the watering switch state for a functional channel with a specific watering time.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param watering_active: The desired watering state (True for active, False for inactive).
    :type watering_active: bool
    :param watering_time: The watering time in seconds.
    :type watering_time: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "wateringActive": watering_active,
        "wateringTime": watering_time
    }
    return await rest_connection.async_post("device/control/setWateringSwitchStateWithTime", data)


async def set_display_async(rest_connection: RestConnection, device_id: str, channel_index: int, display: str):
    """
    Set the climate control display.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param display: The display as string. Possible values are defined in the ClimateControlDisplay enum.
    :type display: str
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "display": display,
    }
    return await rest_connection.async_post("device/configuration/setClimateControlDisplay", data)


async def set_acoustic_alarm_signal_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                          acoustic_alarm_signal: str):
    """
    Set the acoustic alarm signal.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param acoustic_alarm_signal: The acoustic alarm signal as string. Possible values are defined in the AcousticAlarmSignal enum.
    :type acoustic_alarm_signal: str
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "acousticAlarmSignal": acoustic_alarm_signal,
    }
    return await rest_connection.async_post("device/configuration/setAcousticAlarmSignal", data)


async def set_acoustic_alarm_timing_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                          acoustic_alarm_timing: str):
    """
    Set the acoustic alarm timing.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param acoustic_alarm_timing: The acoustic alarm timing as string. Possible values are defined in the AcousticAlarmTiming enum.
    :type acoustic_alarm_timing: str
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "acousticAlarmTiming": acoustic_alarm_timing,
    }
    return await rest_connection.async_post("device/configuration/setAcousticAlarmTiming", data)


async def set_acoustic_water_alarm_trigger_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                                 acoustic_water_alarm_trigger: str):
    """
    Set the acoustic water alarm trigger.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param acoustic_water_alarm_trigger: The acoustic water alarm trigger as string. Possible values are defined in the WaterAlarmTrigger enum.
    :type acoustic_water_alarm_trigger: str
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "acousticWaterAlarmTrigger": acoustic_water_alarm_trigger,
    }
    return await rest_connection.async_post("device/configuration/setAcousticWaterAlarmTrigger", data)


async def set_inapp_water_alarm_trigger_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                              inapp_water_alarm_trigger: str):
    """
    Set the in-app water alarm trigger.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param inapp_water_alarm_trigger: The in-app water alarm trigger as string. Possible values are defined in the WaterAlarmTrigger enum.
    :type inapp_water_alarm_trigger: str
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "inAppWaterAlarmTrigger": inapp_water_alarm_trigger,
    }
    return await rest_connection.async_post("device/configuration/setInAppWaterAlarmTrigger", data)


async def set_siren_water_alarm_trigger_async(rest_connection: RestConnection, device_id: str, channel_index: int,
                                              siren_water_alarm_trigger: str):
    """
    Set the siren water alarm trigger.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param siren_water_alarm_trigger: The siren water alarm trigger as string. Possible values are defined in the WaterAlarmTrigger enum.
    :type siren_water_alarm_trigger: str
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "sirenWaterAlarmTrigger": siren_water_alarm_trigger,
    }
    return await rest_connection.async_post("device/configuration/setSirenWaterAlarmTrigger", data)


async def start_light_scene_async(rest_connection: RestConnection, device_id: str, channel_index: int, scene_id: int,
                                  dim_level: float):
    """
    Start a light scene for a functional channel.

    :param rest_connection: The REST connection instance.
    :type rest_connection: RestConnection
    :param device_id: The device ID.
    :type device_id: str
    :param channel_index: The channel index.
    :type channel_index: int
    :param scene_id: The ID of the light scene.
    :type scene_id: int
    :param dim_level: The desired dim level (0.0 to 1.0).
    :type dim_level: float
    :return: The response from the cloud.
    :rtype: dict
    """
    data = {
        "channelIndex": channel_index,
        "deviceId": device_id,
        "id": scene_id,
        "dimLevel": dim_level
    }
    return await rest_connection.async_post("device/control/startLightScene", data)
