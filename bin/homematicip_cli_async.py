import asyncio
import datetime
import json
import logging
import os
from pprint import pprint
import homematicip

from homematicip.aio.home import AsyncHome
from homematicip.base.base_connection import HmipConnectionError


def on_update_handler(data, event_type, obj):
    if obj:
        data["api_name"] = obj.__class__.__name__
    pprint(data)
    # save the data.
    _file_name = "{}_{}.json".format(
        obj.__class__.__name__, datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    )
    _full_path = os.path.join("tests/json_data", _file_name)
    with open(_full_path, "w") as fl:
        json.dump(data, fl, indent=4)


async def get_home(loop):
    _config = homematicip.find_and_load_config_file()
    if _config is None:
        print("Could not find configuration file. Script will exit")
        return

    home = AsyncHome(loop)
    home.set_auth_token(_config.auth_token)
    await home.init(_config.access_point)
    return home


async def update_state(home):
    await home.get_current_state()
    for d in home.devices:
        print("{} {} {}".format(d.id, d.label, str(d)))
    for d in home.groups:
        print("{} {} {}".format(d.id, d.label, str(d)))


async def wait_for_ws_incoming(home):
    await home.get_current_state()
    for d in home.devices:
        d.on_update(on_update_handler)
    for d in home.groups:
        d.on_update(on_update_handler)
    reader = await home.enable_events()
    await reader


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    home = None
    try:
        home = loop.run_until_complete(get_home(loop))
    except HmipConnectionError:
        print("Problem connecting")
    if home:
        try:
            loop.run_until_complete(update_state(home))
        except HmipConnectionError:
            print("Problem connecting")
        try:
            loop.run_until_complete(wait_for_ws_incoming(home))
        except HmipConnectionError:
            print("Problem connecting")
        except KeyboardInterrupt:
            loop.run_until_complete(home.close_websocket_connection())
