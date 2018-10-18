from datetime import datetime, timedelta, timezone

from homematicip.aio.group import AsyncGroup
from homematicip.aio.home import AsyncHome

dt = datetime.now(timezone.utc).astimezone()
utc_offset = dt.utcoffset() // timedelta(seconds=1)

def test_all_groups_implemented(no_ssl_fake_async_home:AsyncHome):
    for g in no_ssl_fake_async_home.groups:
        assert type(g) != AsyncGroup