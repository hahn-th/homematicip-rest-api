import asyncio
import aiohttp
import homematicip.async
import config
import logging

from logging import handlers
from operator import attrgetter
from argparse import ArgumentParser
from homematicip.async.home import Home, AsyncHome


async def main(loop):
    loop=asyncio.get_event_loop()
    home = AsyncHome(loop)
    home.set_auth_token(config.AUTH_TOKEN)
    await home.init(config.ACCESS_POINT)

    await home.get_current_state()
    #home.start_incoming_websocket_data()
    for d in home.devices:
        print('{} {} {}'.format(d.id, d.label, str(d)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    #loop.create_task(main(loop))
    loop.run_until_complete(main(loop))
    #loop.run_forever()