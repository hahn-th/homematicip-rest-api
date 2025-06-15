import asyncio
import json
import logging
import signal
import sys
import traceback
from argparse import RawDescriptionHelpFormatter, ArgumentParser
from importlib.metadata import version

import homematicip
from homematicip.async_home import AsyncHome
from homematicip.cli.hmip_cli import setup_logger
import homematicip.commands.functional_channel_commands
from homematicip.connection.rest_connection import RestConnection, RestResult

logger = logging.getLogger("hmip_cmd")


async def main_async(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = get_parser()
    parsed_args = parser.parse_args(args)

    if len(sys.argv) == 1:
        parser.print_help()
        return

    try:
        config = setup_config(parsed_args)

        if config is None:
            print("Could not find configuration file. Script will exit")
            sys.exit(-1)

        setup_logger(
            config.log_level, 20, config.log_file
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

        return 255

async def run(config: homematicip.HmipConfig, home: AsyncHome, logger: logging.Logger, args):
    batch_definition = get_batch_job_definition(args.batch_file)

    results = []

    if not batch_definition:
        logger.error("No batch definition found.")
        return False

    definition = batch_definition.get("definition")
    interval = batch_definition.get("interval", 8)

    commands = batch_definition.get("commands")
    if not commands:
        logger.error("No jobs found in batch definition.")
        return False

    first_run = True
    for command in commands:
        if not first_run:
            await asyncio.sleep(interval)
        first_run = False

        function_name = command.get("function")
        params = command.get("params", {})
        active = command.get("active", True)

        if not active:
            continue

        if not function_name:
            logger.error("Job function name is missing.")
            continue

        if not isinstance(params, dict):
            logger.error(f"Parameters for function '{function_name}' must be a dictionary.")
            continue

        params["device_id"] = args.device
        params["channel_index"] = args.channel

        print(f"{function_name} with params: {params}")
        results.append(f"{function_name} with params: {params}")
        result: RestResult = await run_command_async(function_name, params, home._connection)
        log_entry = f"{function_name} - {result.status} {result.status_text if result.status_text else ''} {result.text if result.text else ''}"
        print(log_entry)
        results.append(log_entry)

    if results:
        print("\n".join(results))

    return True


async def run_command_async(function_name: str, params: dict, connection: RestConnection):
    """Run a command on the home."""
    if not hasattr(homematicip.commands.functional_channel_commands, function_name):
        print(f"Command '{function_name}' not found.")
        return False

    try:
        conn = {"rest_connection": connection}
        p = {**params, **conn}
        method = getattr(homematicip.commands.functional_channel_commands, function_name)
        result = await method(**p)
        return result
    except Exception as e:
        print(f"Error executing command '{function_name}': {e}")
        return False


def get_batch_job_definition(batch_file: str):
    with open(batch_file, "r") as f:
        batch_data = json.load(f)

    return batch_data

def setup_config(args) -> homematicip.HmipConfig:
    """Initialize configuration."""
    return homematicip.find_and_load_config_file()

async def get_home(config: homematicip.HmipConfig) -> AsyncHome:
    """Initialize home instance."""
    home = AsyncHome()
    await home.init_async(config.access_point, config.auth_token)
    return home

def get_parser():
    """Return ArgumentParser for hmip_cli."""
    parser = ArgumentParser(
        description=f"Run any command to any device for the homematicip API\nVersion: {version('homematicip')}\nPython: {sys.version} ",
        formatter_class=RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-d",
        "--device",
        dest="device",
        type=str,
        help='the device you want to test',
    )

    parser.add_argument(
        "-i",
        "--index",
        dest="channel",
        help="channel indices to specify one or more specific channels",
        default=None,
    )

    parser.add_argument(
        "batch_file",
        help="Path to a JSON batch file with commands to execute"
    )

    return parser

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()