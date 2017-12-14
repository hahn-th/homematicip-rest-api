import asyncio
import json

import os

import config
import logging
import datetime
from pprint import pprint
from homematicip.async.home import AsyncHome


def on_update_handler(data, event_type, obj):
    if obj:
        data['api_name'] = obj.__class__.__name__
    pprint(data)
    # save the data.
    _file_name = '{}_{}.json'.format(obj.__class__.__name__,
                                     datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    _full_path = os.path.join('tests/json_data', _file_name)
    with open(_full_path, 'w') as fl:
        json.dump(data, fl, indent=4)


async def main():
    loop = asyncio.get_event_loop()
    home = AsyncHome(loop)
    home.set_auth_token(config.AUTH_TOKEN)
    await home.init(config.ACCESS_POINT)

    await home.get_current_state()
    home.enable_events()
    # home.start_incoming_websocket_data()
    for d in home.devices:
        print('{} {} {}'.format(d.id, d.label, str(d)))
        d.on_update(on_update_handler)
    for d in home.groups:
        d.on_update(on_update_handler)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    # loop.run_until_complete(main(loop))
    loop.run_forever()
