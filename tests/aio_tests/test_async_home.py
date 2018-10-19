from datetime import datetime, timedelta, timezone

import pytest
from conftest import fake_home_download_configuration, no_ssl_verification

from homematicip.aio.home import AsyncHome
from homematicip.base.enums import *

dt = datetime.now(timezone.utc).astimezone()
utc_offset = dt.utcoffset() // timedelta(seconds=1)

@pytest.mark.asyncio
async def test_async_home_base(no_ssl_fake_async_home: AsyncHome):
    assert no_ssl_fake_async_home.connected == True
    assert no_ssl_fake_async_home.currentAPVersion == "1.2.4"
    assert no_ssl_fake_async_home.deviceUpdateStrategy == DeviceUpdateStrategy.AUTOMATICALLY_IF_POSSIBLE
    assert no_ssl_fake_async_home.dutyCycle == 8.0
    assert no_ssl_fake_async_home.pinAssigned == False
    assert no_ssl_fake_async_home.powerMeterCurrency == "EUR"
    assert no_ssl_fake_async_home.powerMeterUnitPrice == 0.0
    assert no_ssl_fake_async_home.timeZoneId == "Europe/Vienna"
    assert no_ssl_fake_async_home.updateState == HomeUpdateState.UP_TO_DATE

@pytest.mark.asyncio
async def test_home_location(no_ssl_fake_async_home: AsyncHome):
    assert no_ssl_fake_async_home.location.city == "1010  Wien, Österreich"
    assert no_ssl_fake_async_home.location.latitude == "48.208088"
    assert no_ssl_fake_async_home.location.longitude == "16.358608"
    assert no_ssl_fake_async_home.location._rawJSONData == fake_home_download_configuration()["home"]["location"]
    assert str(no_ssl_fake_async_home.location) == "city(1010  Wien, Österreich) latitude(48.208088) longitude(16.358608)"

@pytest.mark.asyncio
async def test_home_set_location(no_ssl_fake_async_home: AsyncHome):
    await no_ssl_fake_async_home.set_location("Berlin, Germany", "52.530644", "13.383068")
    await no_ssl_fake_async_home.get_current_state()
    assert no_ssl_fake_async_home.location.city == "Berlin, Germany"
    assert no_ssl_fake_async_home.location.latitude == "52.530644"
    assert no_ssl_fake_async_home.location.longitude == "13.383068"
    assert str(no_ssl_fake_async_home.location) == "city(Berlin, Germany) latitude(52.530644) longitude(13.383068)"


@pytest.mark.asyncio
async def test_security_zones_activation(no_ssl_fake_async_home: AsyncHome):
    internal, external = no_ssl_fake_async_home.get_security_zones_activation()
    assert internal == False
    assert external == False

    await no_ssl_fake_async_home.set_security_zones_activation(True,True)
    await no_ssl_fake_async_home.get_current_state()

    internal, external = no_ssl_fake_async_home.get_security_zones_activation()
    assert internal == True
    assert external == True