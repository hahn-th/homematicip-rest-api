from homematicip.base.homematicip_object import HomeMaticIPObject
from homematicip.base.enums import WeatherCondition, WeatherDayTime


class Weather(HomeMaticIPObject):
    """this class represents the weather of the home location"""

    def __init__(self, connection):
        super().__init__(connection)
        #:float: the current temperature
        self.temperature = 0.0
        #:WeatherCondition: the current weather
        self.weatherCondition = WeatherCondition.UNKNOWN
        #:datetime: the current datime
        self.weatherDayTime = WeatherDayTime.DAY
        #:float: the minimum temperature of the day
        self.minTemperature = 0.0
        #:float: the maximum temperature of the day
        self.maxTemperature = 0.0
        #:float: the current humidity
        self.humidity = 0
        #:float: the current windspeed
        self.windSpeed = 0.0
        #:int: the current wind direction in 360° where 0° is north
        self.windDirection = 0
        #:float: the current vapor
        self.vaporAmount = 0.0

    def from_json(self, js):
        super().from_json(js)
        self.temperature = js["temperature"]
        self.weatherCondition = WeatherCondition.from_str(js["weatherCondition"])
        self.weatherDayTime = WeatherDayTime.from_str(js["weatherDayTime"])
        self.minTemperature = js["minTemperature"]
        self.maxTemperature = js["maxTemperature"]
        self.humidity = js["humidity"]
        self.windSpeed = js["windSpeed"]
        self.windDirection = js["windDirection"]
        self.vaporAmount = js["vaporAmount"]

    def __str__(self):
        return "temperature({}) weatherCondition({}) weatherDayTime({}) minTemperature({}) maxTemperature({}) humidity({}) vaporAmount({}) windSpeed({}) windDirection({})".format(
            self.temperature,
            self.weatherCondition,
            self.weatherDayTime,
            self.minTemperature,
            self.maxTemperature,
            self.humidity,
            self.vaporAmount,
            self.windSpeed,
            self.windDirection,
        )
