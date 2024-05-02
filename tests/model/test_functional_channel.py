from homematicip.model.functional_channels import FunctionalChannel


def test_operation_lock_channel(filled_model):
    device = filled_model.devices["3014F711000BBBB000000000"]

    fc = device.functionalChannels["0"]
    assert isinstance(fc, FunctionalChannel)

    assert fc.functionalChannelType == "DEVICE_OPERATIONLOCK"
    assert fc.routerModuleEnabled == False
    assert fc.rssiDeviceValue == -45
    assert fc.rssiPeerValue == -54
