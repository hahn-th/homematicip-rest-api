from .home import *
from .device import *
from .auth import *
import requests

clientCharacteristics = {"clientCharacteristics": {
		                                                  "apiVersion": "7",
		                                                  "applicationIdentifier": "statistic.bot",
		                                                  "applicationVersion": "1.0", 
		                                                  "deviceManufacturer": "Microsoft",
		                                                  "deviceType": "Computer",
		                                                  "language": "de-AT",
		                                                  "osType": "Windows",
		                                                  "osVersion": "10",
	                                                  }
                                                  }

auth_token = ""
urlREST = ""
urlWebSocket=""

def set_auth_token(token):
  global auth_token
  auth_token = token

def get_auth_token():
  global auth_token
  return auth_token

def get_clientCharacteristics():
  return clientCharacteristics

def init(accesspoint_id):
  global urlREST
  global clientCharacteristics
  global urlWebSocket
  accesspoint_id=accesspoint_id.replace('-',' ')
  clientCharacteristics["id"] = accesspoint_id
  result = requests.post("https://lookup.homematic.com:48335/getHost", json=clientCharacteristics)
  js = json.loads(result.text)
  urlREST=js["urlREST"]
  urlWebSocket=js["urlWebSocket"]
  clientCharacteristics["id"]

def get_urlREST():
  return urlREST
def get_urlWebSocket():
  return urlWebSocket

