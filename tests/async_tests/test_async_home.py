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

@pytest.mark.asyncio
async def test_home_location(fake_async_home: AsyncHome):
    assert fake_async_home.location.city == "1010  Wien, österreich"
    assert fake_async_home.location.latitude == "48.208088"
    assert fake_async_home.location.longitude == "16.358608"
    assert fake_async_home.location._rawJSONData == fake_home_download_configuration()["home"]["location"]
    assert str(fake_async_home.location) == "city(1010  Wien, österreich) latitude(48.208088) longitude(16.358608)"

@pytest.mark.asyncio
async def test_home_set_location(fake_async_home: AsyncHome):
    with no_ssl_verification():
        await fake_async_home.set_location("Berlin, Germany", "52.530644", "13.383068")
        await fake_async_home.get_current_state()
        assert fake_async_home.location.city == "Berlin, Germany"
        assert fake_async_home.location.latitude == "52.530644"
        assert fake_async_home.location.longitude == "13.383068"
        assert str(fake_async_home.location) == "city(Berlin, Germany) latitude(52.530644) longitude(13.383068)"


@pytest.mark.asyncio
async def test_security_zones_activation(fake_async_home: AsyncHome):
    with no_ssl_verification():
        internal, external = fake_async_home.get_security_zones_activation()
        assert internal == False
        assert external == False

        await fake_async_home.set_security_zones_activation(True,True)
        await fake_async_home.get_current_state()

        internal, external = fake_async_home.get_security_zones_activation()
        assert internal == True
        assert external == True