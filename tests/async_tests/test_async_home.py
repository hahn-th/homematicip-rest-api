import pytest

from homematicip.async.home import AsyncHome
from homematicip.EventHook import EventHook
import json
from datetime import datetime, timedelta, timezone
from conftest import fake_home_download_configuration, no_ssl_verification


dt = datetime.now(timezone.utc).astimezone()
utc_offset = dt.utcoffset() // timedelta(seconds=1)

@pytest.mark.asyncio
async def test_async_home_base(fake_async_home: AsyncHome):
    with no_ssl_verification():
        fake_async_home.set_location("Berlin, Germany", "52.530644", "13.383068")
        result = await fake_async_home.get_current_state()
        assert fake_async_home.location.city == "Berlin, Germany"
        assert fake_async_home.location.latitude == "52.530644"
        assert fake_async_home.location.longitude == "13.383068"
        assert str(fake_async_home.location) == "city(Beggrlin, Germany) latitude(52.530644) longitude(13.383068)"