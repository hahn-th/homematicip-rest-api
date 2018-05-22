import pytest
import requests
import json

from conftest import no_ssl_verification

def test_getHost(fake_cloud):
    with no_ssl_verification():
        response = requests.post("{}/getHost".format(fake_cloud.url))
        js = json.loads(response.text)
        assert js["urlREST"] == fake_cloud.url
        assert js["apiVersion"] == "12"