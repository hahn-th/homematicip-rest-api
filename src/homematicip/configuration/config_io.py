import json
import logging
import os
import platform
from configparser import ConfigParser
from dataclasses import asdict

from homematicip.configuration.config import PersistentConfig
from homematicip.configuration.log_helper import get_home_path


class ConfigIO:

    @classmethod
    def find_config_in_well_known_locations(cls) -> PersistentConfig | None:
        """Find the configuration file in the well known locations.
        @return the configuration if found, None otherwise."""
        for location in cls._get_well_known_locations():
            if os.path.exists(location):
                return cls.from_file(location)

        return None

    @classmethod
    def _get_well_known_locations(cls) -> list[str]:
        """Get the well known locations for the configuration file."""
        config_filename = "config.json"
        search_locations = [os.path.join("./", config_filename)]

        os_name = platform.system()

        if os_name == "Windows":
            appdata = os.getenv("localappdata")
            programdata = os.getenv("programdata")
            search_locations.append(
                os.path.join(appdata, "homematicip-rest-api", config_filename)
            )
            search_locations.append(
                os.path.join(programdata, "homematicip-rest-api", config_filename)
            )
        elif os_name == "Linux":
            search_locations.append(f"~/.homematicip-rest-api/{config_filename}")
            search_locations.append(f"/etc/homematicip-rest-api/{config_filename}")
        elif os_name == "Darwin":  # MAC
            # are these folders right?
            search_locations.append(f"~/Library/Preferences/homematicip-rest-api/{config_filename}")
            search_locations.append(
                f"/Library/Application Support/homematicip-rest-api/{config_filename}"
            )
        return search_locations

    @classmethod
    def from_file(cls, file_path) -> PersistentConfig:
        """Open a file and load the configuration from it."""
        with open(file_path,"r") as f:
            json_config = json.load(f)
            config = PersistentConfig(**json_config)

        # config_parser = ConfigParser()
        # config_parser.read(file_path)
        #
        # config = PersistentConfig()
        # config.auth_token = config_parser.get('AUTH', 'authtoken', fallback=None)
        # config.accesspoint_id = config_parser.get('AUTH', 'accesspoint', fallback=None)
        # config.level = int(config_parser.get('LOGGING', 'level', fallback=logging.INFO))
        # config.log_file = config_parser.get('LOGGING', 'log_file', fallback=None)

        return config

    @classmethod
    def to_file(cls, config: PersistentConfig) -> str:
        """Write the configuration to a file.
        @return the file path of the written file."""
        # config_parser = ConfigParser()
        # config_parser['AUTH'] = {
        #     'authtoken': config.auth_token,
        #     'accesspoint': config.accesspoint_id
        # }
        # config_parser['LOGGING'] = {
        #     'level': config.level,
        #     'log_file': config.log_file
        # }
        #
        filename = os.path.join(get_home_path(), "config.json")

        with open(filename, 'w') as file:
            json.dump(asdict(config), file)

        return filename
