import json

import pytest
import requests
from homematicip_demo.fake_cloud_server import AsyncFakeCloudServer

from conftest import no_ssl_verification


def test_getHost(fake_cloud):
    with no_ssl_verification():
        response = requests.post(f"{fake_cloud.url}/getHost")
        js = json.loads(response.text)
        assert js["urlREST"] == fake_cloud.url
        assert js["apiVersion"] == "12"


@pytest.mark.asyncio
async def test_calling_internal_func():
    with pytest.raises(NameError):
        await AsyncFakeCloudServer().call_method("__init__")


@pytest.mark.asyncio
async def test_calling_invalid_func():
    with pytest.raises(NameError):
        await AsyncFakeCloudServer().call_method("get_this_function_does_not_exist")


def test_invlid_authorization(fake_cloud):
    with no_ssl_verification():
        response = requests.post(f"{fake_cloud.url}/hmip/home/getCurrentState")
        js = json.loads(response.text)
        assert js["errorCode"] == "INVALID_AUTHORIZATION"
        assert response.status_code == 403


def test_invalid_url(fake_cloud):
    with no_ssl_verification():
        response = requests.post(f"{fake_cloud.url}/hmip/invalid/path")
        js = json.loads(response.text)
        assert js["errorCode"] == "Can't find method post_hmip_invalid_path"
        assert response.status_code == 404
