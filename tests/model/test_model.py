import json
from homematicip.model import build_model_from_json
from homematicip.model.group import Group, GroupChannelReference
from homematicip.model.home import Home, FunctionalHome


def test_update_device(sample_data_complete):
    device_id = "3014F7110000RAIN_SENSOR"
    updated_json_binary = b'{"availableFirmwareVersion":"1.0.18","connectionType":"HMIP_RF","firmwareVersion":"1.0.18","firmwareVersionInteger":65554,"functionalChannels":{"0":{"busConfigMismatch":null,"coProFaulty":false,"coProRestartNeeded":false,"coProUpdateFailure":false,"configPending":false,"deviceId":"3014F7110000RAIN_SENSOR","deviceOverheated":false,"deviceOverloaded":false,"devicePowerFailureDetected":false,"deviceUndervoltage":false,"dutyCycle":false,"functionalChannelType":"DEVICE_BASE","groupIndex":0,"groups":["00000000-0000-0000-0000-000000000042"],"index":0,"label":"","lowBat":null,"multicastRoutingEnabled":false,"powerShortCircuit":null,"routerModuleEnabled":false,"routerModuleSupported":false,"rssiDeviceValue":-91,"rssiPeerValue":null,"shortCircuitDataLine":null,"supportedOptionalFeatures":{"IFeatureBusConfigMismatch":false,"IFeatureDeviceCoProError":false,"IFeatureDeviceCoProRestart":false,"IFeatureDeviceCoProUpdate":false,"IFeatureDeviceIdentify":false,"IFeatureDeviceOverheated":false,"IFeatureDeviceOverloaded":false,"IFeatureDevicePowerFailure":false,"IFeatureDeviceTemperatureOutOfRange":false,"IFeatureDeviceUndervoltage":false,"IFeatureMulticastRouter":false,"IFeaturePowerShortCircuit":false,"IFeatureRssiValue":true,"IFeatureShortCircuitDataLine":false,"IOptionalFeatureDutyCycle":true,"IOptionalFeatureLowBat":false},"temperatureOutOfRange":false,"unreach":false},"1":{"deviceId":"3014F7110000RAIN_SENSOR","functionalChannelType":"RAIN_DETECTION_CHANNEL","groupIndex":1,"groups":["00000000-0000-0000-0000-000000000043"],"index":1,"label":"","rainSensorSensitivity":10.0,"raining":false}},"homeId":"00000000-0000-0000-0000-000000000001","id":"3014F7110000RAIN_SENSOR","label":"Regensensor","lastStatusUpdate":1610893608847,"liveUpdateState":"LIVE_UPDATE_NOT_SUPPORTED","manufacturerCode":1,"modelId":412,"modelType":"HmIP-SRD","oem":"eQ-3","permanentlyReachable":true,"serializedGlobalTradeItemNumber":"3014F7110000RAIN_SENSOR","type":"RAIN_SENSOR","updateState":"UP_TO_DATE"}'
    updated_json = json.loads(updated_json_binary)
    base = build_model_from_json(sample_data_complete)
    device = base.devices[device_id]
    last_update_status_before = device.lastStatusUpdate

    new_device = device.model_copy(update={**updated_json})
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
