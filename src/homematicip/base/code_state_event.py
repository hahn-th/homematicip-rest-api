from dataclasses import dataclass


@dataclass()
class CodeStateEvent:
    """Class to hold a device code state event (HmIP-WKP keypad)."""

    pushEventType: str | None = None
    deviceId: str | None = None
    codeIndex: int | None = None
    codeState: str | None = None

    def from_json(self, data: dict) -> None:
        """Create a CodeStateEvent from a JSON dictionary."""
        self.pushEventType = data.get("pushEventType")
        self.deviceId = data.get("deviceId")
        self.codeIndex = data.get("codeIndex")
        self.codeState = data.get("codeState")

    # {
    #     "pushEventType": "DEVICE_CODE_STATE_EVENT",
    #     "deviceId": "xxx",
    #     "codeIndex": 1,
    #     "codeState": "KNOWN_CODE_ID_RECEIVED",
    # }
