from homematicip import HomeMaticIPObject
import json
from datetime import datetime


class Group(HomeMaticIPObject.HomeMaticIPObject):
    """this class represents a group """
    id = None
    homeId = None
    label = None
    lastStatusUpdate = None
    groupType = None
    updateState = None
    unreach = None
    lowBat = None
    metagroup = None
    devices = None
    def from_json(self, js, devices):
        self.id = js["id"]
        self.homeId = js["homeId"]
        self.label = js["label"]
        self.lastStatusUpdate = datetime.fromtimestamp(js["lastStatusUpdate"] / 1000.0)
        self.groupType = js["type"]

        self.devices = []
        for channel in js["channels"]:
            self.devices.append([d for d in devices if d.id == channel["deviceId"]])


    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"{} {}".format(self.groupType, self.label)

    def set_label(self, label):
        data = { "deviceId" : self.id, "label" : label }
        return self._restCall("home/setDeviceLabel", json.dumps(data))

class MetaGroup(Group):
    """ a meta group is a "Room" inside the homematic configuration """

    groups = None
    def from_json(self, js, devices, groups):
        self.id = js["id"]
        self.homeId = js["homeId"]
        self.label = js["label"]
        self.lastStatusUpdate = datetime.fromtimestamp(js["lastStatusUpdate"] / 1000.0)
        self.groupType = js["type"]

        self.devices = []
        for channel in js["channels"]:
            [d for d in devices if d.id == channel["deviceId"]]
            if d:
                self.devices.append(d)
        self.groups = []
        for group in js["groups"]:
            [g for g in groups if g == group]
            if g:
                g.metaGroup = self
                self.groups.append(g)

class SecurityGroup(Group):
    open = None
    motionDetected = None
    sabotage = None
    smokeDetectorAlarmType = None

    def from_json(self, js, devices):
        super(SecurityGroup, self).from_json(js, devices)
        self.open = js["open"]
        self.motionDetected = js["motionDetected"]
        self.sabotage = js["sabotage"]
        self.smokeDetectorAlarmType = js["smokeDetectorAlarmType"]