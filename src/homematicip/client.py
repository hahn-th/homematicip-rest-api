from homematicip.base.homematicip_object import HomeMaticIPObject
from homematicip.base.enums import ClientType


class Client(HomeMaticIPObject):
    """A client is an app which has access to the access point.
    e.g. smartphone, 3th party apps, google home, conrad connect
    """

    def __init__(self, connection):
        super().__init__(connection)
        #:str: the unique id of the client
        self.id = ""
        #:str: a human understandable name of the client
        self.label = ""
        #:str: the home where the client belongs to
        self.homeId = ""
        #:str: the c2c service name
        self.c2cServiceIdentifier = ""
        #:ClientType: the type of this client
        self.clientType = ClientType.APP

    def from_json(self, js):
        super().from_json(js)
        self.id = js["id"]
        self.label = js["label"]
        self.homeId = js["homeId"]
        self.clientType = ClientType.from_str(js["clientType"])
        if "c2cServiceIdentifier" in js:
            self.c2cServiceIdentifier = js["c2cServiceIdentifier"]

    def __str__(self):
        return "label({})".format(self.label)
