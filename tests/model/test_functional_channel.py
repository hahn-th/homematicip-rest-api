import json

from homematicip.model.functional_channels import FunctionalChannel


def test_operation_lock_channel(filled_model):
    device = filled_model.devices["3014F711000BBBB000000000"]

    fc = device.functionalChannels["0"]
    assert isinstance(fc, FunctionalChannel)

    assert fc.functionalChannelType == "DEVICE_OPERATIONLOCK"
    assert fc.routerModuleEnabled == False
    assert fc.rssiDeviceValue == -45
    assert fc.rssiPeerValue == -54


def test_update_functional_channel(filled_model):
    device = filled_model.devices["3014F7110000RAIN_SENSOR"]
    old_channel_0 = device.functionalChannels["0"]

    changed_data = b'{"availableFirmwareVersion":"1.0.18","connectionType":"HMIP_RF","firmwareVersion":"1.0.18","firmwareVersionInteger":65554,"functionalChannels":{"0":{"busConfigMismatch":null,"coProFaulty":false,"coProRestartNeeded":false,"coProUpdateFailure":false,"configPending":false,"deviceId":"3014F7110000RAIN_SENSOR","deviceOverheated":false,"deviceOverloaded":false,"devicePowerFailureDetected":false,"deviceUndervoltage":false,"dutyCycle":false,"functionalChannelType":"DEVICE_BASE","groupIndex":0,"groups":["00000000-0000-0000-0000-000000000042"],"index":0,"label":"","lowBat":null,"multicastRoutingEnabled":false,"powerShortCircuit":null,"routerModuleEnabled":false,"routerModuleSupported":false,"rssiDeviceValue":-91,"rssiPeerValue":null,"shortCircuitDataLine":null,"supportedOptionalFeatures":{"IFeatureBusConfigMismatch":false,"IFeatureDeviceCoProError":false,"IFeatureDeviceCoProRestart":false,"IFeatureDeviceCoProUpdate":false,"IFeatureDeviceIdentify":false,"IFeatureDeviceOverheated":false,"IFeatureDeviceOverloaded":false,"IFeatureDevicePowerFailure":false,"IFeatureDeviceTemperatureOutOfRange":false,"IFeatureDeviceUndervoltage":false,"IFeatureMulticastRouter":false,"IFeaturePowerShortCircuit":false,"IFeatureRssiValue":true,"IFeatureShortCircuitDataLine":false,"IOptionalFeatureDutyCycle":true,"IOptionalFeatureLowBat":false},"temperatureOutOfRange":false,"unreach":false},"1":{"deviceId":"3014F7110000RAIN_SENSOR","functionalChannelType":"RAIN_DETECTION_CHANNEL","groupIndex":1,"groups":["00000000-0000-0000-0000-000000000043"],"index":1,"label":"","rainSensorSensitivity":90.0,"raining":true}},"homeId":"00000000-0000-0000-0000-000000000001","id":"3014F7110000RAIN_SENSOR","label":"Regensensor","lastStatusUpdate":1610893558747,"liveUpdateState":"LIVE_UPDATE_NOT_SUPPORTED","manufacturerCode":1,"modelId":412,"modelType":"HmIP-SRD","oem":"eQ-3","permanentlyReachable":true,"serializedGlobalTradeItemNumber":"3014F7110000RAIN_SENSOR","type":"RAIN_SENSOR","updateState":"UP_TO_DATE"}'
    rainSensorSensitivityOld = device.functionalChannels["1"].rainSensorSensitivity

    device.update_from_dict(json.loads(changed_data))

    assert device.functionalChannels["0"] == old_channel_0
    assert device.functionalChannels["1"].rainSensorSensitivity != rainSensorSensitivityOld