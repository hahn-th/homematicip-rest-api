from unittest.mock import MagicMock

import pytest

from homematicip.home import Home


@pytest.fixture
def fake_home():
    home = Home()
    home.from_json = MagicMock()
    return home


def test__parse_device(fake_home):
    assert False


def test_get_devices(fake_home):
    assert False


def test__get_clients(fake_home):
    assert False


def test__parse_group(fake_home):
    assert False


def test__get_groups(fake_home):
    assert False
