import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from conftest import utc_offset
from homematicip.base.base_connection import BaseConnection
from homematicip.base.enums import *
from homematicip.device import AccelerationSensor, Device
from homematicip.EventHook import EventHook
from homematicip.functionalHomes import *
from homematicip.group import Group, MetaGroup, SecurityZoneGroup
from homematicip.home import Client, Home
from homematicip.rule import *
from homematicip.securityEvent import *
from homematicip_demo.helper import (
    fake_home_download_configuration,
    no_ssl_verification,
)


@pytest.fixture
def home_data():
    path = Path(__file__).parent.parent.joinpath("homematicip_demo/json_data/home.json")
    data = None
    with open(path, encoding="utf-8") as file:
        data = json.load(file)
    return data


def send_event(fake_home: Home, pushEventType: EventType, type: str, data):
    event_data = build_json_payload(pushEventType, type, data)
    with no_ssl_verification():
        fake_home._rest_call("ws/send", json.dumps(event_data))


def build_json_payload(pushEventType: EventType, type: str, data) -> dict:
    if type:
        event_data = {
            "events": {"0": {"pushEventType": str(pushEventType), type: data}}
        }
    else:
        event_data = {"events": {"0": {"pushEventType": str(pushEventType)}}}

    return event_data


def test_websocket_device(fake_home: Home, home_data):
    # preparing event data for device added
    device_base_id = "3014F7110000000000000031"
    device_added = home_data["devices"][device_base_id].copy()
    device_added_id = "NEW_DEVICE"
    device_added["id"] = device_added_id
    for x in device_added["functionalChannels"].values():
        x["deviceId"] = device_added_id

    event_data = build_json_payload(EventType.DEVICE_ADDED, "device", device_added)
    fake_home._ws_on_message(None, message=json.dumps(event_data))

    device_added = home_data["devices"][device_base_id].copy()
    device_added_by_change_id = "NEW_DEVICE_2"
    device_added["id"] = device_added_by_change_id
    for x in device_added["functionalChannels"].values():
        x["deviceId"] = device_added_by_change_id

    event_data = build_json_payload(EventType.DEVICE_CHANGED, "device", device_added)
    fake_home._ws_on_message(None, message=json.dumps(event_data))

    # preparing event data for device changed
    device_changed = home_data["devices"][device_base_id].copy()
    device_changed["label"] = "CHANGED"

    event_data = build_json_payload(EventType.DEVICE_CHANGED, "device", device_changed)
    fake_home._ws_on_message(None, message=json.dumps(event_data))

    # send_event(fake_home, EventType.DEVICE_CHANGED, "device", device_changed)
    # preparing event data for device remove
    device_delete_id = "3014F7110000000000BCBB11"
    assert fake_home.search_device_by_id(device_delete_id) != None

    event_data = build_json_payload(EventType.DEVICE_REMOVED, "id", device_delete_id)
    fake_home._ws_on_message(None, message=json.dumps(event_data))
    # send_event(fake_home, EventType.DEVICE_REMOVED, "id", device_delete_id)

    time.sleep(1)
    d = fake_home.search_device_by_id(device_added_id)
    assert d.label == "Garagentor"
    assert isinstance(d, AccelerationSensor)

    d = fake_home.search_device_by_id(device_added_by_change_id)
    assert d.label == "Garagentor"
    assert isinstance(d, AccelerationSensor)

    d = fake_home.search_device_by_id(device_base_id)
    assert d.label == "CHANGED"
    assert isinstance(d, AccelerationSensor)

    assert fake_home.search_device_by_id(device_delete_id) is None


def test_websocket_group(fake_home: Home, home_data):
    # preparing event data for group added
    group_base_id = "00000000-0000-0000-0000-000000000020"
    group_added = home_data["groups"][group_base_id].copy()
    group_added_id = "NEW_group"
    group_added["id"] = group_added_id
    payload = build_json_payload(EventType.GROUP_ADDED, "group", group_added)
    fake_home._ws_on_message(None, json.dumps(payload))

    group_added = home_data["groups"][group_base_id].copy()
    group_added_by_change_id = "NEW_group_2"
    group_added["id"] = group_added_by_change_id
    payload = build_json_payload(EventType.GROUP_CHANGED, "group", group_added)
    fake_home._ws_on_message(None, json.dumps(payload))

    # preparing event data for group changed
    group_changed_id = "00000000-0000-0000-0000-000000000016"
    group_changed = home_data["groups"][group_changed_id].copy()
    group_changed["label"] = "CHANGED"
    payload = build_json_payload(EventType.GROUP_CHANGED, "group", group_changed)
    fake_home._ws_on_message(None, json.dumps(payload))
    # preparing event data for group remove
    group_delete_id = "00000000-0000-0000-0000-000000000012"
    assert fake_home.search_group_by_id(group_delete_id) != None
    payload = build_json_payload(EventType.GROUP_REMOVED, "id", group_delete_id)
    fake_home._ws_on_message(None, json.dumps(payload))

    time.sleep(1)
    d = fake_home.search_group_by_id(group_added_id)
    assert d.label == "Badezimmer"
    assert isinstance(d, MetaGroup)

    d = fake_home.search_group_by_id(group_added_by_change_id)
    assert d.label == "Badezimmer"
    assert isinstance(d, MetaGroup)

    d = fake_home.search_group_by_id(group_changed_id)
    assert d.label == "CHANGED"
    assert isinstance(d, SecurityZoneGroup)

    assert fake_home.search_group_by_id(group_delete_id) is None


def test_websocket_security_journal_changed(fake_home: Home, home_data):
    payload = build_json_payload(EventType.SECURITY_JOURNAL_CHANGED, None, None)
    fake_home._ws_on_message(None, json.dumps(payload))
    time.sleep(1)


def test_websocket_home_changed(fake_home: Home, home_data):
    new_home = home_data["home"].copy()
    new_home["weather"]["humidity"] = 60

    assert fake_home.weather.humidity == 54

    payload = build_json_payload(EventType.HOME_CHANGED, "home", new_home)
    fake_home._ws_on_message(None, json.dumps(payload))

    time.sleep(1)
    assert fake_home.weather.humidity == 60


def test_websocket_client(fake_home: Home, home_data):
    # preparing event data for client added
    client_base_id = "00000000-0000-0000-0000-000000000000"
    client_added = home_data["clients"][client_base_id].copy()
    client_added_id = "NEW_CLIENT"
    client_added["id"] = client_added_id
    payload = build_json_payload(EventType.CLIENT_ADDED, "client", client_added)
    fake_home._ws_on_message(None, json.dumps(payload))

    # preparing event data for client changed
    client_changed = home_data["clients"][client_base_id].copy()
    client_changed["label"] = "CHANGED"
    payload = build_json_payload(EventType.CLIENT_CHANGED, "client", client_changed)
    fake_home._ws_on_message(None, json.dumps(payload))
    # preparing event data for client remove
    client_delete_id = "AA000000-0000-0000-0000-000000000000"
    c = fake_home.search_client_by_id(client_delete_id)
    assert c != None
    assert c.label == "REMOVE_ME"
    payload = build_json_payload(EventType.CLIENT_REMOVED, "id", client_delete_id)
    fake_home._ws_on_message(None, json.dumps(payload))

    time.sleep(1)
    d = fake_home.search_client_by_id(client_added_id)
    assert d.label == "TEST-Client"
    assert isinstance(d, Client)

    d = fake_home.search_client_by_id(client_base_id)
    assert d.label == "CHANGED"
    assert isinstance(d, Client)

    assert fake_home.search_client_by_id(client_delete_id) is None


ws_error_called = False


@pytest.mark.flaky(reruns=10, reruns_delay=4)
def test_websocket_error(fake_home: Home, home_data):
    global ws_error_called

    def on_error(err):
        global ws_error_called
        ws_error_called = True

    fake_home.onWsError += on_error

    fake_home.enable_events()
    with no_ssl_verification():
        fake_home._connection._restCallRequestCounter = 1
        fake_home._rest_call("ws/sleep", json.dumps({"seconds": 5}))

    assert ws_error_called

    # testing automatic reconnection
    time.sleep(5)  # give the reconnection routine time to reconnect

    client_base_id = "00000000-0000-0000-0000-000000000000"
    client_changed = home_data["clients"][client_base_id].copy()
    client_changed["label"] = "CHANGED"
    send_event(fake_home, EventType.CLIENT_CHANGED, "client", client_changed)
    time.sleep(2)
    d = fake_home.search_client_by_id(client_base_id)
    assert d.label == "CHANGED"
    assert isinstance(d, Client)

    fake_home.disable_events()
