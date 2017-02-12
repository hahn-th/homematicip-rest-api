from homematicip import HomeMaticIPObject
import json

class Device(HomeMaticIPObject.HomeMaticIPObject):
  """this class represents a generic homematic ip device """
  id=None
  homeId=None
  label=None
  lastStatusUpdate=None
  deviceType=None
  updateState=None
  firmwareVersion=None
  availableFirmwareVersion=None
  unreach=None
  lowBat=None
  
  def from_json(self,js):
    self.id = js["id"]
    self.homeId = js["homeId"]
    self.label = js["label"]
    self.lastStatusUpdate = js["lastStatusUpdate"]
    self.deviceType = js["type"]
    self.updateState = js["updateState"]
    self.firmwareVersion = js["firmwareVersion"]
    self.availableFirmwareVersion = js["availableFirmwareVersion"]

class HeatingThermostat(Device):
  temperatureOffset=None
  operationLockActive=None
  valvePosition=None
  def from_json(self,js):
    super(HeatingThermostat,self).from_json(js)
    for cid in js["functionalChannels"]:
      c = js["functionalChannels"][cid]
      type = c["functionalChannelType"]
      if type == "HEATING_THERMOSTAT_CHANNEL":
        self.temperatureOffset = c["temperatureOffset"]
        self.valvePosition = c["valvePosition"]
      elif type == "DEVICE_OPERATIONLOCK":
        self.unreach = c["unreach"]
        self.lowBat = c["lowBat"]
        self.operationLockActive = c["operationLockActive"]

class ShutterContact(Device):
  sabotage = None
  open = None
  eventDelay = None
  def from_json(self,js):
    super(ShutterContact,self).from_json(js)
    for cid in js["functionalChannels"]:
      c = js["functionalChannels"][cid]
      type = c["functionalChannelType"]
      if type == "SHUTTER_CONTACT_CHANNEL":
        self.open = c["open"]
        self.eventDelay = c["eventDelay"]
      elif type == "DEVICE_SABOTAGE":
        self.unreach = c["unreach"]
        self.lowBat = c["lowBat"]
        self.sabotage = c["sabotage"]

class WallMountedThermostatPro(Device):
  temperatureOffset=None
  display=None
  operationLockActive=None
  actualTemperature=None
  humidity=None
  def from_json(self,js):
    super(WallMountedThermostatPro,self).from_json(js)
    for cid in js["functionalChannels"]:
      c = js["functionalChannels"][cid]
      type = c["functionalChannelType"]
      if type == "WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL":
        self.temperatureOffset = c["temperatureOffset"]
        self.display = c["display"]
        self.actualTemperature = c["actualTemperature"]
        self.humidity = c["humidity"]

      elif type == "DEVICE_OPERATIONLOCK":
        self.unreach = c["unreach"]
        self.lowBat = c["lowBat"]
        self.operationLockActive = c["operationLockActive"]
  
class SmokeDetector(Device):
  smokeDetectorAlarmType=None
  def from_json(self,js):
    super(SmokeDetector,self).from_json(js)
    for cid in js["functionalChannels"]:
      c = js["functionalChannels"][cid]
      type = c["functionalChannelType"]
      if type == "SMOKE_DETECTOR_CHANNEL":
        self.smokeDetectorAlarmType = c["smokeDetectorAlarmType"]
      elif type == "DEVICE_BASE":
        self.unreach = c["unreach"]
        self.lowBat = c["lowBat"]
