import pytest
from aiohttp import web
import ssl
from datetime import datetime, timedelta, timezone
import time


from aiohttp_wsgi import WSGIHandler
from pytest_aiohttp import aiohttp_server
from pytest_localserver.http import WSGIServer

from homematicip.aio.auth import AsyncAuth
from homematicip.aio.home import AsyncHome
from homematicip.home import Home
from homematicip.connection import Connection

from homematicip_demo.fake_cloud_server import FakeCloudServer
from homematicip_demo.helper import *




@pytest.fixture
async def fake_cloud(request,aiohttp_server):
    """Defines the testserver funcarg"""
    fake_cloud_server = FakeCloudServer()
    wsgi_handler = WSGIHandler(fake_cloud_server)
    
    app = web.Application()
    app.router.add_route("*", "/{path_info:.*}", wsgi_handler)
    ssl_context = ssl._create_default_https_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(get_full_path("server.crt"), get_full_path("server.key"))
    server = await aiohttp_server(app)
    web.run_app(app,ssl_context=ssl_context)

    app.url = server.url
    server._server._timeout = 5  # added to allow timeouts in the fake server
    server.start()
    request.addfinalizer(server.stop)
    return server


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
    utc_offset = utc_offset + 3600
