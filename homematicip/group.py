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
        time = js["lastStatusUpdate"]
        if time > 0:
            self.lastStatusUpdate = datetime.fromtimestamp(time / 1000.0)
        else:
            self.lastStatusUpdate = None

        self.groupType = js["type"]

        self.devices = []
        for channel in js["channels"]:
            for d in devices:
                if d.id == channel["deviceId"]:
                    self.devices.append(d)

    def __str__(self):
        return "{} {}".format(self.groupType, self.label)

    def set_label(self, label):
        data = {"groupId": self.id, "label": label}
        return self._restCall("group/setGroupLabel", json.dumps(data))


class MetaGroup(Group):
    """ a meta group is a "Room" inside the homematic configuration """

    groups = None

    def from_json(self, js, devices, groups = None):
        self.id = js["id"]
        self.homeId = js["homeId"]
        self.label = js["label"]
        time = js["lastStatusUpdate"]
        if time > 0:
            self.lastStatusUpdate = datetime.fromtimestamp(time / 1000.0)
        else:
            self.lastStatusUpdate = None
        self.groupType = js["type"]

        self.devices = []
        for channel in js["channels"]:
            for d in devices:
                if d.id == channel["deviceId"]:
                    self.devices.append(d)

        self.groups = []
        if (groups != None):
            for group in js["groups"]:
                for g in groups:
                    if g.id == group:
                        g.metaGroup = self
                        self.groups.append(g)


class SecurityGroup(Group):
    windowState = None
    motionDetected = None
    sabotage = None
    smokeDetectorAlarmType = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.windowState = js["windowState"]
        self.motionDetected = js["motionDetected"]
        self.sabotage = js["sabotage"]
        self.smokeDetectorAlarmType = js["smokeDetectorAlarmType"]

    def __str__(self):
        return "{}: windowState({}) motionDetected({}) sabotage({}) smokeDetectorAlarmType({})".format(
            super().__str__(),
            self.windowState, self.motionDetected, self.sabotage,
            self.smokeDetectorAlarmType)


class SwitchingGroup(Group):
    on = None
    dimLevel = None
    processing = None
    shutterLevel = None
    slatsLevel = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.on = js["on"]
        self.dimLevel = js["dimLevel"]
        try:  # TODO: FIX that ugly hack -> maybe linked_switching shouldn't inherit anymore from switchingGroup
            self.processing = js["processing"]
            self.shutterLevel = js["shutterLevel"]
            self.slatsLevel = js["slatsLevel"]
        except:
            pass

    def set_switch_state(self, on=True):
        data = {"groupId": self.id, "on": on}
        return self._restCall("group/switching/setState",
                              body=json.dumps(data))

    def turn_on(self):
        return self.set_switch_state(True)

    def turn_off(self):
        return self.set_switch_state(False)

    def set_shutter_level(self, level):
        data = {"groupId": self.id, "shutterLevel": level}
        return self._restCall("group/switching/setShutterLevel",
                              body=json.dumps(data))

    def set_shutter_stop(self):
        data = {"groupId": self.id}
        return self._restCall("group/switching/stop", body=json.dumps(data))

    def __str__(self):
        return "{}: on({}) dimLevel({}) processing({}) shutterLevel({}) slatsLevel({})".format(
            super().__str__(),
            self.on, self.dimLevel, self.processing, self.shutterLevel,
            self.slatsLevel)


class LinkedSwitchingGroup(SwitchingGroup):
    def set_light_group_switches(self, devices):
        switchChannels = []
        for d in devices:
            channel = {"channelIndex": 1, "deviceId": d.id}
            switchChannels.append(channel)
        data = {"groupId": self.id, "switchChannels": switchChannels}
        return self._restCall("home/security/setLightGroupSwitches",
                              body=json.dumps(data))


class ExtendedLinkedSwitchingGroup(SwitchingGroup):
    onTime = None
    onLevel = None
    sensorSpecificParameters = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.onTime = js["onTime"]
        self.onLevel = js["onLevel"]
        self.sensorSpecificParameters = js["sensorSpecificParameters"]

    def __str__(self):
        return "{} onTime({}) onLevel({})".format(
            super().__str__(),
            self.onTime, self.onLevel)

    def set_on_time(self, onTimeSeconds):
        data = {"groupId": self.id, "onTime": onTimeSeconds}
        return self._restCall("group/switching/linked/setOnTime",
                              body=json.dumps(data))


class AlarmSwitchingGroup(Group):
    SIGNAL_OPTICAL_DISABLE_OPTICAL_SIGNAL = "DISABLE_OPTICAL_SIGNAL"
    SIGNAL_OPTICAL_BLINKING_ALTERNATELY_REPEATING = "BLINKING_ALTERNATELY_REPEATING"
    SIGNAL_OPTICAL_BLINKING_BOTH_REPEATING = "BLINKING_BOTH_REPEATING"
    SIGNAL_OPTICAL_DOUBLE_FLASHING_REPEATING = "DOUBLE_FLASHING_REPEATING"
    SIGNAL_OPTICAL_FLASHING_BOTH_REPEATING = "FLASHING_BOTH_REPEATING"
    SIGNAL_OPTICAL_CONFIRMATION_SIGNAL_0 = "CONFIRMATION_SIGNAL_0"
    SIGNAL_OPTICAL_CONFIRMATION_SIGNAL_1 = "CONFIRMATION_SIGNAL_1"
    SIGNAL_OPTICAL_CONFIRMATION_SIGNAL_2 = "CONFIRMATION_SIGNAL_2"

    on = None
    dimLevel = None
    onTime = None
    signalAcoustic = None
    signalOptical = None
    smokeDetectorAlarmType = None
    acousticFeedbackEnabled = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.onTime = js["onTime"]
        self.on = js["on"]
        self.dimLevel = js["dimLevel"]
        self.signalAcoustic = js["signalAcoustic"]
        self.signalOptical = js["signalOptical"]
        self.smokeDetectorAlarmType = js["smokeDetectorAlarmType"]
        self.acousticFeedbackEnabled = js["acousticFeedbackEnabled"]

    def set_on_time(self, onTimeSeconds):
        data = {"groupId": self.id, "onTime": onTimeSeconds}
        return self._restCall("group/switching/arlarm/setOnTime",
                              body=json.dumps(data))

    def __str__(self):
        return "{}: on({}) dimLevel({}) onTime({}) signalAcoustic({}) signalOptical({}) smokeDetectorAlarmType({}) acousticFeedbackEnabled({})".format(
            super().__str__(),
            self.on, self.dimLevel, self.onTime, self.signalAcoustic,
            self.signalOptical, self.smokeDetectorAlarmType,
            self.acousticFeedbackEnabled)

    def test_signal_optical(self,
                            signalOptical=SIGNAL_OPTICAL_BLINKING_ALTERNATELY_REPEATING):
        data = {"groupId": self.id, "signalOptical": signalOptical}
        return self._restCall("group/switching/arlarm/testSignalOptical",
                              body=json.dumps(data))

    def set_signal_optical(self,
                           signalOptical=SIGNAL_OPTICAL_BLINKING_ALTERNATELY_REPEATING):
        data = {"groupId": self.id, "signalOptical": signalOptical}
        return self._restCall("group/switching/arlarm/setSignalOptical",
                              body=json.dumps(data))


# at the moment it doesn't look like this class has any special properties/functions
# keep it as a placeholder in the meantime
class HeatingHumidyLimiterGroup(Group):
    def __str__(self):
        return super().__str__()


# at the moment it doesn't look like this class has any special properties/functions
# keep it as a placeholder in the meantime
class HeatingTemperatureLimiterGroup(Group):
    def __str__(self):
        return super().__str__()


class HeatingChangeoverGroup(Group):
    on = None
    dimLevel = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.on = js["on"]

    def __str__(self):
        return "{} on({})".format(
            super().__str__(), self.on)


# at the moment it doesn't look like this class has any special properties/functions
# keep it as a placeholder in the meantime
class InboxGroup(Group):
    def __str__(self):
        return super().__str__()


class SecurityZoneGroup(Group):
    active = False
    silent = False
    ignorableDevices = []
    windowState = ""
    motionDetected = None
    sabotage = None
    presenceDetected = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.active = js["active"]
        self.silent = js["silent"]
        self.windowState = js["windowState"]
        self.motionDetected = js["motionDetected"]
        self.sabotage = js["sabotage"]
        self.ignorableDevices = []
        for device in js["ignorableDevices"]:
            self.ignorableDevices.append(
                [d for d in devices if d.id == device][0])

    def __str__(self):
        return "{} active({}) silent({}) windowState({}) motionDetected({}) sabotage({}) presenceDetected({}) ignorableDevices(#{})".format(
            super().__str__(),
            self.active, self.silent, self.windowState, self.motionDetected,
            self.sabotage, self.presenceDetected, len(self.ignorableDevices))


class HeatingCoolingPeriod(HomeMaticIPObject.HomeMaticIPObject):
    starttime = None
    endtime = None
    value = None

    def from_json(self, js):
        super().from_json(js)
        self.starttime = js["starttime"]
        self.endtime = js["endtime"]
        self.value = js["value"]


class HeatingCoolingProfileDay(HomeMaticIPObject.HomeMaticIPObject):
    baseValue = None
    periods = None

    def from_json(self, js):
        super().from_json(js)
        self.baseValue = js["baseValue"]
        self.periods = []
        for p in js["periods"]:
            period = HeatingCoolingPeriod(self._connection)
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
        data = {"groupId": self.groupId, "profileIndex": self.index,
                "profileName": self.name}
        js = self._restCall("group/heating/getProfile", body=json.dumps(data))
        self.homeId = js["homeId"]
        self.type = js["type"]
        self.profileDays = {}

        for i in range(0, 7):
            day = HeatingCoolingProfileDay(self._connection)
            day.from_json(js["profileDays"][calendar.day_name[i].upper()])
            self.profileDays[i] = day

    def from_json(self, js):
        super().from_json(js)
        self.id = js["profileId"]
        self.groupId = js["groupId"]
        self.index = js["index"]
        self.name = js["name"]
        self.visible = js["visible"]
        self.enabled = js["enabled"]

    def _time_to_totalminutes(self, time):
        s = time.split(":")
        return int(s[0]) * 60 + int(s[1])

    def update_profile(self):
        days = {}
        for i in xrange(0, 7):
            periods = []
            day = self.profileDays[i]
            for p in day.periods:
                periods.append({"endtime": p.endtime, "starttime": p.starttime,
                                "value": p.value
                                   ,
                                "endtimeAsMinutesOfDay": self._time_to_totalminutes(
                                    p.endtime)
                                   ,
                                "starttimeAsMinutesOfDay": self._time_to_totalminutes(
                                    p.starttime)})

            dayOfWeek = calendar.day_name[i].upper()
            days[dayOfWeek] = {"baseValue": day.baseValue,
                               "dayOfWeek": dayOfWeek, "periods": periods}

        data = {"groupId": self.groupId,
                "profile": {"groupId": self.groupId, "homeId": self.homeId,
                            "id": self.id
                    , "index": self.index, "name": self.name,
                            "profileDays": days, "type": self.type},
                "profileIndex": self.index}
        return self._restCall("group/heating/updateProfile",
                              body=json.dumps(data))


class HeatingGroup(Group):
    windowOpenTemperature = None
    setPointTemperature = None
    windowState = None
    maxTemperature = None
    minTemperature = None
    cooling = None
    partyMode = None
    controlMode = None
    activeProfile = None
    boostMode = None
    boostDuration = None
    actualTemperature = None
    humidity = None
    coolingAllowed = None
    coolingIgnored = None
    ecoAllowed = None
    ecoIgnored = None
    controllable = None
    floorHeatingMode = None
    humidityLimitEnabled = None
    humidityLimitValue = None
    externalClockEnabled = None
    externalClockHeatingTemperature = None
    externalClockCoolingTemperature = None
    profiles = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.windowOpenTemperature = js["windowOpenTemperature"]
        self.setPointTemperature = js["setPointTemperature"]
        self.windowState = js["windowState"]
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
        self.externalClockHeatingTemperature = js[
            "externalClockHeatingTemperature"]
        self.externalClockCoolingTemperature = js[
            "externalClockCoolingTemperature"]

        profiles = []
        activeProfile = js["activeProfile"]  # not self.!!!!
        for k, v in js["profiles"].items():
            profile = HeatingCoolingProfile(self._connection)
            profile.from_json(v)
            profiles.append(profile)
            if activeProfile == k:
                self.activeProfile = profile
        self.profiles = sorted(profiles, key=attrgetter('index'))

    def __str__(self):
        return "{} windowOpenTemperature({}) setPointTemperature({}) windowState({}) motionDetected({}) sabotage({}) cooling({}) partyMode({}) controlMode({}) actualTemperature({})".format(
            super().__str__(),
            self.windowOpenTemperature, self.setPointTemperature,
            self.windowState, self.maxTemperature, self.minTemperature,
            self.cooling, self.partyMode, self.controlMode,
            self.actualTemperature)

    def set_point_temperature(self, temperature):
        data = {"groupId": self.id, "setPointTemperature": temperature}
        return self._restCall("group/heating/setSetPointTemperature",
                              body=json.dumps(data))

    def set_boost(self, enable=True):
        data = {"groupId": self.id, "boost": enable}
        return self._restCall("group/heating/setBoost", body=json.dumps(data))

    def set_active_profile(self, index):
        data = {"groupId": self.id, "profileIndex": index}
        return self._restCall("group/heating/setActiveProfile",
                              body=json.dumps(data))


class HeatingDehumidifierGroup(Group):
    on = None
    dimLevel = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.on = js["on"]

    def __str__(self):
        return "{}: on({})".format(
            super().__str__(), self.on)


class HeatingCoolingDemandGroup(Group):
    on = None
    dimLevel = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.on = js["on"]
        self.dimLevel = js["dimLevel"]

    def __str__(self):
        return "{}: on({}) dimLevel({}) ".format(
            super().__str__(),
            self.on, self.dimLevel)


# at the moment it doesn't look like this class has any special properties/functions
# keep it as a placeholder in the meantime
class HeatingExternalClockGroup(Group):
    def __str__(self):
        return super().__str__()


class HeatingCoolingDemandBoilerGroup(Group):
    boilerFollowUpTime = None
    boilerLeadTime = None
    on = None
    dimLevel = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.on = js["on"]
        self.boilerLeadTime = js["boilerLeadTime"]
        self.boilerFollowUpTime = js["boilerFollowUpTime"]

    def __str__(self):
        return "{}: on({}) boilerFollowUpTime({}) boilerLeadTime({})".format(
            super().__str__(),
            self.on, self.boilerFollowUpTime, self.boilerLeadTime)


class HeatingCoolingDemandPumpGroup(Group):
    pumpProtectionDuration = None
    pumpProtectionSwitchingInterval = None
    pumpFollowUpTime = None
    pumpLeadTime = None
    on = None
    dimLevel = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.on = js["on"]
        self.pumpProtectionSwitchingInterval = js[
            "pumpProtectionSwitchingInterval"]
        self.pumpProtectionDuration = js["pumpProtectionDuration"]
        self.pumpFollowUpTime = js["pumpFollowUpTime"]
        self.pumpLeadTime = js["pumpLeadTime"]

    def __str__(self):
        return "{}: on({}) pumpProtectionDuration({}) pumpProtectionSwitchingInterval({}) pumpFollowUpTime({}) " \
               "pumpLeadTime({})".format(
            super().__str__(),
            self.on, self.pumpProtectionDuration,
            self.pumpProtectionSwitchingInterval,
            self.pumpFollowUpTime, self.pumpLeadTime)


class TimeProfilePeriod(HomeMaticIPObject.HomeMaticIPObject):
    weekdays = []
    hour = 0
    minute = 0
    astroOffset = 0
    astroLimitationType = "NO_LIMITATION"  # NOT_EARLIER_THAN_TIME, NOT_LATER_THAN_TIME
    switchTimeMode = "REGULAR_SWITCH_TIME"  # ASTRO_SUNRISE_SWITCH_TIME, ASTRO_SUNSET_SWITCH_TIME
    dimLevel = 1.0
    rampTime = 0

    def from_json(self, js):
        super().from_json(js)
        self.weekdays = js["weekdays"]
        self.hour = js["hour"]
        self.minute = js["minute"]
        self.astroOffset = js["astroOffset"]
        self.astroLimitationType = js["astroLimitationType"]
        self.switchTimeMode = js["switchTimeMode"]
        self.dimLevel = js["dimLevel"]
        self.rampTime = js["rampTime"]


class TimeProfile(HomeMaticIPObject.HomeMaticIPObject):
    id = None
    homeId = None
    groupId = None
    type = None
    periods = []

    def get_details(self):
        data = {"groupId": self.groupId}
        js = self._restCall("group/switching/profile/getProfile",
                            body=json.dumps(data))
        self.homeId = js["homeId"]
        self.type = js["type"]
        self.id = js["id"]
        self.periods = []
        for p in js["periods"]:
            period = TimeProfilePeriod(self._connection)
            period.from_json(p)
            self.periods.append(period)


class SwitchingProfileGroup(Group):
    on = None
    dimLevel = None
    profileId = None  # Not sure why it is there. You can't use it to query something.
    profileMode = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.on = js["on"]
        self.dimLevel = js["dimLevel"]
        self.profileId = js["profileId"]
        self.profileMode = js["profileMode"]

    def __str__(self):
        return "{}: on({}) dimLevel({}) profileMode({})".format(
            super().__str__(),
            self.on, self.dimLevel, self.profileMode)

    def set_group_channels(self):
        channels = []
        for d in self.devices:
            channels.append[{"channelIndex": 1, "deviceId": d.id}]
        data = {"groupId": self.id, "channels": channels}
        return self._restCall("group/switching/profile/setGroupChannels",
                              body=json.dumps(data))

    def set_profile_mode(self, devices, automatic=True):
        channels = []
        for d in devices:
            channels.append[{"channelIndex": 1, "deviceId": d.id}]
        data = {"groupId": self.id, "channels": channels,
                "profileMode": "AUTOMATIC" if automatic else "MANUAL"}
        return self._restCall("group/switching/profile/setProfileMode",
                              body=json.dumps(data))

    def create(self, label):
        data = {"label": label}
        result = self._restCall(
            "group/switching/profile/createSwitchingProfileGroup",
            body=json.dumps(data))
        if "groupId" in result:
            self.id = result["groupId"]
        return result


class OverHeatProtectionRule(Group):
    temperatureLowerThreshold = None
    temperatureUpperThreshold = None
    targetShutterLevel = None
    targetSlatsLevel = None
    startHour = None
    startMinute = None
    startSunrise = None
    endHour = None
    endMinute = None
    endSunset = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.temperatureLowerThreshold = js["temperatureLowerThreshold"]
        self.temperatureUpperThreshold = js["temperatureUpperThreshold"]
        self.targetShutterLevel = js["targetShutterLevel"]
        self.targetSlatsLevel = js["targetSlatsLevel"]
        self.startHour = js["startHour"]
        self.startMinute = js["startMinute"]
        self.startSunrise = js["startSunrise"]
        self.endHour = js["endHour"]
        self.endMinute = js["endMinute"]
        self.endSunset = js["endSunset"]

    def __str__(self):
        return "{}: tempLower({}) tempUpper({}) targetShutterLevel({}) targetSlatsLevel({})".format(
            super().__str__(),
            self.temperatureLowerThreshold, self.temperatureUpperThreshold,
            self.targetShutterLevel, self.targetSlatsLevel)


class SmokeAlarmDetectionRule(Group):
    smokeDetectorAlarmType = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.smokeDetectorAlarmType = js["smokeDetectorAlarmType"]

    def __str__(self):
        return "{}: smokeDetectorAlarmType({})".format(
            super().__str__(),
            self.smokeDetectorAlarmType)


class ShutterWindProtectionRule(Group):
    windSpeedThreshold = None
    targetShutterLevel = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.windSpeedThreshold = js["windSpeedThreshold"]
        self.targetShutterLevel = js["targetShutterLevel"]

    def __str__(self):
        return "{}: windSpeedThreshold({}) targetShutterLevel({})".format(
            super().__str__(),
            self.windSpeedThreshold, self.targetShutterLevel)


class LockOutProtectionRule(Group):
    triggered = None
    windowState = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.triggered = js["triggered"]
        self.windowState = js["windowState"]

    def __str__(self):
        return "{}: triggered({}) windowState({})".format(
            super().__str__(), self.triggered,
            self.windowState)
