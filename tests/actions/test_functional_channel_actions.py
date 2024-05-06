import pytest

from homematicip.action.functional_channel_actions import action_start_impulse, action_set_switch_state, \
    action_set_slats_level, action_set_shutter_level, action_set_dim_level, set_acceleration_sensor_mode_action, \
    set_acceleration_sensor_neutral_position, set_acceleration_sensor_sensitivity, \
    set_acceleration_sensor_trigger_angle, set_acceleration_sensor_event_filter_period, set_notification_sound_type, \
    set_minimum_floor_heating_valve_position, set_operation_lock, action_send_door_command, action_set_door_state, \
    action_set_rgb_dim_level, action_set_rgb_dim_level_with_time, action_set_primary_shading_level, \
    action_set_secondary_shading_level, action_reset_energy_counter, action_set_display, \
    action_set_acoustic_alarm_signal, action_set_acoustic_alarm_timing, action_set_acoustic_water_alarm_trigger, \
    action_set_inapp_water_alarm_trigger, action_set_siren_water_alarm_trigger
from homematicip.connection.rest_connection import RestResult, RestConnection
from homematicip.model.enums import AccelerationSensorMode, AccelerationSensorNeutralPosition, \
    AccelerationSensorSensitivity, NotificationSoundType, DoorCommand, LockState, RGBColorState, ClimateControlDisplay, \
    AcousticAlarmSignal, AcousticAlarmTiming, WaterAlarmTrigger
from homematicip.model.functional_channels import FunctionalChannel
from homematicip.runner import Runner


@pytest.fixture
def runner(mocker, filled_model):
    conn = mocker.Mock(spec=RestConnection)
    conn.async_post.return_value = RestResult(status=200)
    runner = Runner(_rest_connection=conn, model=filled_model)
    return runner


@pytest.fixture
def sample_functional_channel() -> FunctionalChannel:
    return FunctionalChannel(index=1, deviceId="00000000-0000-0000-0000-000000000001", groups=[])


@pytest.mark.asyncio
async def test_set_slats_level(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "BLIND_CHANNEL"
    sample_functional_channel.shutterLevel = 0.5
    result = await action_set_slats_level(runner, sample_functional_channel, 0.4)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setSlatsLevel"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["shutterLevel"] == 0.5
    assert runner.rest_connection.async_post.call_args[0][1]["slatsLevel"] == 0.4
    assert result.status == 200

    result = await action_set_slats_level(runner, sample_functional_channel, 0.3, shutter_level=0.8)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setSlatsLevel"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["shutterLevel"] == 0.8
    assert runner.rest_connection.async_post.call_args[0][1]["slatsLevel"] == 0.3
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_shutter_level(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "BLIND_CHANNEL"
    result = await action_set_shutter_level(runner, sample_functional_channel, 0.4)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setShutterLevel"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["shutterLevel"] == 0.4
    assert result.status == 200


@pytest.mark.asyncio
async def test_action_set_switch_state(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "SWITCH_CHANNEL"
    result = await action_set_switch_state(runner, sample_functional_channel, True)
    assert result.status == 200


@pytest.mark.asyncio
async def test_start_impulse(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "IMPULSE_OUTPUT_CHANNEL"
    result = await action_start_impulse(runner, sample_functional_channel)
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_dim_level(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "DIMMER_CHANNEL"
    result = await action_set_dim_level(runner, sample_functional_channel, 0.5)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setDimLevel"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["dimLevel"] == 0.5
    assert result.status == 200


@pytest.mark.asyncio
async def test_acceleration_sensor_mode(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "ACCELERATION_SENSOR_CHANNEL"
    result = await set_acceleration_sensor_mode_action(runner, sample_functional_channel,
                                                       AccelerationSensorMode.FLAT_DECT)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setAccelerationSensorMode"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["accelerationSensorMode"] == str(
        AccelerationSensorMode.FLAT_DECT)
    assert result.status == 200


@pytest.mark.asyncio
async def test_acceleration_sensor_neutral_position(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "ACCELERATION_SENSOR_CHANNEL"
    result = await set_acceleration_sensor_neutral_position(runner, sample_functional_channel,
                                                            AccelerationSensorNeutralPosition.VERTICAL)
    assert runner.rest_connection.async_post.call_args[0][
               0] == "device/configuration/setAccelerationSensorNeutralPosition"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["accelerationSensorNeutralPosition"] == str(
        AccelerationSensorNeutralPosition.VERTICAL)
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_acceleration_sensor_sensitivity(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "ACCELERATION_SENSOR_CHANNEL"
    result = await set_acceleration_sensor_sensitivity(runner, sample_functional_channel,
                                                       AccelerationSensorSensitivity.SENSOR_RANGE_2G)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setAccelerationSensorSensitivity"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["accelerationSensorSensitivity"] == str(
        AccelerationSensorSensitivity.SENSOR_RANGE_2G)
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_acceleration_sensor_trigger_angle(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "ACCELERATION_SENSOR_CHANNEL"
    result = await set_acceleration_sensor_trigger_angle(runner, sample_functional_channel, 45)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setAccelerationSensorTriggerAngle"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["accelerationSensorTriggerAngle"] == 45
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_acceleration_sensor_event_filter_period(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "ACCELERATION_SENSOR_CHANNEL"
    result = await set_acceleration_sensor_event_filter_period(runner, sample_functional_channel, 0.5)
    assert runner.rest_connection.async_post.call_args[0][
               0] == "device/configuration/setAccelerationSensorEventFilterPeriod"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["accelerationSensorEventFilterPeriod"] == 0.5
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_notification_sound_type(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "ACCELERATION_SENSOR_CHANNEL"
    result = await set_notification_sound_type(runner, sample_functional_channel, NotificationSoundType.SOUND_NO_SOUND,
                                               True)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setNotificationSoundType"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["notificationSoundType"] == str(
        NotificationSoundType.SOUND_NO_SOUND)
    assert runner.rest_connection.async_post.call_args[0][1]["isHighToLow"] == True
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_minimum_floor_heating_valve_position(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "DEVICE_BASE_FLOOR_HEATING"
    result = await set_minimum_floor_heating_valve_position(runner, sample_functional_channel, 0.5)
    assert runner.rest_connection.async_post.call_args[0][
               0] == "device/configuration/setMinimumFloorHeatingValvePosition"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["minimumFloorHeatingValvePosition"] == 0.5
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_operation_lock(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "DEVICE_OPERATIONLOCK"
    result = await set_operation_lock(runner, sample_functional_channel, True)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setOperationLock"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["operationLock"] is True
    assert result.status == 200


@pytest.mark.asyncio
async def test_send_door_command(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "DOOR_CHANNEL"
    result = await action_send_door_command(runner, sample_functional_channel, DoorCommand.OPEN)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/sendDoorCommand"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["doorCommand"] == str(DoorCommand.OPEN)
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_door_state(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "DOOR_LOCK_CHANNEL"
    result = await action_set_door_state(runner, sample_functional_channel, LockState.OPEN, "1234")
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setLockState"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["authorizationPin"] == "1234"
    assert runner.rest_connection.async_post.call_args[0][1]["targetLockState"] == str(LockState.OPEN)
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_rgb_dim_level(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "NOTIFICATION_LIGHT_CHANNEL"
    result = await action_set_rgb_dim_level(runner, sample_functional_channel, RGBColorState.BLUE, 0.5)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setSimpleRGBColorDimLevel"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["dimLevel"] == 0.5
    assert runner.rest_connection.async_post.call_args[0][1]["simpleRGBColorState"] == str(RGBColorState.BLUE)
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_rgb_dim_level_with_time(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "NOTIFICATION_LIGHT_CHANNEL"
    result = await action_set_rgb_dim_level_with_time(runner, sample_functional_channel, RGBColorState.BLUE, 0.5, 10.5,
                                                      20.5)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setSimpleRGBColorDimLevelWithTime"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["dimLevel"] == 0.5
    assert runner.rest_connection.async_post.call_args[0][1]["onTime"] == 10.5
    assert runner.rest_connection.async_post.call_args[0][1]["rampTime"] == 20.5
    assert runner.rest_connection.async_post.call_args[0][1]["simpleRGBColorState"] == str(RGBColorState.BLUE)
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_primary_shading_level(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "SHADING_CHANNEL"
    result = await action_set_primary_shading_level(runner, sample_functional_channel, 0.5)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setPrimaryShadingLevel"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["primaryShadingLevel"] == 0.5
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_secondary_shading_level(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "SHADING_CHANNEL"
    result = await action_set_secondary_shading_level(runner, sample_functional_channel, 0.5, 0.8)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setSecondaryShadingLevel"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["primaryShadingLevel"] == 0.5
    assert runner.rest_connection.async_post.call_args[0][1]["secondaryShadingLevel"] == 0.8
    assert result.status == 200


@pytest.mark.asyncio
async def test_reset_energy_counter(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "SWITCH_MEASURING_CHANNEL"
    result = await action_reset_energy_counter(runner, sample_functional_channel)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/resetEnergyCounter"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_display(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL"
    result = await action_set_display(runner, sample_functional_channel, ClimateControlDisplay.ACTUAL)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setClimateControlDisplay"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["display"] == str(ClimateControlDisplay.ACTUAL)
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_acoustic_alarm_signal(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "WATER_SENSOR_CHANNEL"
    result = await action_set_acoustic_alarm_signal(runner, sample_functional_channel,
                                                    AcousticAlarmSignal.DISABLE_ACOUSTIC_SIGNAL)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setAcousticAlarmSignal"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["acousticAlarmSignal"] == str(
        AcousticAlarmSignal.DISABLE_ACOUSTIC_SIGNAL)
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_acoustic_alarm_timing(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "WATER_SENSOR_CHANNEL"
    result = await action_set_acoustic_alarm_timing(runner, sample_functional_channel,
                                                    AcousticAlarmTiming.PERMANENT)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setAcousticAlarmTiming"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["acousticAlarmTiming"] == str(
        AcousticAlarmTiming.PERMANENT)
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_acoustic_water_alarm_trigger(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "WATER_SENSOR_CHANNEL"
    result = await action_set_acoustic_water_alarm_trigger(runner, sample_functional_channel,
                                                           WaterAlarmTrigger.WATER_DETECTION)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setAcousticWaterAlarmTrigger"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["acousticWaterAlarmTrigger"] == str(
        WaterAlarmTrigger.WATER_DETECTION)
    assert result.status == 200


@pytest.mark.asyncio
async def test_action_set_inapp_water_alarm_trigger(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "WATER_SENSOR_CHANNEL"
    result = await action_set_inapp_water_alarm_trigger(runner, sample_functional_channel,
                                                        WaterAlarmTrigger.WATER_DETECTION)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setInAppWaterAlarmTrigger"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["inAppWaterAlarmTrigger"] == str(
        WaterAlarmTrigger.WATER_DETECTION)
    assert result.status == 200


@pytest.mark.asyncio
async def test_action_set_siren_water_alarm_trigger(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "WATER_SENSOR_CHANNEL"
    result = await action_set_siren_water_alarm_trigger(runner, sample_functional_channel, WaterAlarmTrigger.WATER_DETECTION)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setSirenWaterAlarmTrigger"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["sirenWaterAlarmTrigger"] == str(WaterAlarmTrigger.WATER_DETECTION)
    assert result.status == 200