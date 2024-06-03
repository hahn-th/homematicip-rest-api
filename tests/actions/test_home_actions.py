from datetime import datetime

import pytest

from homematicip.action.home_actions import action_set_security_zones_activation, action_set_silent_alarm, \
    action_set_location, action_set_intrusion_alert_through_smoke_detectors, action_activate_absence_with_period, \
    action_activate_absence_permanent, action_activate_absence_with_duration, action_deactivate_absence, \
    action_activate_vacation, action_deactivate_vacation, action_set_zone_activation_delay, action_set_timezone, \
    action_set_powermeter_unit_price, action_start_inclusion, get_security_zones_activation
from homematicip.connection.rest_connection import RestResult, RestConnection
from homematicip.runner import Runner


@pytest.fixture
def runner(mocker, filled_model):
    conn = mocker.Mock(spec=RestConnection)
    conn.async_post.return_value = RestResult(status=200)
    runner = Runner(_rest_connection=conn, model=filled_model)
    return runner


@pytest.mark.asyncio
async def test_action_set_security_zones_activation(runner):
    await action_set_security_zones_activation(runner.rest_connection, internal=True, external=True)
    runner.rest_connection.async_post.assert_called_once_with("home/security/setZonesActivation",
                                                              {"zonesActivation": {"EXTERNAL": True, "INTERNAL": True}})


def test_get_security_zones_activation(filled_model):
    internal, external = get_security_zones_activation(filled_model)
    assert internal is False
    assert external is False

    filled_model.groups["00000000-0000-0000-0000-000000000005"].active = True  # External
    internal, external = get_security_zones_activation(filled_model)
    assert internal is False
    assert external is True

    filled_model.groups["00000000-0000-0000-0000-000000000016"].active = True  # Internal
    internal, external = get_security_zones_activation(filled_model)
    assert internal is True
    assert external is True


@pytest.mark.asyncio
async def test_action_set_silent_alarm(runner):
    await action_set_silent_alarm(runner.rest_connection, internal=True, external=True)
    runner.rest_connection.async_post.assert_called_once_with("home/security/setZonesSilentAlarm", {
        "zonesSilentAlarm": {"EXTERNAL": True, "INTERNAL": True}})


@pytest.mark.asyncio
async def test_action_set_location(runner):
    await action_set_location(runner.rest_connection, "city", 1.0, 2.0)
    runner.rest_connection.async_post.assert_called_once_with("home/setLocation",
                                                              {"city": "city", "latitude": 1.0, "longitude": 2.0})


@pytest.mark.asyncio
async def test_action_set_intrusion_alert_through_smoke_detectors(runner):
    await action_set_intrusion_alert_through_smoke_detectors(runner.rest_connection, activate=True)
    runner.rest_connection.async_post.assert_called_once_with("home/security/setIntrusionAlertThroughSmokeDetectors",
                                                              {"intrusionAlertThroughSmokeDetectors": True})


@pytest.mark.asyncio
async def test_action_activate_absence_with_period(runner):
    await action_activate_absence_with_period(runner.rest_connection, datetime(2020, 1, 1, 0, 0))
    runner.rest_connection.async_post.assert_called_once_with("home/heating/activateAbsenceWithPeriod",
                                                              {"endTime": "2020_01_01 00:00"})


@pytest.mark.asyncio
async def test_action_activate_absence_permanent(runner):
    await action_activate_absence_permanent(runner.rest_connection)
    runner.rest_connection.async_post.assert_called_once_with("home/heating/activateAbsencePermanent")


@pytest.mark.asyncio
async def test_action_activate_absence_with_duration(runner):
    await action_activate_absence_with_duration(runner.rest_connection, 30)
    runner.rest_connection.async_post.assert_called_once_with("home/heating/activateAbsenceWithDuration",
                                                              {"duration": 30})


@pytest.mark.asyncio
async def test_action_deactivate_absence(runner):
    await action_deactivate_absence(runner.rest_connection)
    runner.rest_connection.async_post.assert_called_once_with("home/heating/deactivateAbsence")


@pytest.mark.asyncio
async def test_action_activate_vacation(runner):
    await action_activate_vacation(runner.rest_connection, datetime(2020, 1, 1, 0, 0), 12.0)
    runner.rest_connection.async_post.assert_called_once_with("home/heating/activateVacation",
                                                              {"endTime": "2020_01_01 00:00", "temperature": 12.0})


@pytest.mark.asyncio
async def test_action_deactivate_vacation(runner):
    await action_deactivate_vacation(runner.rest_connection)
    runner.rest_connection.async_post.assert_called_once_with("home/heating/deactivateVacation")


@pytest.mark.asyncio
async def test_action_set_zone_activation_delay(runner):
    await action_set_zone_activation_delay(runner.rest_connection, 10)
    runner.rest_connection.async_post.assert_called_once_with("home/security/setZoneActivationDelay",
                                                              {"zoneActivationDelay": 10})


@pytest.mark.asyncio
async def test_action_set_timezone(runner):
    await action_set_timezone(runner.rest_connection, "Europe/Berlin")
    runner.rest_connection.async_post.assert_called_once_with("home/setTimezone", {"timezoneId": "Europe/Berlin"})


@pytest.mark.asyncio
async def test_action_set_powermeter_unit_price(runner):
    await action_set_powermeter_unit_price(runner.rest_connection, 0.25)
    runner.rest_connection.async_post.assert_called_once_with("home/setPowerMeterUnitPrice",
                                                              {"powerMeterUnitPrice": 0.25})


@pytest.mark.asyncio
async def test_action_start_inclusion(runner):
    device_id = "1234"
    await action_start_inclusion(runner.rest_connection, device_id)
    runner.rest_connection.async_post.assert_called_once_with("home/startInclusionModeForDevice",
                                                              {"deviceId": device_id})
