# coding=utf-8
from homematicip import HomeMaticIPObject
import json
from datetime import datetime


class SecurityEvent(HomeMaticIPObject.HomeMaticIPObject):
    """this class represents a security event """
    eventTimestamp = None
    eventType = None
    label = None
    def from_json(self, js):
        self.label = js["label"]
        self.eventTimestamp = datetime.fromtimestamp(js["eventTimestamp"] / 1000.0)
        self.eventType = js["eventType"]


    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __unicode__(self):
        return u"{} {} {}".format(self.eventType, self.label, self.eventTimestamp.strftime("%Y.%m.%d %H:%M:%S"))

class SecurityZoneEvent(SecurityEvent):
    """ This class will be used by other events which are just adding "securityZoneValues" """
    external_zone = None
    internal_zone = None

    def from_json(self, js):
        super(SecurityZoneEvent, self).from_json(js)
        self.external_zone = js["securityZoneValues"]["EXTERNAL"];
        self.internal_zone = js["securityZoneValues"]["INTERNAL"];

    def __unicode__(self):
        return u"{}: external_zone({}) internal_zone({}) ".format(super(SecurityZoneEvent, self).__unicode__(),
                                                self.external_zone, self.internal_zone) 

class SensorEvent(SecurityEvent):
    def from_json(self, js):
        super(SensorEvent, self).from_json(js)

class AccessPointDisconnectedEvent(SecurityEvent):
    def from_json(self, js):
        super(AccessPointDisconnectedEvent, self).from_json(js)

class AccessPointConnectedEvent(SecurityEvent):
    def from_json(self, js):
        super(AccessPointConnectedEvent, self).from_json(js)


class ActivationChangedEvent(SecurityZoneEvent):
    pass

class SilenceChangedEvent(SecurityZoneEvent):
    pass
