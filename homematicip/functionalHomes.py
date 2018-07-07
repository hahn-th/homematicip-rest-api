from typing import List

from homematicip.HomeMaticIPObject import HomeMaticIPObject
from homematicip.group import Group
from homematicip.base.enums import *


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

        self.functionalGroups = []
        for gid in js["functionalGroups"]:
            for g in groups:
                if g.id == gid:
                    self.functionalGroups.append(g)

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
        self.absenceEndTime = self.fromtimestamp(js["absenceEndTime"])
        self.absenceType = AbsenceType(js["absenceType"])
        self.coolingEnabled = js["coolingEnabled"]
        self.ecoDuration = js["ecoDuration"]
        self.ecoTemperature = js["ecoTemperature"]
        self.optimumStartStopEnabled = js["optimumStartStopEnabled"]
        
        self.floorHeatingSpecificGroups = []
        for type,gid in js["floorHeatingSpecificGroups"].items():
            for g in groups:
                if g.id == gid:
                    self.floorHeatingSpecificGroups.append(g)

class WeatherAndEnvironmentHome(FunctionalHome):
    pass