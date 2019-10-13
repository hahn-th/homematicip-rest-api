import asyncio
from aiohttp import web
import ssl
import time
from datetime import datetime, timedelta, timezone
from threading import Thread
from aiohttp.test_utils import TestServer
import pytest
from pytest_localserver.http import WSGIServer

from homematicip.aio.auth import AsyncAuth
from homematicip.aio.home import AsyncHome
from homematicip.home import Home
from homematicip.connection import Connection

from homematicip_demo.fake_cloud_server import FakeCloudServer, AsyncFakeCloudServer
from homematicip_demo.helper import *


@pytest.fixture
def ssl_ctx():
    ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
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
    loop.close()


@pytest.fixture
async def aio_fake_cloud(aiohttp_server, ssl_ctx):
    """Defines the testserver funcarg"""

    loop = asyncio.new_event_loop()
    stop_threads = False
    t = Thread(name="aio_fake_cloud",target=start_background_loop, args=(lambda: stop_threads, loop))
    t.setDaemon(True)
    t.start()

    aio_server = AsyncFakeCloudServer()
    app = web.Application()
    app.router.add_get("/{name}", aio_server)
    app.router.add_post("/{name}", aio_server)
    # fill route table
    server = TestServer(app, ssl=ssl_ctx)
    await server.start_server(loop)
    aio_server.url = str(server._root)
    server.url = aio_server.url
    yield server
    server.close()
    stop_threads = True


@pytest.fixture
def fake_cloud(request):
    """Defines the testserver funcarg"""
    app = FakeCloudServer()
    server = WSGIServer(
        application=app,
        ssl_context=(get_full_path("server.crt"), get_full_path("server.key")),
    )
    app.url = server.url
    server._server._timeout = 5  # added to allow timeouts in the fake server
    server.start()
    yield server
    server.stop()


def get_home(fake_cloud):
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
def old_fake_home(fake_cloud):
    return get_home(fake_cloud)


@pytest.fixture
def fake_home(aio_fake_cloud):
    return get_home(aio_fake_cloud)


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
