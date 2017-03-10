# coding=utf-8
from homematicip import HomeMaticIPObject
import json
from datetime import datetime
import calendar
from operator import attrgetter

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
    metaGroup = None
    devices = None
    def from_json(self, js, devices):
        self.id = js["id"]
        self.homeId = js["homeId"]
        self.label = js["label"]
        self.lastStatusUpdate = datetime.fromtimestamp(js["lastStatusUpdate"] / 1000.0)
        self.groupType = js["type"]

        self.devices = []
        for channel in js["channels"]:
            for d in devices:
                if d.id == channel["deviceId"]:
                    self.devices.append(d)


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
            for d in devices:
                if d.id == channel["deviceId"]:
                    self.devices.append(d)
        self.groups = []
        for group in js["groups"]:
            for g in groups:
                if g.id == group:
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
    
    def set_switch_state(self, on=True):
        data = { "groupId":self.id, "on":on }
        return self._restCall("group/switching/setState", body=json.dumps(data))
    
    def turn_on(self):
        return self.set_state(True)

    def turn_off(self):
        return self.set_state(False)

    def __unicode__(self):
        return u"{}: on({}) dimLevel({}) ".format(super(SwitchingGroup, self).__unicode__(),
                                                self.on, self.dimLevel) 

class LinkedSwitchingGroup(SwitchingGroup):
    def set_light_group_switches(self, devices):
        switchChannels = []
        for d in devices:
            channel = { "channelIndex" : 1, "deviceId" : d.id }
            switchChannels.append(channel)
        data = { "groupId" : self.id, "switchChannels" : switchChannels }
        return self._restCall("home/security/setLightGroupSwitches", body=json.dumps(data))

class ExtendedLinkedSwitchingGroup(SwitchingGroup):
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
    SIGNAL_OPTICAL_BLINKING_ALTERNATELY_REPEATING = "BLINKING_ALTERNATELY_REPEATING"
    SIGNAL_OPTICAL_DOUBLE_FLASHING_REPEATING = "DOUBLE_FLASHING_REPEATING"

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

    def test_signal_optical(self,signalOptical=SIGNAL_OPTICAL_BLINKING_ALTERNATELY_REPEATING):
        data = { "groupId":self.id, "signalOptical":signalOptical }
        return self._restCall("group/switching/arlarm/testSignalOptical", body=json.dumps(data))

    def set_signal_optical(self,signalOptical=SIGNAL_OPTICAL_BLINKING_ALTERNATELY_REPEATING):
        data = { "groupId":self.id, "signalOptical":signalOptical }
        return self._restCall("group/switching/arlarm/setSignalOptical", body=json.dumps(data))


#at the moment it doesn't look like this class has any special properties/functions
#keep it as a placeholder in the meantime
class HeatingHumidyLimiterGroup(Group):
    def __unicode__(self):
        return super(HeatingHumidyLimiterGroup,self).__unicode__()
    
#at the moment it doesn't look like this class has any special properties/functions
#keep it as a placeholder in the meantime
class HeatingTemperatureLimiterGroup(Group):
    def __unicode__(self):
        return super(HeatingTemperatureLimiterGroup,self).__unicode__()

class HeatingChangeoverGroup(Group):
    on = None
    dimLevel = None
    sensorSpecificParameters = None

    def from_json(self, js, devices):
        super(HeatingChangeoverGroup, self).from_json(js, devices)
        self.on = js["on"]
        self.dimLevel = js["dimLevel"]

    def __unicode__(self):
        return u"{} on({}) dimLevel({})".format(super(HeatingChangeoverGroup, self).__unicode__(),
                                                self.on, self.dimLevel) 

#at the moment it doesn't look like this class has any special properties/functions
#keep it as a placeholder in the meantime
class InboxGroup(Group):
    def __unicode__(self):
        return super(InboxGroup,self).__unicode__()

class SecurityZoneGroup(Group):
    active = None
    silent = None
    ignorableDevices = None
    open = None
    motionDetected = None
    sabotage = None
    def from_json(self, js, devices):
        super(SecurityZoneGroup, self).from_json(js, devices)
        self.active = js["active"]
        self.silent = js["silent"]
        self.open = js["open"]
        self.motionDetected = js["motionDetected"]
        self.sabotage = js["sabotage"]
        self.ignorableDevices = []
        for device in js["ignorableDevices"]:
            self.ignorableDevices.append([d for d in devices if d.id == device][0])


    def __unicode__(self):
        return u"{} active({}) silent({}) open({}) motionDetected({}) sabotage({}) ignorableDevices(#{})".format(super(SecurityZoneGroup, self).__unicode__(),
                                                self.active, self.silent, self.open, self.motionDetected, self.sabotage, len(self.ignorableDevices) ) 
class HeatingCoolingPeriod(HomeMaticIPObject.HomeMaticIPObject):
    starttime = None
    endtime = None
    value = None

    def from_json(self, js):
        super(HeatingCoolingPeriod, self).from_json(js)
        self.starttime = js["starttime"]
        self.endtime = js["endtime"]
        self.value = js["value"]

class HeatingCoolingProfileDay(HomeMaticIPObject.HomeMaticIPObject):
    baseValue = None
    periods = None
    def from_json(self, js):
        super(HeatingCoolingProfileDay, self).from_json(js)
        self.baseValue = js["baseValue"]
        self.periods = []
        for p in js["periods"]:
            period = HeatingCoolingPeriod()
            period.from_json(p)
            self.periods.append(period)

class HeatingCoolingProfile(HomeMaticIPObject.HomeMaticIPObject):
    id = None
    homeId = None

    groupId = None
    index = None
    visible = None
    enabled = None

    name = None
    type = None
    profileDays = None

    def get_details(self):
        data = { "groupId": self.groupId, "profileIndex" : self.index, "profileName" : self.name }
        js = self._restCall("group/heating/getProfile", body=json.dumps(data))
        self.homeId = js["homeId"]
        self.type = js["type"]
        self.profileDays = {}
        
        for i in xrange(0,7):
            day = HeatingCoolingProfileDay()
            day.from_json(js["profileDays"][calendar.day_name[i].upper()])
            self.profileDays[i] = day

    def from_json(self, js):
        super(HeatingCoolingProfile, self).from_json(js)
        self.id = js["profileId"]
        self.groupId = js["groupId"]
        self.index = js["index"]
        self.name = js["name"]
        self.visible = js["visible"]
        self.enabled = js["enabled"]

    def _time_to_totalminutes(self,time):
        s = time.split(":")
        return int(s[0])*60+int(s[1])

    def update_profile(self):
        days = {}
        for i in xrange(0,7):
            periods = []
            day = self.profileDays[i]
            for p in day.periods:                
                periods.append( { "endtime" : p.endtime, "starttime":p.starttime, "value" : p.value
                                 , "endtimeAsMinutesOfDay" : self._time_to_totalminutes(p.endtime)
                                 , "starttimeAsMinutesOfDay" : self._time_to_totalminutes(p.starttime) } )

            dayOfWeek = calendar.day_name[i].upper()
            days[dayOfWeek] = { "baseValue" : day.baseValue, "dayOfWeek" : dayOfWeek, "periods" : periods }

        data = { "groupId" : self.groupId, "profile": { "groupId" : self.groupId, "homeId" : self.homeId, "id" : self.id
                                                       , "index" : self.index, "name" : self.name, "profileDays" : days, "type" : self.type }, "profileIndex" : self.index }
        return self._restCall("group/heating/updateProfile", body=json.dumps(data) )
        

class HeatingGroup(Group):
    windowOpenTemperature = None
    setPointTemperature = None
    open = None
    maxTemperature = None
    minTemperature = None
    cooling = None
    partyMode = None
    controlMode = None
    activeProfile                      = None
    boostMode                          = None
    boostDuration                      = None
    actualTemperature                  = None
    humidity                           = None
    coolingAllowed                     = None
    coolingIgnored                     = None
    ecoAllowed                         = None
    ecoIgnored                         = None
    controllable                       = None
    floorHeatingMode                   = None
    humidityLimitEnabled               = None
    humidityLimitValue                 = None
    externalClockEnabled               = None
    externalClockHeatingTemperature    = None
    externalClockCoolingTemperature    = None
    profiles                           = None

    def from_json(self, js, devices):
        super(HeatingGroup, self).from_json(js, devices)
        self.windowOpenTemperature = js["windowOpenTemperature"]
        self.setPointTemperature = js["setPointTemperature"]
        self.open = js["open"]
        self.maxTemperature = js["maxTemperature"]
        self.minTemperature = js["minTemperature"]
        self.cooling = js["cooling"]
        self.partyMode = js["partyMode"]
        self.controlMode = js["controlMode"]
        self.boostMode = js["boostMode"]
        self.boostDuration = js["boostDuration"]
        self.actualTemperature = js["actualTemperature"]
        self.humidity = js["humidity"]
        self.coolingAllowed = js["coolingAllowed"]
        self.coolingIgnored = js["coolingIgnored"]
        self.ecoAllowed = js["ecoAllowed"]
        self.ecoIgnored = js["ecoIgnored"]
        self.controllable = js["controllable"]
        self.floorHeatingMode = js["floorHeatingMode"]
        self.humidityLimitEnabled = js["humidityLimitEnabled"]
        self.humidityLimitValue = js["humidityLimitValue"]
        self.externalClockEnabled = js["externalClockEnabled"]
        self.externalClockHeatingTemperature = js["externalClockHeatingTemperature"]
        self.externalClockCoolingTemperature = js["externalClockCoolingTemperature"]

        profiles = []
        activeProfile = js["activeProfile"] #not self.!!!!
        for k,v in js["profiles"].items():
            profile = HeatingCoolingProfile()
            profile.from_json(v)
            profiles.append(profile)
            if activeProfile == k:
                self.activeProfile = profile
        self.profiles = sorted(profiles, key=attrgetter('index'))


    def __unicode__(self):
        return u"{} windowOpenTemperature({}) setPointTemperature({}) open({}) motionDetected({}) sabotage({}) cooling({}) partyMode({}) controlMode({}) actualTemperature({})".format(super(HeatingGroup, self).__unicode__(),
                                                self.windowOpenTemperature, self.setPointTemperature, self.open, self.maxTemperature, self.minTemperature, self.cooling,self.partyMode,self.controlMode, self.actualTemperature ) 

    def set_point_temperature(self,temperature):
        data = { "groupId" : self.id, "setPointTemperature" : temperature}
        return self._restCall("group/heating/setSetPointTemperature", body=json.dumps(data))

    def set_boost(self,enable=True):
        data = { "groupId" : self.id, "boost" : enable}
        return self._restCall("group/heating/setBoost", body=json.dumps(data))

class HeatingDehumidifierGroup(Group):
    on = None
    dimLevel = None

    def from_json(self, js, devices):
        super(HeatingDehumidifierGroup, self).from_json(js, devices)
        self.on = js["on"]
        self.dimLevel = js["dimLevel"]

    def __unicode__(self):
        return u"{}: on({}) dimLevel({}) ".format(super(HeatingDehumidifierGroup, self).__unicode__(),
                                                self.on, self.dimLevel) 

class HeatingCoolingDemandGroup(Group):
    on = None
    dimLevel = None

    def from_json(self, js, devices):
        super(HeatingCoolingDemandGroup, self).from_json(js, devices)
        self.on = js["on"]
        self.dimLevel = js["dimLevel"]

    def __unicode__(self):
        return u"{}: on({}) dimLevel({}) ".format(super(HeatingCoolingDemandGroup, self).__unicode__(),
                                                self.on, self.dimLevel) 

#at the moment it doesn't look like this class has any special properties/functions
#keep it as a placeholder in the meantime
class HeatingExternalClockGroup(Group):
    def __unicode__(self):
        return super(HeatingExternalClockGroup,self).__unicode__()

class HeatingCoolingDemandBoilerGroup(Group):
    boilerFollowUpTime = None
    boilerLeadTime = None
    on = None
    dimLevel = None

    def from_json(self, js, devices):
        super(HeatingCoolingDemandBoilerGroup, self).from_json(js, devices)
        self.on = js["on"]
        self.dimLevel = js["dimLevel"]
        self.boilerLeadTime = js["boilerLeadTime"]
        self.boilerFollowUpTime = js["boilerFollowUpTime"]

    def __unicode__(self):
        return u"{}: on({}) dimLevel({}) boilerFollowUpTime({}) boilerLeadTime({})".format(super(HeatingCoolingDemandBoilerGroup, self).__unicode__(),
                                                self.on, self.dimLevel, self.boilerFollowUpTime, self.boilerLeadTime) 

class HeatingCoolingDemandPumpGroup(Group):
    pumpProtectionDuration = None
    pumpProtectionSwitchingInterval = None
    pumpFollowUpTime = None
    pumpLeadTime = None
    on = None
    dimLevel = None

    def from_json(self, js, devices):
        super(HeatingCoolingDemandPumpGroup, self).from_json(js, devices)
        self.on = js["on"]
        self.dimLevel = js["dimLevel"]
        self.pumpProtectionSwitchingInterval = js["pumpProtectionSwitchingInterval"]
        self.pumpProtectionDuration = js["pumpProtectionDuration"]
        self.pumpFollowUpTime = js["pumpFollowUpTime"]
        self.pumpLeadTime = js["pumpLeadTime"]

    def __unicode__(self):
        return u"{}: on({}) dimLevel({}) pumpProtectionDuration({}) pumpProtectionSwitchingInterval({}) pumpFollowUpTime({}) pumpLeadTime({})".format(super(HeatingCoolingDemandPumpGroup, self).__unicode__(),
                                                self.on, self.dimLevel, self.pumpProtectionDuration, self.pumpProtectionSwitchingInterval, self.pumpFollowUpTime, self.pumpLeadTime) 