# coding=utf-8
import json
from datetime import datetime

from homematicip.base.HomeMaticIPObject import HomeMaticIPObject


class SecurityEvent(HomeMaticIPObject):
    """this class represents a security event """

    def __init__(self, connection):
        super().__init__(connection)
        self.eventTimestamp = None
        self.eventType = None
        self.label = None

    def from_json(self, js):
        super().from_json(js)
        self.label = js["label"]
        time = js["eventTimestamp"]
        if time > 0:
            self.eventTimestamp = datetime.fromtimestamp(time / 1000.0)
        else:
            self.eventTimestamp = None
        self.eventType = js["eventType"]

    def __str__(self):
        return "{} {} {}".format(
            self.eventType,
            self.label,
            self.eventTimestamp.strftime("%Y.%m.%d %H:%M:%S"),
        )


class SecurityZoneEvent(SecurityEvent):
    """ This class will be used by other events which are just adding "securityZoneValues" """

    def __init__(self, connection):
        super().__init__(connection)
        self.external_zone = None
        self.internal_zone = None

    def from_json(self, js):
        super().from_json(js)
        self.external_zone = js["securityZoneValues"]["EXTERNAL"]
        self.internal_zone = js["securityZoneValues"]["INTERNAL"]

    def __str__(self):
        return "{} external_zone({}) internal_zone({}) ".format(
            super().__str__(), self.external_zone, self.internal_zone
        )


class SensorEvent(SecurityEvent):
    pass


class AccessPointDisconnectedEvent(SecurityEvent):
    pass


class AccessPointConnectedEvent(SecurityEvent):
    pass


class ActivationChangedEvent(SecurityZoneEvent):
    pass


class SilenceChangedEvent(SecurityZoneEvent):
    pass


class SabotageEvent(SecurityEvent):
    pass


class MoistureDetectionEvent(SecurityEvent):
    pass


class SmokeAlarmEvent(SecurityEvent):
    pass


class ExternalTriggeredEvent(SecurityEvent):
    pass


class OfflineAlarmEvent(SecurityEvent):
    pass


class WaterDetectionEvent(SecurityEvent):
    pass


class MainsFailureEvent(SecurityEvent):
    pass


class OfflineWaterDetectionEvent(SecurityEvent):
    pass
