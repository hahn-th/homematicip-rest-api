from homematicip.group import Group

from typing import Iterable

class FunctionalChannel():
    """ this is the base class for the functional channels """

    def __init__(self):
        self.index = -1
        self.groupIndex = -1
        self.label = ""
        self.groupIndex = -1

        self.groups = Iterable[Group]

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        self.index = js["index"]
        self.groupIndex = js["groupIndex"]
        self.label = js["label"]

        self.groups = []
        for id in js["groups"]:
            for g in groups:
                if g.id == id:
                    self.groups.append(g)
                    break

class DeviceBaseChannel(FunctionalChannel):
    """ this is the representive of the DEVICE_BASE channel"""
    def __init__(self):
        super().__init__()
        self.unreach = None
        self.lowBat = None
        self.routerModuleSupported = False
        self.routerModuleEnabled = False
        self.rssiDeviceValue = 0
        self.rssiPeerValue = 0
        self.dutyCycle = False
        self.configPending = False

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.unreach = js["unreach"]
        self.lowBat = js["lowBat"]
        self.routerModuleSupported = js["routerModuleSupported"]
        self.routerModuleEnabled = js["routerModuleEnabled"]
        self.rssiDeviceValue = js["rssiDeviceValue"]
        self.rssiPeerValue = js["rssiPeerValue"]
        self.dutyCycle = js["dutyCycle"]
        self.configPending = js["configPending"]

class DeviceSabotageChannel(DeviceBaseChannel):
    """ this is the representive of the DEVICE_SABOTAGE channel"""
    def __init__(self):
        super().__init__()
        self.sabotage = False

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.sabotage = js["sabotage"]

class DeviceOperationLockChannel(DeviceBaseChannel):
    """ this is the representive of the DEVICE_OPERATIONLOCK channel"""
    def __init__(self):
        super().__init__()
        self.operationLockActive = False

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.operationLockActive = js["operationLockActive"]