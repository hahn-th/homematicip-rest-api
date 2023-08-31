import json
import logging

from hmip_cli import (
    _channel_supports_action,
    getRssiBarString,
    _get_target_channel_indices,
    _get_target_channels,
    _execute_action_for_device,
    _execute_cli_action,
)
from homematicip.base.enums import CliActions
from homematicip.base.helpers import anonymizeConfig, handle_config
from homematicip.home import Home
from homematicip_demo.helper import (
    fake_home_download_configuration,
    no_ssl_verification,
)


def test_getRssiBarString():
    assert getRssiBarString(-50) == "[**********]"
    assert getRssiBarString(-55) == "[*********_]"
    assert getRssiBarString(-60) == "[********__]"
    assert getRssiBarString(-65) == "[*******___]"
    assert getRssiBarString(-70) == "[******____]"
    assert getRssiBarString(-75) == "[*****_____]"
    assert getRssiBarString(-80) == "[****______]"
    assert getRssiBarString(-85) == "[***_______]"
    assert getRssiBarString(-90) == "[**________]"
    assert getRssiBarString(-95) == "[*_________]"
    assert getRssiBarString(-100) == "[__________]"


def test_handle_config_error():
    assert handle_config({"errorCode": "Dummy"}, False) is None


def test_anonymizeConfig():
    c = (
        '{"id":"d0fea2b1-ef3b-44b1-ae96-f9b31f75de84",'
        '"id2":"d0fea2b1-ef3b-44b1-ae96-f9b31f75de84",'
        '"inboxGroup":"2dc54a8d-ceee-4626-8f27-b24e78dc05de",'
        '"availableFirmwareVersion": "0.0.0",'
        '"sgtin":"3014F71112345AB891234561", "sgtin_silvercrest" : "301503771234567891234567",'
        '"location":'
        '{"city": "Vatican City, Vatican","latitude":"41.9026011","longitude":"12.4533701"}}'
    )
    c = handle_config(json.loads(c), True)

    js = json.loads(c)

    assert js["id"] == "00000000-0000-0000-0000-000000000000"
    assert js["id"] == js["id2"]
    assert js["inboxGroup"] == "00000000-0000-0000-0000-000000000001"
    assert js["sgtin"] == "3014F7110000000000000000"
    assert js["sgtin_silvercrest"] == "3014F7110000000000000001"
    assert js["availableFirmwareVersion"] == "0.0.0"

    l = js["location"]
    assert l["city"] == "1010, Vienna, Austria"
    assert l["latitude"] == "48.208088"
    assert l["longitude"] == "16.358608"

    c = '{"id":"test"}'
    c = anonymizeConfig(c, "original", "REPLACED")
    assert c == '{"id":"test"}'


def test_get_target_channel_indices(fake_home: Home):
    d = fake_home.search_device_by_id("3014F71100000000000DRBL4")

    assert _get_target_channel_indices(d, [1]) == [1]
    assert _get_target_channel_indices(d, None) == [1]
    assert _get_target_channel_indices(d, [1, 2, 3]) == [1, 2, 3]


def test_get_target_channels(fake_home: Home):
    d = fake_home.search_device_by_id("3014F71100000000000DRBL4")

    result = _get_target_channels(d, None)
    assert len(result) == 1
    assert result[0].index == 1

    result = _get_target_channels(d, [1, 3])
    assert len(result) == 2
    assert result[0].index == 1
    assert result[1].index == 3


def test_execute_action_for_device_shutter_level(fake_home: Home):
    class Args:
        def __init__(self) -> None:
            self.channels: list = [1, 2, 3]

    args = Args()
    d = fake_home.search_device_by_id("3014F71100000000000DRBL4")

    with no_ssl_verification():
        _execute_action_for_device(
            d, args, CliActions.SET_SHUTTER_LEVEL, "set_shutter_level", 0.5
        )
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F71100000000000DRBL4")
        assert d.functionalChannels[1].shutterLevel == 0.5
        assert d.functionalChannels[2].shutterLevel == 0.5
        assert d.functionalChannels[3].shutterLevel == 0.5


def test_execute_action_for_device_slats_level(fake_home: Home):
    class Args:
        def __init__(self) -> None:
            self.channels: list = [1, 2, 3]

    args = Args()
    d = fake_home.search_device_by_id("3014F71100000000000DRBL4")

    with no_ssl_verification():
        _execute_action_for_device(
            d, args, CliActions.SET_SLATS_LEVEL, "set_slats_level", 0.5
        )
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F71100000000000DRBL4")
        assert d.functionalChannels[1].slatsLevel == 0.5
        assert d.functionalChannels[2].slatsLevel == 0.5
        assert d.functionalChannels[3].slatsLevel == 0.5


def test_channel_supports_action(fake_home: Home):
    d = fake_home.search_device_by_id("3014F71100000000000DRBL4")
    assert False == _channel_supports_action(
        d.functionalChannels[1], CliActions.SET_DIM_LEVEL
    )
    assert True == _channel_supports_action(
        d.functionalChannels[1], CliActions.SET_SHUTTER_LEVEL
    )
