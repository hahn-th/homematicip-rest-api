from datetime import datetime

from homematicip.securityEvent import SecurityEvent, SecurityZoneEvent, SensorEvent, \
    AccessPointDisconnectedEvent, AccessPointConnectedEvent, ActivationChangedEvent, \
    SilenceChangedEvent


class AsyncSecurityEvent(SecurityEvent):
    """this class represents a security event """
    pass


class AsyncSecurityZoneEvent(SecurityZoneEvent, AsyncSecurityEvent):
    """ This class will be used by other events which are just adding "securityZoneValues" """
    pass


class AsyncSensorEvent(SensorEvent, AsyncSecurityEvent):
    pass


class AsyncAccessPointDisconnectedEvent(AccessPointDisconnectedEvent, AsyncSecurityEvent):
    pass


class AsyncAccessPointConnectedEvent(AccessPointConnectedEvent, AsyncSecurityEvent):
    pass


class AsyncActivationChangedEvent(ActivationChangedEvent, AsyncSecurityZoneEvent):
    pass


class AsyncSilenceChangedEvent(SilenceChangedEvent, AsyncSecurityZoneEvent):
    pass
