from homematicip.base.homematicip_object import HomeMaticIPObject
from homematicip.base.enums import DeviceUpdateState


class AccessPointUpdateState(HomeMaticIPObject):
    def __init__(self, connection):
        super().__init__(connection)
        self.accessPointUpdateState = DeviceUpdateState.UP_TO_DATE
        self.successfulUpdateTimestamp = None
        self.updateStateChangedTimestamp = None

    def from_json(self, js):
        self.accessPointUpdateState = js["accessPointUpdateState"]
        self.successfulUpdateTimestamp = self.fromtimestamp(
            js["successfulUpdateTimestamp"]
        )
        self.updateStateChangedTimestamp = self.fromtimestamp(
            js["updateStateChangedTimestamp"]
        )
