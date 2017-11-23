from datetime import datetime


def get_functional_channel(channel_type, js):
    for channel in js['functionalChannels'].values():
        if channel['functionalChannelType'] == channel_type:
            return channel
    return None


class Weather:
    temperature = 0.0
    weatherCondition = "CLEAR"
    weatherDayTime = "DAY"
    minTemperature = 0.0
    maxTemperature = 0.0
    humidity = 0
    windSpeed = 0.0
    windDirection = 0

    def from_json(self, js):
        self.temperature = js["temperature"]
        self.weatherCondition = js["weatherCondition"]
        self.weatherDayTime = js["weatherDayTime"]
        self.minTemperature = js["minTemperature"]
        self.maxTemperature = js["maxTemperature"]
        self.humidity = js["humidity"]
        self.windSpeed = js["windSpeed"]
        self.windDirection = js["windDirection"]


class Location:
    city = "London"
    latitude = "51.509865"
    longitude = "-0.118092"

    def from_json(self, js):
        self.city = js["city"]
        self.latitude = js["latitude"]
        self.longitude = js["longitude"]

    def __str__(self):
        return "city({}) latitude({}) longitude({})".format(self.city,
                                                            self.latitude,
                                                            self.longitude)


class Client:
    id = None
    label = None
    homeId = None

    def from_json(self, js):
        self.id = js["id"]
        self.label = js["label"]
        self.homeId = js["homeId"]

    def __str__(self):
        return "label({})".format(self.label)


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
