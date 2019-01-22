# coding=utf-8
import platform
import configparser
import os
from collections import namedtuple

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

HmipConfig = namedtuple(
    "HmipConfig", ["auth_token", "access_point", "log_level", "log_file", "raw_config"]
)


def find_and_load_config_file() -> HmipConfig:
    for f in get_config_file_locations():
        try:
            return load_config_file(f)
        except FileNotFoundError:
            pass
    return None


def load_config_file(config_file: str) -> HmipConfig:
    """Loads the config ini file.
    :raises a FileNotFoundError when the config file does not exist."""
    _config = configparser.ConfigParser()
    with open(config_file, "r") as fl:
        _config.read_file(fl)
        logging_filename = _config.get("LOGGING", "FileName", fallback="hmip.log")
        if logging_filename == "None":
            logging_filename = None

        _hmip_config = HmipConfig(
            _config["AUTH"]["AuthToken"],
            _config["AUTH"]["AccessPoint"],
            int(_config.get("LOGGING", "Level", fallback=30)),
            logging_filename,
            _config._sections,
        )
        return _hmip_config


def get_config_file_locations() -> []:
    search_locations = ["./config.ini"]

    os_name = platform.system()

    if os_name == "Windows":
        appdata = os.getenv("appdata")
        programdata = os.getenv("programdata")
        search_locations.append(
            os.path.join(appdata, "homematicip-rest-api\\config.ini")
        )
        search_locations.append(
            os.path.join(programdata, "homematicip-rest-api\\config.ini")
        )
    elif os_name == "Linux":
        search_locations.append("~/.homematicip-rest-api/config.ini")
        search_locations.append("/etc/homematicip-rest-api/config.ini")
    elif os_name == "Darwin":  # MAC
        # are these folders right?
        search_locations.append("~/Library/Preferences/homematicip-rest-api/config.ini")
        search_locations.append(
            "/Library/Application Support/homematicip-rest-api/config.ini"
        )
    return search_locations
