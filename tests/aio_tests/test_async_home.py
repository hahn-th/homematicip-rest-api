from datetime import datetime, timedelta, timezone

import pytest
from conftest import fake_home_download_configuration, no_ssl_verification, utc_offset

from homematicip.aio.home import AsyncHome
from homematicip.base.enums import *
from homematicip.base.base_connection import HmipWrongHttpStatusError
from homematicip.functionalHomes import *
from homematicip.aio.securityEvent import *


@pytest.mark.asyncio
async def test_async_home_base(no_ssl_fake_async_home: AsyncHome):
    assert no_ssl_fake_async_home.connected == True
    assert no_ssl_fake_async_home.currentAPVersion == "1.2.4"
    assert (
        no_ssl_fake_async_home.deviceUpdateStrategy
        == DeviceUpdateStrategy.AUTOMATICALLY_IF_POSSIBLE
    )
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
    assert (
        no_ssl_fake_async_home.location._rawJSONData
        == fake_home_download_configuration()["home"]["location"]
    )
    assert (
        str(no_ssl_fake_async_home.location)
        == "city(1010  Wien, Österreich) latitude(48.208088) longitude(16.358608)"
    )


@pytest.mark.asyncio
async def test_home_set_location(no_ssl_fake_async_home: AsyncHome):
    await no_ssl_fake_async_home.set_location(
        "Berlin, Germany", "52.530644", "13.383068"
    )
    await no_ssl_fake_async_home.get_current_state()
    assert no_ssl_fake_async_home.location.city == "Berlin, Germany"
    assert no_ssl_fake_async_home.location.latitude == "52.530644"
    assert no_ssl_fake_async_home.location.longitude == "13.383068"
    assert (
        str(no_ssl_fake_async_home.location)
        == "city(Berlin, Germany) latitude(52.530644) longitude(13.383068)"
    )


@pytest.mark.asyncio
async def test_security_zones_activation(no_ssl_fake_async_home: AsyncHome):
    internal, external = no_ssl_fake_async_home.get_security_zones_activation()
    assert internal == False
    assert external == False

    await no_ssl_fake_async_home.set_security_zones_activation(True, True)
    await no_ssl_fake_async_home.get_current_state()

    internal, external = no_ssl_fake_async_home.get_security_zones_activation()
    assert internal == True
    assert external == True


@pytest.mark.asyncio
async def test_set_pin(no_ssl_fake_async_home: AsyncHome):
    assert no_ssl_fake_async_home._fake_cloud.app.pin == None

    await no_ssl_fake_async_home.set_pin(1234)
    assert no_ssl_fake_async_home._fake_cloud.app.pin == 1234

    with pytest.raises(HmipWrongHttpStatusError):
        await no_ssl_fake_async_home.set_pin(
            5555
        )  # ignore errors. just check if the old pin is still active
    assert no_ssl_fake_async_home._fake_cloud.app.pin == 1234

    await no_ssl_fake_async_home.set_pin(5555, 1234)
    assert no_ssl_fake_async_home._fake_cloud.app.pin == 5555

    await no_ssl_fake_async_home.set_pin(None, 5555)
    assert no_ssl_fake_async_home._fake_cloud.app.pin == None


@pytest.mark.asyncio
async def test_indoor_climate_home(no_ssl_fake_async_home: AsyncHome):
    for fh in no_ssl_fake_async_home.functionalHomes:
        if not isinstance(fh, IndoorClimateHome):
            continue
        assert fh.active == True
        assert fh.absenceType == AbsenceType.NOT_ABSENT
        assert fh.coolingEnabled == False
        assert fh.ecoDuration == EcoDuration.PERMANENT
        assert fh.ecoTemperature == 17.0
        assert fh.optimumStartStopEnabled == False

        minutes = 20
        await no_ssl_fake_async_home.activate_absence_with_duration(minutes)
        absence_end = datetime.now() + timedelta(minutes=minutes)
        absence_end = absence_end.replace(second=0, microsecond=0)

        await no_ssl_fake_async_home.get_current_state()

        assert fh.absenceType == AbsenceType.PERIOD
        assert fh.absenceEndTime == absence_end

        absence_end = datetime.strptime("2100_01_01 22:22", "%Y_%m_%d %H:%M")

        await no_ssl_fake_async_home.activate_absence_with_period(absence_end)

        await no_ssl_fake_async_home.get_current_state()

        assert fh.absenceType == AbsenceType.PERIOD
        assert fh.absenceEndTime == absence_end

        await no_ssl_fake_async_home.deactivate_absence()

        await no_ssl_fake_async_home.get_current_state()
        assert fh.absenceType == AbsenceType.NOT_ABSENT
        assert fh.absenceEndTime == None


@pytest.mark.asyncio
async def test_set_powermeter_unit_price(no_ssl_fake_async_home: AsyncHome):

    await no_ssl_fake_async_home.set_powermeter_unit_price(12.0)
    await no_ssl_fake_async_home.get_current_state()
    assert no_ssl_fake_async_home.powerMeterUnitPrice == 12.0

    await no_ssl_fake_async_home.set_powermeter_unit_price(8.5)
    await no_ssl_fake_async_home.get_current_state()
    assert no_ssl_fake_async_home.powerMeterUnitPrice == 8.5


@pytest.mark.asyncio
async def test_set_timezone(no_ssl_fake_async_home: AsyncHome):

    assert no_ssl_fake_async_home.timeZoneId == "Europe/Vienna"
    await no_ssl_fake_async_home.set_timezone("Europe/Berlin")
    await no_ssl_fake_async_home.get_current_state()
    assert no_ssl_fake_async_home.timeZoneId == "Europe/Berlin"

    await no_ssl_fake_async_home.set_timezone("Europe/Vienna")
    await no_ssl_fake_async_home.get_current_state()
    assert no_ssl_fake_async_home.timeZoneId == "Europe/Vienna"


@pytest.mark.asyncio
async def test_heating_vacation(no_ssl_fake_async_home: AsyncHome):
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = tomorrow.replace(second=0, microsecond=0)

    await no_ssl_fake_async_home.activate_vacation(tomorrow, 12)

    await no_ssl_fake_async_home.get_current_state()
    heatingHome = no_ssl_fake_async_home.get_functionalHome(IndoorClimateHome)
    assert heatingHome.absenceEndTime == tomorrow
    assert heatingHome.absenceType == AbsenceType.VACATION

    await no_ssl_fake_async_home.deactivate_vacation()

    await no_ssl_fake_async_home.get_current_state()
    heatingHome = no_ssl_fake_async_home.get_functionalHome(IndoorClimateHome)
    assert heatingHome.absenceEndTime == None
    assert heatingHome.absenceType == AbsenceType.NOT_ABSENT


@pytest.mark.asyncio
async def test_security_setZoneActivationDelay(no_ssl_fake_async_home: AsyncHome):
    securityAlarmHome = no_ssl_fake_async_home.get_functionalHome(SecurityAndAlarmHome)
    assert securityAlarmHome.zoneActivationDelay == 0.0

    await no_ssl_fake_async_home.set_zone_activation_delay(5.0)
    await no_ssl_fake_async_home.get_current_state()
    securityAlarmHome = no_ssl_fake_async_home.get_functionalHome(SecurityAndAlarmHome)
    assert securityAlarmHome.zoneActivationDelay == 5.0

    await no_ssl_fake_async_home.set_zone_activation_delay(0.0)
    await no_ssl_fake_async_home.get_current_state()
    securityAlarmHome = no_ssl_fake_async_home.get_functionalHome(SecurityAndAlarmHome)
    assert securityAlarmHome.zoneActivationDelay == 0.0


@pytest.mark.asyncio
async def test_security_setIntrusionAlertThroughSmokeDetectors(
    no_ssl_fake_async_home: AsyncHome
):
    securityAlarmHome = no_ssl_fake_async_home.get_functionalHome(SecurityAndAlarmHome)
    assert securityAlarmHome.intrusionAlertThroughSmokeDetectors == False

    await no_ssl_fake_async_home.set_intrusion_alert_through_smoke_detectors(True)
    await no_ssl_fake_async_home.get_current_state()
    securityAlarmHome = no_ssl_fake_async_home.get_functionalHome(SecurityAndAlarmHome)
    assert securityAlarmHome.intrusionAlertThroughSmokeDetectors == True

    await no_ssl_fake_async_home.set_intrusion_alert_through_smoke_detectors(False)
    await no_ssl_fake_async_home.get_current_state()
    securityAlarmHome = no_ssl_fake_async_home.get_functionalHome(SecurityAndAlarmHome)
    assert securityAlarmHome.intrusionAlertThroughSmokeDetectors == False


@pytest.mark.asyncio
async def test_home_getSecurityJournal(no_ssl_fake_async_home: AsyncHome):
    journal = await no_ssl_fake_async_home.get_security_journal()
    # todo make more advanced tests
    assert isinstance(journal[0], AsyncActivationChangedEvent)
    assert isinstance(journal[1], AsyncActivationChangedEvent)
    assert isinstance(journal[2], AsyncAccessPointDisconnectedEvent)
    assert isinstance(journal[3], AsyncAccessPointConnectedEvent)
    assert isinstance(journal[4], AsyncSensorEvent)
    assert isinstance(journal[5], AsyncSabotageEvent)
    assert isinstance(journal[6], AsyncMoistureDetectionEvent)
    assert isinstance(journal[7], AsyncSecurityEvent)


@pytest.mark.asyncio
async def test_home_getOAuthOTK(no_ssl_fake_async_home: AsyncHome):
    token = await no_ssl_fake_async_home.get_OAuth_OTK()
    assert token.authToken == "C001ED"
    assert token.expirationTimestamp == datetime(
        2018, 12, 23, 11, 38, 21, 680000
    ) + timedelta(0, utc_offset)

@pytest.mark.asyncio
async def test_clearconfig(no_ssl_fake_async_home: AsyncHome):
    d1 = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000001")
    await no_ssl_fake_async_home.get_current_state(clearConfig=True)
    d2 = no_ssl_fake_async_home.search_device_by_id("3014F7110000000000000001")

    assert d1.id == d2.id
    assert d1 != d2
