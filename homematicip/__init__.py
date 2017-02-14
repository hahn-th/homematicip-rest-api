from .home import *
from .device import *
from .auth import *
import requests

clientCharacteristics = {"clientCharacteristics":
    {
        "apiVersion": "7",
        "applicationIdentifier": "homematicip-python",
        "applicationVersion": "1.0",
        "deviceManufacturer": "none",
        "deviceType": "Computer",
        "language": "de-AT",
        "osType": "Windows",
        "osVersion": "10",
    },
    "id": None
}

auth_token = ""
urlREST = ""
urlWebSocket = ""


def set_auth_token(token):
    global auth_token
    auth_token = token


def get_auth_token():
    global auth_token
    return auth_token


def get_clientCharacteristics():
    return clientCharacteristics


def init(accesspoint_id, lookup=True):
    global urlREST
    global clientCharacteristics
    global urlWebSocket
    accesspoint_id = accesspoint_id.replace('-', '').upper()
    clientCharacteristics["id"] = accesspoint_id
    if lookup:
        result = requests.post("https://lookup.homematic.com:48335/getHost", json=clientCharacteristics)
        js = json.loads(result.text)
        urlREST = js["urlREST"]
        urlWebSocket = js["urlWebSocket"]
    else:
        urlREST = "https://ps2.homematic.com:16969"
        urlWebSocket = "wss://ps2.homematic.com:18888"


def get_urlREST():
    return urlREST


def get_urlWebSocket():
    return urlWebSocket
