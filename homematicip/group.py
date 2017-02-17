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
        data = { "groupId" : self.id, "label" : label }
        return self._restCall("group/setGroupLabel", json.dumps(data))


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

    def __unicode__(self):
        return u"{}: open({}) motionDetected({}) sabotage({}) smokeDetectorAlarmType({})".format(super(SecurityGroup, self).__unicode__(),
                                                   self.open, self.motionDetected, self.sabotage, self.smokeDetectorAlarmType)        

class SwitchingGroup(Group):
    on = None
    dimLevel = None

    def from_json(self, js, devices):
        super(SwitchingGroup, self).from_json(js, devices)
        self.on = js["on"]
        self.dimLevel = js["dimLevel"]
    
    def set_state(self, on=True):
        data = { "groupId":self.id, "on":on }
        return self._restCall("group/switching/setState", body=json.dumps(data))
    
    def turn_on(self):
        return self.set_state(True)

    def turn_off(self):
        return self.set_state(False)

    def __unicode__(self):
        return u"{}: on({}) dimLevel({}) ".format(super(SwitchingGroup, self).__unicode__(),
                                                self.on, self.dimLevel) 

class LinkedSwitchingGroup(Group):
    on = None
    dimLevel = None

    def from_json(self, js, devices):
        super(LinkedSwitchingGroup, self).from_json(js, devices)
        self.on = js["on"]
        self.dimLevel = js["dimLevel"]

    def __unicode__(self):
        return u"{}: on({}) dimLevel({}) ".format(super(LinkedSwitchingGroup, self).__unicode__(),
                                                self.on, self.dimLevel) 
    def set_light_group_switches(self, devices):
        switchChannels = []
        for d in devices:
            channel = { "channelIndex" : 1, "deviceId" : d.id }
            switchChannels.append(channel)
        data = { "groupId" : self.id, "switchChannels" : switchChannels }
        return self._restCall("home/security/setLightGroupSwitches", body=json.dumps(data))

class ExtendedLinkedSwitchingGroup(Group):
    onTime = None
    onLevel = None
    sensorSpecificParameters = None

    def from_json(self, js, devices):
        super(ExtendedLinkedSwitchingGroup, self).from_json(js, devices)
        self.onTime = js["onTime"]
        self.onLevel = js["onLevel"]
        self.sensorSpecificParameters = js["sensorSpecificParameters"]

    def __unicode__(self):
        return u"{} onTime({}) onLevel({})".format(super(ExtendedLinkedSwitchingGroup, self).__unicode__(),
                                                self.onTime, self.onLevel) 
    def set_on_time(self, onTimeSeconds):
        data = { "groupId":self.id, "onTime":onTimeSeconds }
        return self._restCall("group/switching/linked/setOnTime", body=json.dumps(data))

class AlarmSwitchingGroup(Group):
    on = None
    dimLevel = None
    onTime = None
    signalAcoustic = None
    signalOptical = None
    smokeDetectorAlarmType = None
    acousticFeedbackEnabled = None

    def from_json(self, js, devices):
        super(AlarmSwitchingGroup, self).from_json(js, devices)
        self.onTime = js["onTime"]
        self.on = js["on"]
        self.dimLevel = js["dimLevel"]
        self.signalAcoustic = js["signalAcoustic"]
        self.signalOptical = js["signalOptical"]
        self.smokeDetectorAlarmType = js["smokeDetectorAlarmType"]
        self.acousticFeedbackEnabled = js["acousticFeedbackEnabled"]

    def set_on_time(self, onTimeSeconds):
        data = { "groupId":self.id, "onTime":onTimeSeconds }
        return self._restCall("group/switching/arlarm/setOnTime", body=json.dumps(data))

    def __unicode__(self):
        return u"{}: on({}) dimLevel({}) onTime({}) signalAcoustic({}) signalOptical({}) smokeDetectorAlarmType({}) acousticFeedbackEnabled({})".format(super(AlarmSwitchingGroup, self).__unicode__(),
                                                self.on, self.dimLevel, self.onTime, self.signalAcoustic, self.signalOptical, self.smokeDetectorAlarmType, self.acousticFeedbackEnabled) 


