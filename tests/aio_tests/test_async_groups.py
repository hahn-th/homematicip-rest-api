import pytest

from homematicip.aio.home import AsyncHome
from homematicip.EventHook import EventHook
from homematicip.aio.group import AsyncGroup
import json
from datetime import datetime, timedelta, timezone
from conftest import no_ssl_verification


dt = datetime.now(timezone.utc).astimezone()
utc_offset = dt.utcoffset() // timedelta(seconds=1)

def test_all_groups_implemented(fake_async_home:AsyncHome):
    for g in fake_async_home.groups:
        assert type(g) != AsyncGroup