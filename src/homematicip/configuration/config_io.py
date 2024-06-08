import json
import os
from dataclasses import asdict

from homematicip.configuration.config import PersistentConfig
from homematicip.configuration.config_folder import get_well_known_folders, get_default_app_config_folder


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
        """Return a list of well known locations where the configuration file can be found."""
        folders = get_well_known_folders()
        return [os.path.join(folder, "config.json") for folder in folders]

    @classmethod
    def from_file(cls, file_path) -> PersistentConfig:
        """Open a file and load the configuration from it."""
        with open(file_path, "r",  encoding='utf-8') as f:
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
        filename = os.path.join(get_default_app_config_folder(), "config.json")

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(asdict(config), file)

        return filename
