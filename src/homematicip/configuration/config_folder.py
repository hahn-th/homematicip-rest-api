import os
import platform
from typing import List


def get_well_known_folders() -> List[str]:
    """Return a list of folders, where the configuration file can be found."""
    app_name = "homematicip-rest-api"
    os_name = platform.system()

    if os_name == 'Linux':
        user_path = os.path.join(os.path.expanduser('~'), '.config', app_name)
        system_path = os.path.join('/etc', app_name)
    elif os_name == 'Darwin':  # macOS
        user_path = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', app_name)
        system_path = os.path.join('/Library', 'Application Support', app_name)
    elif os_name == 'Windows':
        user_path = os.path.join(os.getenv('APPDATA'), app_name)
        system_path = os.path.join(os.getenv('PROGRAMDATA'), app_name)
    else:
        raise ValueError(f"Unsupported operating system: {os_name}")

    return [user_path, system_path, os.getcwd()]


def get_default_app_config_folder() -> str:
    """Return the default application directory."""
    os_name = platform.system()

    if os_name == 'Linux':
        return os.path.join(os.path.expanduser('~'), '.config', 'homematicip-rest-api')
    elif os_name == 'Darwin':  # macOS
        return os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'homematicip-rest-api')
    elif os_name == 'Windows':
        return os.path.join(os.getenv('APPDATA'), 'homematicip-rest-api')
    else:
        raise ValueError(f"Unsupported operating system: {os_name}")
