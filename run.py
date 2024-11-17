import asyncio
import logging
import sys
import time

import homematicip
from homematicip.home import Home


def setup_config() -> homematicip.HmipConfig:
    """Initialize configuration."""
    _config = homematicip.find_and_load_config_file()

    return _config


def get_home(config: homematicip.HmipConfig) -> Home:
    """Initialize home instance."""
    home = Home()
    home.set_auth_token(config.auth_token)
    home.init(config.access_point, config.auth_token)
    return home

async def run_forever_task(home: Home):
    """Task to run forever."""
    await home.enable_events(print_output)
    while True:
        await asyncio.sleep(1)

async def print_output(message):
    print(message)



async def main():
    config = setup_config()

    if config is None:
        print("Could not find configuration file. Script will exit")
        sys.exit(-1)

    home = get_home(config)

    try:
        await run_forever_task(home)
    except KeyboardInterrupt:
        print("Client wird durch Benutzer beendet.")
    finally:
        home.disable_events()
        print("WebSocket-Client beendet.")


if __name__ == "__main__":
    asyncio.run(main())