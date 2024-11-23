from datetime import timedelta
from unittest.mock import Mock, patch, AsyncMock

import pytest

from conftest import utc_offset
from homematicip.base.channel_event import ChannelEvent
from homematicip.connection_v2.connection_context import ConnectionContext
from homematicip.device import Device, BaseDevice
from homematicip.functionalHomes import *
from homematicip.group import Group
from homematicip.home import Home
from homematicip.rule import *
from homematicip.securityEvent import *
from homematicip_demo.helper import (
    fake_home_download_configuration,
    no_ssl_verification,
)


def test_init():
    context = ConnectionContext(auth_token="auth_token", accesspoint_id="access_point_id")
    with patch('homematicip.connection_v2.connection_context.ConnectionContextBuilder.build_context',
               return_value=context) as mock_create:
        home = Home()
        home.init('access_point_id', 'auth_token')
        assert home._connection_context is context
        assert home._connection is not None


def test_init_with_context(fake_connection_context_with_ssl):
    home = Home()
    home.init_with_context(fake_connection_context_with_ssl)
    assert home._connection_context == fake_connection_context_with_ssl
    assert home._connection is not None


def test_update_event(fake_home: Home):
    fake_handler = Mock()
    fake_home.on_update(fake_handler.method)
    fake_home.fire_update_event()
    fake_handler.method.assert_called()
    fake_home.remove_callback(fake_handler.method)
    assert fake_handler.method not in fake_home._on_update


def test_channel_event(fake_home: Home):
    fake_handler = Mock()
    fake_home.on_channel_event(fake_handler.method)
    fake_home.fire_channel_event()
    fake_handler.method.assert_called()
    fake_home.remove_channel_event_handler(fake_handler.method)
    assert fake_handler.method not in fake_home._on_channel_event


def test_remove_event(fake_home: Home):
    fake_handler = Mock()
    fake_home.on_remove(fake_handler.method)
    fake_home.fire_remove_event()
    fake_handler.method.assert_called()
    fake_home.remove_callback(fake_handler.method)
    assert fake_handler.method not in fake_home._on_remove


def test_create_event(fake_home: Home):
    fake_handler = Mock()
    fake_home.on_create(fake_handler.method)
    fake_home.fire_create_event()
    fake_handler.method.assert_called()
    fake_home.remove_callback(fake_handler.method)
    assert fake_handler.method not in fake_home._on_create


def test_home_base(fake_home: Home):
    assert fake_home.connected is True
    assert fake_home.currentAPVersion == "1.2.4"
    assert (
            fake_home.deviceUpdateStrategy == DeviceUpdateStrategy.AUTOMATICALLY_IF_POSSIBLE
    )
    assert fake_home.dutyCycle == 8.0
    assert fake_home.pinAssigned is False
    assert fake_home.powerMeterCurrency == "EUR"
    assert fake_home.powerMeterUnitPrice == 0.0
    assert fake_home.timeZoneId == "Europe/Vienna"
    assert fake_home.updateState == HomeUpdateState.UP_TO_DATE
    assert fake_home.apExchangeState == ApExchangeState.NONE

    assert fake_home._rawJSONData == fake_home_download_configuration()["home"]


def test_home_location(fake_home: Home):
    assert fake_home.location.city == "1010  Wien, Österreich"
    assert fake_home.location.latitude == "48.208088"
    assert fake_home.location.longitude == "16.358608"
    assert (
            fake_home.location._rawJSONData
            == fake_home_download_configuration()["home"]["location"]
    )
    assert (
            str(fake_home.location)
            == "city(1010  Wien, Österreich) latitude(48.208088) longitude(16.358608)"
    )


def test_home_download_configuration(fake_home: Home):
    configuration = fake_home.download_configuration()

    assert isinstance(configuration, dict)


@pytest.mark.asyncio
async def test_home_download_configuration_without_context():
    home = Home()

    assert home._connection_context is None
    with pytest.raises(Exception):
        await home.download_configuration_async()


@pytest.mark.asyncio
async def test_home_download_configuration_result_failed(fake_home: Home):
    mock_response = AsyncMock()
    mock_response.success = False

    with patch.object(fake_home, '_rest_call_async', return_value=mock_response):
        with pytest.raises(Exception):
            await fake_home.download_configuration_async()


def test_home_update_home(fake_home: Home):
    configuration = fake_home.download_configuration()

    fake_home.update_home(configuration)


def test_home_set_location(fake_home: Home):
    with no_ssl_verification():
        fake_home.set_location("Berlin, Germany", "52.530644", "13.383068")
        fake_home.get_current_state()
        assert fake_home.location.city == "Berlin, Germany"
        assert fake_home.location.latitude == "52.530644"
        assert fake_home.location.longitude == "13.383068"
        assert (
                str(fake_home.location)
                == "city(Berlin, Germany) latitude(52.530644) longitude(13.383068)"
        )


def test_home_weather(fake_home: Home):
    assert fake_home.weather.humidity == 54
    assert fake_home.weather.maxTemperature == 16.6
    assert fake_home.weather.minTemperature == 16.6
    assert fake_home.weather.temperature == 16.6
    assert fake_home.weather.weatherCondition == WeatherCondition.LIGHT_CLOUDY
    assert fake_home.weather.weatherDayTime == WeatherDayTime.NIGHT
    assert fake_home.weather.windDirection == 294
    assert fake_home.weather.windSpeed == 8.568
    assert (
            fake_home.weather._rawJSONData
            == fake_home_download_configuration()["home"]["weather"]
    )
    assert (
            str(fake_home.weather)
            == "temperature(16.6) weatherCondition(LIGHT_CLOUDY) weatherDayTime(NIGHT) minTemperature(16.6) maxTemperature(16.6) humidity(54) vaporAmount(5.465858858389302) windSpeed(8.568) windDirection(294)"
    )


def test_clients(fake_home: Home):
    client = fake_home.search_client_by_id("00000000-0000-0000-0000-000000000000")
    assert client.label == "TEST-Client"
    assert client.homeId == "00000000-0000-0000-0000-000000000001"
    assert client.id == "00000000-0000-0000-0000-000000000000"
    assert client.clientType == ClientType.APP

    assert (
            client._rawJSONData
            == fake_home_download_configuration()["clients"][
                "00000000-0000-0000-0000-000000000000"
            ]
    )
    assert str(client) == "label(TEST-Client)"


def test_rules(fake_home: Home):
    with no_ssl_verification():
        rule = fake_home.search_rule_by_id("00000000-0000-0000-0000-000000000065")
        assert rule.active is True
        assert rule.label == "Alarmanlage"
        assert isinstance(rule, SimpleRule)
        assert rule.ruleErrorCategories == []
        assert rule.errorRuleTriggerItems == []
        assert rule.errorRuleConditionItems == []
        assert rule.errorRuleActionItems == []

        assert str(rule) == "SIMPLE Alarmanlage active(True)"

        # disable test
        rule.disable()
        rule.set_label("DISABLED_RULE")
        fake_home.get_current_state()
        rule = fake_home.search_rule_by_id("00000000-0000-0000-0000-000000000065")
        assert rule.active is False
        assert rule.label == "DISABLED_RULE"

        # enable test
        rule.enable()
        rule.set_label("ENABLED_RULE")
        fake_home.get_current_state()
        rule = fake_home.search_rule_by_id("00000000-0000-0000-0000-000000000065")
        assert rule.active is True
        assert rule.label == "ENABLED_RULE"

        rule.id = "INVALID_ID"
        result = rule.disable()
        assert not result.success
        result = rule.set_label("NEW LABEL")
        assert not result.success


def test_security_zones_activation(fake_home: Home):
    with no_ssl_verification():
        internal, external = fake_home.get_security_zones_activation()
        assert internal is False
        assert external is False

        fake_home.set_security_zones_activation(True, True)
        fake_home.get_current_state()

        internal, external = fake_home.get_security_zones_activation()
        assert internal is True
        assert external is True


def test_set_pin(fake_home: Home):
    with no_ssl_verification():
        def get_pin(fake_home_inner):
            result = fake_home_inner._rest_call("home/getPin")
            return result.json["pin"]

        assert get_pin(fake_home) is None

        fake_home.set_pin("1234")
        assert get_pin(fake_home) == "1234"

        fake_home.set_pin("5555")

        # ignore errors. just check if the old pin is still active
        assert get_pin(fake_home) == "1234"

        fake_home.set_pin("5555", "1234")
        assert get_pin(fake_home) == "5555"

        fake_home.set_pin(None, "5555")
        assert get_pin(fake_home) is None


def test_set_timezone(fake_home: Home):
    with no_ssl_verification():
        assert fake_home.timeZoneId == "Europe/Vienna"
        fake_home.set_timezone("Europe/Berlin")
        fake_home.get_current_state()
        assert fake_home.timeZoneId == "Europe/Berlin"

        fake_home.set_timezone("Europe/Vienna")
        fake_home.get_current_state()
        assert fake_home.timeZoneId == "Europe/Vienna"


def test_set_powermeter_unit_price(fake_home: Home):
    with no_ssl_verification():
        fake_home.set_powermeter_unit_price(12.0)
        fake_home.get_current_state()
        assert fake_home.powerMeterUnitPrice == 12.0
        fake_home.set_powermeter_unit_price(8.5)
        fake_home.get_current_state()
        assert fake_home.powerMeterUnitPrice == 8.5


def test_indoor_climate_home(fake_home: Home):
    with no_ssl_verification():
        for fh in fake_home.functionalHomes:
            if not isinstance(fh, IndoorClimateHome):
                continue
            assert fh.active is True
            assert fh.absenceType == AbsenceType.NOT_ABSENT
            assert fh.coolingEnabled is False
            assert fh.ecoDuration == EcoDuration.PERMANENT
            assert fh.ecoTemperature == 17.0
            assert fh.optimumStartStopEnabled is False

            minutes = 20
            fake_home.activate_absence_with_duration(minutes)
            absence_end = datetime.now() + timedelta(minutes=minutes)
            absence_end = absence_end.replace(second=0, microsecond=0)

            fake_home.get_current_state()

            assert fh.absenceType == AbsenceType.PERIOD
            assert fh.absenceEndTime == absence_end

            absence_end = datetime.strptime("2100_01_01 22:22", "%Y_%m_%d %H:%M")

            fake_home.activate_absence_with_period(absence_end)

            fake_home.get_current_state()

            assert fh.absenceType == AbsenceType.PERIOD
            assert fh.absenceEndTime == absence_end

            fake_home.activate_absence_permanent()

            fake_home.get_current_state()

            assert fh.absenceType == AbsenceType.PERMANENT
            assert fh.absenceEndTime == datetime.strptime(
                "2100_12_31 23:59", "%Y_%m_%d %H:%M"
            )
            assert fh.ecoDuration == EcoDuration.PERMANENT

            fake_home.deactivate_absence()

            fake_home.get_current_state()
            assert fh.absenceType == AbsenceType.NOT_ABSENT
            assert fh.absenceEndTime is None


def test_get_functionalHome(fake_home: Home):
    functionalHome = fake_home.get_functionalHome(SecurityAndAlarmHome)
    assert isinstance(functionalHome, SecurityAndAlarmHome)

    functionalHome = fake_home.get_functionalHome(IndoorClimateHome)
    assert isinstance(functionalHome, IndoorClimateHome)

    functionalHome = fake_home.get_functionalHome(WeatherAndEnvironmentHome)
    assert isinstance(functionalHome, WeatherAndEnvironmentHome)

    functionalHome = fake_home.get_functionalHome(AccessControlHome)
    assert isinstance(functionalHome, AccessControlHome)

    functionalHome = fake_home.get_functionalHome(Home)
    assert functionalHome is None


def test_security_setIntrusionAlertThroughSmokeDetectors(fake_home: Home):
    with no_ssl_verification():
        securityAlarmHome = fake_home.get_functionalHome(SecurityAndAlarmHome)
        assert securityAlarmHome.intrusionAlertThroughSmokeDetectors is False

        fake_home.set_intrusion_alert_through_smoke_detectors(True)
        fake_home.get_current_state()
        securityAlarmHome = fake_home.get_functionalHome(SecurityAndAlarmHome)
        assert securityAlarmHome.intrusionAlertThroughSmokeDetectors is True

        fake_home.set_intrusion_alert_through_smoke_detectors(False)
        fake_home.get_current_state()
        securityAlarmHome = fake_home.get_functionalHome(SecurityAndAlarmHome)
        assert securityAlarmHome.intrusionAlertThroughSmokeDetectors is False


def test_heating_vacation(fake_home: Home):
    with no_ssl_verification():
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow = tomorrow.replace(second=0, microsecond=0)

        fake_home.activate_vacation(tomorrow, 12)

        fake_home.get_current_state()
        heatingHome = fake_home.get_functionalHome(IndoorClimateHome)
        assert heatingHome.absenceEndTime == tomorrow
        assert heatingHome.absenceType == AbsenceType.VACATION

        fake_home.deactivate_vacation()

        fake_home.get_current_state()
        heatingHome = fake_home.get_functionalHome(IndoorClimateHome)
        assert heatingHome.absenceEndTime is None
        assert heatingHome.absenceType == AbsenceType.NOT_ABSENT


def test_security_setZoneActivationDelay(fake_home: Home):
    with no_ssl_verification():
        securityAlarmHome = fake_home.get_functionalHome(SecurityAndAlarmHome)
        assert securityAlarmHome.zoneActivationDelay == 0.0

        fake_home.set_zone_activation_delay(5.0)
        fake_home.get_current_state()
        securityAlarmHome = fake_home.get_functionalHome(SecurityAndAlarmHome)
        assert securityAlarmHome.zoneActivationDelay == 5.0

        fake_home.set_zone_activation_delay(0.0)
        fake_home.get_current_state()
        securityAlarmHome = fake_home.get_functionalHome(SecurityAndAlarmHome)
        assert securityAlarmHome.zoneActivationDelay == 0.0


def test_home_getSecurityJournal(fake_home: Home):
    with no_ssl_verification():
        journal = fake_home.get_security_journal()
        # todo make more advanced tests
        assert isinstance(journal[0], ActivationChangedEvent)
        assert isinstance(journal[1], ActivationChangedEvent)
        assert isinstance(journal[2], AccessPointDisconnectedEvent)
        assert isinstance(journal[3], AccessPointConnectedEvent)
        assert isinstance(journal[4], SensorEvent)
        assert isinstance(journal[5], SabotageEvent)
        assert isinstance(journal[6], MoistureDetectionEvent)
        assert isinstance(journal[7], SecurityEvent)


def test_home_unknown_types(fake_home: Home):
    with no_ssl_verification():
        fake_home._rest_call("fake/loadConfig", {"file": "unknown_types.json"})
        fake_home.get_current_state(clear_config=True)
        group = fake_home.groups[0]
        assert isinstance(group, Group)
        assert group.groupType == "DUMMY_GROUP"

        device = fake_home.devices[0]
        assert isinstance(device, BaseDevice)
        assert device.deviceType == "DUMMY_DEVICE"

        func_home = fake_home.functionalHomes[0]
        assert isinstance(func_home, FunctionalHome)
        assert func_home.solution == "DUMMY_FUNCTIONAL_HOME"


def test_home_getOAuthOTK(fake_home: Home):
    with no_ssl_verification():
        token = fake_home.get_OAuth_OTK()
        assert token.authToken == "C001ED"
        assert token.expirationTimestamp == datetime(
            2018, 12, 23, 11, 38, 21, 680000
        ) + timedelta(0, utc_offset)


def test_search_channel(fake_home: Home):
    with no_ssl_verification():
        ch = fake_home.search_channel("3014F71100000000000WWRC6", 10)
        assert ch.index == 10
        assert ch.device.id == "3014F71100000000000WWRC6"


def test_get_devices_fails(fake_home: Home):
    config = fake_home.download_configuration()

    with patch.object(fake_home, 'search_device_by_id', side_effect=Exception("Device not found")):
        result = fake_home._get_devices(config)
        assert result is None


def test_search_channel_not_found(fake_home: Home):
    ch = fake_home.search_channel("3014F71100000000000WWRC6", 100)
    assert ch is None


def test_set_cooling(fake_home):
    result = fake_home.set_cooling(True)
    assert result.success


def test_get_security_journal_with_error(fake_home: Home):
    with patch.object(fake_home, '_rest_call_async', return_value=AsyncMock(success=False)):
        result = fake_home.get_security_journal()
        assert result is None


def test_set_zones_device_assignment(fake_home: Home):
    d = Device(None)
    d.id = "device1"
    internal = external = [d]
    with patch.object(fake_home, '_rest_call_async', return_value=AsyncMock(success=True)):
        result = fake_home.set_zones_device_assignment(internal, external)
        assert result.success


@pytest.mark.asyncio
async def test_on_message_group_changed(fake_home):
    # preparing event data for group changed
    group = fake_home.groups[0]
    payload = {
        "events":
            {
                "0":
                    {
                        "pushEventType": "GROUP_CHANGED",
                        "group": group._rawJSONData,
                    }
            }
    }
    fake_handler = Mock()
    group.on_update(fake_handler)
    await fake_home._ws_on_message(json.dumps(payload))

    fake_handler.assert_called()


@pytest.mark.asyncio
async def test_on_message_group_changed_add(fake_home):
    # preparing event data for group changed
    group = fake_home.groups[0]
    group.id = "0815"
    payload = {
        "events":
            {
                "0":
                    {
                        "pushEventType": "GROUP_CHANGED",
                        "group": group._rawJSONData,
                    }
            }
    }
    group_before = len(fake_home.groups)
    await fake_home._ws_on_message(json.dumps(payload))

    assert len(fake_home.groups) == group_before + 1


@pytest.mark.asyncio
async def test_on_message_group_added(fake_home):
    # preparing event data for group changed
    group = fake_home.groups[0]
    group.id = "0815"
    payload = {
        "events":
            {
                "0":
                    {
                        "pushEventType": "GROUP_ADDED",
                        "group": group._rawJSONData,
                    }
            }
    }
    group_before = len(fake_home.groups)
    await fake_home._ws_on_message(json.dumps(payload))

    assert len(fake_home.groups) == group_before + 1


@pytest.mark.asyncio
async def test_on_message_group_removed(fake_home):
    # preparing event data for group changed
    group = fake_home.groups[0]
    payload = {
        "events":
            {
                "0":
                    {
                        "pushEventType": "GROUP_REMOVED",
                        "id": group.id,
                    }
            }
    }
    group_before = len(fake_home.groups)
    await fake_home._ws_on_message(json.dumps(payload))

    assert len(fake_home.groups) == group_before - 1


@pytest.mark.asyncio
async def test_on_message_device_changed(fake_home):
    # preparing event data for device changed
    device = fake_home.devices[0]
    payload = {
        "events":
            {
                "0":
                    {
                        "pushEventType": "DEVICE_CHANGED",
                        "device": device._rawJSONData,
                    }
            }
    }
    fake_handler = Mock()
    device.on_update(fake_handler)
    await fake_home._ws_on_message(json.dumps(payload))

    fake_handler.assert_called()


@pytest.mark.asyncio
async def test_on_message_device_changed_add(fake_home):
    # preparing event data for device changed
    device = fake_home.devices[0]
    device.id = "0815"
    payload = {
        "events":
            {
                "0":
                    {
                        "pushEventType": "DEVICE_CHANGED",
                        "device": device._rawJSONData,
                    }
            }
    }
    device_before = len(fake_home.devices)
    await fake_home._ws_on_message(json.dumps(payload))

    assert len(fake_home.devices) == device_before + 1


@pytest.mark.asyncio
async def test_on_message_device_added(fake_home):
    # preparing event data for device changed
    device = fake_home.devices[0]
    device.id = "0815"
    payload = {
        "events":
            {
                "0":
                    {
                        "pushEventType": "DEVICE_ADDED",
                        "device": device._rawJSONData,
                    }
            }
    }
    device_before = len(fake_home.devices)
    await fake_home._ws_on_message(json.dumps(payload))

    assert len(fake_home.devices) == device_before + 1


@pytest.mark.asyncio
async def test_on_message_device_removed(fake_home):
    # preparing event data for group changed
    device = fake_home.devices[0]
    payload = {
        "events":
            {
                "0":
                    {
                        "pushEventType": "DEVICE_REMOVED",
                        "id": device.id,
                    }
            }
    }
    devices_before = len(fake_home.devices)
    await fake_home._ws_on_message(json.dumps(payload))

    assert len(fake_home.devices) == devices_before - 1


@pytest.mark.asyncio
async def test_on_message_client_added(fake_home):
    # preparing event data for group changed
    client = fake_home.clients[0]
    client.id = "0815"
    payload = {
        "events":
            {
                "0":
                    {
                        "pushEventType": "CLIENT_ADDED",
                        "client": client._rawJSONData,
                    }
            }
    }
    group_before = len(fake_home.clients)
    await fake_home._ws_on_message(json.dumps(payload))

    assert len(fake_home.clients) == group_before + 1


@pytest.mark.asyncio
async def test_on_message_client_changed(fake_home):
    client = fake_home.clients[0]
    raw_data = client._rawJSONData
    raw_data["label"] = "sample"
    payload = {
        "events":
            {
                "0":
                    {
                        "pushEventType": "CLIENT_CHANGED",
                        "client": raw_data,
                    }
            }
    }
    fake_handler = Mock()
    client.on_update(fake_handler)
    await fake_home._ws_on_message(json.dumps(payload))

    assert fake_handler.called


@pytest.mark.asyncio
async def test_on_message_client_removed(fake_home):
    # preparing event data for group changed
    client = fake_home.clients[0]
    payload = {
        "events":
            {
                "0":
                    {
                        "pushEventType": "CLIENT_REMOVED",
                        "id": client.id,
                    }
            }
    }
    fake_handler = Mock()
    client.on_remove(fake_handler)
    clients_before = len(fake_home.clients)
    await fake_home._ws_on_message(json.dumps(payload))

    assert len(fake_home.clients) == clients_before - 1
    assert fake_handler.called


@pytest.mark.asyncio
async def test_on_message_home_changed(fake_home):
    raw_data = fake_home._rawJSONData
    raw_data["label"] = "sample"
    payload = {
        "events":
            {
                "0":
                    {
                        "pushEventType": "HOME_CHANGED",
                        "home": raw_data,
                    }
            }
    }
    fake_handler = Mock()
    fake_home.on_update(fake_handler)
    await fake_home._ws_on_message(json.dumps(payload))

    assert fake_handler.called


@pytest.mark.asyncio
async def test_on_message_channel_event(fake_home):
    # preparing event data for channel event
    payload = {
        "events":
            {
                "0":
                    {
                        "pushEventType": "DEVICE_CHANNEL_EVENT",
                        "deviceId": "xxx",
                        "channelIndex": 1,
                        "channelEventType": "DOOR_BELL_SENSOR_EVENT",
                    }
            }
    }
    fake_handler = Mock()
    fake_home.on_channel_event(fake_handler)
    await fake_home._ws_on_message(json.dumps(payload))

    fake_handler.assert_called_once_with(ChannelEvent("DEVICE_CHANNEL_EVENT", "xxx", 1, "DOOR_BELL_SENSOR_EVENT"))


@pytest.mark.asyncio
async def test_enable_events(fake_home):
    mock_websocket_handler = Mock()
    mock_websocket_handler.listen = AsyncMock()
    mock_additional_handler = AsyncMock()

    with patch('homematicip.async_home.WebSocketHandler', return_value=mock_websocket_handler):
        await fake_home.enable_events(mock_additional_handler)

        assert fake_home._websocket_client is mock_websocket_handler
        assert mock_websocket_handler.listen.called
        assert len(mock_websocket_handler.add_on_message_handler.mock_calls) == 2


@pytest.mark.asyncio
async def test_enable_events_active(fake_home):
    fake_home._websocket_client = Mock()
    await fake_home.enable_events()

    assert not fake_home._websocket_client.listen.called


@pytest.mark.asyncio
async def test_disable_events(fake_home):
    fake_client = Mock()
    fake_home._websocket_client = fake_client
    fake_home.disable_events()

    assert fake_home._websocket_client is None
    assert fake_client.stop_listening.called
