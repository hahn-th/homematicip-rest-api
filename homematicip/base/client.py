class Client:
    id = None
    label = None
    homeId = None

    def from_json(self, js):
        self.id = js["id"]
        self.label = js["label"]
        self.homeId = js["homeId"]

    def __repr__(self):
        return u"label({})".format(self.label)
