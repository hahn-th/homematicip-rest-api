import pytest
import asyncio
from homematicip.async.home import AsyncHome
from homematicip.base.base_connection import HmipConnectionError


@pytest.fixture
async def fake_async_home(event_loop):
    _home = AsyncHome(event_loop)
    return _home


async def raise_timeout(*args, **kwargs):
    raise asyncio.TimeoutError


@pytest.mark.asyncio
async def test_on_connection_lost(fake_async_home, monkeypatch):
    monkeypatch.setattr(fake_async_home._connection._websession, 'ws_connect',
                        raise_timeout)
    fake_async_home._restCallRequestCounter = 1
    fake_async_home._connection._restCallTimout = 0.1

    def connection_handler(future_):
        with pytest.raises(HmipConnectionError):
            _result = future_.result()

    ws_connection = fake_async_home.enable_events()

    with pytest.raises(HmipConnectionError):
        await ws_connection
    #
    # fake_async_home.on_connection_lost(connection_handler)



    await asyncio.sleep(1)
