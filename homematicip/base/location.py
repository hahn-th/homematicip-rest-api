class Location:
    city = "London"
    latitude = "51.509865"
    longitude = "-0.118092"

    def from_json(self, js):
        self.city = js["city"]
        self.latitude = js["latitude"]
        self.longitude = js["longitude"]

    def __repr__(self):
        return u"city({}) latitude({}) longitude({})".format(self.city,
                                                             self.latitude,
                                                             self.longitude)