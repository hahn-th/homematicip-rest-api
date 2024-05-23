import json

import pytest

from homematicip.model.model import build_model_from_json
from homematicip.events.event_manager import EventManager
from homematicip.events.hmip_event_handler import HmipEventHandler


def test_device_removed(sample_data_complete):
    assert True


@pytest.mark.asyncio
async def test_device_added(sample_data_complete):
    change_event_b = b'{"events":{"0":{"pushEventType":"DEVICE_ADDED","device":{"availableFirmwareVersion":"1.0.18","connectionType":"HMIP_RF","firmwareVersion":"1.0.18","firmwareVersionInteger":65554,"functionalChannels":{"0":{"busConfigMismatch":null,"coProFaulty":false,"coProRestartNeeded":false,"coProUpdateFailure":false,"configPending":false,"deviceId":"3014F71100000000000TEST","deviceOverheated":false,"deviceOverloaded":false,"devicePowerFailureDetected":false,"deviceUndervoltage":false,"dutyCycle":false,"functionalChannelType":"DEVICE_BASE","groupIndex":0,"groups":["00000000-0000-0000-0000-000000000042"],"index":0,"label":"","lowBat":null,"multicastRoutingEnabled":false,"powerShortCircuit":null,"routerModuleEnabled":false,"routerModuleSupported":false,"rssiDeviceValue":-91,"rssiPeerValue":null,"shortCircuitDataLine":null,"supportedOptionalFeatures":{"IFeatureBusConfigMismatch":false,"IFeatureDeviceCoProError":false,"IFeatureDeviceCoProRestart":false,"IFeatureDeviceCoProUpdate":false,"IFeatureDeviceIdentify":false,"IFeatureDeviceOverheated":false,"IFeatureDeviceOverloaded":false,"IFeatureDevicePowerFailure":false,"IFeatureDeviceTemperatureOutOfRange":false,"IFeatureDeviceUndervoltage":false,"IFeatureMulticastRouter":false,"IFeaturePowerShortCircuit":false,"IFeatureRssiValue":true,"IFeatureShortCircuitDataLine":false,"IOptionalFeatureDutyCycle":true,"IOptionalFeatureLowBat":false},"temperatureOutOfRange":false,"unreach":false},"1":{"deviceId":"3014F71100000000000TEST","functionalChannelType":"RAIN_DETECTION_CHANNEL","groupIndex":1,"groups":["00000000-0000-0000-0000-000000000043"],"index":1,"label":"","rainSensorSensitivity":90.0,"raining":true}},"homeId":"00000000-0000-0000-0000-000000000001","id":"3014F71100000000000TEST","label":"Regensensor","lastStatusUpdate":1610893558747,"liveUpdateState":"LIVE_UPDATE_NOT_SUPPORTED","manufacturerCode":1,"modelId":412,"modelType":"HmIP-SRD","oem":"eQ-3","permanentlyReachable":true,"serializedGlobalTradeItemNumber":"3014F71100000000000TEST","type":"RAIN_SENSOR","updateState":"UP_TO_DATE"}}}}'
    change_event = json.loads(change_event_b)

    event_manager = EventManager()
    model = build_model_from_json(sample_data_complete)
    new_device_id = "3014F71100000000000TEST"

    hmip_event_handler = HmipEventHandler(event_manager=event_manager, model=model)
    await hmip_event_handler.process_event_async(change_event)

    assert model.devices[new_device_id] is not None
    assert model.devices[new_device_id].functionalChannels["1"].rainSensorSensitivity == 90.0

@pytest.mark.asyncio
async def test_device_updated(sample_data_complete):
    event_manager = EventManager()
    model = build_model_from_json(sample_data_complete)
    device_id = "3014F7110000RAIN_SENSOR"
    lastStatusUpdateOld = model.devices[device_id].lastStatusUpdate
    rainSensorSensitivityOld = model.devices[device_id].functionalChannels["1"].rainSensorSensitivity
    change_event_b = b'{"events":{"0":{"pushEventType":"DEVICE_CHANGED","device":{"availableFirmwareVersion":"1.0.18","connectionType":"HMIP_RF","firmwareVersion":"1.0.18","firmwareVersionInteger":65554,"functionalChannels":{"0":{"busConfigMismatch":null,"coProFaulty":false,"coProRestartNeeded":false,"coProUpdateFailure":false,"configPending":false,"deviceId":"3014F7110000RAIN_SENSOR","deviceOverheated":false,"deviceOverloaded":false,"devicePowerFailureDetected":false,"deviceUndervoltage":false,"dutyCycle":false,"functionalChannelType":"DEVICE_BASE","groupIndex":0,"groups":["00000000-0000-0000-0000-000000000042"],"index":0,"label":"","lowBat":null,"multicastRoutingEnabled":false,"powerShortCircuit":null,"routerModuleEnabled":false,"routerModuleSupported":false,"rssiDeviceValue":-91,"rssiPeerValue":null,"shortCircuitDataLine":null,"supportedOptionalFeatures":{"IFeatureBusConfigMismatch":false,"IFeatureDeviceCoProError":false,"IFeatureDeviceCoProRestart":false,"IFeatureDeviceCoProUpdate":false,"IFeatureDeviceIdentify":false,"IFeatureDeviceOverheated":false,"IFeatureDeviceOverloaded":false,"IFeatureDevicePowerFailure":false,"IFeatureDeviceTemperatureOutOfRange":false,"IFeatureDeviceUndervoltage":false,"IFeatureMulticastRouter":false,"IFeaturePowerShortCircuit":false,"IFeatureRssiValue":true,"IFeatureShortCircuitDataLine":false,"IOptionalFeatureDutyCycle":true,"IOptionalFeatureLowBat":false},"temperatureOutOfRange":false,"unreach":false},"1":{"deviceId":"3014F7110000RAIN_SENSOR","functionalChannelType":"RAIN_DETECTION_CHANNEL","groupIndex":1,"groups":["00000000-0000-0000-0000-000000000043"],"index":1,"label":"","rainSensorSensitivity":90.0,"raining":true}},"homeId":"00000000-0000-0000-0000-000000000001","id":"3014F7110000RAIN_SENSOR","label":"Regensensor","lastStatusUpdate":1610893558747,"liveUpdateState":"LIVE_UPDATE_NOT_SUPPORTED","manufacturerCode":1,"modelId":412,"modelType":"HmIP-SRD","oem":"eQ-3","permanentlyReachable":true,"serializedGlobalTradeItemNumber":"3014F7110000RAIN_SENSOR","type":"RAIN_SENSOR","updateState":"UP_TO_DATE"}}}}'
    change_event = json.loads(change_event_b)

    hmip_event_handler = HmipEventHandler(event_manager=event_manager, model=model)
    await hmip_event_handler.process_event_async(change_event)

    assert model.devices[device_id].lastStatusUpdate != lastStatusUpdateOld
    assert model.devices[device_id].functionalChannels["1"].rainSensorSensitivity != rainSensorSensitivityOld


def test_client_removed(sample_data_complete):
    assert True


def test_client_added(sample_data_complete):
    assert True


def test_client_updated(sample_data_complete):
    assert True


def test_group_removed(sample_data_complete):
    assert True


def test_group_added(sample_data_complete):
    assert True


def test_group_updated(sample_data_complete):
    assert True
