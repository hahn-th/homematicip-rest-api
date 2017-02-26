import platform
import locale

from .home import *
from .device import *
from .auth import *
from .group import *
from .securityEvent import *

import requests

clientCharacteristics = {"clientCharacteristics":
    {
        "apiVersion": "8",
        "applicationIdentifier": "homematicip-python",
        "applicationVersion": "1.0",
        "deviceManufacturer": "none",
        "deviceType": "Computer",
        "language": locale.getdefaultlocale()[0],
        "osType": platform.system(),
        "osVersion": platform.release(),
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
        urlREST = "https://ps1.homematic.com:6969"
        urlWebSocket = "wss://ps1.homematic.com:8888"


def get_urlREST():
    return urlREST


def get_urlWebSocket():
    return urlWebSocket
