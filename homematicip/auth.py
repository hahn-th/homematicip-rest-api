import json
import uuid

import requests

import homematicip


class Auth(object):
    uuid = None
    headers = {'content-type': 'application/json', 'accept': 'application/json', 'VERSION': '7'}
    pin = None
    def __init__(self):
        self.uuid = str(uuid.uuid4())

    def connectionRequest(self, access_point):
        data = {"deviceId": self.uuid, "deviceName": "homematicip-python", "sgtin": access_point}
        headers = self.headers
        if self.pin != None:
            headers["PIN"] = self.pin
        response = requests.post("{}/hmip/auth/connectionRequest".format(homematicip.get_urlREST()), json=data,
                                 headers=headers)
        return response

    def isRequestAcknowledged(self):
        data = {"deviceId": self.uuid}
        response = requests.post("{}/hmip/auth/isRequestAcknowledged".format(homematicip.get_urlREST()), json=data,
                                 headers=self.headers)
        return response.status_code == 200

    def requestAuthToken(self):
        data = {"deviceId": self.uuid}
        response = requests.post("{}/hmip/auth/requestAuthToken".format(homematicip.get_urlREST()), json=data,
                                 headers=self.headers)
        return json.loads(response.text)["authToken"]

    def confirmAuthToken(self, authToken):
        data = {"deviceId": self.uuid, "authToken": authToken}
        response = requests.post("{}/hmip/auth/confirmAuthToken".format(homematicip.get_urlREST()), json=data,
                                 headers=self.headers)
        return json.loads(response.text)["clientId"]
