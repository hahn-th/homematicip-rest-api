import pytest
import requests
import json
import asyncio
from conftest import no_ssl_verification
from homematicip_demo.fake_cloud_server import FakeCloudServer

@pytest.mark.asyncio
async def test_aio_fake_cloud(aio_fake_cloud):
    while True:
        await asyncio.sleep(1)


def test_getHost(fake_cloud):
    with no_ssl_verification():
        response = requests.post("{}/getHost".format(fake_cloud.url))
        js = json.loads(response.text)
        assert js["urlREST"] == fake_cloud.url
        assert js["apiVersion"] == "12"


@pytest.mark.asyncio
async def test_calling_internal_func():
    with pytest.raises(NameError):
        await FakeCloudServer().call_method("__init__")


@pytest.mark.asyncio
async def test_calling_invalid_func():
    with pytest.raises(NameError):
        await FakeCloudServer().call_method("get_this_function_does_not_exist")


def test_invlid_authorization(fake_cloud):
    with no_ssl_verification():
        response = requests.post("{}/hmip/home/getCurrentState".format(fake_cloud.url))
        js = json.loads(response.text)
        assert js["errorCode"] == "INVALID_AUTHORIZATION"
        assert response.status_code == 403


def test_invalid_url(fake_cloud):
    with no_ssl_verification():
        response = requests.post("{}/hmip/invalid/path".format(fake_cloud.url))
        js = json.loads(response.text)
        assert js["errorCode"] == "Can't find method post_hmip_invalid_path"
        assert response.status_code == 404
