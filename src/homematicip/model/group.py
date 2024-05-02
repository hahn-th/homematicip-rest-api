from typing import Optional

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
