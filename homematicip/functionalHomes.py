from datetime import datetime
from typing import List

from homematicip.base.enums import *
from homematicip.base.HomeMaticIPObject import HomeMaticIPObject
from homematicip.group import Group


class FunctionalHome(HomeMaticIPObject):
    def __init__(self, connection):
        super().__init__(connection)

        self.functionalGroups = List[Group]
        self.solution = ""
        self.active = False

    def from_json(self, js, groups: List[Group]):
        super().from_json(js)

        self.solution = js["solution"]
        self.active = js["active"]

        self.functionalGroups = self.assignGroups(js["functionalGroups"], groups)

    def assignGroups(self, gids, groups: List[Group]):
        ret = []
        for gid in gids:
            for g in groups:
                if g.id == gid:
                    ret.append(g)
        return ret


class IndoorClimateHome(FunctionalHome):
    def __init__(self, connection):
        super().__init__(connection)
        self.absenceEndTime = None
        self.absenceType = AbsenceType.NOT_ABSENT
        self.coolingEnabled = False
        self.ecoDuration = EcoDuration.PERMANENT
        self.ecoTemperature = 0.0
        self.optimumStartStopEnabled = False
        self.floorHeatingSpecificGroups = []

    def from_json(self, js, groups: List[Group]):
        super().from_json(js, groups)
        if js["absenceEndTime"] is None:
            self.absenceEndTime = None
        else:
            # Why can't EQ-3 use the timestamp here like everywhere else -.-
            self.absenceEndTime = datetime.strptime(
                js["absenceEndTime"], "%Y_%m_%d %H:%M"
            )
        self.absenceType = AbsenceType.from_str(js["absenceType"])
        self.coolingEnabled = js["coolingEnabled"]
        self.ecoDuration = EcoDuration.from_str(js["ecoDuration"])
        self.ecoTemperature = js["ecoTemperature"]
        self.optimumStartStopEnabled = js["optimumStartStopEnabled"]

        self.floorHeatingSpecificGroups = self.assignGroups(
            js["floorHeatingSpecificGroups"].values(), groups
        )


class WeatherAndEnvironmentHome(FunctionalHome):
    pass


class LightAndShadowHome(FunctionalHome):
    def __init__(self, connection):
        super().__init__(connection)
        self.extendedLinkedShutterGroups = []
        self.extendedLinkedSwitchingGroups = []
        self.shutterProfileGroups = []
        self.switchingProfileGroups = []

    def from_json(self, js, groups: List[Group]):
        super().from_json(js, groups)

        self.extendedLinkedShutterGroups = self.assignGroups(
            js["extendedLinkedShutterGroups"], groups
        )
        self.extendedLinkedSwitchingGroups = self.assignGroups(
            js["extendedLinkedSwitchingGroups"], groups
        )
        self.shutterProfileGroups = self.assignGroups(
            js["shutterProfileGroups"], groups
        )
        self.switchingProfileGroups = self.assignGroups(
            js["switchingProfileGroups"], groups
        )


class SecurityAndAlarmHome(FunctionalHome):
    def __init__(self, connection):
        super().__init__(connection)
        self.activationInProgress = False
        self.alarmActive = False
        self.alarmEventDeviceId = ""
        self.alarmEventTimestamp = None
        self.intrusionAlertThroughSmokeDetectors = False
        self.zoneActivationDelay = 0.0
        self.securityZoneActivationMode = (
            SecurityZoneActivationMode.ACTIVATION_WITH_DEVICE_IGNORELIST
        )

        self.securitySwitchingGroups = []
        self.securityZones = []

    def from_json(self, js, groups: List[Group]):
        super().from_json(js, groups)
        self.activationInProgress = js["activationInProgress"]
        self.alarmActive = js["alarmActive"]
        if js["alarmEventDeviceChannel"] != None:
            self.alarmEventDeviceId = js["alarmEventDeviceChannel"]["deviceId"]
        self.alarmEventTimestamp = self.fromtimestamp(js["alarmEventTimestamp"])
        self.intrusionAlertThroughSmokeDetectors = js[
            "intrusionAlertThroughSmokeDetectors"
        ]
        self.zoneActivationDelay = js["zoneActivationDelay"]
        self.securityZoneActivationMode = SecurityZoneActivationMode.from_str(
            js["securityZoneActivationMode"]
        )

        self.securitySwitchingGroups = self.assignGroups(
            js["securitySwitchingGroups"].values(), groups
        )
        self.securityZones = self.assignGroups(js["securityZones"].values(), groups)


class AccessControlHome(FunctionalHome):
    def __init__(self, connection):
        super().__init__(connection)
        self.accessAuthorizationProfileGroups = []
        self.lockProfileGroups = []
        self.autoRelockProfileGroups = []
        self.extendedLinkedGarageDoorGroups = []
        self.extendedLinkedNotificationGroups = []

    def from_json(self, js, groups: List[Group]):
        super().from_json(js, groups)
        self.accessAuthorizationProfileGroups = self.assignGroups(
            js["accessAuthorizationProfileGroups"], groups
        )
        self.lockProfileGroups = self.assignGroups(js["lockProfileGroups"], groups)
        self.autoRelockProfileGroups = self.assignGroups(
            js["autoRelockProfileGroups"], groups
        )
        self.extendedLinkedGarageDoorGroups = self.assignGroups(
            js["extendedLinkedGarageDoorGroups"], groups
        )
        self.extendedLinkedNotificationGroups = self.assignGroups(
            js["extendedLinkedNotificationGroups"], groups
        )
