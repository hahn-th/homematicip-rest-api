from homematicip import HomeMaticIPObject
import json
from datetime import datetime

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
    self.lastStatusUpdate = datetime.fromtimestamp(js["lastStatusUpdate"]/1000.0)
    self.deviceType = js["type"]
    self.updateState = js["updateState"]
    self.firmwareVersion = js["firmwareVersion"]
    self.availableFirmwareVersion = js["availableFirmwareVersion"]

  def __str__(self):
    return unicode(self).encode('utf-8')
  def __unicode__(self):
    return u"{} {}".format(self.deviceType,self.label)

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

  def __unicode__(self):
    return u"{}: valvePosition({})".format(super(HeatingThermostat,self).__unicode__(),self.valvePosition)

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
  def __unicode__(self):
    return u"{}: open({}) sabotage ({})".format(super(ShutterContact,self).__unicode__(),self.open,self.sabotage)
        
class WallMountedThermostatPro(Device):
  DISPLAY_ACTUAL = "ACTUAL"
  DISPLAY_SETPOINT = "SETPOINT"
  DISPLAY_ACTUAL_HUMIDITY = "ACTUAL_HUMIDITY"


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

  def set_display(self, display=DISPLAY_ACTUAL):
    data = {"channelIndex": 1, "deviceId" : self.id, "display":display }
    return self._restCall("device/configuration/setClimateControlDisplay",json.dumps(data))

  def __unicode__(self):
    return u"{}: actualTemperature({}) humidity({})".format(super(WallMountedThermostatPro,self).__unicode__(),self.actualTemperature,self.humidity)

  
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
        
  def __unicode__(self):
    return u"{}: smokeDetectorAlarmType({})".format(super(SmokeDetector,self).__unicode__(),self.smokeDetectorAlarmType)
