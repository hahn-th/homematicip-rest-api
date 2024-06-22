import copy

import pytest



def manipulated_sample_data_device(sample_data_complete):
    """Manipulate the sample data for the device.
    The dutyCycle attribute of the RAIN_SENSOR device is set to true."""
    manipulated = copy.deepcopy(sample_data_complete)
    manipulated["devices"]["3014F7110000RAIN_SENSOR"]["functionalChannels"]["0"]["dutyCycle"] = "true"
    manipulated["devices"]["3014F7110000RAIN_SENSOR"]["functionalChannels"]["1"]["raining"] = "false"
    return manipulated
