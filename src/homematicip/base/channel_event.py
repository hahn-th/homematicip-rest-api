from dataclasses import dataclass


@dataclass
class ChannelEvent:
    """Class to hold a channel event."""

    pushEventType: str | None = None
    deviceId: str | None = None
    channelIndex: int | None = None
    channelEventType: str | None = None

    # {
    #     "pushEventType": "DEVICE_CHANNEL_EVENT",
    #     "deviceId": "xxx",
    #     "channelIndex": 1,
    #     "channelEventType": "DOOR_BELL_SENSOR_EVENT",
    # }
