import pytest
import json

from functools import partialmethod
import warnings
import requests
import contextlib
import aiohttp

from unittest.mock import MagicMock
from homematicip.aio.connection import AsyncConnection
from homematicip.async.home import AsyncHome
from homematicip.home import Home
from homematicip.connection import Connection

from pytest_localserver.http import WSGIServer
from fake_cloud_server import FakeCloudServer

def AsyncMock(*args, **kwargs):
    m = MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro

def fake_home_download_configuration():
    with open("tests/json_data/home.json", encoding="UTF-8") as f:
        return json.load(f)

@contextlib.contextmanager
def no_ssl_verification():
    old_request = requests.Session.request
    requests.Session.request = partialmethod(old_request, verify=False)
    
    old_aiohttp_post = aiohttp.ClientSession.post
    old_aiohttp_get = aiohttp.ClientSession.get
    old_aiohttp_put = aiohttp.ClientSession.put
    aiohttp.ClientSession.post = partialmethod(old_aiohttp_post,  ssl=False)
    aiohttp.ClientSession.get = partialmethod(old_aiohttp_get,  ssl=False)
    aiohttp.ClientSession.put = partialmethod(old_aiohttp_put,  ssl=False)


    warnings.filterwarnings('ignore', 'Unverified HTTPS request')
    yield
    warnings.resetwarnings()

    requests.Session.request = old_request
    aiohttp.ClientSession.post = old_aiohttp_post
    aiohttp.ClientSession.get = old_aiohttp_get
    aiohttp.ClientSession.put = old_aiohttp_put



@pytest.fixture
def fake_cloud(request):
    """Defines the testserver funcarg"""
    app = FakeCloudServer()
    server = WSGIServer(application = app, ssl_context=('./tests/server.crt','./tests/server.key'))
    app.url = server.url
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
        home.set_auth_token("8A45BAA53BE37E3FCA58E9976EFA4C497DAFE55DB997DB9FD685236E5E63ED7DE")
        home._connection.init(accesspoint_id="3014F711A000000BAD0C0DED", lookup_url=lookup_url)
        home.get_current_state()
    return home

@pytest.fixture
def fake_connection(event_loop):
    _connection = AsyncConnection(event_loop)
    _connection.api_call = AsyncMock(return_value='called')
    return _connection

@pytest.fixture
def async_connection(event_loop):
    _connection = AsyncConnection(event_loop)
    yield _connection
    _connection._websession.close()

@pytest.fixture
async def fake_async_home(fake_cloud,event_loop):
    home = AsyncHome(event_loop)
    with no_ssl_verification():
        lookup_url = "{}/getHost".format(fake_cloud.url)
    #    home.download_configuration = fake_home_download_configuration
        home._connection = AsyncConnection(event_loop)
        home.set_auth_token("8A45BAA53BE37E3FCA58E9976EFA4C497DAFE55DB997DB9FD685236E5E63ED7DE")
        await home._connection.init(accesspoint_id="3014F711A000000BAD0C0DED", lookup_url=lookup_url)
        await home.get_current_state()
    yield home