import hashlib
import json

import pytest

from conftest import no_ssl_verification
from homematicip.auth import Auth
from homematicip.base.enums import ClientType
from homematicip.home import Home


def test_auth_challenge_no_pin(fake_home: Home):
    with no_ssl_verification():
        auth = Auth(fake_home)
        sgtin = "3014F711A000000BAD0C0DED"
        devicename = "auth_test"
        assert auth.connectionRequest(sgtin, devicename).status_code == 200
        assert auth.isRequestAcknowledged() is False
        assert auth.isRequestAcknowledged() is False

        fake_home._connection._rest_call("auth/simulateBlueButton")

        assert auth.isRequestAcknowledged() is True

        token = auth.requestAuthToken()
        assert token == hashlib.sha512(auth.uuid.encode("utf-8")).hexdigest().upper()

        resultId = auth.confirmAuthToken(token)
        assert resultId == auth.uuid

        fake_home.get_current_state()

        client = fake_home.search_client_by_id(resultId)
        assert client != None
        assert client.label == devicename
        assert client.clientType == ClientType.APP
