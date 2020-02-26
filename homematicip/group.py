# coding=utf-8
import calendar
import json
from datetime import datetime
from operator import attrgetter

from homematicip.base.enums import *
from homematicip.base.HomeMaticIPObject import HomeMaticIPObject


class Group(HomeMaticIPObject):
    """this class represents a group """

    def __init__(self, connection):
        super().__init__(connection)
        self.id = None
        self.homeId = None
        self.label = None
        self.lastStatusUpdate = None
        self.groupType = None
        self.unreach = None
        self.metaGroup = None
        self.devices = None

    def from_json(self, js, devices):
        super().from_json(js)
        self.id = js["id"]
        self.homeId = js["homeId"]
        self.label = js["label"]
        self.unreach = js["unreach"]

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

    def delete(self):
        data = {"groupId": self.id}
        return self._restCall("group/deleteGroup", body=json.dumps(data))


class MetaGroup(Group):
    """ a meta group is a "Room" inside the homematic configuration """

    def __init__(self, connection):
        super().__init__(connection)
        self.groups = None
        self.lowBat = False
        self.sabotage = False
        self.configPending = False
        self.dutyCycle = False
        self.incorrectPositioned = None

    def from_json(self, js, devices, groups):

        super().from_json(js, devices)

        self.lowBat = js["lowBat"]
        self.sabotage = js["sabotage"]
        self.configPending = js["configPending"]
        self.dutyCycle = js["dutyCycle"]
        self.incorrectPositioned = js["incorrectPositioned"]

        self.groups = []
        for group in js["groups"]:
            for g in groups:
                if g.id == group:
                    g.metaGroup = self
                    self.groups.append(g)


class SecurityGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.windowState = None
        self.motionDetected = None
        self.presenceDetected = None
        self.sabotage = None
        self.smokeDetectorAlarmType = SmokeDetectorAlarmType.IDLE_OFF
        self.dutyCycle = None
        self.lowBat = None
        self.moistureDetected = None
        self.powerMainsFailure = None
        self.waterlevelDetected = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.windowState = js["windowState"]
        self.motionDetected = js["motionDetected"]
        self.presenceDetected = js["presenceDetected"]
        self.sabotage = js["sabotage"]
        self.smokeDetectorAlarmType = SmokeDetectorAlarmType.from_str(
            js["smokeDetectorAlarmType"]
        )
        self.dutyCycle = js["dutyCycle"]
        self.lowBat = js["lowBat"]
        self.moistureDetected = js["moistureDetected"]
        self.powerMainsFailure = js["powerMainsFailure"]
        self.waterlevelDetected = js["waterlevelDetected"]

    def __str__(self):
        return "{} windowState({}) motionDetected({}) presenceDetected({}) sabotage({}) smokeDetectorAlarmType({}) dutyCycle({}) lowBat({}) powerMainsFailure({}) moistureDetected({}) waterlevelDetected({})".format(
            super().__str__(),
            self.windowState,
            self.motionDetected,
            self.presenceDetected,
            self.sabotage,
            self.smokeDetectorAlarmType,
            self.dutyCycle,
            self.lowBat,
            self.powerMainsFailure,
            self.moistureDetected,
            self.waterlevelDetected,
        )


class SwitchGroupBase(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.on = None
        self.dimLevel = None
        self.dutyCycle = None
        self.lowBat = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.set_attr_from_dict("on", js)
        self.set_attr_from_dict("dimLevel", js)
        self.set_attr_from_dict("dutyCycle", js)
        self.set_attr_from_dict("lowBat", js)

    def set_switch_state(self, on=True):
        data = {"groupId": self.id, "on": on}
        return self._restCall("group/switching/setState", body=json.dumps(data))

    def turn_on(self):
        return self.set_switch_state(True)

    def turn_off(self):
        return self.set_switch_state(False)

    def __str__(self):
        return f"{super().__str__()} on({self.on}) dimLevel({self.dimLevel}) dutyCycle({self.dutyCycle}) lowBat({self.lowBat})"


class SwitchingGroup(SwitchGroupBase):
    def __init__(self, connection):
        super().__init__(connection)
        self.processing = None
        self.shutterLevel = None
        self.slatsLevel = None
        self.primaryShadingLevel = 0.0
        self.primaryShadingStateType = ShadingStateType.NOT_EXISTENT
        self.processing = None
        self.secondaryShadingLevel = 0.0
        self.secondaryShadingStateType = ShadingStateType.NOT_EXISTENT

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.set_attr_from_dict("processing", js)
        self.set_attr_from_dict("shutterLevel", js)
        self.set_attr_from_dict("slatsLevel", js)
        self.set_attr_from_dict("primaryShadingLevel", js)
        self.set_attr_from_dict("primaryShadingStateType", js, ShadingStateType)
        self.set_attr_from_dict("secondaryShadingLevel", js)
        self.set_attr_from_dict("secondaryShadingStateType", js, ShadingStateType)

    def set_shutter_level(self, level):
        data = {"groupId": self.id, "shutterLevel": level}
        return self._restCall("group/switching/setShutterLevel", body=json.dumps(data))

    def set_slats_level(self, slatsLevel, shutterlevel):
        data = {
            "groupId": self.id,
            "shutterLevel": shutterlevel,
            "slatsLevel": slatsLevel,
        }
        return self._restCall("group/switching/setSlatsLevel", body=json.dumps(data))

    def set_shutter_stop(self):
        data = {"groupId": self.id}
        return self._restCall("group/switching/stop", body=json.dumps(data))

    def __str__(self):
        return f"{super().__str__()} processing({self.processing}) shutterLevel({self.shutterLevel}) slatsLevel({self.slatsLevel})"


class ShutterProfile(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.dutyCycle = None
        self.lowBat = None
        self.unreach = None

        self.processing = None
        self.shutterLevel = None
        self.slatsLevel = None
        self.primaryShadingLevel = 0.0
        self.primaryShadingStateType = ShadingStateType.NOT_EXISTENT
        self.processing = None
        self.secondaryShadingLevel = 0.0
        self.secondaryShadingStateType = ShadingStateType.NOT_EXISTENT
        self.profileMode = ProfileMode.MANUAL

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.set_attr_from_dict("dutyCycle", js)
        self.set_attr_from_dict("lowBat", js)
        self.set_attr_from_dict("unreach", js)

        self.set_attr_from_dict("profileMode", js, ProfileMode)

        self.set_attr_from_dict("processing", js)
        self.set_attr_from_dict("shutterLevel", js)
        self.set_attr_from_dict("slatsLevel", js)
        self.set_attr_from_dict("primaryShadingLevel", js)
        self.set_attr_from_dict("primaryShadingStateType", js, ShadingStateType)
        self.set_attr_from_dict("secondaryShadingLevel", js)
        self.set_attr_from_dict("secondaryShadingStateType", js, ShadingStateType)

    def set_profile_mode(self, profileMode: ProfileMode):
        data = {"groupId": self.id, "profileMode": profileMode}
        return self._restCall("group/heating/setProfileMode", body=json.dumps(data))

    def set_shutter_level(self, level):
        data = {"groupId": self.id, "shutterLevel": level}
        return self._restCall("group/switching/setShutterLevel", body=json.dumps(data))

    def set_slats_level(self, slatsLevel, shutterlevel):
        data = {
            "groupId": self.id,
            "shutterLevel": shutterlevel,
            "slatsLevel": slatsLevel,
        }
        return self._restCall("group/switching/setSlatsLevel", body=json.dumps(data))

    def set_shutter_stop(self):
        data = {"groupId": self.id}
        return self._restCall("group/switching/stop", body=json.dumps(data))

    def __str__(self):
        return (
            f"{super().__str__()} processing({self.processing}) shutterLevel({self.shutterLevel}) "
            f"slatsLevel({self.slatsLevel}) profileMode({self.profileMode})"
        )


class LinkedSwitchingGroup(Group):
    def set_light_group_switches(self, devices):
        switchChannels = []
        for d in devices:
            channel = {"channelIndex": 1, "deviceId": d.id}
            switchChannels.append(channel)
        data = {"groupId": self.id, "switchChannels": switchChannels}
        return self._restCall(
            "home/security/setLightGroupSwitches", body=json.dumps(data)
        )


class ExtendedLinkedSwitchingGroup(SwitchGroupBase):
    def __init__(self, connection):
        super().__init__(connection)
        self.onTime = None
        self.onLevel = None
        self.sensorSpecificParameters = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.onTime = js["onTime"]
        self.onLevel = js["onLevel"]
        self.sensorSpecificParameters = js["sensorSpecificParameters"]

    def __str__(self):
        return "{} onTime({}) onLevel({})".format(
            super().__str__(), self.onTime, self.onLevel
        )

    def set_on_time(self, onTimeSeconds):
        data = {"groupId": self.id, "onTime": onTimeSeconds}
        return self._restCall("group/switching/linked/setOnTime", body=json.dumps(data))


class ExtendedLinkedShutterGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.dutyCycle = None
        self.lowBat = None
        self.shutterLevel = None
        self.slatsLevel = None
        self.topSlatsLevel = None
        self.bottomSlatsLevel = None
        self.topShutterLevel = None
        self.bottomShutterLevel = None
        self.processing = None
        self.primaryShadingLevel = 0.0
        self.primaryShadingStateType = ShadingStateType.NOT_EXISTENT
        self.secondaryShadingLevel = 0.0
        self.secondaryShadingStateType = ShadingStateType.NOT_EXISTENT
        self.groupVisibility = GroupVisibility.INVISIBLE_GROUP_AND_CONTROL

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.set_attr_from_dict("dutyCycle", js)
        self.set_attr_from_dict("lowBat", js)
        self.set_attr_from_dict("groupVisibility", js, GroupVisibility)
        self.set_attr_from_dict("topSlatsLevel", js)
        self.set_attr_from_dict("bottomSlatsLevel", js)
        self.set_attr_from_dict("topShutterLevel", js)
        self.set_attr_from_dict("bottomShutterLevel", js)
        self.set_attr_from_dict("processing", js)
        self.set_attr_from_dict("shutterLevel", js)
        self.set_attr_from_dict("slatsLevel", js)
        self.set_attr_from_dict("primaryShadingLevel", js)
        self.set_attr_from_dict("primaryShadingStateType", js, ShadingStateType)
        self.set_attr_from_dict("secondaryShadingLevel", js)
        self.set_attr_from_dict("secondaryShadingStateType", js, ShadingStateType)

    def __str__(self):
        return "{} shutterLevel({}) slatsLevel({})".format(
            super().__str__(), self.shutterLevel, self.slatsLevel
        )

    def set_shutter_level(self, level):
        data = {"groupId": self.id, "shutterLevel": level}
        return self._restCall("group/switching/setShutterLevel", body=json.dumps(data))

    def set_slats_level(self, slatsLevel=0.0, shutterLevel=None):
        data = {
            "groupId": self.id,
            "shutterLevel": shutterLevel,
            "slatsLevel": slatsLevel,
        }
        return self._restCall("group/switching/setSlatsLevel", body=json.dumps(data))

    def set_shutter_stop(self):
        data = {"groupId": self.id}
        return self._restCall("group/switching/stop", body=json.dumps(data))


class AlarmSwitchingGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.on = None
        self.dimLevel = None
        self.onTime = None
        self.signalAcoustic = AcousticAlarmSignal.DISABLE_ACOUSTIC_SIGNAL
        self.signalOptical = OpticalAlarmSignal.DISABLE_OPTICAL_SIGNAL
        self.smokeDetectorAlarmType = SmokeDetectorAlarmType.IDLE_OFF
        self.acousticFeedbackEnabled = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.onTime = js["onTime"]
        self.on = js["on"]
        self.dimLevel = js["dimLevel"]
        self.signalAcoustic = AcousticAlarmSignal.from_str(js["signalAcoustic"])
        self.signalOptical = OpticalAlarmSignal.from_str(js["signalOptical"])
        self.smokeDetectorAlarmType = SmokeDetectorAlarmType.from_str(
            js["smokeDetectorAlarmType"]
        )
        self.acousticFeedbackEnabled = js["acousticFeedbackEnabled"]

    def set_on_time(self, onTimeSeconds):
        data = {"groupId": self.id, "onTime": onTimeSeconds}
        return self._restCall("group/switching/alarm/setOnTime", body=json.dumps(data))

    def __str__(self):
        return "{} on({}) dimLevel({}) onTime({}) signalAcoustic({}) signalOptical({}) smokeDetectorAlarmType({}) acousticFeedbackEnabled({})".format(
            super().__str__(),
            self.on,
            self.dimLevel,
            self.onTime,
            self.signalAcoustic,
            self.signalOptical,
            self.smokeDetectorAlarmType,
            self.acousticFeedbackEnabled,
        )

    def test_signal_optical(
        self, signalOptical=OpticalAlarmSignal.BLINKING_ALTERNATELY_REPEATING
    ):
        data = {"groupId": self.id, "signalOptical": str(signalOptical)}
        return self._restCall(
            "group/switching/alarm/testSignalOptical", body=json.dumps(data)
        )

    def set_signal_optical(
        self, signalOptical=OpticalAlarmSignal.BLINKING_ALTERNATELY_REPEATING
    ):
        data = {"groupId": self.id, "signalOptical": str(signalOptical)}
        return self._restCall(
            "group/switching/alarm/setSignalOptical", body=json.dumps(data)
        )

    def test_signal_acoustic(
        self, signalAcoustic=AcousticAlarmSignal.FREQUENCY_FALLING
    ):
        data = {"groupId": self.id, "signalAcoustic": str(signalAcoustic)}
        return self._restCall(
            "group/switching/alarm/testSignalAcoustic", body=json.dumps(data)
        )

    def set_signal_acoustic(self, signalAcoustic=AcousticAlarmSignal.FREQUENCY_FALLING):
        data = {"groupId": self.id, "signalAcoustic": str(signalAcoustic)}
        return self._restCall(
            "group/switching/alarm/setSignalAcoustic", body=json.dumps(data)
        )


# at the moment it doesn't look like this class has any special
# properties/functions
# keep it as a placeholder in the meantime
class HeatingHumidyLimiterGroup(Group):
    pass


# at the moment it doesn't look like this class has any special
# properties/functions
# keep it as a placeholder in the meantime
class HeatingTemperatureLimiterGroup(Group):
    pass


class HeatingChangeoverGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.on = None
        self.dimLevel = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.on = js["on"]

    def __str__(self):
        return "{} on({})".format(super().__str__(), self.on)


# at the moment it doesn't look like this class has any special
# properties/functions
# keep it as a placeholder in the meantime
class InboxGroup(Group):
    pass


class SecurityZoneGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.active = False
        self.silent = False
        self.ignorableDevices = []
        self.windowState = ""
        self.motionDetected = None
        self.sabotage = None
        self.presenceDetected = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.active = js["active"]
        self.silent = js["silent"]
        self.windowState = js["windowState"]
        self.motionDetected = js["motionDetected"]
        self.sabotage = js["sabotage"]
        self.ignorableDevices = []
        for device in js["ignorableDevices"]:
            self.ignorableDevices.append([d for d in devices if d.id == device][0])

    def __str__(self):
        return "{} active({}) silent({}) windowState({}) motionDetected({}) sabotage({}) presenceDetected({}) ignorableDevices(#{})".format(
            super().__str__(),
            self.active,
            self.silent,
            self.windowState,
            self.motionDetected,
            self.sabotage,
            self.presenceDetected,
            len(self.ignorableDevices),
        )


class HeatingCoolingPeriod(HomeMaticIPObject):
    def __init__(self, connection):
        super().__init__(connection)
        self.starttime = None
        self.endtime = None
        self.value = None

    def from_json(self, js):
        super().from_json(js)
        self.starttime = js["starttime"]
        self.endtime = js["endtime"]
        self.value = js["value"]


class HeatingCoolingProfileDay(HomeMaticIPObject):
    def __init__(self, connection):
        super().__init__(connection)
        self.baseValue = None
        self.periods = None

    def from_json(self, js):
        super().from_json(js)
        self.baseValue = js["baseValue"]
        self.periods = []
        for p in js["periods"]:
            period = HeatingCoolingPeriod(self._connection)
            period.from_json(p)
            self.periods.append(period)


class HeatingCoolingProfile(HomeMaticIPObject):
    def __init__(self, connection):
        super().__init__(connection)
        self.id = None
        self.homeId = None

        self.groupId = None
        self.index = None
        self.visible = None
        self.enabled = None

        self.name = None
        self.type = None
        self.profileDays = None

    def get_details(self):
        data = {
            "groupId": self.groupId,
            "profileIndex": self.index,
            "profileName": self.name,
        }
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
                periods.append(
                    {
                        "endtime": p.endtime,
                        "starttime": p.starttime,
                        "value": p.value,
                        "endtimeAsMinutesOfDay": self._time_to_totalminutes(p.endtime),
                        "starttimeAsMinutesOfDay": self._time_to_totalminutes(
                            p.starttime
                        ),
                    }
                )

            dayOfWeek = calendar.day_name[i].upper()
            days[dayOfWeek] = {
                "baseValue": day.baseValue,
                "dayOfWeek": dayOfWeek,
                "periods": periods,
            }

        data = {
            "groupId": self.groupId,
            "profile": {
                "groupId": self.groupId,
                "homeId": self.homeId,
                "id": self.id,
                "index": self.index,
                "name": self.name,
                "profileDays": days,
                "type": self.type,
            },
            "profileIndex": self.index,
        }
        return self._restCall("group/heating/updateProfile", body=json.dumps(data))


class HeatingGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.windowOpenTemperature = None
        self.setPointTemperature = None
        self.windowState = None
        self.maxTemperature = None
        self.minTemperature = None
        self.cooling = None
        self.partyMode = None
        self.controlMode = ClimateControlMode.AUTOMATIC
        self.activeProfile = None
        self.boostMode = None
        self.boostDuration = None
        self.actualTemperature = None
        self.humidity = None
        self.coolingAllowed = None
        self.coolingIgnored = None
        self.ecoAllowed = None
        self.ecoIgnored = None
        self.controllable = None
        self.floorHeatingMode = None
        self.humidityLimitEnabled = None
        self.humidityLimitValue = None
        self.externalClockEnabled = None
        self.externalClockHeatingTemperature = None
        self.externalClockCoolingTemperature = None
        self.profiles = None
        self.dutyCycle = False
        self.lowBat = False
        self.valvePosition = 0.0
        self.heatingFailureSupported = False
        self.valveSilentModeEnabled = False
        self.valveSilentModeSupported = False
        self.lastSetPointReachedTimestamp = None
        self.lastSetPointUpdatedTimestamp = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.windowOpenTemperature = js["windowOpenTemperature"]
        self.setPointTemperature = js["setPointTemperature"]
        self.windowState = js["windowState"]
        self.maxTemperature = js["maxTemperature"]
        self.minTemperature = js["minTemperature"]
        self.cooling = js["cooling"]
        self.partyMode = js["partyMode"]
        self.controlMode = ClimateControlMode.from_str(js["controlMode"])
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
        self.dutyCycle = js["dutyCycle"]
        self.lowBat = js["lowBat"]
        self.valvePosition = js["valvePosition"]
        self.heatingFailureSupported = js["heatingFailureSupported"]
        self.valveSilentModeEnabled = js["valveSilentModeEnabled"]
        self.valveSilentModeSupported = js["valveSilentModeSupported"]
        self.lastSetPointReachedTimestamp = self.fromtimestamp(
            js["lastSetPointReachedTimestamp"]
        )
        self.lastSetPointUpdatedTimestamp = self.fromtimestamp(
            js["lastSetPointUpdatedTimestamp"]
        )

        profiles = []
        activeProfile = js["activeProfile"]  # not self.!!!!
        for k, v in js["profiles"].items():
            profile = HeatingCoolingProfile(self._connection)
            profile.from_json(v)
            profiles.append(profile)
            if activeProfile == k:
                self.activeProfile = profile
        self.profiles = sorted(profiles, key=attrgetter("index"))

    def __str__(self):
        return "{} windowOpenTemperature({}) setPointTemperature({}) windowState({}) motionDetected({}) sabotage({}) cooling({}) partyMode({}) controlMode({}) actualTemperature({}) valvePosition({})".format(
            super().__str__(),
            self.windowOpenTemperature,
            self.setPointTemperature,
            self.windowState,
            self.maxTemperature,
            self.minTemperature,
            self.cooling,
            self.partyMode,
            self.controlMode,
            self.actualTemperature,
            self.valvePosition,
        )

    def set_point_temperature(self, temperature):
        data = {"groupId": self.id, "setPointTemperature": temperature}
        return self._restCall(
            "group/heating/setSetPointTemperature", body=json.dumps(data)
        )

    def set_boost(self, enable=True):
        data = {"groupId": self.id, "boost": enable}
        return self._restCall("group/heating/setBoost", body=json.dumps(data))

    def set_boost_duration(self, duration: int):
        data = {"groupId": self.id, "boostDuration": duration}
        return self._restCall("group/heating/setBoostDuration", body=json.dumps(data))

    def set_active_profile(self, index):
        data = {"groupId": self.id, "profileIndex": index}
        return self._restCall("group/heating/setActiveProfile", body=json.dumps(data))

    def set_control_mode(self, mode=ClimateControlMode.AUTOMATIC):
        data = {"groupId": self.id, "controlMode": str(mode)}
        return self._restCall("group/heating/setControlMode", body=json.dumps(data))


class HeatingDehumidifierGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.on = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.on = js["on"]

    def __str__(self):
        return "{} on({})".format(super().__str__(), self.on)


class HeatingCoolingDemandGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.on = None
        self.dimLevel = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.on = js["on"]
        self.dimLevel = js["dimLevel"]

    def __str__(self):
        return "{} on({}) dimLevel({}) ".format(
            super().__str__(), self.on, self.dimLevel
        )


class HeatingFailureAlertRuleGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        #:bool: is this rule active
        self.enabled = False
        #:HeatingFailureValidationType: the heating failure value
        self.heatingFailureValidationResult = (
            HeatingFailureValidationType.NO_HEATING_FAILURE
        )
        #:int:how often the system will check for an error
        self.checkInterval = 0
        #:int:time in ms for the validation period. default 24Hours
        self.validationTimeout = 0
        #:datetime: last time of execution
        self.lastExecutionTimestamp = 0

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.enabled = js["enabled"]
        self.heatingFailureValidationResult = HeatingFailureValidationType.from_str(
            js["heatingFailureValidationResult"]
        )
        self.checkInterval = js["checkInterval"]
        self.validationTimeout = js["validationTimeout"]
        self.lastExecutionTimestamp = self.fromtimestamp(js["lastExecutionTimestamp"])

    def __str__(self):
        return (
            "{} enabled({}) heatingFailureValidationResult({}) "
            "checkInterval({}) validationTimeout({}) lastExecutionTimestamp({})"
        ).format(
            super().__str__(),
            self.enabled,
            self.heatingFailureValidationResult,
            self.checkInterval,
            self.validationTimeout,
            self.lastExecutionTimestamp,
        )


class HumidityWarningRuleGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        #:bool: is this rule active
        self.enabled = False
        #:HumidityValidationType: the current humidity result
        self.humidityValidationResult = (
            HumidityValidationType.GREATER_LOWER_LESSER_UPPER_THRESHOLD
        )
        #:int:the lower humidity threshold
        self.humidityLowerThreshold = 0
        #:int:the upper humidity threshold
        self.humidityUpperThreshold = 0
        #:bool:is it currently triggered?
        self.triggered = False
        #:bool:should the windows be opened?
        self.ventilationRecommended = False
        #:datetime: last time of execution
        self.lastExecutionTimestamp = None
        #:datetime: last time the humidity got updated
        self.lastStatusUpdate = None
        #:Device: the climate sensor which get used as an outside reference. None if OpenWeatherMap will be used
        self.outdoorClimateSensor = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.enabled = js["enabled"]
        self.humidityValidationResult = HumidityValidationType.from_str(
            js["humidityValidationResult"]
        )
        self.humidityLowerThreshold = js["humidityLowerThreshold"]
        self.humidityUpperThreshold = js["humidityUpperThreshold"]
        self.triggered = js["triggered"]
        self.ventilationRecommended = js["ventilationRecommended"]
        self.lastExecutionTimestamp = self.fromtimestamp(js["lastExecutionTimestamp"])
        self.lastStatusUpdate = self.fromtimestamp(js["lastStatusUpdate"])

        jsOutdoorClimateSensor = js["outdoorClimateSensor"]
        if jsOutdoorClimateSensor != None:
            did = jsOutdoorClimateSensor["deviceId"]
            for d in devices:
                if d.id == did:
                    self.outdoorClimateSensor = d
                    break

    def __str__(self):
        return (
            "{} enabled({}) humidityValidationResult({}) "
            "humidityLowerThreshold({}) humidityUpperThreshold({}) "
            "triggered({}) lastExecutionTimestamp({}) "
            "lastStatusUpdate({}) ventilationRecommended({})"
        ).format(
            super().__str__(),
            self.enabled,
            self.humidityValidationResult,
            self.humidityLowerThreshold,
            self.humidityUpperThreshold,
            self.triggered,
            self.lastExecutionTimestamp,
            self.lastStatusUpdate,
            self.ventilationRecommended,
        )


# at the moment it doesn't look like this class has any special
# properties/functions
# keep it as a placeholder in the meantime
class HeatingExternalClockGroup(Group):
    pass


class HeatingCoolingDemandBoilerGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.boilerFollowUpTime = None
        self.boilerLeadTime = None
        self.on = None
        self.dimLevel = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.on = js["on"]
        self.boilerLeadTime = js["boilerLeadTime"]
        self.boilerFollowUpTime = js["boilerFollowUpTime"]

    def __str__(self):
        return "{} on({}) boilerFollowUpTime({}) boilerLeadTime({})".format(
            super().__str__(), self.on, self.boilerFollowUpTime, self.boilerLeadTime
        )


class HeatingCoolingDemandPumpGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.pumpProtectionDuration = 0
        self.pumpProtectionSwitchingInterval = 0
        self.pumpFollowUpTime = 0
        self.pumpLeadTime = 0
        self.on = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.on = js["on"]
        self.pumpProtectionSwitchingInterval = js["pumpProtectionSwitchingInterval"]
        self.pumpProtectionDuration = js["pumpProtectionDuration"]
        self.pumpFollowUpTime = js["pumpFollowUpTime"]
        self.pumpLeadTime = js["pumpLeadTime"]

    def __str__(self):
        return (
            "{} on({}) pumpProtectionDuration({}) pumpProtectionSwitchingInterval({}) pumpFollowUpTime({}) "
            "pumpLeadTime({})".format(
                super().__str__(),
                self.on,
                self.pumpProtectionDuration,
                self.pumpProtectionSwitchingInterval,
                self.pumpFollowUpTime,
                self.pumpLeadTime,
            )
        )


class TimeProfilePeriod(HomeMaticIPObject):
    def __init__(self, connection):
        super().__init__(connection)
        self.weekdays = []
        self.hour = 0
        self.minute = 0
        self.astroOffset = 0
        self.astroLimitationType = (
            "NO_LIMITATION"  # NOT_EARLIER_THAN_TIME, NOT_LATER_THAN_TIME
        )
        self.switchTimeMode = (
            "REGULAR_SWITCH_TIME"  # ASTRO_SUNRISE_SWITCH_TIME, ASTRO_SUNSET_SWITCH_TIME
        )
        self.dimLevel = 1.0
        self.rampTime = 0

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


class TimeProfile(HomeMaticIPObject):
    def __init__(self, connection):
        super().__init__(connection)
        self.id = None
        self.homeId = None
        self.groupId = None
        self.type = None
        self.periods = []

    def get_details(self):
        data = {"groupId": self.groupId}
        js = self._restCall("group/switching/profile/getProfile", body=json.dumps(data))
        self.homeId = js["homeId"]
        self.type = js["type"]
        self.id = js["id"]
        self.periods = []
        for p in js["periods"]:
            period = TimeProfilePeriod(self._connection)
            period.from_json(p)
            self.periods.append(period)


class SwitchingProfileGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.on = None
        self.dimLevel = None
        self.profileId = (
            None  # Not sure why it is there.  You can't use it to query something.
        )
        self.profileMode = ProfileMode.MANUAL

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.set_attr_from_dict("on", js)
        self.set_attr_from_dict("dimLevel", js)
        self.set_attr_from_dict("profileId", js)
        self.set_attr_from_dict("profileMode", js, ProfileMode)

    def __str__(self):
        return "{} on({}) dimLevel({}) profileMode({})".format(
            super().__str__(), self.on, self.dimLevel, self.profileMode
        )

    def set_group_channels(self):
        channels = []
        for d in self.devices:
            channels.append[{"channelIndex": 1, "deviceId": d.id}]
        data = {"groupId": self.id, "channels": channels}
        return self._restCall(
            "group/switching/profile/setGroupChannels", body=json.dumps(data)
        )

    def set_profile_mode(self, devices, automatic=True):
        channels = []
        for d in devices:
            channels.append[{"channelIndex": 1, "deviceId": d.id}]
        data = {
            "groupId": self.id,
            "channels": channels,
            "profileMode": ProfileMode.AUTOMATIC if automatic else ProfileMode.MANUAL,
        }
        return self._restCall(
            "group/switching/profile/setProfileMode", body=json.dumps(data)
        )

    def create(self, label):
        data = {"label": label}
        result = self._restCall(
            "group/switching/profile/createSwitchingProfileGroup", body=json.dumps(data)
        )
        if "groupId" in result:
            self.id = result["groupId"]
        return result


class OverHeatProtectionRule(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.temperatureLowerThreshold = None
        self.temperatureUpperThreshold = None
        self.targetShutterLevel = None
        self.targetSlatsLevel = None
        self.startHour = None
        self.startMinute = None
        self.startSunrise = None
        self.endHour = None
        self.endMinute = None
        self.endSunset = None

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
        return "{} tempLower({}) tempUpper({}) targetShutterLevel({}) targetSlatsLevel({})".format(
            super().__str__(),
            self.temperatureLowerThreshold,
            self.temperatureUpperThreshold,
            self.targetShutterLevel,
            self.targetSlatsLevel,
        )


class SmokeAlarmDetectionRule(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.smokeDetectorAlarmType = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.smokeDetectorAlarmType = js["smokeDetectorAlarmType"]

    def __str__(self):
        return "{} smokeDetectorAlarmType({})".format(
            super().__str__(), self.smokeDetectorAlarmType
        )


class ShutterWindProtectionRule(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.windSpeedThreshold = None
        self.targetShutterLevel = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.windSpeedThreshold = js["windSpeedThreshold"]
        self.targetShutterLevel = js["targetShutterLevel"]

    def __str__(self):
        return "{} windSpeedThreshold({}) targetShutterLevel({})".format(
            super().__str__(), self.windSpeedThreshold, self.targetShutterLevel
        )


class LockOutProtectionRule(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.triggered = None
        self.windowState = None

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.triggered = js["triggered"]
        self.windowState = js["windowState"]

    def __str__(self):
        return "{} triggered({}) windowState({})".format(
            super().__str__(), self.triggered, self.windowState
        )


class EnvironmentGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.actualTemperature = 0.0
        self.illumination = 0.0
        self.raining = False
        self.windSpeed = 0.0
        self.humidity = 0.0

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.actualTemperature = js["actualTemperature"]
        self.illumination = js["illumination"]
        self.raining = js["raining"]
        self.windSpeed = js["windSpeed"]
        self.humidity = js["humidity"]

    def __str__(self):
        return "{} actualTemperature({}) illumination({}) raining({}) windSpeed({}) humidity({})".format(
            super().__str__(),
            self.actualTemperature,
            self.illumination,
            self.raining,
            self.windSpeed,
            self.humidity,
        )


class HotWaterGroup(Group):
    def __init__(self, connection):
        super().__init__(connection)
        self.on = None
        self.onTime = 0.0
        self.profileId = (
            None  # Not sure why it is there.  You can't use it to query something.
        )
        self.profileMode = ProfileMode.MANUAL

    def from_json(self, js, devices):
        super().from_json(js, devices)
        self.set_attr_from_dict("on", js)
        self.set_attr_from_dict("onTime", js)
        self.set_attr_from_dict("profileId", js)
        self.set_attr_from_dict("profileMode", js, ProfileMode)

    def __str__(self):
        return f"{super().__str__()} on({self.on}) onTime({self.onTime}) profileMode({self.profileMode})"

    def set_profile_mode(self, profileMode: ProfileMode):
        data = {"groupId": self.id, "profileMode": profileMode}
        return self._restCall("group/heating/setProfileMode", body=json.dumps(data))
