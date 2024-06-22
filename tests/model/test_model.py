import copy
import json
from unittest.mock import Mock

from homematicip.model.model import build_model_from_json, update_model_from_json
from homematicip.model.model_components import GroupChannelReference, Group, Device
from homematicip.model.hmip_base import HmipBaseModel
from homematicip.model.home import Home, FunctionalHome


def test_update_device(sample_data_complete):
    device_id = "3014F7110000RAIN_SENSOR"
    updated_json_binary = b'{"availableFirmwareVersion":"1.0.18","connectionType":"HMIP_RF","firmwareVersion":"1.0.18","firmwareVersionInteger":65554,"functionalChannels":{"0":{"busConfigMismatch":null,"coProFaulty":false,"coProRestartNeeded":false,"coProUpdateFailure":false,"configPending":false,"deviceId":"3014F7110000RAIN_SENSOR","deviceOverheated":false,"deviceOverloaded":false,"devicePowerFailureDetected":false,"deviceUndervoltage":false,"dutyCycle":false,"functionalChannelType":"DEVICE_BASE","groupIndex":0,"groups":["00000000-0000-0000-0000-000000000042"],"index":0,"label":"","lowBat":null,"multicastRoutingEnabled":false,"powerShortCircuit":null,"routerModuleEnabled":false,"routerModuleSupported":false,"rssiDeviceValue":-91,"rssiPeerValue":null,"shortCircuitDataLine":null,"supportedOptionalFeatures":{"IFeatureBusConfigMismatch":false,"IFeatureDeviceCoProError":false,"IFeatureDeviceCoProRestart":false,"IFeatureDeviceCoProUpdate":false,"IFeatureDeviceIdentify":false,"IFeatureDeviceOverheated":false,"IFeatureDeviceOverloaded":false,"IFeatureDevicePowerFailure":false,"IFeatureDeviceTemperatureOutOfRange":false,"IFeatureDeviceUndervoltage":false,"IFeatureMulticastRouter":false,"IFeaturePowerShortCircuit":false,"IFeatureRssiValue":true,"IFeatureShortCircuitDataLine":false,"IOptionalFeatureDutyCycle":true,"IOptionalFeatureLowBat":false},"temperatureOutOfRange":false,"unreach":false},"1":{"deviceId":"3014F7110000RAIN_SENSOR","functionalChannelType":"RAIN_DETECTION_CHANNEL","groupIndex":1,"groups":["00000000-0000-0000-0000-000000000043"],"index":1,"label":"","rainSensorSensitivity":10.0,"raining":false}},"homeId":"00000000-0000-0000-0000-000000000001","id":"3014F7110000RAIN_SENSOR","label":"Regensensor","lastStatusUpdate":1610893608847,"liveUpdateState":"LIVE_UPDATE_NOT_SUPPORTED","manufacturerCode":1,"modelId":412,"modelType":"HmIP-SRD","oem":"eQ-3","permanentlyReachable":true,"serializedGlobalTradeItemNumber":"3014F7110000RAIN_SENSOR","type":"RAIN_SENSOR","updateState":"UP_TO_DATE"}'
    updated_json = json.loads(updated_json_binary)
    base = build_model_from_json(sample_data_complete)
    device = base.devices[device_id]
    last_update_status_before = device.lastStatusUpdate

    new_device = Device(**updated_json)
    base.devices[device_id] = new_device

    assert device.id == new_device.id
    assert last_update_status_before != new_device.lastStatusUpdate
    assert base.devices[device_id].lastStatusUpdate == new_device.lastStatusUpdate


def test_group_initialisation(filled_model):
    group = filled_model.groups['00000000-0000-0000-0000-0000000000EN']

    assert isinstance(group, Group)
    assert group.id == "00000000-0000-0000-0000-0000000000EN"
    assert group.type == "ENERGY"
    assert group.label == "EnergyGroupHWR"

    assert len(group.channels) == 1

    ch_ref = group.channels[0]
    assert isinstance(ch_ref, GroupChannelReference)
    assert ch_ref.deviceId == "3014F7110000000000000019"
    assert ch_ref.channelIndex == 1


def test_home(filled_model):
    home = filled_model.home

    assert isinstance(home, Home)
    assert home.id == "00000000-0000-0000-0000-000000000001"
    assert home.lastReadyForUpdateTimestamp == 1522319489138
    assert home.currentAPVersion == "1.2.4"


def test_home_functional_homes(filled_model):
    home = filled_model.home

    indoor_climate = home.functionalHomes['INDOOR_CLIMATE']
    light_and_shadow = home.functionalHomes['LIGHT_AND_SHADOW']

    assert isinstance(indoor_climate, FunctionalHome)
    assert indoor_climate.active == True
    assert indoor_climate.coolingEnabled == False
    assert indoor_climate.solution == "INDOOR_CLIMATE"

    assert isinstance(light_and_shadow, FunctionalHome)
    assert light_and_shadow.active == True
    assert len(light_and_shadow.extendedLinkedShutterGroups) == 0
    assert light_and_shadow.solution == "LIGHT_AND_SHADOW"


def test_on_update_event():
    """Test, if the on_update event is triggered correctly."""
    subscriber = Mock()
    model = HmipBaseModel()
    model.subscribe_on_update(subscriber)

    model.fire_on_update()

    subscriber.assert_called_once_with(model)


def test_on_removed_event():
    """Test, if the on_remove event is triggered correctly."""
    subscriber = Mock()
    model = HmipBaseModel()
    model.subscribe_on_remove(subscriber)

    model.fire_on_remove()

    subscriber.assert_called_once_with(model)


def test_unsubscribe_on_update_event():
    """Test, if the unsubscribe_on_update method works correctly."""
    subscriber = Mock()
    model = HmipBaseModel()
    model.subscribe_on_update(subscriber)
    model.unsubscribe_on_update(subscriber)
    model.fire_on_update()

    subscriber.assert_not_called()


def test_unsubscribe_on_remove_event():
    """Test, if the unsubscribe_on_remove method works correctly."""
    subscriber = Mock()
    model = HmipBaseModel()
    model.subscribe_on_remove(subscriber)
    model.unsubscribe_on_remove(subscriber)
    model.fire_on_remove()

    subscriber.assert_not_called()


def test_hmip_base_model_subscribers_after_update(sample_data_complete):
    device_id = "3014F7110000RAIN_SENSOR"
    updated_json_binary = b'{"availableFirmwareVersion":"1.0.18","connectionType":"HMIP_RF","firmwareVersion":"1.0.18","firmwareVersionInteger":65554,"functionalChannels":{"0":{"busConfigMismatch":null,"coProFaulty":false,"coProRestartNeeded":false,"coProUpdateFailure":false,"configPending":false,"deviceId":"3014F7110000RAIN_SENSOR","deviceOverheated":false,"deviceOverloaded":false,"devicePowerFailureDetected":false,"deviceUndervoltage":false,"dutyCycle":false,"functionalChannelType":"DEVICE_BASE","groupIndex":0,"groups":["00000000-0000-0000-0000-000000000042"],"index":0,"label":"","lowBat":null,"multicastRoutingEnabled":false,"powerShortCircuit":null,"routerModuleEnabled":false,"routerModuleSupported":false,"rssiDeviceValue":-91,"rssiPeerValue":null,"shortCircuitDataLine":null,"supportedOptionalFeatures":{"IFeatureBusConfigMismatch":false,"IFeatureDeviceCoProError":false,"IFeatureDeviceCoProRestart":false,"IFeatureDeviceCoProUpdate":false,"IFeatureDeviceIdentify":false,"IFeatureDeviceOverheated":false,"IFeatureDeviceOverloaded":false,"IFeatureDevicePowerFailure":false,"IFeatureDeviceTemperatureOutOfRange":false,"IFeatureDeviceUndervoltage":false,"IFeatureMulticastRouter":false,"IFeaturePowerShortCircuit":false,"IFeatureRssiValue":true,"IFeatureShortCircuitDataLine":false,"IOptionalFeatureDutyCycle":true,"IOptionalFeatureLowBat":false},"temperatureOutOfRange":false,"unreach":false},"1":{"deviceId":"3014F7110000RAIN_SENSOR","functionalChannelType":"RAIN_DETECTION_CHANNEL","groupIndex":1,"groups":["00000000-0000-0000-0000-000000000043"],"index":1,"label":"","rainSensorSensitivity":10.0,"raining":false}},"homeId":"00000000-0000-0000-0000-000000000001","id":"3014F7110000RAIN_SENSOR","label":"Regensensor","lastStatusUpdate":1610893608847,"liveUpdateState":"LIVE_UPDATE_NOT_SUPPORTED","manufacturerCode":1,"modelId":412,"modelType":"HmIP-SRD","oem":"eQ-3","permanentlyReachable":true,"serializedGlobalTradeItemNumber":"3014F7110000RAIN_SENSOR","type":"RAIN_SENSOR","updateState":"UP_TO_DATE"}'
    updated_json = json.loads(updated_json_binary)
    base = build_model_from_json(sample_data_complete)
    device = base.devices[device_id]
    last_update_status_before = device.lastStatusUpdate
    subscriber = Mock()

    device.subscribe_on_update(subscriber)

    device.update_from_dict({**updated_json})

    assert device.id == device_id
    assert last_update_status_before != device.lastStatusUpdate
    assert len(device._on_update_handler) == 1
    subscriber.assert_called_once_with(device)
    assert base.devices[device_id].lastStatusUpdate == device.lastStatusUpdate


def test_update_home_from_json(sample_data_complete):
    """Test, if the home is updated correctly."""
    # arrange
    manipulated = copy.deepcopy(sample_data_complete)
    manipulated["home"]["functionalHomes"]["INDOOR_CLIMATE"]["active"] = "false"
    manipulated["home"]["connected"] = "false"

    model_current = build_model_from_json(sample_data_complete)
    model_expected = build_model_from_json(manipulated)
    event_manager = Mock()

    old_state_climate = model_current.home.functionalHomes['INDOOR_CLIMATE'].active
    new_state_climate = model_expected.home.functionalHomes['INDOOR_CLIMATE'].active
    old_state_connected = model_current.home.connected
    new_state_connected = model_expected.home.connected

    # act
    update_model_from_json(model_current, event_manager, manipulated)

    # assert
    assert len(event_manager.mock_calls) == 1
    assert old_state_climate != new_state_climate
    assert old_state_connected != new_state_connected


def test_update_model_from_json_changed_devices(sample_data_complete):
    """Test, if the home is updated correctly."""
    # arrange
    manipulated = copy.deepcopy(sample_data_complete)
    manipulated["devices"]["3014F7110000RAIN_SENSOR"]["functionalChannels"]["0"]["dutyCycle"] = "true"
    manipulated["devices"]["3014F7110DIN_RAIL_SWITCH"]["functionalChannels"]["1"]["on"] = "true"

    model_current = build_model_from_json(sample_data_complete)
    model_expected = build_model_from_json(manipulated)
    event_manager = Mock()

    old_state_duty = model_current.devices['3014F7110000RAIN_SENSOR'].functionalChannels["0"].dutyCycle
    new_state_duty = model_expected.devices['3014F7110000RAIN_SENSOR'].functionalChannels["0"].dutyCycle
    old_state_on = model_current.devices['3014F7110DIN_RAIL_SWITCH'].functionalChannels["1"].on
    new_state_on = model_expected.devices['3014F7110DIN_RAIL_SWITCH'].functionalChannels["1"].on

    # act
    update_model_from_json(model_current, event_manager, manipulated)

    # assert
    assert len(event_manager.mock_calls) == 2
    assert old_state_duty != new_state_duty
    assert old_state_on != new_state_on


def test_update_model_from_json_with_new_device(sample_data_complete):
    """Test, if the home is updated correctly."""
    # arrange
    manipulated = copy.deepcopy(sample_data_complete)
    manipulated["devices"]["3014F7110000RAIN_SENSO2"] = copy.deepcopy(
        sample_data_complete["devices"]["3014F7110000RAIN_SENSOR"])

    model_current = build_model_from_json(sample_data_complete)
    event_manager = Mock()
    contains_device_before = "3014F7110000RAIN_SENSO2" in model_current.devices

    # act
    update_model_from_json(model_current, event_manager, manipulated)

    # assert
    assert contains_device_before is False
    assert "3014F7110000RAIN_SENSO2" in model_current.devices
    assert len(event_manager.mock_calls) == 1


def test_update_model_from_json_updated_group(sample_data_complete):
    """Test, if the home is updated correctly."""
    # arrange
    manipulated = copy.deepcopy(sample_data_complete)
    manipulated["groups"]["00000000-0000-0000-0000-0000000000EN"]["label"] = "EnergyGroupHWR2"

    model_current = build_model_from_json(sample_data_complete)
    model_expected = build_model_from_json(manipulated)
    event_manager = Mock()

    old_label = model_current.groups['00000000-0000-0000-0000-0000000000EN'].label
    new_label = model_expected.groups['00000000-0000-0000-0000-0000000000EN'].label

    # act
    update_model_from_json(model_current, event_manager, manipulated)

    # assert
    assert len(event_manager.mock_calls) == 1
    assert old_label != new_label
    assert model_current.groups['00000000-0000-0000-0000-0000000000EN'].label == new_label


def test_update_model_from_json_with_new_group(sample_data_complete):
    """Test, if the home is updated correctly."""
    # arrange
    manipulated = copy.deepcopy(sample_data_complete)
    manipulated["groups"]["00000000-0000-0000-0000-0000000000EN2"] = copy.deepcopy(
        sample_data_complete["groups"]["00000000-0000-0000-0000-0000000000EN"])

    model_current = build_model_from_json(sample_data_complete)
    event_manager = Mock()
    contains_group_before = "00000000-0000-0000-0000-0000000000EN2" in model_current.groups

    # act
    update_model_from_json(model_current, event_manager, manipulated)

    # assert
    assert contains_group_before is False
    assert "00000000-0000-0000-0000-0000000000EN2" in model_current.groups
    assert len(event_manager.mock_calls) == 1


def test_update_model_from_json_with_new_client(sample_data_complete):
    """Test, if the home is updated correctly."""
    # arrange
    manipulated = copy.deepcopy(sample_data_complete)
    manipulated["clients"]["00000000-0000-0000-0000-000000000NEW"] = copy.deepcopy(
        sample_data_complete["clients"]["00000000-0000-0000-0000-000000000000"])

    model_current = build_model_from_json(sample_data_complete)
    event_manager = Mock()
    contains_client_before = "00000000-0000-0000-0000-000000000NEW" in model_current.clients

    # act
    update_model_from_json(model_current, event_manager, manipulated)

    # assert
    assert contains_client_before is False
    assert "00000000-0000-0000-0000-000000000NEW" in model_current.clients
    assert len(event_manager.mock_calls) == 1


def test_update_model_from_json_updated_client(sample_data_complete):
    """Test, if the home is updated correctly."""
    # arrange
    manipulated = copy.deepcopy(sample_data_complete)
    manipulated["clients"]["00000000-0000-0000-0000-000000000000"]["label"] = "ChangedLabel"

    model_current = build_model_from_json(sample_data_complete)
    model_expected = build_model_from_json(manipulated)
    event_manager = Mock()

    old_label = model_current.clients['00000000-0000-0000-0000-000000000000'].label
    new_label = model_expected.clients['00000000-0000-0000-0000-000000000000'].label

    # act
    update_model_from_json(model_current, event_manager, manipulated)

    # assert
    assert len(event_manager.mock_calls) == 1
    assert old_label != new_label
    assert model_current.clients['00000000-0000-0000-0000-000000000000'].label == new_label
