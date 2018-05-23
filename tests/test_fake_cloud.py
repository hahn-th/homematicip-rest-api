import pytest
import requests
import json

from conftest import no_ssl_verification
from fake_cloud_server import FakeCloudServer


def test_getHost(fake_cloud):
    with no_ssl_verification():
        response = requests.post("{}/getHost".format(fake_cloud.url))
        js = json.loads(response.text)
        assert js["urlREST"] == fake_cloud.url
        assert js["apiVersion"] == "12"

def test_calling_internal_func():
    with pytest.raises(NameError):
        FakeCloudServer().call_method("__init__")

def test_calling_invalid_func():
    with pytest.raises(NameError):
        FakeCloudServer().call_method("get_this_function_does_not_exist")