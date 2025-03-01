import asyncio
import logging
import sys
import time

import homematicip
from homematicip.async_home import AsyncHome

def setup_config() -> homematicip.HmipConfig:
    """Initialize configuration."""
    _config = homematicip.find_and_load_config_file()

    return _config


async def get_home(config: homematicip.HmipConfig) -> AsyncHome:
    """Initialize home instance."""
    home = AsyncHome()
    await home.init_async(config.access_point, config.auth_token)
    return home

async def run_forever_task(home: AsyncHome):
    """Task to run forever."""
    await home.enable_events(print_output)

async def print_output(message):
    print(message)

async def close_after_15_seconds(home: AsyncHome):
    for i in range(15):
        print(f"WebSocket is connected: {home.websocket_is_connected()}")
        print(f"Closing in {15-i} seconds")
        await asyncio.sleep(1)

    await home.disable_events_async()


async def main():
    config = setup_config()

    logging.basicConfig(
        level=logging.DEBUG,  # Set the logging level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)  # Output to console
        ]
    )

    if config is None:
        print("Could not find configuration file. Script will exit")
        sys.exit(-1)

    home = await get_home(config)

    try:
        # task_events = asyncio.create_task(home.enable_events(print_output))
        # task = asyncio.create_task(close_after_15_seconds(home))
        #
        # await asyncio.gather(task_events, task)
        await home.get_current_state_async()
        asyncio.create_task(home.enable_events())

        for i in range(10):
            print(f"WebSocket is connected: {home.websocket_is_connected()}")
            print(f"Closing in {10-i} seconds")
            await asyncio.sleep(1)
        await home.disable_events_async()
        print(home.websocket_is_connected())
    except KeyboardInterrupt:
        print("Client wird durch Benutzer beendet.")
    finally:
        await home.disable_events_async()
        print("WebSocket-Client beendet.")


if __name__ == "__main__":
    asyncio.run(main())