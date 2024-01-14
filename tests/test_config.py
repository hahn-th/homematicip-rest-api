import io
import os
import platform

import homematicip


def fake_windows():
    return "Windows"


def fake_linux():
    return "Linux"


def fake_mac():
    return "Darwin"


def fake_getenv(var):
    if var == "appdata":
        return "C:\\APPDATA"
    if var == "programdata":
        return "C:\\PROGRAMDATA"


def test_find_and_load_config_file():
    with io.open("./config.ini", mode="w") as f:
        f.write("[AUTH]\nauthtoken = TEMP_TOKEN\naccesspoint = TEMP_AP")
    config = homematicip.find_and_load_config_file()
    assert config.auth_token == "TEMP_TOKEN"
    assert config.access_point == "TEMP_AP"
    os.remove("./config.ini")

    assert homematicip.find_and_load_config_file() is None


def test_get_config_file_locations_win():
    platform.system = fake_windows
    os.getenv = fake_getenv
    locations = homematicip.get_config_file_locations()
    assert locations[0] == "./config.ini"
    assert (
        locations[1].replace("/", "\\")
        == "C:\\APPDATA\\homematicip-rest-api\\config.ini"
    )
    assert (
        locations[2].replace("/", "\\")
        == "C:\\PROGRAMDATA\\homematicip-rest-api\\config.ini"
    )


def test_get_config_file_locations_linux():
    platform.system = fake_linux
    locations = homematicip.get_config_file_locations()
    assert locations[0] == "./config.ini"
    assert locations[1] == "~/.homematicip-rest-api/config.ini"
    assert locations[2] == "/etc/homematicip-rest-api/config.ini"


def test_get_config_file_locations_mac():
    platform.system = fake_mac
    locations = homematicip.get_config_file_locations()
    assert locations[0] == "./config.ini"
    assert locations[1] == "~/Library/Preferences/homematicip-rest-api/config.ini"
    assert (
        locations[2] == "/Library/Application Support/homematicip-rest-api/config.ini"
    )
