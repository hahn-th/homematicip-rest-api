import logging
import os
from logging.handlers import TimedRotatingFileHandler

import click
from click import ClickException

from homematicip.configuration.config import Config
from homematicip.configuration.config_io import ConfigIO
from homematicip.configuration.log_helper import get_logger_filename
from homematicip.model.model import Model
from homematicip.model.model_components import FunctionalChannel, Device, Group
from homematicip.runner import Runner


async def get_initialized_runner(including_model: bool = True) -> Runner:
    config = get_config()
    logger = setup_logger(
        config.level, config.log_file
    )

    r = Runner(config=config)

    if including_model:
        await r.async_initialize_runner()
    else:
        await r.async_initialize_runner_without_init_model()

    return r


def get_config() -> Config:
    """Get Config object from the configuration file. If no configuration file is found, raise an exception."""
    persistent_config = ConfigIO.find_config_in_well_known_locations()

    if persistent_config is None:
        raise ClickException(
            "No configuration file found. Run hmip auth to get an auth token.")

    return Config.from_persistent_config(persistent_config)


def setup_basic_logging(log_level: int, logger_filename: str = None) -> None:
    """Setup basic logging configuration."""
    if not logger_filename or logger_filename.strip() == '':
        logger_filename = get_logger_filename()

    should_roll_over = os.path.isfile(logger_filename)

    handler = logging.handlers.RotatingFileHandler(logger_filename, mode='w', backupCount=20, delay=True)
    if should_roll_over:
        handler.doRollover()

    logging.basicConfig(level=log_level, handlers=[handler],
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    logging.getLogger("httpx").setLevel(logging.CRITICAL)
    logging.getLogger("httpcore").setLevel(logging.CRITICAL)
    logging.getLogger("websockets.client").setLevel(logging.CRITICAL)


def setup_logger(
        log_level: int, log_file: str
) -> logging.Logger:
    """Initialize logger. If log_file is set, log to file, otherwise to stdout. The log level """
    setup_basic_logging(log_level, log_file)

    logger = _create_logger(log_level, log_file)
    return logger


def _create_logger(level: int, file_name: str) -> logging.Logger:
    """Create a logger based on the level"""
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = (
        TimedRotatingFileHandler(file_name, when="midnight", backupCount=5)
        if file_name
        else logging.StreamHandler()
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)
    return logger


def get_rssi_bar_string(rssi_value):
    """Create a bar string for the rssi value."""
    # Observed values: -93..-47
    width = 10
    dots = 0
    if rssi_value:
        dots = int(round((100 + rssi_value) / 5))
        dots = max(0, min(width, dots))

    return "[{}{}]".format("*" * dots, "_" * (width - dots))


def get_channel_by_index_of_first(device: Device, index: int = None) -> FunctionalChannel | None:
    """Get the first channel of a device or the channel with the given index."""
    if index is not None:
        if str(index) not in device.functionalChannels:
            raise click.BadParameter(f"Channel {index} not found for device {device.label or device.id} (.")

        return device.functionalChannels[str(index)]

    click.echo("No channel index given. Use first channel.")
    return device.functionalChannels["1"]


def is_group(id: str, model: Model) -> bool:
    """Check if the given id is a group id."""
    return id in model.groups


def is_device(id: str, model: Model) -> bool:
    """Check if the given id is a device id."""
    return id in model.devices


def get_device_or_group(id: str, model: Model) -> Device | Group | FunctionalChannel | None:
    """Get a device or group by id."""
    if is_device(id, model):
        return model.devices[id]

    if is_group(id, model):
        return model.groups[id]

    return None


def get_device_name(device: Device) -> str:
    """Get the name of a device."""
    return device.label or device.id


def get_channel_name(channel: FunctionalChannel) -> str:
    """Get the name of a channel."""
    return channel.label or channel.index


def get_group_name(group: Group) -> str:
    """Get the name of a group."""
    return group.label or group.id
