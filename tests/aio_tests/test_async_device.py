import pytest

from homematicip.aio.home import AsyncHome
from homematicip.EventHook import EventHook
import json
from datetime import datetime, timedelta, timezone
from conftest import no_ssl_verification


dt = datetime.now(timezone.utc).astimezone()
utc_offset = dt.utcoffset() // timedelta(seconds=1)

@pytest.mark.asyncio
async def test_basic_device_functions(fake_async_home:AsyncHome):
    with no_ssl_verification():
        d = fake_async_home.search_device_by_id('3014F7110000000000000009')
        assert d.label == "Brunnen"
        assert d.routerModuleEnabled == True

        await d.set_label("new label")
        await d.set_router_module_enabled(False)
        await fake_async_home.get_current_state()
        d = fake_async_home.search_device_by_id('3014F7110000000000000009')
        assert d.label == "new label"
        assert d.routerModuleEnabled == False

        await d.set_label("other label")
        await d.set_router_module_enabled(True)
        await fake_async_home.get_current_state()
        d = fake_async_home.search_device_by_id('3014F7110000000000000009')
        assert d.label == "other label"
        assert d.routerModuleEnabled == True

        d2 = fake_async_home.search_device_by_id('3014F7110000000000000005')
        await d.delete()
        await fake_async_home.get_current_state()
        d = fake_async_home.search_device_by_id('3014F7110000000000000009')
        assert d == None
        assert d2 is fake_async_home.search_device_by_id('3014F7110000000000000005') # make sure that the objects got updated and not completely renewed