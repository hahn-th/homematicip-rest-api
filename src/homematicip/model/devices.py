from typing import Optional

from pydantic import BaseModel

from homematicip.model.enums import ConnectionType, DeviceArchetype
from homematicip.model.functional_channels import FunctionalChannel
from homematicip.model.hmip_base import HmipBaseModel


class ModelDeviceBase(BaseModel):
    pass


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
