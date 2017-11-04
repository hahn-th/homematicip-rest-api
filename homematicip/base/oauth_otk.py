from datetime import datetime

class OAuthOTK:
    authToken = None
    expirationTimestamp = None

    def from_json(self, js):
        self.authToken = js["authToken"]
        time = js["expirationTimestamp"]
        if time > 0:
            self.expirationTimestamp = datetime.fromtimestamp(time / 1000.0)
        else:
            self.expirationTimestamp = None