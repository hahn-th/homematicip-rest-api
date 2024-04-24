from homematicip.base.homematicip_object import HomeMaticIPObject


class Location(HomeMaticIPObject):
    """This class represents the possible location"""

    def __init__(self, connection):
        super().__init__(connection)
        #:str: the name of the city
        self.city = "London"
        #:float: the latitude of the location
        self.latitude = 51.509865
        #:float: the longitue of the location
        self.longitude = -0.118092

    def from_json(self, js):
        super().from_json(js)
        self.city = js["city"]
        self.latitude = js["latitude"]
        self.longitude = js["longitude"]

    def __str__(self):
        return "city({}) latitude({}) longitude({})".format(
            self.city, self.latitude, self.longitude
        )
