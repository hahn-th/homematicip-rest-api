# coding=utf-8
from aenum import auto, Enum


class AutoNameEnum(Enum):
    """ auto() will generate the name of the attribute as value """
    def _generate_next_value_(name, start, count, last_values):
        return name
    def __str__(self):
        return self.value

    @classmethod
    def from_str(cls, text):
        if text is None:
            return None
        return cls(text)


class AcousticAlarmTiming(AutoNameEnum):
    PERMANENT = auto()
    THREE_MINUTES = auto()
    SIX_MINUTES = auto()
    ONCE_PER_MINUTE = auto()

class WaterAlarmTrigger(AutoNameEnum):
    NO_ALARM = auto()
    MOISTURE_DETECTION = auto()
    WATER_DETECTION = auto()
    WATER_MOISTURE_DETECTION = auto()

class AcousticAlarmSignal(AutoNameEnum):
    DISABLE_ACOUSTIC_SIGNAL = auto()
    FREQUENCY_RISING = auto()
    FREQUENCY_FALLING = auto()
    FREQUENCY_RISING_AND_FALLING = auto()
    FREQUENCY_ALTERNATING_LOW_HIGH = auto()
    FREQUENCY_ALTERNATING_LOW_MID_HIGH = auto()
    FREQUENCY_HIGHON_OFF = auto()
    FREQUENCY_HIGHON_LONGOFF = auto()
    FREQUENCY_LOWON_OFF_HIGHON_OFF = auto()
    FREQUENCY_LOWON_LONGOFF_HIGHON_LONGOFF = auto()

class ClimateControlDisplay(AutoNameEnum):
    ACTUAL = auto()
    SETPOINT = auto()
    ACTUAL_HUMIDITY = auto()

class WindowState(AutoNameEnum):
    OPEN = auto()
    CLOSED = auto()
    TILTED = auto()

class ValveState(AutoNameEnum):
    STATE_NOT_AVAILABLE = auto()
    RUN_TO_START = auto()
    WAIT_FOR_ADAPTION = auto()
    ADAPTION_IN_PROGRESS = auto()
    ADAPTION_DONE = auto()
    TOO_TIGHT = auto()
    ADJUSTMENT_TOO_BIG = auto()
    ADJUSTMENT_TOO_SMALL = auto()
    ERROR_POSITION = auto()

class HeatingValveType(AutoNameEnum):
    NORMALLY_CLOSE = auto()
    NORMALLY_OPEN = auto()

class RGBColorState(AutoNameEnum):
    BLACK = auto()
    BLUE = auto()
    GREEN = auto()
    TURQUOISE = auto()
    RED = auto()
    PURPLE = auto()
    YELLOW = auto()
    WHITE = auto()

class DeviceUpdateStrategy(AutoNameEnum):
    MANUALLY = auto()
    AUTOMATICALLY_IF_POSSIBLE = auto()

class ApExchangeState(AutoNameEnum):
    NONE = auto()
    REQUESTED = auto()
    IN_PROGRESS = auto()
    DONE = auto()
    REJECTED = auto()

class HomeUpdateState(AutoNameEnum):
    UP_TO_DATE = auto()
    UPDATE_AVAILABLE = auto()
    PERFORM_UPDATE_SENT = auto()
    PERFORMING_UPDATE = auto()

class WeatherCondition(AutoNameEnum):
    CLEAR = auto()
    LIGHT_CLOUDY = auto()
    CLOUDY = auto()
    CLOUDY_WITH_RAIN = auto()
    CLOUDY_WITH_SNOW_RAIN = auto()
    HEAVILY_CLOUDY = auto()
    HEAVILY_CLOUDY_WITH_RAIN = auto()
    HEAVILY_CLOUDY_WITH_STRONG_RAIN = auto()
    HEAVILY_CLOUDY_WITH_SNOW = auto()
    HEAVILY_CLOUDY_WITH_SNOW_RAIN = auto()
    HEAVILY_CLOUDY_WITH_THUNDER = auto()
    HEAVILY_CLOUDY_WITH_RAIN_AND_THUNDER = auto()
    FOGGY = auto()
    UNKNOWN = auto()

class WeatherDayTime(AutoNameEnum):
    DAY = auto()
    TWILIGHT = auto()
    NIGHT = auto()

class AbsenceType(AutoNameEnum):
    NOT_ABSENT = auto()
    PERIOD = auto()
    PERMANENT = auto()
    VACATION = auto()
    PARTY = auto()

class EcoDuration(AutoNameEnum):
    ONE = auto()
    TWO = auto()
    FOUR = auto()
    SIX = auto()
    PERMANENT = auto()


class SecurityZoneActivationMode(AutoNameEnum):
    ACTIVATION_WITH_DEVICE_IGNORELIST = auto()
    ACTIVATION_IF_ALL_IN_VALID_STATE = auto()