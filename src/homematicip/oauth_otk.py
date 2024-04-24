from homematicip.base.homematicip_object import HomeMaticIPObject


class OAuthOTK(HomeMaticIPObject):
    def __init__(self, connection):
        super().__init__(connection)
        self.authToken = None
        self.expirationTimestamp = None

    def from_json(self, js):
        super().from_json(js)
        self.authToken = js["authToken"]
        self.expirationTimestamp = self.fromtimestamp(js["expirationTimestamp"])
