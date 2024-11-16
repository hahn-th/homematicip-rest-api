from dataclasses import dataclass


@dataclass
class ChannelEvent:
    """Class to hold a channel event."""

    pushEventType: str
    deviceId: str
    channelIndex: int
    channelEventType: str

    # {
    #     "pushEventType": "DEVICE_CHANNEL_EVENT",
    #     "deviceId": "xxx",
    #     "channelIndex": 1,
    #     "channelEventType": "DOOR_BELL_SENSOR_EVENT",
    # }
