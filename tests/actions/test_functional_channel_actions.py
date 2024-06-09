import pytest

from homematicip.action.functional_channel_actions import async_start_impulse_fc, async_set_switch_state_fc, \
    async_set_slats_level_fc, async_set_shutter_level_fc, async_set_dim_level_fc, async_set_acceleration_sensor_mode_action_fc, \
    async_set_acceleration_sensor_neutral_position_fc, async_set_acceleration_sensor_sensitivity_fc, \
    async_set_acceleration_sensor_trigger_angle_fc, async_set_acceleration_sensor_event_filter_period_fc, async_set_notification_sound_type_fc, \
    async_set_minimum_floor_heating_valve_position_fc, async_set_operation_lock_fc, async_send_door_command_fc, async_set_door_state_fc, \
    async_set_rgb_dim_level_fc, async_set_rgb_dim_level_with_time_fc, async_set_primary_shading_level_fc, \
    async_set_secondary_shading_level_fc, async_reset_energy_counter_fc, async_set_display_fc, \
    async_set_acoustic_alarm_signal_fc, async_set_acoustic_alarm_timing_fc, async_set_acoustic_water_alarm_trigger_fc, \
    async_set_inapp_water_alarm_trigger_fc, async_set_siren_water_alarm_trigger_fc, async_set_optical_signal_fc
from homematicip.connection.rest_connection import RestResult, RestConnection
from homematicip.model.enums import AccelerationSensorMode, AccelerationSensorNeutralPosition, \
    AccelerationSensorSensitivity, NotificationSoundType, DoorCommand, LockState, RGBColorState, ClimateControlDisplay, \
    AcousticAlarmSignal, AcousticAlarmTiming, WaterAlarmTrigger, OpticalSignalBehaviour
from homematicip.model.model_components import FunctionalChannel
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
    result = await async_set_slats_level_fc(runner.rest_connection, sample_functional_channel, 0.4)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setSlatsLevel"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["shutterLevel"] == 0.5
    assert runner.rest_connection.async_post.call_args[0][1]["slatsLevel"] == 0.4
    assert result.status == 200

    result = await async_set_slats_level_fc(runner.rest_connection, sample_functional_channel, 0.3, shutter_level=0.8)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setSlatsLevel"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["shutterLevel"] == 0.8
    assert runner.rest_connection.async_post.call_args[0][1]["slatsLevel"] == 0.3
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_shutter_level(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "BLIND_CHANNEL"
    result = await async_set_shutter_level_fc(runner.rest_connection, sample_functional_channel, 0.4)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setShutterLevel"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["shutterLevel"] == 0.4
    assert result.status == 200


@pytest.mark.asyncio
async def test_action_set_switch_state(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "SWITCH_CHANNEL"
    result = await async_set_switch_state_fc(runner.rest_connection, sample_functional_channel, True)
    assert result.status == 200


@pytest.mark.asyncio
async def test_start_impulse(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "IMPULSE_OUTPUT_CHANNEL"
    result = await async_start_impulse_fc(runner.rest_connection, sample_functional_channel)
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_dim_level(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "DIMMER_CHANNEL"
    result = await async_set_dim_level_fc(runner.rest_connection, sample_functional_channel, 0.5)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setDimLevel"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["dimLevel"] == 0.5
    assert result.status == 200


@pytest.mark.asyncio
async def test_acceleration_sensor_mode(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "ACCELERATION_SENSOR_CHANNEL"
    result = await async_set_acceleration_sensor_mode_action_fc(runner.rest_connection, sample_functional_channel,
                                                                AccelerationSensorMode.FLAT_DECT)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setAccelerationSensorMode"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["accelerationSensorMode"] == AccelerationSensorMode.FLAT_DECT.value
    assert result.status == 200


@pytest.mark.asyncio
async def test_acceleration_sensor_neutral_position(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "ACCELERATION_SENSOR_CHANNEL"
    result = await async_set_acceleration_sensor_neutral_position_fc(runner.rest_connection, sample_functional_channel,
                                                                     AccelerationSensorNeutralPosition.VERTICAL)
    assert runner.rest_connection.async_post.call_args[0][
               0] == "device/configuration/setAccelerationSensorNeutralPosition"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["accelerationSensorNeutralPosition"] == AccelerationSensorNeutralPosition.VERTICAL.value
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_acceleration_sensor_sensitivity(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "ACCELERATION_SENSOR_CHANNEL"
    result = await async_set_acceleration_sensor_sensitivity_fc(runner.rest_connection, sample_functional_channel,
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
    result = await async_set_acceleration_sensor_trigger_angle_fc(runner.rest_connection, sample_functional_channel, 45)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setAccelerationSensorTriggerAngle"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["accelerationSensorTriggerAngle"] == 45
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_acceleration_sensor_event_filter_period(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "ACCELERATION_SENSOR_CHANNEL"
    result = await async_set_acceleration_sensor_event_filter_period_fc(runner.rest_connection, sample_functional_channel, 0.5)
    assert runner.rest_connection.async_post.call_args[0][
               0] == "device/configuration/setAccelerationSensorEventFilterPeriod"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["accelerationSensorEventFilterPeriod"] == 0.5
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_notification_sound_type(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "ACCELERATION_SENSOR_CHANNEL"
    result = await async_set_notification_sound_type_fc(runner.rest_connection, sample_functional_channel, NotificationSoundType.SOUND_NO_SOUND,
                                               True)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setNotificationSoundType"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["notificationSoundType"] == NotificationSoundType.SOUND_NO_SOUND.value
    assert runner.rest_connection.async_post.call_args[0][1]["isHighToLow"] == True
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_minimum_floor_heating_valve_position(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "DEVICE_BASE_FLOOR_HEATING"
    result = await async_set_minimum_floor_heating_valve_position_fc(runner.rest_connection, sample_functional_channel, 0.5)
    assert runner.rest_connection.async_post.call_args[0][
               0] == "device/configuration/setMinimumFloorHeatingValvePosition"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["minimumFloorHeatingValvePosition"] == 0.5
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_operation_lock(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "DEVICE_OPERATIONLOCK"
    result = await async_set_operation_lock_fc(runner.rest_connection, sample_functional_channel, True)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setOperationLock"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["operationLock"] is True
    assert result.status == 200


@pytest.mark.asyncio
async def test_send_door_command(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "DOOR_CHANNEL"
    result = await async_send_door_command_fc(runner.rest_connection, sample_functional_channel, DoorCommand.OPEN)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/sendDoorCommand"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["doorCommand"] == DoorCommand.OPEN.value
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_door_state(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "DOOR_LOCK_CHANNEL"
    result = await async_set_door_state_fc(runner.rest_connection, sample_functional_channel, LockState.OPEN, "1234")
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setLockState"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["authorizationPin"] == "1234"
    assert runner.rest_connection.async_post.call_args[0][1]["targetLockState"] == LockState.OPEN.value
    assert result.status == 200


@pytest.mark.asyncio
async def test_action_set_optical_signal(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "NOTIFICATION_LIGHT_CHANNEL"
    dim_level = 0.7
    optical_signal_behaviour = OpticalSignalBehaviour.FLASH_MIDDLE
    simple_rgb_color_state = RGBColorState.BLUE
    result = await async_set_optical_signal_fc(runner.rest_connection, sample_functional_channel, optical_signal_behaviour,
                                               simple_rgb_color_state, dim_level)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setOpticalSignal"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == sample_functional_channel.index
    assert runner.rest_connection.async_post.call_args[0][1]["opticalSignalBehaviour"] == optical_signal_behaviour.value
    assert runner.rest_connection.async_post.call_args[0][1]["simpleRGBColorState"] == simple_rgb_color_state.value
    assert runner.rest_connection.async_post.call_args[0][1]["dimLevel"] == dim_level
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_rgb_dim_level(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "NOTIFICATION_LIGHT_CHANNEL"
    result = await async_set_rgb_dim_level_fc(runner.rest_connection, sample_functional_channel, RGBColorState.BLUE, 0.5)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setSimpleRGBColorDimLevel"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["dimLevel"] == 0.5
    assert runner.rest_connection.async_post.call_args[0][1]["simpleRGBColorState"] == RGBColorState.BLUE.value
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_rgb_dim_level_with_time(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "NOTIFICATION_LIGHT_CHANNEL"
    result = await async_set_rgb_dim_level_with_time_fc(runner.rest_connection, sample_functional_channel, RGBColorState.BLUE, 0.5, 10.5,
                                                        20.5)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setSimpleRGBColorDimLevelWithTime"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["dimLevel"] == 0.5
    assert runner.rest_connection.async_post.call_args[0][1]["onTime"] == 10.5
    assert runner.rest_connection.async_post.call_args[0][1]["rampTime"] == 20.5
    assert runner.rest_connection.async_post.call_args[0][1]["simpleRGBColorState"] == RGBColorState.BLUE.value
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_primary_shading_level(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "SHADING_CHANNEL"
    result = await async_set_primary_shading_level_fc(runner.rest_connection, sample_functional_channel, 0.5)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setPrimaryShadingLevel"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["primaryShadingLevel"] == 0.5
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_secondary_shading_level(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "SHADING_CHANNEL"
    result = await async_set_secondary_shading_level_fc(runner.rest_connection, sample_functional_channel, 0.5, 0.8)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/setSecondaryShadingLevel"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["primaryShadingLevel"] == 0.5
    assert runner.rest_connection.async_post.call_args[0][1]["secondaryShadingLevel"] == 0.8
    assert result.status == 200


@pytest.mark.asyncio
async def test_reset_energy_counter(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "SWITCH_MEASURING_CHANNEL"
    result = await async_reset_energy_counter_fc(runner.rest_connection, sample_functional_channel)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/control/resetEnergyCounter"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_display(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL"
    result = await async_set_display_fc(runner.rest_connection, sample_functional_channel, ClimateControlDisplay.ACTUAL)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setClimateControlDisplay"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["display"] == ClimateControlDisplay.ACTUAL.value
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_acoustic_alarm_signal(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "WATER_SENSOR_CHANNEL"
    result = await async_set_acoustic_alarm_signal_fc(runner.rest_connection, sample_functional_channel,
                                                      AcousticAlarmSignal.DISABLE_ACOUSTIC_SIGNAL)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setAcousticAlarmSignal"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["acousticAlarmSignal"] == AcousticAlarmSignal.DISABLE_ACOUSTIC_SIGNAL.value
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_acoustic_alarm_timing(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "WATER_SENSOR_CHANNEL"
    result = await async_set_acoustic_alarm_timing_fc(runner.rest_connection, sample_functional_channel,
                                                      AcousticAlarmTiming.PERMANENT)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setAcousticAlarmTiming"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["acousticAlarmTiming"] == AcousticAlarmTiming.PERMANENT.value
    assert result.status == 200


@pytest.mark.asyncio
async def test_set_acoustic_water_alarm_trigger(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "WATER_SENSOR_CHANNEL"
    result = await async_set_acoustic_water_alarm_trigger_fc(runner.rest_connection, sample_functional_channel,
                                                             WaterAlarmTrigger.WATER_DETECTION)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setAcousticWaterAlarmTrigger"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["acousticWaterAlarmTrigger"] == WaterAlarmTrigger.WATER_DETECTION.value
    assert result.status == 200


@pytest.mark.asyncio
async def test_action_set_inapp_water_alarm_trigger(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "WATER_SENSOR_CHANNEL"
    result = await async_set_inapp_water_alarm_trigger_fc(runner.rest_connection, sample_functional_channel,
                                                        WaterAlarmTrigger.WATER_DETECTION)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setInAppWaterAlarmTrigger"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["inAppWaterAlarmTrigger"] == WaterAlarmTrigger.WATER_DETECTION.value
    assert result.status == 200


@pytest.mark.asyncio
async def test_action_set_siren_water_alarm_trigger(runner, sample_functional_channel):
    sample_functional_channel.functionalChannelType = "WATER_SENSOR_CHANNEL"
    result = await async_set_siren_water_alarm_trigger_fc(runner.rest_connection, sample_functional_channel,
                                                          WaterAlarmTrigger.WATER_DETECTION)
    assert runner.rest_connection.async_post.call_args[0][0] == "device/configuration/setSirenWaterAlarmTrigger"
    assert runner.rest_connection.async_post.call_args[0][1]["deviceId"] == "00000000-0000-0000-0000-000000000001"
    assert runner.rest_connection.async_post.call_args[0][1]["channelIndex"] == 1
    assert runner.rest_connection.async_post.call_args[0][1]["sirenWaterAlarmTrigger"] == WaterAlarmTrigger.WATER_DETECTION.value
    assert result.status == 200
