import pytest
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import time

from homematicip.home import Home
from homematicip.base.base_connection import BaseConnection
from homematicip.rule import *
from homematicip.EventHook import EventHook
from homematicip.base.enums import *
from homematicip.functionalHomes import *
from homematicip.securityEvent import *
from homematicip.group import Group,MetaGroup
from homematicip.device import Device, AccelerationSensor


from homematicip_demo.helper import (
    fake_home_download_configuration,
    no_ssl_verification,
)
from conftest import utc_offset

def send_event(fake_home: Home, pushEventType: EventType, type: str, data):
    event_data = {"events": {"0": {"pushEventType": str(pushEventType), type: data}}}
    with no_ssl_verification():
        fake_home._restCall("ws/send", json.dumps(event_data))


def test_websocket_device(fake_home: Home):
    path = Path(__file__).parent.parent.joinpath("homematicip_demo/json_data/home.json")
    home_data = None
    with open(path, encoding="utf-8") as file:
        home_data = json.load(file, encoding="UTF-8")

    fake_home.enable_events()

    # preparing event data for device added
    device_base_id = "3014F7110000000000000031"
    device_added = home_data["devices"][device_base_id].copy()
    device_added_id = "NEW_DEVICE"
    device_added["id"] = device_added_id
    for x in device_added["functionalChannels"].values():
        x["deviceId"] = device_added_id
    send_event(fake_home, EventType.DEVICE_ADDED, "device", device_added)

    device_added = home_data["devices"][device_base_id].copy()
    device_added_by_change_id = "NEW_DEVICE_2"
    device_added["id"] = device_added_by_change_id
    for x in device_added["functionalChannels"].values():
        x["deviceId"] = device_added_by_change_id
    send_event(fake_home, EventType.DEVICE_CHANGED, "device", device_added)

    # preparing event data for device changed
    device_changed = home_data["devices"][device_base_id].copy()
    device_changed["label"] = "CHANGED"
    send_event(fake_home, EventType.DEVICE_CHANGED, "device", device_changed)
    #preparing event data for device remove
    device_delete_id = "3014F7110000000000BCBB11"
    assert fake_home.search_device_by_id(device_delete_id) != None  
    send_event(fake_home, EventType.DEVICE_REMOVED, "id", device_delete_id)

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

    assert fake_home.search_device_by_id(device_delete_id) == None  

    fake_home.disable_events()

def test_websocket_group(fake_home: Home):
    path = Path(__file__).parent.parent.joinpath("homematicip_demo/json_data/home.json")
    home_data = None
    with open(path, encoding="utf-8") as file:
        home_data = json.load(file, encoding="UTF-8")

    fake_home.enable_events()

    # preparing event data for group added
    group_base_id = "00000000-0000-0000-0000-000000000020"
    group_added = home_data["groups"][group_base_id].copy()
    group_added_id = "NEW_group"
    group_added["id"] = group_added_id
    send_event(fake_home, EventType.GROUP_ADDED, "group", group_added)

    group_added = home_data["groups"][group_base_id].copy()
    group_added_by_change_id = "NEW_group_2"
    group_added["id"] = group_added_by_change_id
    send_event(fake_home, EventType.GROUP_CHANGED, "group", group_added)

    # preparing event data for group changed
    group_changed = home_data["groups"][group_base_id].copy()
    group_changed["label"] = "CHANGED"
    send_event(fake_home, EventType.GROUP_CHANGED, "group", group_changed)
    #preparing event data for group remove
    group_delete_id = "00000000-0000-0000-0000-000000000012"
    assert fake_home.search_group_by_id(group_delete_id) != None  
    send_event(fake_home, EventType.GROUP_REMOVED, "id", group_delete_id)

    time.sleep(1)
    d = fake_home.search_group_by_id(group_added_id)
    assert d.label == "Badezimmer"
    assert isinstance(d, MetaGroup)

    d = fake_home.search_group_by_id(group_added_by_change_id)
    assert d.label == "Badezimmer"
    assert isinstance(d, MetaGroup)

    d = fake_home.search_group_by_id(group_base_id)
    assert d.label == "CHANGED"
    assert isinstance(d, MetaGroup)

    assert fake_home.search_group_by_id(group_delete_id) == None  

    fake_home.disable_events()
