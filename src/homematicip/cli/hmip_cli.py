import asyncio
import json
import logging
import signal
import sys
import time
import traceback
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from asyncio import iscoroutinefunction
from importlib.metadata import version
from logging.handlers import TimedRotatingFileHandler
from operator import attrgetter

import homematicip
from homematicip.async_home import AsyncHome
from homematicip.base.enums import CliActions, ClimateControlDisplay, LockState
from homematicip.base.functionalChannels import FunctionalChannel
from homematicip.base.helpers import handle_config
from homematicip.class_maps import FUNCTIONALCHANNEL_CLI_MAP
from homematicip.device import BaseDevice, Device, TemperatureHumiditySensorDisplay
from homematicip.group import ExtendedLinkedSwitchingGroup, HeatingGroup
from homematicip.rule import SimpleRule

logger = logging.getLogger("hmip_cli")


async def main_async(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = get_parser()
    parsed_args = get_args(parser, args)

    if len(sys.argv) == 1:
        parser.print_help()
        return

    try:
        config = setup_config(parsed_args)

        if config is None:
            print("Could not find configuration file. Script will exit")
            sys.exit(-1)

        setup_logger(
            config.log_level, parsed_args.debug_level, config.log_file
        )
        home = await get_home(config)

        if not await run(config, home, logger, parsed_args):
            print(
                "Command not found. Use -h or --help argument for available commands."
            )
            sys.exit(-1)
    except KeyboardInterrupt:
        # Shell standard is 128 + signum = 130 (SIGINT = 2)
        sys.stdout.write("\n")
        return 128 + signal.SIGINT
    except Exception as e:
        # stderr and exit code 255
        sys.stderr.write("\n")
        sys.stderr.write(f"\033[91m{type(e).__name__}: {str(e)}\033[0;0m")
        sys.stderr.write("\n")
        # at this point, you're guaranteed to have args and thus log_level
        if parsed_args.debug_level:
            if parsed_args.debug_level < 10:
                # traceback prints to stderr by default
                traceback.print_exc()

        return 255


def setup_config(args) -> homematicip.HmipConfig:
    """Initialize configuration."""
    if args.config_file:
        try:
            _config = homematicip.load_config_file(args.config_file)
        except FileNotFoundError:
            print("##### CONFIG FILE NOT FOUND: {} #####".format(args.config_file))
            return
    else:
        _config = homematicip.find_and_load_config_file()

    return _config


async def get_home(config: homematicip.HmipConfig) -> AsyncHome:
    """Initialize home instance."""
    home = AsyncHome()
    await home.init_async(config.access_point, config.auth_token)
    return home


def setup_logger(default_debug_level: int, argument_debug_level: int, log_file: str) -> logging.Logger:
    global logger

    debug_level = argument_debug_level if argument_debug_level else default_debug_level

    # Create console handler with custom formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(levelname)-7s - %(asctime)s - %(name)s - %(message)s"))

    # Create file handler if log_file is provided
    handlers = [console_handler]
    if log_file:
        file_handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=5)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        handlers.append(file_handler)

    # Configure basic logging with handlers
    logging.basicConfig(level=debug_level, handlers=handlers)
    logger = logging.getLogger("hmip_cli")

    third_party_loggers = [
        "httpx",
        "httpcore.http11",
        "httpcore.connection",
        "asyncio",
        "websockets.client"
    ]
    for logger_name in third_party_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


async def run(config: homematicip.HmipConfig, home: AsyncHome, logger: logging.Logger, args):
    """Execution of cli commands with parsed args."""
    command_entered = False
    if args.server_config:
        print(
            f"Running homematicip-rest-api with fake server configuration {args.server_config}"
        )
        global server_config
        server_config = args.server_config
        home.download_configuration_async = fake_download_configuration

    if args.dump_config:
        command_entered = True
        json_state = await home.download_configuration_async()

        output = handle_config(json_state, args.anonymize)
        if output:
            print(output)

    if not await home.get_current_state_async():
        return

    if args.list_devices:
        command_entered = True
        sorted_devices = sorted(home.devices, key=attrgetter("deviceType", "label"))
        for device in sorted_devices:
            print("{} {}".format(device.id, str(device)))

    if args.list_groups:
        command_entered = True
        sorted_groups = sorted(home.groups, key=attrgetter("groupType", "label"))
        for g in sorted_groups:
            print(g)

    if args.list_last_status_update:
        command_entered = True
        print("Devices:")
        sorted_devices = sorted(home.devices, key=attrgetter("deviceType", "label"))
        for device in sorted_devices:
            print("\t{}\t{}\t{}".format(device.id, device.label, device.lastStatusUpdate))
        print("Groups:")
        sorted_groups = sorted(home.groups, key=attrgetter("groupType", "label"))
        for g in sorted_groups:
            print("\t{}\t{}\t{}".format(g.groupType, g.label, g.lastStatusUpdate))

    if args.list_group_ids:
        command_entered = True
        sorted_groups = sorted(home.groups, key=attrgetter("groupType", "label"))
        for g in sorted_groups:
            print("Id: {} - Type: {} - Label: {}".format(g.id, g.groupType, g.label))

    if args.protectionmode:
        command_entered = True
        if args.protectionmode == "presence":
            await home.set_security_zones_activation_async(False, True)
        elif args.protectionmode == "absence":
            await home.set_security_zones_activation_async(True, True)
        elif args.protectionmode == "disable":
            await home.set_security_zones_activation_async(False, False)

    if args.new_pin:
        command_entered = True
        await home.set_pin_async(args.new_pin, args.old_pin)
    if args.delete_pin:
        command_entered = True
        await home.set_pin_async(None, args.old_pin)

    if args.list_security_journal:
        command_entered = True
        journal = await home.get_security_journal_async()
        for entry in journal:
            print(entry)

    if args.list_firmware:
        command_entered = True
        print(
            "{:45s} - Firmware: {:6} - Available Firmware: {:6} UpdateState: {}".format(
                "HmIP AccessPoint",
                home.currentAPVersion if home.currentAPVersion is not None else "None",
                home.availableAPVersion
                if home.availableAPVersion is not None
                else "None",
                home.updateState,
            )
        )
        sorted_devices = sorted(home.devices, key=attrgetter("deviceType", "label"))
        for device in sorted_devices:
            if type(device) == BaseDevice:
                # skip unknown devices to avoid exception
                continue
            print(
                "{:45s} - Firmware: {:6} - Available Firmware: {:6} UpdateState: {} LiveUpdateState: {}".format(
                    device.label,
                    device.firmwareVersion,
                    device.availableFirmwareVersion
                    if device.availableFirmwareVersion is not None
                    else "None",
                    device.updateState,
                    device.liveUpdateState,
                )
            )

    if args.list_rssi:
        command_entered = True

        print(
            "{:45s} - Duty cycle: {:2}".format(
                "HmIP AccessPoint",
                home.dutyCycle if home.dutyCycle is not None else "None",
            )
        )

        sorted_devices = sorted(home.devices, key=attrgetter("deviceType", "label"))
        for device in sorted_devices:
            print(
                "{:45s} - RSSI: {:4} {} - Peer RSSI: {:4} - {} {} permanentlyReachable: {}".format(
                    device.label,
                    device.rssiDeviceValue if device.rssiDeviceValue is not None else "None",
                    get_rssi_bar_string(device.rssiDeviceValue),
                    device.rssiPeerValue if device.rssiPeerValue is not None else "None",
                    get_rssi_bar_string(device.rssiPeerValue),
                    "Unreachable" if device.unreach else "",
                    device.permanentlyReachable,
                )
            )
    if args.list_rules:
        command_entered = True
        sorted_rules = sorted(home.rules, key=attrgetter("ruleType", "label"))
        for device in sorted_rules:
            print("{} {}".format(device.id, str(device)))

    if args.device:
        command_entered = False
        devices = []
        for argdevice in args.device:
            if argdevice == "*":
                devices = home.devices
                break
            else:
                device = home.search_device_by_id(argdevice)
                if device is None:
                    logger.error("Could not find device %s", argdevice)
                else:
                    devices.append(device)

        for device in devices:
            if args.device_new_label:
                await device.set_label_async(args.device_new_label)
                command_entered = True

            if args.device_switch_state is not None:
                await _execute_action_for_device(
                    device,
                    args,
                    CliActions.SET_SWITCH_STATE,
                    "async_set_switch_state",
                    args.device_switch_state,
                )
                command_entered = True

            if args.device_dim_level is not None:
                await _execute_action_for_device(
                    device,
                    args,
                    CliActions.SET_DIM_LEVEL,
                    "async_set_dim_level",
                    args.device_dim_level,
                )
                command_entered = True

            if args.device_set_lock_state is not None:
                target_lock_state = LockState.from_str(args.device_set_lock_state)
                if target_lock_state not in LockState:
                    logger.error("%s is not a lock state.", args.device_set_lock_state)

                else:
                    pin = args.pin[0] if len(args.pin) > 0 else ""
                    await _execute_action_for_device(
                        device,
                        args,
                        CliActions.SET_LOCK_STATE,
                        "async_set_lock_state",
                        target_lock_state,
                        pin,
                    )
                command_entered = True

            if args.toggle_garage_door is not None:
                await _execute_action_for_device(
                    device,
                    args,
                    CliActions.TOGGLE_GARAGE_DOOR,
                    "async_send_start_impulse",
                )
                command_entered = True

            if args.device_send_door_command is not None:
                await _execute_action_for_device(
                    device,
                    args,
                    CliActions.SEND_DOOR_COMMAND,
                    "async_send_door_command",
                    args.device_send_door_command,
                )
                command_entered = True

            if args.device_shutter_level is not None:
                await _execute_action_for_device(
                    device,
                    args,
                    CliActions.SET_SHUTTER_LEVEL,
                    "async_set_shutter_level",
                    args.device_shutter_level,
                )
                command_entered = True

            if args.device_slats_level is not None:
                slats_level = args.device_slats_level[0]
                shutter_level = (
                    args.device_slats_level[1]
                    if len(args.device_slats_level) > 1
                    else None
                )
                await _execute_action_for_device(
                    device,
                    args,
                    CliActions.SET_SLATS_LEVEL,
                    "async_set_slats_level",
                    slats_level,
                    shutter_level,
                )
                command_entered = True

            if args.device_shutter_stop is not None:
                await _execute_action_for_device(
                    device,
                    args,
                    CliActions.SET_SHUTTER_STOP,
                    "async_set_shutter_stop",
                )
                command_entered = True

            if args.device_display is not None:
                if isinstance(device, TemperatureHumiditySensorDisplay):
                    device.set_display(
                        ClimateControlDisplay(args.device_display.upper())
                    )
                else:
                    logger.error(
                        "can't set display of device %s of type %s",
                        device.id,
                        device.deviceType,
                    )
                command_entered = True

            if args.device_enable_router_module is not None:
                if device.routerModuleSupported:
                    device.set_router_module_enabled(args.device_enable_router_module)
                    print(
                        "{} the router module for device {}".format(
                            "Enabled"
                            if args.device_enable_router_module
                            else "Disabled",
                            device.id,
                        )
                    )
                else:
                    logger.error(
                        "the device %s doesn't support the router module", device.id
                    )
                command_entered = True

            if args.reset_energy_counter:
                await _execute_action_for_device(
                    device,
                    args,
                    CliActions.RESET_ENERGY_COUNTER,
                    "async_reset_energy_counter",
                )
                command_entered = True

            if args.print_infos:
                command_entered = True
                print(device)
                print("------")
                for fc in device.functionalChannels:
                    print(f"   Ch {fc.index}: {str(fc)}")
                    if (
                            args.print_allowed_commands
                            and fc.functionalChannelType in FUNCTIONALCHANNEL_CLI_MAP
                    ):
                        print(
                            f"   -> Allowed commands: {FUNCTIONALCHANNEL_CLI_MAP[fc.functionalChannelType]}"
                        )

            if args.print_allowed_commands and device is not None:
                command_entered = True
                print(f"Allowed commands for selected channels device {device.id}")
                target_channels = []
                if args.channels:
                    target_channels = _get_target_channels(device, args.channels)
                else:
                    target_channels = device.functionalChannels

                for fc in target_channels:
                    print(
                        f"   -> Ch {fc.index}, Type {fc.functionalChannelType} Allowed commands: ",
                        end=" ",
                    )
                    if fc.functionalChannelType in FUNCTIONALCHANNEL_CLI_MAP:
                        print(
                            f"{[str(val) for val in FUNCTIONALCHANNEL_CLI_MAP[fc.functionalChannelType]]}"
                        )
                    else:
                        print("None")

    if args.set_zones_device_assignment:
        internal = []
        external = []
        error = False
        command_entered = True
        for id in args.external_devices:
            device = home.search_device_by_id(id)
            if device is None:
                logger.error("Device %s is not registered on this Access Point", id)
                error = True
            else:
                external.append(device)

        for id in args.internal_devices:
            device = home.search_device_by_id(id)
            if device is None:
                logger.error("Device %s is not registered on this Access Point", id)
                error = True
            else:
                internal.append(device)
        if not error:
            await home.set_zones_device_assignment_async(internal, external)

    if args.activate_absence:
        command_entered = True
        await home.activate_absence_with_duration_async(args.activate_absence)

    if args.activate_absence_permanent:
        command_entered = True
        await home.activate_absence_permanent_async()

    if args.deactivate_absence:
        command_entered = True
        await home.deactivate_absence_async()

    if args.inclusion_device_id:
        command_entered = True
        await home.start_inclusion_async(args.inclusion_device_id)

    if args.group:
        command_entered = False
        group = None
        for g in home.groups:
            if g.id == args.group:
                group = g
                break
        if group is None:
            logger.error("Could not find group %s", args.group)
            return

        if args.device_switch_state is not None:
            if isinstance(group, ExtendedLinkedSwitchingGroup):
                await group.set_switch_state_async(args.device_switch_state)

            command_entered = True

        if args.group_list_profiles:
            command_entered = True
            for p in group.profiles:
                is_active = p.id == group.activeProfile.id
                print(
                    f"Index: {p.index} - Id: {p.id} - Name: {p.name} - Active: {is_active} (Enabled: {p.enabled}, Visible: {p.visible})"
                )

        if args.group_shutter_level:
            command_entered = True
            await group.set_shutter_level_async(args.group_shutter_level)

        if args.group_shutter_stop:
            command_entered = True
            await group.set_shutter_stop_async()

        if args.group_slats_level:
            slats_level = args.group_slats_level[0]
            shutter_level = (
                args.group_slats_level[1] if len(args.group_slats_level) > 1 else None
            )

            command_entered = True
            await group.set_slats_level_async(slats_level, shutter_level)

        if args.group_set_point_temperature:
            command_entered = True
            if isinstance(group, HeatingGroup):
                await group.set_point_temperature_async(args.group_set_point_temperature)
            else:
                logger.error("Group %s isn't a HEATING group", g.id)

        if args.group_activate_profile:
            command_entered = True
            if isinstance(group, HeatingGroup):
                index = args.group_activate_profile
                for p in group.profiles:
                    if p.name == args.group_activate_profile:
                        index = p.index
                        break
                await group.set_active_profile_async(index)
            else:
                logger.error("Group %s isn't a HEATING group", g.id)

        if args.group_boost is not None:
            command_entered = True
            if isinstance(group, HeatingGroup):
                await group.set_boost_async(args.group_boost)
            else:
                logger.error("Group %s isn't a HEATING group", g.id)

        if args.group_boost_duration is not None:
            command_entered = True
            if isinstance(group, HeatingGroup):
                await group.set_boost_duration_async(args.group_boost_duration)
            else:
                logger.error("Group %s isn't a HEATING group", g.id)

        if args.print_infos:
            command_entered = True
            print(group)
            print("------")
            if group.metaGroup:
                print("   Metagroup: {}".format(str(group.metaGroup)))
                print("------")
            for fc in group.devices:
                print("   Assigned device: {}".format(str(fc)))

    if args.rules:
        command_entered = False
        rules = []
        for argrule in args.rules:
            if argrule == "*":
                rules = home.rules
                break
            else:
                r = home.search_rule_by_id(argrule)
                if r is None:
                    logger.error("Could not find automation rule %s", argrule)
                else:
                    rules.append(r)

        for rule in rules:
            if args.rule_activation is not None:
                if isinstance(rule, SimpleRule):
                    await rule.set_rule_enabled_state_async(args.rule_activation)
                    command_entered = True
                else:
                    logger.error(
                        "can't enable/disable rule %s of type %s",
                        rule.id,
                        rule.ruleType,
                    )

    if args.list_events:
        command_entered = True
        home.onEvent += print_events

        try:
            logger.info("Listening for events. Press Ctrl+c to stop.")
            print("Listening for events. Press Ctrl+c to stop.")
            await home.enable_events()
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await home.disable_events_async()
        finally:
            logger.info("Stopping websocket connection.")
            await home.disable_events_async()
            logger.info("Stopped listening for events.")
            print("Stopped listening for events.")

    if args.listen_channel_event:
        command_entered = True
        home.on_channel_event(lambda x: print(x))
        await home.enable_events(additional_message_handler=lambda x: print(x))
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            return

    return command_entered


def print_message(message):
    print(message)


def get_args(parser, args):
    """Parse arguments passed in from shell."""
    return parser.parse_args(args)


def get_parser():
    """Return ArgumentParser for hmip_cli."""
    parser = ArgumentParser(
        description=f"a cli wrapper for the homematicip API\nVersion: {version('homematicip')}\nPython: {sys.version} ",
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--config_file",
        type=str,
        help="the configuration file. If nothing is specified the script will search for it.",
    )
    parser.add_argument(
        "--server-config",
        type=str,
        dest="server_config",
        help="the server configuration file. e.g. output from --dump-configuration.",
    )
    parser.add_argument(
        "--debug-level",
        dest="debug_level",
        type=int,
        help="the debug level which should get used(Critical=50, DEBUG=10)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {}\nPython: {}".format(version("homematicip"), sys.version),
    )

    group = parser.add_argument_group("Display Configuration")
    group.add_argument(
        "--dump-configuration",
        action="store_true",
        dest="dump_config",
        help="dumps the current configuration from the AP",
    )
    group.add_argument(
        "--anonymize",
        action="store_true",
        dest="anonymize",
        help="used together with --dump-configuration to anonymize the output",
    )
    group.add_argument(
        "--list-devices",
        action="store_true",
        dest="list_devices",
        help="list all devices",
    )
    group.add_argument(
        "--list-groups", action="store_true", dest="list_groups", help="list all groups"
    )
    group.add_argument(
        "--list-group-ids",
        action="store_true",
        dest="list_group_ids",
        help="list all groups and their ids",
    )
    group.add_argument(
        "--list-firmware",
        action="store_true",
        dest="list_firmware",
        help="list the firmware of all devices",
    )
    group.add_argument(
        "--list-rssi",
        action="store_true",
        dest="list_rssi",
        help="list the reception quality of all devices",
    )
    group.add_argument(
        "--list-events",
        action="store_true",
        dest="list_events",
        help="prints all the events",
    )
    group.add_argument(
        "--list-last-status-update",
        action="store_true",
        dest="list_last_status_update",
        help="prints the last status update of all systems",
    )

    parser.add_argument(
        "--list-security-journal",
        action="store_true",
        dest="list_security_journal",
        help="display the security journal",
    )
    parser.add_argument(
        "--list-rules",
        action="store_true",
        dest="list_rules",
        help="display all automation rules",
    )

    parser.add_argument(
        "-d",
        "--device",
        dest="device",
        action="append",
        help='the device you want to modify (see "Device Settings").\nYou can use * to modify all devices or enter the parameter multiple times to modify more devices',
    )
    parser.add_argument(
        "-g",
        "--group",
        dest="group",
        help='the group you want to modify (see "Group Settings")',
    )
    parser.add_argument(
        "--print-infos",
        action="store_true",
        dest="print_infos",
        help="Print channels or devices, which belongs to devices or groups.",
    )
    parser.add_argument(
        "-ac",
        "--print-allowed-commands",
        action="store_true",
        dest="print_allowed_commands",
        help="Print allowed commands for channels of a device. Use together with a device and optional combined with arguments --print-infos or single --channel.",
    )
    parser.add_argument(
        "-r",
        "--rule",
        dest="rules",
        action="append",
        help='the automation you want to modify (see "Automation Rule Settings").\nYou can use * to modify all automations or enter the parameter multiple times to modify more automations',
    )

    group = parser.add_argument_group("Device Settings")
    group.add_argument(
        "--toggle-garage-door",
        action="store_true",
        dest="toggle_garage_door",
        help="Toggle Garage Door for devices with IMPULSE_OUTPUT_CHANNEL channel like HmIP-WGC ",
        default=None,
    )
    group.add_argument(
        "--send-door-command",
        nargs="?",
        dest="device_send_door_command",
        help="Control door for all devices, which has a channel called Door_Channel like Hmip-MOD-HO. Allowed parameters are OPEN, CLOSE, STOP and PARTIAL_OPEN.",
        default=None,
    )

    group.add_argument(
        "--turn-on",
        action="store_true",
        dest="device_switch_state",
        help="turn the switch on",
        default=None,
    )
    group.add_argument(
        "--turn-off",
        action="store_false",
        dest="device_switch_state",
        help="turn the switch off",
        default=None,
    )

    group.add_argument(
        "--channel",
        nargs="*",
        dest="channels",
        help="used together with --turn-on and --turn-off to specify one or more specific channels",
        default=None,
    )

    group.add_argument(
        "--pin",
        nargs="*",
        dest="pin",
        help="special pin used for door lock drive if set in the app",
        default="",
    )

    group.add_argument(
        "--set-lock-state",
        action="store",
        dest="device_set_lock_state",
        help="set door lock state to OPEN, LOCKED or UNLOCKED. Add --pin for special pin or --channel.",
        default=None,
    )

    group.add_argument(
        "--set-dim-level",
        action="store",
        dest="device_dim_level",
        help="set dimmer to level (0..1)",
        default=None,
    )
    group.add_argument(
        "--set-shutter-level",
        action="store",
        dest="device_shutter_level",
        help="set shutter to level (0..1)",
    )
    group.add_argument(
        "--set-slats-level",
        nargs="+",
        action="store",
        dest="device_slats_level",
        help="set slats to level (0..1). Optional set shutter level with a second argument like 'set-slats-level 0.5 0.8'",
    )
    group.add_argument(
        "--set-shutter-stop",
        action="store_true",
        dest="device_shutter_stop",
        help="stop shutter",
        default=None,
    )

    group.add_argument("--set-label", dest="device_new_label", help="set a new label")
    group.add_argument(
        "--set-display",
        dest="device_display",
        action="store",
        help="set the display mode",
        choices=["actual", "setpoint", "actual_humidity"],
    )
    group.add_argument(
        "--enable-router-module",
        action="store_true",
        dest="device_enable_router_module",
        help="enables the router module of the device",
        default=None,
    )
    group.add_argument(
        "--disable-router-module",
        action="store_false",
        dest="device_enable_router_module",
        help="disables the router module of the device",
        default=None,
    )
    group.add_argument(
        "--reset-energy-counter",
        action="store_true",
        dest="reset_energy_counter",
        help="resets the energy counter",
    )

    group = parser.add_argument_group("Home Settings")
    group.add_argument(
        "--set-protection-mode",
        dest="protectionmode",
        action="store",
        help="set the protection mode",
        choices=["presence", "absence", "disable"],
    )
    group.add_argument(
        "--set-pin", dest="new_pin", action="store", help="set a new pin"
    )
    group.add_argument(
        "--delete-pin", dest="delete_pin", action="store_true", help="deletes the pin"
    )
    group.add_argument(
        "--old-pin",
        dest="old_pin",
        action="store",
        help="the current pin. used together with --set-pin or --delete-pin",
        default=None,
    )
    group.add_argument(
        "--set-zones-device-assignment",
        dest="set_zones_device_assignment",
        action="store_true",
        help="sets the zones devices assignment",
    )
    group.add_argument(
        "--external-devices",
        dest="external_devices",
        nargs="+",
        help="sets the devices for the external zone",
    )
    group.add_argument(
        "--internal-devices",
        dest="internal_devices",
        nargs="+",
        help="sets the devices for the internal zone",
    )
    group.add_argument(
        "--activate-absence",
        dest="activate_absence",
        action="store",
        help="activates absence for provided amount of minutes",
        default=None,
        type=int,
    )
    group.add_argument(
        "--activate-absence-permanent",
        dest="activate_absence_permanent",
        action="store_true",
        help="activates absence forever",
    )
    group.add_argument(
        "--deactivate-absence",
        action="store_true",
        dest="deactivate_absence",
        help="deactivates absence",
    )
    group.add_argument(
        "--start-inclusion",
        action="store",
        dest="inclusion_device_id",
        help="start inclusion for device with given id",
    )

    group = parser.add_argument_group("Group Settings")
    group.add_argument(
        "--list-profiles",
        dest="group_list_profiles",
        action="store_true",
        help="displays all profiles for a group",
    )
    group.add_argument(
        "--activate-profile",
        dest="group_activate_profile",
        help="activates a profile by using its index or its name",
    )
    group.add_argument(
        "--set-group-shutter-level",
        action="store",
        dest="group_shutter_level",
        help="set all shutters in group to level (0..1)",
    )
    group.add_argument(
        "--set-group-shutter-stop",
        action="store_true",
        dest="group_shutter_stop",
        help="stop all shutters in group",
        default=None,
    )
    group.add_argument(
        "--set-group-slats-level",
        nargs="+",
        action="store",
        dest="group_slats_level",
        help="set all slats in group to level (0..1). Optional set shutter level with a second argument like 'set-slats-level 0.5 0.8'",
    )
    group.add_argument(
        "--set-point-temperature",
        action="store",
        dest="group_set_point_temperature",
        help='sets the temperature for the given group. The group must be of the type "HEATING"',
        default=None,
        type=float,
    )

    group.add_argument(
        "--set-boost",
        action="store_true",
        dest="group_boost",
        help="activates the boost mode for a HEATING group",
        default=None,
    )
    group.add_argument(
        "--set-boost-stop",
        action="store_false",
        dest="group_boost",
        help="deactivates the boost mode for a HEATING group",
        default=None,
    )
    group.add_argument(
        "--set-boost-duration",
        dest="group_boost_duration",
        action="store",
        help="sets the boost duration for a HEATING group in minutes",
        default=None,
        type=int,
    )

    group = parser.add_argument_group("Automation Rule Settings")
    group.add_argument(
        "--enable-rule",
        action="store_true",
        dest="rule_activation",
        help="activates the automation rules",
        default=None,
    )
    group.add_argument(
        "--disable-rule",
        action="store_false",
        dest="rule_activation",
        help="deactivates the automation rules",
        default=None,
    )

    group = parser.add_argument_group("Listen")
    group.add_argument(
        "--listen-channel-events",
        action="store_true",
        dest="listen_channel_event",
        help="listens for channel events",
    )

    return parser


def _get_target_channel_indices(device: BaseDevice, channels: list = None) -> list:
    """Get list with adressed channel indices. Is the channels list None, than the channel 1 is used."""
    target_channels_indices = []
    if channels:
        target_channels_indices = [*channels]
    else:
        target_channels_indices.append(1)
    return target_channels_indices


def _get_target_channels(device: Device, channels: list = None):
    target_channels_indices = _get_target_channel_indices(device, channels)

    target_channels = [
        device.functionalChannels[int(channel_index)]
        for channel_index in target_channels_indices
    ]
    return target_channels


async def _execute_action_for_device(
        device, cli_args, action: CliActions, function_name: str, *args
) -> None:
    target_channels = _get_target_channels(device, cli_args.channels)
    for fc in target_channels:
        await _execute_cli_action(
            fc,
            action,
            function_name,
            *args,
        )


async def _execute_cli_action(
        channel: FunctionalChannel, action: CliActions, callback_name: str, *args
) -> bool:
    """Execute the callback, if allowed"""
    if _channel_supports_action(channel, action):
        logger.debug(
            f"{str(action)} allowed for channel {channel.functionalChannelType}"
        )
        print(
            f"Execute {action} for channel {channel.functionalChannelType} (Index: {channel.index})",
            end=" ... ",
        )

        callback = getattr(channel, callback_name, None)
        if not callback:
            print(
                f"Function {callback_name} could not be found in channeltype {type(channel)}"
            )
            return
        if not callable(callback):
            print(
                f"Function {callback_name} could not be executed in channeltype {type(channel)}"
            )
            return False

        if iscoroutinefunction(callback):
            result = await callback(*args)
        else:
            result = callback(*args)

        if result == "":
            result = "OK"
        print(f"{result}")
        return True
    else:
        logger.warning(
            f"{str(action)} IS NOT allowed for channel {channel.functionalChannelType}"
        )
        print(
            f"{str(action)} is not supported by channel {channel.functionalChannelType} (Index: {channel.index})"
        )
        return False


def _channel_supports_action(channel: FunctionalChannel, action: CliActions) -> bool:
    """Check, if a channel could execute the given function"""
    return (
            channel.functionalChannelType in FUNCTIONALCHANNEL_CLI_MAP
            and action in FUNCTIONALCHANNEL_CLI_MAP[channel.functionalChannelType]
    )


def print_events(event_list):
    for event in event_list:
        print("EventType: {} Data: {}".format(event["eventType"], event["data"]))


def get_rssi_bar_string(rssi_value):
    # Observed values: -93..-47
    width = 10
    dots = 0
    if rssi_value:
        dots = int(round((100 + rssi_value) / 5))
        dots = max(0, min(width, dots))

    return "[{}{}]".format("*" * dots, "_" * (width - dots))

async def fake_download_configuration():
    """Use a json file as configuration source for the server."""
    global server_config
    if server_config:
        with open(server_config) as file:
            return json.load(file)
    return None


def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
