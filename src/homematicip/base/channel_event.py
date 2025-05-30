from dataclasses import dataclass


@dataclass()
class ChannelEvent:
    """Class to hold a channel event."""

    pushEventType: str | None = None
    deviceId: str | None = None
    channelIndex: int | None = None
    channelEventType: str | None = None
    functionalChannelIndex: int | None = None

    def from_json(self, data: dict) -> None:
        """Create a ChannelEvent from a JSON dictionary."""
        self.pushEventType = data.get("pushEventType")
        self.deviceId = data.get("deviceId")
        self.channelIndex = data.get("channelIndex")
        self.channelEventType = data.get("channelEventType")
        self.functionalChannelIndex = data.get("functionalChannelIndex")

        if self.channelIndex is None:
            self.channelIndex = self.functionalChannelIndex

    # {
    #     "pushEventType": "DEVICE_CHANNEL_EVENT",
    #     "deviceId": "xxx",
    #     "channelIndex": 1,
    #     "channelEventType": "DOOR_BELL_SENSOR_EVENT",
    # }
