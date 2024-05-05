import asyncio
import datetime
import json
import logging
import os
import sys
import time
from logging.handlers import TimedRotatingFileHandler
from importlib.metadata import version as metadata_version
import click
import httpx
from alive_progress import alive_bar
from click import ClickException

from homematicip.action.functional_channel_actions import action_set_slats_level, action_set_shutter_level, \
    action_set_switch_state, action_set_dim_level, action_start_impulse
from homematicip.action.group_actions import action_set_boost, action_set_point_temperature, action_set_boost_duration, \
    action_set_active_profile, action_set_control_mode, action_set_shutter_level_group, action_set_slats_level_group
from homematicip.auth import Auth
from homematicip.cli.helper import get_channel_by_index_of_first
from homematicip.cli.helper import get_rssi_bar_string
from homematicip.configuration.config import Config, PersistentConfig
from homematicip.configuration.config_io import ConfigIO
from homematicip.configuration.log_helper import get_logger_filename
from homematicip.connection.rest_connection import ConnectionContext, RestResult
from homematicip.events.event_types import ModelUpdateEvent
from homematicip.model.anoymizer import handle_config
from homematicip.model.enums import ClimateControlMode
from homematicip.runner import Runner


async def get_initialized_runner(including_model: bool = True) -> Runner:
    config = get_config()
    logger = setup_logger(
        config.level, config.log_file
    )

    r = Runner(_config=config)

    if including_model:
        await r.async_initialize_runner()
    else:
        await r.async_initialize_runner_without_init_model()

    return r


def get_config() -> Config:
    """Get Config object from the configuration file. If no configuration file is found, raise an exception."""
    config = ConfigIO.find_config_in_well_known_locations()

    if config is None:
        raise ClickException(
            "No configuration file found. Run hmip auth to get an auth token.")

    return Config.from_persistent_config(config)


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


@click.group
def cli():
    """HomematicIP-Rest-API CLI."""
    pass


@cli.command()
def auth():
    """Generate an auth token."""
    setup_basic_logging(logging.DEBUG)
    logger = logging.getLogger("cli.auth")

    click.echo("Generating an auth token to access the HomematicIP Cloud.", color=True)
    access_point_id = click.prompt("Please enter the access point id", type=str, default="").strip().replace("-",
                                                                                                             "").upper()
    logger.debug(f"Entered access-point-id: {access_point_id}")
    if len(access_point_id) != 24:
        click.echo("The access point id is invalid.", err=True, color=True)
        return

    device_name = click.prompt("Please enter the client/devicename (leave blank to use default)", type=str)
    pin = click.prompt("Please enter the PIN (leave Blank if there is none)", type=str)

    logger.debug(f"Create context and initialize auth")
    context = ConnectionContext.create(access_point_id, "https://lookup.homematic.com:48335/getHost")
    auth = Auth(context)

    while True:
        click.echo("Requesting connection to the HomematicIP Cloud...", color=False)
        result: RestResult = asyncio.run(auth.connection_request(access_point_id, device_name, pin))
        logger.debug(f"Connection request result: {result.status_text} ({result.status})")
        if result.status == 200:
            break

        if httpx.codes.is_error(result.status):
            raise click.ClickException(
                f"Error while requesting connection to the HomematicIP Cloud. Exiting application. Error: {result.exception if result.exception else f"{result.status_text} ({result.status})"}")

        error_code = result.json["errorCode"]
        if error_code == "INVALID_PIN":
            click.echo("PIN IS INVALID!", color=True, err=True)
        else:
            click.echo("Unknown error happened. Exiting application", color=True, err=True)
            return

    click.echo("Please press the blue button on the access point...")
    with alive_bar(0, monitor=False, stats=False) as bar:

        last_request = datetime.datetime.now()
        while True:
            time.sleep(0.1)

            if (datetime.datetime.now() - last_request).seconds > 2:
                logger.debug("Check if request is acknowledged.")
                ack = asyncio.run(auth.is_request_acknowledged())
                if ack:
                    logger.debug("Ack!")
                    break
                last_request = datetime.datetime.now()

            bar()

    logger.debug("Getting auth token and client-id")
    auth_token = asyncio.run(auth.request_auth_token())
    asyncio.run(auth.confirm_auth_token(auth_token))

    logger.debug("Got auth-token and client-id. Persist config.")

    config = PersistentConfig(accesspoint_id=access_point_id, auth_token=auth_token)
    config_path = ConfigIO.to_file(config)

    click.echo("")
    click.echo("==================================================================")
    click.echo("")
    click.echo(f"Client successfully registered at access point {access_point_id}!")
    click.echo(f"Configuration has been written to file {config_path}")
    click.echo("")
    click.echo('You can use the api now with the command \'hmip\'. To get started, type \'hmip --help\'. Have fun!')


@cli.group
def list():
    """List information about devices, groups, rssi, firmware, profiles."""
    pass


@list.command()
def devices():
    """List all devices including the functional channels."""
    runner = asyncio.run(get_initialized_runner())
    model = runner.model
    print("Devices:")
    for device in sorted(model.devices.values(), key=lambda x: x.label):
        click.echo(f"\t({device.id}) - {device.label} - {device.type}")

        for channel in device.functionalChannels.values():
            click.echo(f"\t\t[{channel.index}] - {channel.functionalChannelType:30} - {channel.label or "<no label>"}")


@list.command()
def groups():
    """List all groups."""
    runner = asyncio.run(get_initialized_runner())
    model = runner.model
    print("Groups:")
    for group in sorted(model.groups.values(), key=lambda x: x.label):
        click.echo(f"\t({group.id}) - {group.label} - {group.type}")


@list.command()
def rssi():
    """List RSSI information."""
    runner = asyncio.run(get_initialized_runner())
    model = runner.model
    print("RSSI:")
    print(
        f"{'HmIP AccessPoint':45s} - Duty cycle: {model.home.dutyCycle:2}"
    )

    for d in sorted(model.devices.values(), key=lambda x: x.label):
        fc = d.functionalChannels["0"]
        rssi_device_value = 0
        rssi_peer_value = 0
        unreach = False

        if hasattr(fc, "rssiDeviceValue"):
            rssi_device_value = fc.rssiDeviceValue
        if hasattr(fc, "rssiPeerValue"):
            rssi_peer_value = fc.rssiPeerValue
        if hasattr(fc, "unreach"):
            unreach = fc.unreach
        click.echo(
            "{:45s} - RSSI: {:4} {} - Peer RSSI: {:4} - {} {} permanentlyReachable: {}".format(
                d.label,
                rssi_device_value or "?",
                get_rssi_bar_string(rssi_device_value),
                rssi_peer_value or "?",
                get_rssi_bar_string(rssi_peer_value),
                "Unreachable" if unreach else "",
                d.permanentlyReachable,
            )
        )


@list.command
def firmware():
    """List firmware information."""
    runner = asyncio.run(get_initialized_runner())
    model = runner.model
    home = model.home
    click.echo(
        f"HmIP AccessPoint - Firmware: {home.currentAPVersion:7s} - Available Firmware: {home.availableAPVersion:7s} UpdateState: {home.updateState}"
    )
    sortedDevices = sorted(model.devices.values(), key=lambda x: x.label)
    for d in sortedDevices:
        click.echo(
            f"{d.label:45s} - Firmware: {d.firmwareVersion:7} - Available Firmware: {d.availableFirmwareVersion:7} UpdateState: {d.updateState} LiveUpdateState: {d.liveUpdateState}")


@list.command
@click.argument("group-id", type=str, nargs=1)
def profiles(group_id):
    """List profiles for a group."""
    runner = asyncio.run(get_initialized_runner())
    model = runner.model

    if group_id not in model.groups:
        click.echo(f"Group with id {group_id} not found.", err=True, color=True)
        return

    group = model.groups[group_id]
    click.echo(f"Profiles for Group {group.label} (Type {group.type} - Id {group.id}):")
    if not hasattr(group, "profiles"):
        click.echo(f"Group has no profiles.", err=True, color=True)
        return

    for pid, profile in group.profiles.items():
        click.echo(
            f"\t({profile['index']}) - {profile['name'] or "None"} - Visible: {profile['visible']} Enabled: {profile['enabled']}")


@list.command
def last_status_update():
    """List the last status update for devices and groups."""
    runner = asyncio.run(get_initialized_runner())
    model = runner.model
    click.echo("Devices:")
    for device in sorted(model.devices.values(), key=lambda x: x.label):
        click.echo(f"\t{device.id}\t{device.label:30s}\t{device.lastStatusUpdate}")

    click.echo("Groups:")
    for group in sorted(model.groups.values(), key=lambda x: x.label):
        click.echo(f"\t{group.id}\t{group.label:30s}\t{group.lastStatusUpdate}")

    return True


@list.command
def firmware():
    """List current and available firmware information."""
    runner = asyncio.run(get_initialized_runner())
    model = runner.model
    home = model.home
    click.echo(
        f"{"HmIP AccessPoint":30s} - Firmware: {home.currentAPVersion or "<unknown>":7} - Available Firmware: {home.availableAPVersion or "<unknown>":7} UpdateState: {home.updateState}")

    for device in sorted(model.devices.values(), key=lambda x: x.label):
        click.echo(
            f"{device.label:30s} - Firmware: {device.firmwareVersion or "<unknown>":7} - Available Firmware: {device.availableFirmwareVersion or "<unknown>":7} UpdateState: {device.updateState} LiveUpdateState: {device.liveUpdateState}")


@cli.group
def run():
    """Run actions on devices, groups, home or functional channels."""
    pass


async def _model_update_event_handler(event: ModelUpdateEvent, args) -> None:
    click.echo(f"ModelUpdateEvent: {event}; {args}")


# @cli.command
# def listen():
#     """Listen to events. If filename is specified, events are written to the file. If not, they are written to
#     console."""
#     runner = asyncio.run(get_initialized_runner())
#     runner.event_manager.subscribe(ModelUpdateEvent.ITEM_CREATED, _model_update_event_handler)
#     runner.event_manager.subscribe(ModelUpdateEvent.ITEM_UPDATED, _model_update_event_handler)
#     runner.event_manager.subscribe(ModelUpdateEvent.ITEM_REMOVED, _model_update_event_handler)
#
#     loop = asyncio.new_event_loop()
#     task = loop.create_task(runner.async_listening_for_updates())
#
#     try:
#         click.echo("Waiting for events... press CTRL+C to stop listening.")
#         loop.run_until_complete(task)
#     except asyncio.CancelledError:
#         pass
#     except KeyboardInterrupt:
#         task.cancel()
#         loop.stop()
#         click.echo("Stopping listener...")


@cli.command
def version():
    """Print the version of the homematicip-rest-api."""
    click.echo(f"HomematicIP-Rest-Api: {metadata_version("homematicip")}")
    click.echo(f"Python: {sys.version}")


@run.command()
@click.option("--id", type=str, required=True, help="ID of the device or group, which the run command is applied to.")
@click.option("-c", "--channel", type=int, required=False, default=None,
              help="Index of the Channel. Only necessary, if you have more than one channel on the device. Not "
                   "needed, if you want to control a group.")
def turn_on(id: str, channel: int = None):
    """Turn a device on. Specify a FunctionalChannel-Index."""
    runner = asyncio.run(get_initialized_runner())

    if id not in runner.model.devices:
        click.echo(f"Device with id {id} not found.", err=True, color=True)
        return

    device = runner.model.devices[id]
    fc = get_channel_by_index_of_first(device, channel)

    result = asyncio.run(action_set_switch_state(runner, fc, True))

    click.echo(
        f"Run turn_on for device {device.label or device.id} with result: {result.status_text} ({result.status})")


@run.command()
@click.option("--id", type=str, required=True, help="ID of the device or group, which the run command is applied to.")
@click.option("-c", "--channel", type=int, required=False, default=None,
              help="Index of the Channel. Only necessary, if you have more than one channel on the device. Not "
                   "needed, if you want to control a group.")
def turn_off(id: str, channel: int = None):
    """Turn a device off. Specify a FunctionalChannel-Index.

    ID is the ID of the device.\n
    CHANNEL_INDEX is the index of the channel. If the device has only one channel (excl. BaseChannel 0) this can be omitted."""
    runner = asyncio.run(get_initialized_runner())

    if id not in runner.model.devices:
        click.echo(f"Device with id {id} not found.", err=True, color=True)
        return

    device = runner.model.devices[id]
    fc = get_channel_by_index_of_first(device, channel)

    result = asyncio.run(action_set_switch_state(runner, fc, False))

    click.echo(
        f"Run turn_off for device {device.label or device.id} with result: {result.status_text} ({result.status})")


@run.command()
@click.option("--id", type=str, required=True, help="ID of the device or group, which the run command is applied to.")
@click.option("-c", "--channel", type=int, required=False, default=None,
              help="Index of the Channel. Only necessary, if you have more than one channel on the device. Not "
                   "needed, if you want to control a group.")
@click.option("--state", type=bool, required=True, help="The target state. True or False")
def set_switch_state(id: str, channel: int, state: bool):
    """Set the switch state for a device. specify FunctionalChannel-Index."""
    runner = asyncio.run(get_initialized_runner())

    if id not in runner.model.devices:
        click.echo(f"Device with id {id} not found.", err=True, color=True)
        return

    device = runner.model.devices[id]
    if str(channel) not in device.functionalChannels:
        click.echo(f"Channel with index {channel} not found.", err=True, color=True)
        return

    result = asyncio.run(
        action_set_switch_state(runner, device.functionalChannels[str(channel)], state))

    click.echo(
        f"Run set_switch_state for device {device.label or device.id} with result: {result.status_text} ({result.status})")


@run.command()
@click.argument("filename", type=click.File('w'))
@click.option("--anonymized", is_flag=False, flag_value=True, help="Anonymize the output.", default=True)
def dump(filename, anonymized):
    """Dump configuration to a file. By default, the dump is anonymized. Use flag --anonymized=False to disable
    anonymization.

    FILENAME target filename in which config dump is written."""
    runner = asyncio.run(get_initialized_runner(including_model=False))
    state = asyncio.run(runner.async_get_current_state())
    state_as_string = json.dumps(state, indent=4)
    if anonymized:
        state_as_string = handle_config(state_as_string, anonymized)

    filename.write(state_as_string)
    filename.close()

    click.echo(f"Successfully dumped config to file {filename.name}")
    return


@run.command
@click.option("--id", type=str, required=True, help="ID of the device or group, which the run command is applied to.")
def set_boost(id: str):
    """Set Boost on Group."""
    runner = asyncio.run(get_initialized_runner())

    if id not in runner.model.groups:
        click.echo(f"Group with id {id} not found.", err=True, color=True)
        return

    result = asyncio.run(action_set_boost(runner, runner.model.groups[id], True))
    click.echo(f"Run set_boost with result: {result.status_text}")


@run.command
@click.option("--id", type=str, required=True, help="ID of the device or group, which the run command is applied to.")
def set_boost_stop(id: str):
    """Stop Boost on Group."""
    runner = asyncio.run(get_initialized_runner())

    if id not in runner.model.groups:
        click.echo(f"Group with id {id} not found.", err=True, color=True)
        return

    result = asyncio.run(action_set_boost(runner, runner.model.groups[id], False))
    click.echo(
        f"Run set_boost for group {runner.model.groups[id].label or runner.model.groups[id].id} with "
        f"result: {result.status_text} ({result.status})")


@run.command
@click.option("--id", type=str, required=True, help="ID of the device or group, which the run command is applied to.")
@click.option("-t", "--temperature", type=float, help="Target Temperature", required=True)
def set_point_temperature(id: str, temperature: float):
    """Set point temperature for a group."""
    runner = asyncio.run(get_initialized_runner())

    if id not in runner.model.groups:
        click.echo(f"Group with id {id} not found.", err=True, color=True)
        return

    result = asyncio.run(action_set_point_temperature(runner, runner.model.groups[id], temperature))
    if result.exception is not None:
        click.echo(f"Error while running set_point_temperature: {result.exception}", err=True, color=True)
        return

    click.echo(
        f"Run set_point_temperature for group {runner.model.groups[id].label or runner.model.groups[id].id} with "
        f"result: {result.status_text} ({result.status})")


@run.command
@click.option("--id", type=str, required=True, help="ID of the device or group, which the run command is applied to.")
@click.option("-m", "--minutes", type=int, nargs=1, help="Duration of boost in Minutes", required=True)
def set_boost_duration(id: str, minutes: int):
    """Sets the boost duration for a group in minutes"""
    runner = asyncio.run(get_initialized_runner())

    if id not in runner.model.groups:
        click.echo(f"Group with id {id} not found.", err=True, color=True)
        return

    result = asyncio.run(action_set_boost_duration(runner, runner.model.groups[id], minutes))
    click.echo(
        f"Run set_boost_duration for group {runner.model.groups[id].label or runner.model.groups[id].id} with "
        f"result: {result.status_text} ({result.status})")


@run.command
@click.option("--id", type=str, required=True, help="ID of the device or group, which the run command is applied to.")
@click.option("-p", "--profile_index", type=str, required=True,
              help="index of the profile. Usually this is PROFILE_x. Use 'hmip list profiles <group-id>' to get a "
                   "list of available profiles for a group.")
def set_active_profile(id: str, profile_index: str):
    """Set the active profile for a group."""
    runner = asyncio.run(get_initialized_runner())

    if id not in runner.model.groups:
        click.echo(f"Group with id {id} not found.", err=True, color=True)
        return

    result = asyncio.run(action_set_active_profile(runner, runner.model.groups[id], profile_index))
    click.echo(
        f"Run set_active_profile for group {runner.model.groups[id].label or runner.model.groups[id].id} with "
        f"result: {result.status_text} ({result.status})")


@run.command
@click.option("--id", type=str, required=True, help="ID of the device or group, which the run command is applied to.")
@click.option("--mode", type=ClimateControlMode, help="the control mode. [ECO|AUTOMATIC|MANUAL]")
def set_control_mode(id: str, mode: ClimateControlMode):
    """Set the control mode for a group."""
    runner = asyncio.run(get_initialized_runner())

    if id not in runner.model.groups:
        click.echo(f"Group with id {id} not found.", err=True, color=True)
        return

    result = asyncio.run(action_set_control_mode(runner, runner.model.groups[id], mode))
    click.echo(
        f"Run set_control_mode for group {runner.model.groups[id].label or runner.model.groups[id].id} with "
        f"result: {result.status_text} ({result.status})")


@run.command
@click.option("--id", type=str, required=True, help="ID of the device or group, which the run command is applied to.")
@click.option("-d", "--dim_level", type=click.FloatRange(0.0, 1.0), help="Target Dim Level", required=True)
@click.option("-c", "--channel", type=int, required=False, default=None,
              help="Index of the Channel. Only necessary, if you have more than one channel on the device. Not "
                   "needed, if you want to control a group.")
def set_dim_level(id: str, dim_level: float, channel: int = None):
    """Set the dim level for a device.

    ID is the Id of the device. Use 'list devices' to get desired Id.\n
    DIM_LEVEL is the target dim level. Must be between 0.0 and 1.0.\n
    CHANNEL is the channel index of the device. If the device has only one channel (excl. BaseChannel 0) this can be omitted.
    """
    runner = asyncio.run(get_initialized_runner())
    model = runner.model

    if id not in model.devices:
        click.echo(f"Device with id {id} not found.", err=True, color=True)
        return

    device = model.devices[id]
    fc = get_channel_by_index_of_first(device, channel)

    if fc is None:
        click.echo(f"Channel with index {channel} not found.", err=True, color=True)
        return
    result = asyncio.run(action_set_dim_level(runner, fc, dim_level))
    click.echo(
        f"Run set_dim_level for device {device.label or device.id} and channel {fc.index} with result: {result.status_text} ({result.status})")


@run.command
@click.option("--id", type=str, required=True, help="ID of the device or group, which the run command is applied to.")
@click.option("-c", "--channel", type=int, required=False, default=None,
              help="Index of the Channel. Only necessary, if you have more than one channel on the device. Not "
                   "needed, if you want to control a group.")
@click.option("-s", "--shutter_level", type=click.FloatRange(0.0, 1.0), required=True, help="Target shutter level.")
def set_shutter_level(id: str, shutter_level: float, channel: int):
    runner = asyncio.run(get_initialized_runner())

    if id in runner.model.devices:
        device = runner.model.devices[id]
        fc = get_channel_by_index_of_first(device, channel)
        result = asyncio.run(action_set_shutter_level(runner, fc, shutter_level))
        click.echo(
            f"Run set_shutter_level for device {device.label or device.id} with result: {result.status_text} ({result.status})")
        return

    if id in runner.model.groups:
        group = runner.model.groups[id]
        result = asyncio.run(action_set_shutter_level_group(runner, group, shutter_level))
        click.echo(
            f"Run set_shutter_level for group {group.label or group.id} with result: {result.status_text} ({result.status})")
        return

    click.echo(f"Id is neither a device nor a group.", err=True, color=True)


@run.command
@click.option("--id", type=str, required=True, help="ID of the device or group, which the run command is applied to.")
@click.option("-c", "--channel", type=int, required=False, default=None,
              help="Index of the Channel. Only necessary, if you have more than one channel on the device. Not "
                   "needed, if you want to control a group.")
@click.option("-sl", "--slats-level", type=click.FloatRange(0.0, 1.0), nargs=1, required=True, help="Slats Level.")
@click.option("-sh", "--shutter-level", type=click.FloatRange(0.0, 1.0), nargs=1, required=False, default=None,
              help="Shutter Level.")
def set_slats_level(id: str, slats_level: float, shutter_level: float = None, channel: int = None):
    runner = asyncio.run(get_initialized_runner())

    if id in runner.model.devices:
        device = runner.model.devices[id]
        fc = get_channel_by_index_of_first(device, channel)
        result = asyncio.run(action_set_slats_level(runner, fc, slats_level, shutter_level))
        click.echo(
            f"Run set_slats_level for device {device.label or device.id} with result: {result.status_text} ({result.status})")
        return

    if id in runner.model.groups:
        group = runner.model.groups[id]
        result = asyncio.run(action_set_slats_level_group(runner, group, slats_level, shutter_level))
        click.echo(
            f"Run set_slats_level for group {group.label or group.id} with result: {result.status_text} ({result.status})")
        return

    click.echo(f"Specified Id '{id}' is neither a device nor a group.", err=True, color=True)


@run.command
@click.option("--id", type=str, required=True, help="ID of the device or group, which the run command is applied to.")
@click.option("-c", "--channel", type=int, required=False, default=None,
              help="Index of the Channel. Only necessary, if you have more than one channel on the device. Not "
                   "needed, if you want to control a group.")
def toggle_garage_door(id: str, channel: int = None):
    """Toggle the garage door.

    ID is the Id of the device. Use 'list devices' to get desired Id."""
    runner = asyncio.run(get_initialized_runner())
    model = runner.model

    if id not in model.devices:
        click.echo(f"Device with id {id} not found.", err=True, color=True)
        return

    device = model.devices[id]
    fc = get_channel_by_index_of_first(device, channel)
    result = asyncio.run(action_start_impulse(runner, fc))
    click.echo(
        f"Run toggle_garage_door for device {device.label or device.id} with result: {result.status_text} ({result.status})")

#     #         if args.toggle_garage_door is not None:
#     #             _execute_action_for_device(
#     #                 device,
#     #                 args,
#     #                 CliActions.TOGGLE_GARAGE_DOOR,
#     #                 "send_start_impulse",
#     #             )
#     #             command_entered = True
#     #
#     #         if args.device_send_door_command is not None:
#     #             _execute_action_for_device(
#     #                 device,
#     #                 args,
#     #                 CliActions.SEND_DOOR_COMMAND,
#     #                 "send_door_command",
#     #                 args.device_send_door_command,
#     #             )
#     #             command_entered = True

#     # if args.protectionmode:
#     #     command_entered = True
#     #     if args.protectionmode == "presence":
#     #         home.set_security_zones_activation(False, True)
#     #     elif args.protectionmode == "absence":
#     #         home.set_security_zones_activation(True, True)
#     #     elif args.protectionmode == "disable":
#     #         home.set_security_zones_activation(False, False)
#     #
#     # if args.new_pin:
#     #     command_entered = True
#     #     home.set_pin(args.new_pin, args.old_pin)
#     # if args.delete_pin:
#     #     command_entered = True
#     #     home.set_pin(None, args.old_pin)
#     #
#     # if args.list_security_journal:
#     #     command_entered = True
#     #     journal = home.get_security_journal()
#     #     for entry in journal:
#     #         print(entry)
#     #
#     #

#
#     # if args.list_rules:
#     #     command_entered = True
#     #     sortedRules = sorted(home.rules, key=attrgetter("ruleType", "label"))
#     #     for d in sortedRules:
#     #         print("{} {}".format(d.id, str(d)))
#     #
#     # if args.device:
#     #     command_entered = False
#     #     devices = []
#     #     for argdevice in args.device:
#     #         if argdevice == "*":
#     #             devices = home.devices
#     #             break
#     #         else:
#     #             d = home.search_device_by_id(argdevice)
#     #             if d is None:
#     #                 logger.error("Could not find device %s", argdevice)
#     #             else:
#     #                 devices.append(d)
#     #
#     #     for device in devices:
#     #         if args.device_new_label:
#     #             device.set_label(args.device_new_label)
#     #             command_entered = True
#     #
#     #         if args.device_switch_state is not None:
#     #             _execute_action_for_device(
#     #                 device,
#     #                 args,
#     #                 CliActions.SET_SWITCH_STATE,
#     #                 "set_switch_state",
#     #                 args.device_switch_state,
#     #             )
#     #             command_entered = True
#     #
#     #         if args.device_set_lock_state is not None:
#     #             targetLockState = LockState.from_str(args.device_set_lock_state)
#     #             if targetLockState not in LockState:
#     #                 logger.error("%s is not a lock state.", args.device_set_lock_state)
#     #
#     #             else:
#     #                 pin = args.pin[0] if len(args.pin) > 0 else ""
#     #                 _execute_action_for_device(
#     #                     device,
#     #                     args,
#     #                     CliActions.SET_LOCK_STATE,
#     #                     "set_lock_state",
#     #                     targetLockState,
#     #                     pin,
#     #                 )
#     #             command_entered = True
#     #
#     #
#     #
#     #
#     #         if args.device_slats_level is not None:
#     #             slats_level = args.device_slats_level[0]
#     #             shutter_level = (
#     #                 args.device_slats_level[1]
#     #                 if len(args.device_slats_level) > 1
#     #                 else None
#     #             )
#     #             _execute_action_for_device(
#     #                 device,
#     #                 args,
#     #                 CliActions.SET_SLATS_LEVEL,
#     #                 "set_slats_level",
#     #                 slats_level,
#     #                 shutter_level,
#     #             )
#     #             command_entered = True
#     #
#     #         if args.device_shutter_stop is not None:
#     #             _execute_action_for_device(
#     #                 device,
#     #                 args,
#     #                 CliActions.SET_SHUTTER_STOP,
#     #                 "set_shutter_stop",
#     #             )
#     #             command_entered = True
#     #
#     #         if args.device_display is not None:
#     #             if isinstance(device, TemperatureHumiditySensorDisplay):
#     #                 device.set_display(
#     #                     ClimateControlDisplay(args.device_display.upper())
#     #                 )
#     #             else:
#     #                 logger.error(
#     #                     "can't set display of device %s of type %s",
#     #                     device.id,
#     #                     device.deviceType,
#     #                 )
#     #             command_entered = True
#     #
#     #         if args.device_enable_router_module is not None:
#     #             if device.routerModuleSupported:
#     #                 device.set_router_module_enabled(args.device_enable_router_module)
#     #                 print(
#     #                     "{} the router module for device {}".format(
#     #                         "Enabled"
#     #                         if args.device_enable_router_module
#     #                         else "Disabled",
#     #                         device.id,
#     #                     )
#     #                 )
#     #             else:
#     #                 logger.error(
#     #                     "the device %s doesn't support the router module", device.id
#     #                 )
#     #             command_entered = True
#     #
#     #         if args.reset_energy_counter:
#     #             _execute_action_for_device(
#     #                 device,
#     #                 args,
#     #                 CliActions.RESET_ENERGY_COUNTER,
#     #                 "reset_energy_counter",
#     #             )
#     #             command_entered = True
#     #
#     #         if args.print_infos:
#     #             command_entered = True
#     #             print(d)
#     #             print("------")
#     #             for fc in d.functionalChannels:
#     #                 print(f"   Ch {fc.index}: {str(fc)}")
#     #                 if (
#     #                         args.print_allowed_commands
#     #                         and fc.functionalChannelType in FUNCTIONALCHANNEL_CLI_MAP
#     #                 ):
#     #                     print(
#     #                         f"   -> Allowed commands: {FUNCTIONALCHANNEL_CLI_MAP[fc.functionalChannelType]}"
#     #                     )
#     #
#     #         if args.print_allowed_commands and d is not None:
#     #             command_entered = True
#     #             print(f"Allowed commands for selected channels device {d.id}")
#     #             target_channels = []
#     #             if args.channels:
#     #                 target_channels = _get_target_channels(d, args.channels)
#     #             else:
#     #                 target_channels = d.functionalChannels
#     #
#     #             for fc in target_channels:
#     #                 print(
#     #                     f"   -> Ch {fc.index}, Type {fc.functionalChannelType} Allowed commands: ",
#     #                     end=" ",
#     #                 )
#     #                 if fc.functionalChannelType in FUNCTIONALCHANNEL_CLI_MAP:
#     #                     print(
#     #                         f"{[str(val) for val in FUNCTIONALCHANNEL_CLI_MAP[fc.functionalChannelType]]}"
#     #                     )
#     #                 else:
#     #                     print("None")
#     #
#     # if args.set_zones_device_assignment:
#     #     internal = []
#     #     external = []
#     #     error = False
#     #     command_entered = True
#     #     for id in args.external_devices:
#     #         d = home.search_device_by_id(id)
#     #         if d is None:
#     #             logger.error("Device %s is not registered on this Access Point", id)
#     #             error = True
#     #         else:
#     #             external.append(d)
#     #
#     #     for id in args.internal_devices:
#     #         d = home.search_device_by_id(id)
#     #         if d is None:
#     #             logger.error("Device %s is not registered on this Access Point", id)
#     #             error = True
#     #         else:
#     #             internal.append(d)
#     #     if not error:
#     #         home.set_zones_device_assignment(internal, external)
#     #
#     # if args.activate_absence:
#     #     command_entered = True
#     #     home.activate_absence_with_duration(args.activate_absence)
#     #
#     # if args.activate_absence_permanent:
#     #     command_entered = True
#     #     home.activate_absence_permanent()
#     #
#     # if args.deactivate_absence:
#     #     command_entered = True
#     #     home.deactivate_absence()
#     #
#     # if args.inclusion_device_id:
#     #     command_entered = True
#     #     home.start_inclusion(args.inclusion_device_id)
#     #
#     # if args.group:
#     #     command_entered = False
#     #     group = None
#     #     for g in home.groups:
#     #         if g.id == args.group:
#     #             group = g
#     #             break
#     #     if group is None:
#     #         logger.error("Could not find group %s", args.group)
#     #         return
#     #
#     #     if args.device_switch_state is not None:
#     #         if isinstance(group, ExtendedLinkedSwitchingGroup):
#     #             group.set_switch_state(args.device_switch_state)
#     #
#     #         command_entered = True
#     #
#     #     if args.group_list_profiles:
#     #         command_entered = True
#     #         for p in group.profiles:
#     #             isActive = p.id == group.activeProfile.id
#     #             print(
#     #                 f"Index: {p.index} - Id: {p.id} - Name: {p.name} - Active: {isActive} (Enabled: {p.enabled}, Visible: {p.visible})"
#     #             )
#     #
#     #     if args.group_shutter_level:
#     #         command_entered = True
#     #         group.set_shutter_level(args.group_shutter_level)
#     #
#     #     if args.group_shutter_stop:
#     #         command_entered = True
#     #         group.set_shutter_stop()
#     #

#     #
#     #     if args.group_set_point_temperature:
#     #         command_entered = True
#     #         if isinstance(group, HeatingGroup):
#     #             group.set_point_temperature(args.group_set_point_temperature)
#     #         else:
#     #             logger.error("Group %s isn't a HEATING group", g.id)
#     #
#     #     if args.group_activate_profile:
#     #         command_entered = True
#     #         if isinstance(group, HeatingGroup):
#     #             index = args.group_activate_profile
#     #             for p in group.profiles:
#     #                 if p.name == args.group_activate_profile:
#     #                     index = p.index
#     #                     break
#     #             group.set_active_profile(index)
#     #         else:
#     #             logger.error("Group %s isn't a HEATING group", g.id)
#     #
#     #     if args.group_boost is not None:
#     #         command_entered = True
#     #         if isinstance(group, HeatingGroup):
#     #             group.set_boost(args.group_boost)
#     #         else:
#     #             logger.error("Group %s isn't a HEATING group", g.id)
#     #
#     #     if args.group_boost_duration is not None:
#     #         command_entered = True
#     #         if isinstance(group, HeatingGroup):
#     #             group.set_boost_duration(args.group_boost_duration)
#     #         else:
#     #             logger.error("Group %s isn't a HEATING group", g.id)
#     #
#     #     if args.print_infos:
#     #         command_entered = True
#     #         print(group)
#     #         print("------")
#     #         if group.metaGroup:
#     #             print("   Metagroup: {}".format(str(group.metaGroup)))
#     #             print("------")
#     #         for fc in group.devices:
#     #             print("   Assigned device: {}".format(str(fc)))
#     #
#     # if args.rules:
#     #     command_entered = False
#     #     rules = []
#     #     for argrule in args.rules:
#     #         if argrule == "*":
#     #             rules = home.rules
#     #             break
#     #         else:
#     #             r = home.search_rule_by_id(argrule)
#     #             if r is None:
#     #                 logger.error("Could not find automation rule %s", argrule)
#     #             else:
#     #                 rules.append(r)
#     #
#     #     for rule in rules:
#     #         if args.rule_activation is not None:
#     #             if isinstance(rule, SimpleRule):
#     #                 rule.set_rule_enabled_state(args.rule_activation)
#     #                 command_entered = True
#     #             else:
#     #                 logger.error(
#     #                     "can't enable/disable rule %s of type %s",
#     #                     rule.id,
#     #                     rule.ruleType,
#     #                 )
#     #
#     # if args.list_events:
#     #     command_entered = True
#     #     home.onEvent += printEvents
#     #     home.enable_events()
#     #     try:
#     #         while True:
#     #             time.sleep(1)
#     #     except KeyboardInterrupt:
#     #         return
#
#     return command_entered
#
#
#
# #
# # def _get_target_channel_indices(device: BaseDevice, channels: list = None) -> list:
# #     """Get list with adressed channel indices. Is the channels list None, than the channel 1 is used."""
# #     target_channels_indices = []
# #     if channels:
# #         target_channels_indices = [*channels]
# #     else:
# #         target_channels_indices.append(1)
# #     return target_channels_indices
# #
# #
# # def _get_target_channels(device: Device, channels: list = None):
# #     target_channels_indices = _get_target_channel_indices(device, channels)
# #
# #     target_channels = [
# #         device.functionalChannels[int(channel_index)]
# #         for channel_index in target_channels_indices
# #     ]
# #     return target_channels
# #
# #
# # def _execute_action_for_device(
# #     device, cli_args, action: CliActions, function_name: str, *args
# # ) -> None:
# #     target_channels = _get_target_channels(device, cli_args.channels)
# #     for fc in target_channels:
# #         _execute_cli_action(
# #             fc,
# #             action,
# #             function_name,
# #             *args,
# #         )
# #
# #
# # def _execute_cli_action(
# #     channel: FunctionalChannel, action: CliActions, callback_name: str, *args
# # ) -> bool:
# #     """Execute the callback, if allowed"""
# #     if _channel_supports_action(channel, action):
# #         LOGGER.debug(
# #             f"{str(action)} allowed for channel {channel.functionalChannelType}"
# #         )
# #         print(
# #             f"Execute {action} for channel {channel.functionalChannelType} (Index: {channel.index})",
# #             end=" ... ",
# #         )
# #
# #         callback = getattr(channel, callback_name)
# #         if not callable(callback):
# #             print(
# #                 f"Function {callback_name} could not be executed in channeltype {type(channel)}"
# #             )
# #             return False
# #
# #         result = callback(*args)
# #         if result == "":
# #             result = "OK"
# #         print(f"{result}")
# #         return True
# #     else:
# #         LOGGER.warning(
# #             f"{str(action)} IS NOT allowed for channel {channel.functionalChannelType}"
# #         )
# #         print(
# #             f"{str(action)} is not supported by channel {channel.functionalChannelType} (Index: {channel.index})"
# #         )
# #         return False
# #
# #
# # def _channel_supports_action(channel: FunctionalChannel, action: CliActions) -> bool:
# #     """Check, if a channel could execute the given function"""
# #     return (
# #         channel.functionalChannelType in FUNCTIONALCHANNEL_CLI_MAP
# #         and action in FUNCTIONALCHANNEL_CLI_MAP[channel.functionalChannelType]
# #     )
# #
# #
