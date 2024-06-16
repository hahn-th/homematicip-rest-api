import json
import os
from dataclasses import asdict

from homematicip.configuration.config import PersistentConfig
from homematicip.configuration.config_folder import get_well_known_folders, get_default_app_config_folder
from homematicip.configuration.output_format_config import OutputFormatConfig


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
    def get_output_format_config(cls) -> OutputFormatConfig | None:
        """Find the configuration file in the well known locations.
        @return the configuration if found, None otherwise."""
        config_file_path = os.path.join(get_default_app_config_folder(), "output-format.json")
        if not os.path.exists(config_file_path):
            config_file_path = os.path.join(os.getcwd(), "data/output-format.json")

        if not os.path.exists(config_file_path):
            return None

        return cls.output_format_from_file(config_file_path)

    @classmethod
    def _get_well_known_locations(cls) -> list[str]:
        """Return a list of well known locations where the configuration file can be found."""
        folders = get_well_known_folders()
        return [os.path.join(folder, "config.json") for folder in folders]

    @classmethod
    def from_file(cls, file_path) -> PersistentConfig:
        """Open a file and load the configuration from it."""
        with open(file_path, "r", encoding='utf-8') as f:
            json_config = json.load(f)
            config = PersistentConfig(**json_config)

        return config

    @classmethod
    def output_format_from_file(cls, file_path) -> OutputFormatConfig:
        """Open a file and load the output format configuration from it."""
        with open(file_path, "r", encoding='utf-8') as f:
            json_config = json.load(f)
            config = OutputFormatConfig(**json_config)

        return config

    @classmethod
    def to_file(cls, config: PersistentConfig) -> str:
        """Write the configuration to a file.
        @return the file path of the written file."""
        filename = os.path.join(get_default_app_config_folder(), "config.json")

        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(asdict(config), file)

        return filename
