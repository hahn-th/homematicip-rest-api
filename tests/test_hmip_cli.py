import importlib
import json
import logging

from os.path import join, abspath, dirname


def load_source(modname, filename):
    loader = importlib.machinery.SourceFileLoader(modname, filename)
    spec = importlib.util.spec_from_file_location(modname, filename, loader=loader)
    module = importlib.util.module_from_spec(spec)
    # The module is always executed and not cached in sys.modules.
    # Uncomment the following line to cache the module.
    # sys.modules[module.__name__] = module
    loader.exec_module(module)
    return module


# Load module directly to test it
module_path = abspath(join(dirname(__file__), "../bin/hmip_cli.py"))
hmip_cli = load_source("hmip_cli", module_path)


from homematicip.base.enums import CliActions, DoorState
from homematicip.base.helpers import anonymizeConfig, handle_config
from homematicip.home import Home
from homematicip_demo.helper import (
    fake_home_download_configuration,
    no_ssl_verification,
)


def test_getRssiBarString():
    assert hmip_cli.getRssiBarString(-50) == "[**********]"
    assert hmip_cli.getRssiBarString(-55) == "[*********_]"
    assert hmip_cli.getRssiBarString(-60) == "[********__]"
    assert hmip_cli.getRssiBarString(-65) == "[*******___]"
    assert hmip_cli.getRssiBarString(-70) == "[******____]"
    assert hmip_cli.getRssiBarString(-75) == "[*****_____]"
    assert hmip_cli.getRssiBarString(-80) == "[****______]"
    assert hmip_cli.getRssiBarString(-85) == "[***_______]"
    assert hmip_cli.getRssiBarString(-90) == "[**________]"
    assert hmip_cli.getRssiBarString(-95) == "[*_________]"
    assert hmip_cli.getRssiBarString(-100) == "[__________]"


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

    assert hmip_cli._get_target_channel_indices(d, [1]) == [1]
    assert hmip_cli._get_target_channel_indices(d, None) == [1]
    assert hmip_cli._get_target_channel_indices(d, [1, 2, 3]) == [1, 2, 3]


def test_get_target_channels(fake_home: Home):
    d = fake_home.search_device_by_id("3014F71100000000000DRBL4")

    result = hmip_cli._get_target_channels(d, None)
    assert len(result) == 1
    assert result[0].index == 1

    result = hmip_cli._get_target_channels(d, [1, 3])
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
        hmip_cli._execute_action_for_device(
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
        hmip_cli._execute_action_for_device(
            d, args, CliActions.SET_SLATS_LEVEL, "set_slats_level", 0.5
        )
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F71100000000000DRBL4")
        assert d.functionalChannels[1].slatsLevel == 0.5
        assert d.functionalChannels[2].slatsLevel == 0.5
        assert d.functionalChannels[3].slatsLevel == 0.5


def test_execute_action_for_device_send_door_command(fake_home: Home):
    class Args:
        def __init__(self) -> None:
            self.channels = None

    args = Args()
    d = fake_home.search_device_by_id("3014F0000000000000FAF9B4")

    with no_ssl_verification():
        hmip_cli._execute_action_for_device(
            d, args, CliActions.SEND_DOOR_COMMAND, "send_door_command", "OPEN"
        )
        fake_home.get_current_state()
        d = fake_home.search_device_by_id("3014F0000000000000FAF9B4")
        assert d.functionalChannels[1].doorState == DoorState.OPEN


def test_channel_supports_action(fake_home: Home):
    d = fake_home.search_device_by_id("3014F71100000000000DRBL4")
    assert False == hmip_cli._channel_supports_action(
        d.functionalChannels[1], CliActions.SET_DIM_LEVEL
    )
    assert True == hmip_cli._channel_supports_action(
        d.functionalChannels[1], CliActions.SET_SHUTTER_LEVEL
    )
