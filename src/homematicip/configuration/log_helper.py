import datetime
import os
import platform


def get_logger_filename() -> str:
    """Returns the filename of the logger."""
    path = get_target_log_path()
    ensure_log_path_exists(path)

    return os.path.join(path,
                        f"homematicip-rest-api.log")


def ensure_log_path_exists(path: str):
    """Ensures that the log path exists. If not the path will be created."""
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def get_target_log_path() -> str:
    """Depending on the operating system a path is returned where the log file should be stored.
    :return: the path to the log directory."""
    return os.path.join(get_home_path(), "logs")


def get_home_path() -> str:
    """Depending on the operating system a path is returned where the log file should be stored.
    :return: the path to the log directory.
    """
    os_name = platform.system()
    if os_name == "Windows":
        return os.path.join(os.getenv("LOCALAPPDATA"), "homematicip-rest-api")
    elif os_name == "Linux":
        return os.path.expanduser("~/.homematicip-rest-api")
    elif os_name == "Darwin":
        return "/Library/Application Support/homematicip-rest-api"
