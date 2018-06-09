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
        assert fake_async_home.connected == True
        assert fake_async_home.currentAPVersion == "1.2.4"
        assert fake_async_home.deviceUpdateStrategy == "AUTOMATICALLY_IF_POSSIBLE"
        assert fake_async_home.dutyCycle == 8.0
        assert fake_async_home.pinAssigned == False
        assert fake_async_home.powerMeterCurrency == "EUR"
        assert fake_async_home.powerMeterUnitPrice == 0.0
        assert fake_async_home.timeZoneId == "Europe/Vienna"
        assert fake_async_home.updateState == "UP_TO_DATE"