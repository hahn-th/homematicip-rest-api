from unittest.mock import MagicMock, Mock

import pytest

from homematicip.home import Home
from homematicip.base.base_connection import BaseConnection
from homematicip.group import *
import json
from datetime import datetime, timedelta, timezone

dt = datetime.now(timezone.utc).astimezone()
utc_offset = dt.utcoffset() // timedelta(seconds=1)

def fake_home_download_configuration():
    return json.load(open("tests/json_data/home.json"))


@pytest.fixture
def fake_home():
    home = Home()
    home.download_configuration = fake_home_download_configuration
    home._connection = BaseConnection()
    home.get_current_state()
    return home

def test_meta_group(fake_home):
    g = fake_home.search_group_by_id('00000000-0000-0000-0000-000000000020')
    assert isinstance(g, MetaGroup)
    assert g.label == "Badezimmer"
    assert g.lastStatusUpdate == datetime(2018, 4, 23, 20, 49, 16, 479000) + timedelta(0,utc_offset)
    assert g.lowBat == False
    assert g.metaGroup == None
    assert g.sabotage == None
    assert g.configPending == False
    assert g.unreach == False
    assert g.dutyCycle == False
    for d in g.devices:
        assert d.id in ['3014F7110000000000000025', '3014F7110000000000000016']
    for g_sub in g.groups:
        assert g_sub.id in ['00000000-0000-0000-0000-000000000021', '00000000-0000-0000-0000-000000000021']

    assert str(g) == "META Badezimmer"