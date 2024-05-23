from typing import Optional

from homematicip.model.enums import ConnectionType, DeviceArchetype
from homematicip.model.hmip_base import HmipBaseModel


class GroupChannelReference(HmipBaseModel):
    channelIndex: int
    deviceId: str


class Group(HmipBaseModel):
    id: str = None
    homeId: str = None
    label: Optional[str] = None
    lastStatusUpdate: Optional[int] = None
    type: str = None
    unreach: Optional[bool] = None
    metaGroupId: Optional[str] = None
    channels: list[GroupChannelReference]


class FunctionalChannel(HmipBaseModel):
    """this is the base class for the functional channels"""

    index: int = -1
    groupIndex: int = -1
    label: str = ""
    functionalChannelType: str = ""
    groups: list[str]
    deviceId: str = None
    channelRole: Optional[str] = None


class Device(HmipBaseModel):
    availableFirmwareVersion: Optional[str] = None
    connectionType: Optional[ConnectionType] = ConnectionType.HMIP_LAN
    deviceArchetype: Optional[DeviceArchetype] = DeviceArchetype.HMIP
    deviceType: str = None
    firmwareVersion: Optional[str] = None
    firmwareVersionInteger: Optional[int] = None
    functionalChannels: dict[str, FunctionalChannel]
    homeId: str = None
    id: str = None
    label: Optional[str] = None
    lastStatusUpdate: Optional[int] = None
    liveUpdateState: Optional[str] = None
    manuallyUpdateForced: Optional[bool] = False
    manufacturerCode: Optional[int] = None
    modelId: Optional[int] = None
    modelType: Optional[str] = ""
    oem: Optional[str] = ""
    permanentlyReachable: Optional[bool] = False
    serializedGlobalTradeItemNumber: Optional[str] = ""
    type: str = ""
    updateState: Optional[str] = ""

    # base_channel: FunctionalChannel = None


class Client(HmipBaseModel):
    homeId: str = ""
    id: str = ""
    label: str = ""
    clientType: str = ""
