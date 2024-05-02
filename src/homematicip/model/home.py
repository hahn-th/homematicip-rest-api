"""Various classes to represent home."""
from typing import Optional

from homematicip.model.enums import WeatherCondition, WeatherDayTime
from homematicip.model.hmip_base import HmipBaseModel


class FunctionalHome(HmipBaseModel):
    active: bool
    functionalGroup: list[str] = {}
    solution: str

    vaporAmount: Optional[float] = 0.0


class Location(HmipBaseModel):
    city: str
    latitude: str
    longitude: str


class Weather(HmipBaseModel):
    temperature: Optional[float] = 0.0
    weatherCondition: Optional[WeatherCondition] = WeatherCondition.UNKNOWN
    weatherDayTime: Optional[WeatherDayTime] = WeatherDayTime.DAY
    minTemperature: Optional[float] = 0.0
    maxTemperature: Optional[float] = 0.0
    humidity: Optional[int] = 0
    windSpeed: Optional[float] = 0.0
    # the current wind direction in 360° where 0° is north
    windDirection: Optional[int] = 0


class Home(HmipBaseModel):
    availableAPVersion: Optional[str] = None
    clients: list[str]
    connected: Optional[bool] = None
    currentAPVersion: Optional[str] = None
    deviceUpdateStrategy: Optional[str] = None
    dutyCycle: Optional[float] = None
    functionalHomes: dict[str, FunctionalHome]
    id: str
    lastReadyForUpdateTimestamp: Optional[int] = None
    location: Location
    metaGroups: list[str]
    weather: Weather
