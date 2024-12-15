# coding=utf-8
import json
import uuid

import requests

from homematicip.home import Home


class Auth(object):
    def __init__(self, home: Home):
        self.uuid = str(uuid.uuid4())
        self.headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "VERSION": "12",
            "CLIENTAUTH": home._connection.clientauth_token,
            "ACCESSPOINT-ID": home._connection.accesspoint_id,
        }
        self.url_rest = home._connection.urlREST
        self.accesspoint_id = home._connection.accesspoint_id
        self.pin = None

    def connectionRequest(
            self, access_point, devicename="homematicip-python"
    ) -> requests.Response:
        data = {"deviceId": self.uuid, "deviceName": devicename, "sgtin": access_point}
        headers = self.headers
        if self.pin != None:
            headers["PIN"] = self.pin
        response = requests.post(
            "{}/hmip/auth/connectionRequest".format(self.url_rest),
            json=data,
            headers=headers,
        )
        return response

    def isRequestAcknowledged(self):
        data = {"deviceId": self.uuid, "accessPointId": self.accesspoint_id}
        response = requests.post(
            "{}/hmip/auth/isRequestAcknowledged".format(self.url_rest),
            json=data,
            headers=self.headers,
        )
        return response.status_code == 200

    def requestAuthToken(self):
        data = {"deviceId": self.uuid}
        response = requests.post(
            "{}/hmip/auth/requestAuthToken".format(self.url_rest),
            json=data,
            headers=self.headers,
        )
        return json.loads(response.text)["authToken"]

    def confirmAuthToken(self, authToken):
        data = {"deviceId": self.uuid, "authToken": authToken}
        response = requests.post(
            "{}/hmip/auth/confirmAuthToken".format(self.url_rest),
            json=data,
            headers=self.headers,
        )
        return json.loads(response.text)["clientId"]
