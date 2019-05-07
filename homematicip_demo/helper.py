import contextlib
import json
import warnings
from functools import partial, partialmethod
from pathlib import Path

import requests


def get_full_path(name):
    """Returns full path of incoming relative path.
    Relative path is relative to the script location.
    """
    pth = Path(__file__).parent.joinpath(name)
    return pth


def fake_home_download_configuration():
    _full = get_full_path("json_data/home.json")
    with open(_full, encoding="UTF-8") as f:
        return json.load(f)


@contextlib.contextmanager
def no_ssl_verification():
    old_request = requests.Session.request
    requests.Session.request = partialmethod(old_request, verify=False)

    warnings.filterwarnings("ignore", "Unverified HTTPS request")
    yield
    warnings.resetwarnings()

    requests.Session.request = old_request
