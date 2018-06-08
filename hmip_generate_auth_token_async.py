import asyncio
import json

import os

import config
import logging
import datetime
from pprint import pprint
from homematicip.async.auth import AsyncAuth
from homematicip.base.base_connection import HmipConnectionError


async def get_auth(loop):
    auth = AsyncAuth(loop)
    await auth.init(config.ACCESS_POINT)
    return auth

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    home = None
    try:
        auth = loop.run_until_complete(get_auth(loop))
    except HmipConnectionError:
        print("Problem connecting")
