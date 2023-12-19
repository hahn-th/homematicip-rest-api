import asyncio
import functools
import ssl
import time
from datetime import datetime, timedelta, timezone
from threading import Thread

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from homematicip.aio.auth import AsyncAuth
from homematicip.aio.home import AsyncHome
from homematicip.connection import Connection
from homematicip.home import Home
from homematicip_demo.fake_cloud_server import AsyncFakeCloudServer
from homematicip_demo.helper import *


# content of conftest.py
def pytest_configure(config):
    import sys

    sys._called_from_test = True


def pytest_unconfigure(config):  # pragma: no cover
    import sys  # This was missing from the manual

    del sys._called_from_test


@pytest.fixture
def ssl_ctx():
    ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # ssl_ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    # ssl_ctx.maximum_version = ssl.TLSVersion.TLSv1_3
    ssl_ctx.load_cert_chain(get_full_path("server.crt"), get_full_path("server.key"))
    return ssl_ctx


def start_background_loop(stop_threads, loop: asyncio.AbstractEventLoop) -> None:
    async def wait_for_close(stop_threads):
        while True:
            await asyncio.sleep(1)
            if stop_threads():
                break

    asyncio.set_event_loop(loop)
    loop.run_until_complete(wait_for_close(stop_threads))
    loop.run_until_complete(asyncio.sleep(0))


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


test_server = None


@pytest.fixture(scope="session")
async def session_stop_threads():
    loop = asyncio.new_event_loop()
    stop_threads = False
    t = Thread(
        name="aio_fake_cloud",
        target=start_background_loop,
        args=(lambda: stop_threads, loop),
    )
    t.daemon = True
    t.start()
    yield loop

    stop_threads = True
    t.join()
    while loop.is_running():  # pragma: no cover
        await asyncio.sleep(0.1)
    loop.close()


@pytest.fixture
async def fake_cloud(aiohttp_server, ssl_ctx, session_stop_threads):
    """Defines the testserver funcarg"""
    global test_server
    if test_server is None:
        aio_server = AsyncFakeCloudServer()
        app = web.Application()
        app.router.add_route("GET", "/{tail:.*}", aio_server)
        app.router.add_route("POST", "/{tail:.*}", aio_server)

        test_server = TestServer(app)
        asyncio.run_coroutine_threadsafe(
            test_server.start_server(loop=session_stop_threads, ssl=ssl_ctx),
            session_stop_threads,
        ).result()
        aio_server.url = str(test_server._root)
        test_server.url = aio_server.url
        test_server.aio_server = aio_server
    test_server.aio_server.reset()
    return test_server


@pytest.fixture
def fake_home(fake_cloud):
    home = Home()
    with no_ssl_verification():
        lookup_url = "{}/getHost".format(fake_cloud.url)
        #    home.download_configuration = fake_home_download_configuration
        home._connection = Connection()
        home._fake_cloud = fake_cloud
        home.set_auth_token(
            "8A45BAA53BE37E3FCA58E9976EFA4C497DAFE55DB997DB9FD685236E5E63ED7DE"
        )
        home._connection.init(
            accesspoint_id="3014F711A000000BAD0C0DED", lookup_url=lookup_url
        )
        home.get_current_state()
    return home


@pytest.fixture
async def no_ssl_fake_async_home(fake_cloud, event_loop):
    home = AsyncHome(event_loop)
    home._connection._websession.post = partial(
        home._connection._websession.post, ssl=False
    )

    lookup_url = "{}/getHost".format(fake_cloud.url)
    home._fake_cloud = fake_cloud
    home.set_auth_token(
        "8A45BAA53BE37E3FCA58E9976EFA4C497DAFE55DB997DB9FD685236E5E63ED7DE"
    )
    await home._connection.init(
        accesspoint_id="3014F711A000000BAD0C0DED", lookup_url=lookup_url
    )
    await home.get_current_state()

    yield home

    await home._connection._websession.close()


@pytest.fixture
async def no_ssl_fake_async_auth(event_loop):
    auth = AsyncAuth(event_loop)
    auth._connection._websession.post = partial(
        auth._connection._websession.post, ssl=False
    )
    yield auth

    await auth._connection._websession.close()


dt = datetime.now(timezone.utc).astimezone()
utc_offset = dt.utcoffset() // timedelta(seconds=1)
# the timestamp of the tests were written during DST so utc_offset is one hour less outside of DST
# -> adding one hour extra
if not time.localtime().tm_isdst:
    utc_offset = utc_offset + 3600  # pragma: no cover
