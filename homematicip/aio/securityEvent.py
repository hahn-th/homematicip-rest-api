from datetime import datetime

from homematicip.securityEvent import *


class AsyncSecurityEvent(SecurityEvent):
    """this class represents a security event """

    pass


class AsyncSecurityZoneEvent(SecurityZoneEvent, AsyncSecurityEvent):
    """ This class will be used by other events which are just adding "securityZoneValues" """

    pass


class AsyncSensorEvent(SensorEvent, AsyncSecurityEvent):
    pass


class AsyncAccessPointDisconnectedEvent(
    AccessPointDisconnectedEvent, AsyncSecurityEvent
):
    pass


class AsyncAccessPointConnectedEvent(AccessPointConnectedEvent, AsyncSecurityEvent):
    pass


class AsyncActivationChangedEvent(ActivationChangedEvent, AsyncSecurityZoneEvent):
    pass


class AsyncSilenceChangedEvent(SilenceChangedEvent, AsyncSecurityZoneEvent):
    pass


class AsyncSabotageEvent(SabotageEvent, AsyncSecurityEvent):
    pass


class AsyncMoistureDetectionEvent(MoistureDetectionEvent, AsyncSecurityEvent):
    pass


class AsyncSmokeAlarmEvent(SmokeAlarmEvent, AsyncSecurityEvent):
    pass


class AsyncExternalTriggeredEvent(ExternalTriggeredEvent, AsyncSecurityEvent):
    pass


class AsyncOfflineAlarmEvent(OfflineAlarmEvent, AsyncSecurityEvent):
    pass


class AsyncWaterDetectionEvent(WaterDetectionEvent, AsyncSecurityEvent):
    pass


class AsyncMainsFailureEvent(MainsFailureEvent, AsyncSecurityEvent):
    pass


class AsyncOfflineWaterDetectionEvent(OfflineWaterDetectionEvent, AsyncSecurityEvent):
    pass
