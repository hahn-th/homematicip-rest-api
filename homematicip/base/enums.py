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

class ClientType(AutoNameEnum):
    APP = auto()
    C2C = auto()

class DeviceType(AutoNameEnum):
    DEVICE = auto()
    FULL_FLUSH_SHUTTER = auto()
    PLUGABLE_SWITCH = auto()
    KEY_REMOTE_CONTROL_ALARM = auto()
    MOTION_DETECTOR_INDOOR = auto()
    MOTION_DETECTOR_OUTDOOR = auto()
    ALARM_SIREN_INDOOR = auto()
    PUSH_BUTTON = auto()
    TEMPERATURE_HUMIDITY_SENSOR_DISPLAY = auto()
    PLUGABLE_SWITCH_MEASURING = auto()
    FLOOR_TERMINAL_BLOCK_6 = auto()
    SMOKE_DETECTOR = auto()
    WALL_MOUNTED_THERMOSTAT_PRO = auto()
    SHUTTER_CONTACT = auto()
    HEATING_THERMOSTAT = auto()
    SHUTTER_CONTACT_INVISIBLE = auto()
    BRAND_WALL_MOUNTED_THERMOSTAT = auto()
    TEMPERATURE_HUMIDITY_SENSOR = auto()
    BRAND_SHUTTER = auto()
    PRESENCE_DETECTOR_INDOOR = auto()
    PLUGGABLE_DIMMER = auto()
    BRAND_DIMMER = auto()
    BRAND_SWITCH_MEASURING = auto()
    PRINTED_CIRCUIT_BOARD_SWITCH_BATTERY = auto()
    ROOM_CONTROL_DEVICE = auto()
    TEMPERATURE_HUMIDITY_SENSOR_OUTDOOR = auto()
    WEATHER_SENSOR = auto()
    WEATHER_SENSOR_PRO = auto()
    ROTARY_HANDLE_SENSOR = auto()
    FULL_FLUSH_SWITCH_MEASURING = auto()
    MOTION_DETECTOR_PUSH_BUTTON = auto()
    WATER_SENSOR = auto()
    SHUTTER_CONTACT_MAGNETIC = auto()
    FULL_FLUSH_DIMMER = auto()
    PUSH_BUTTON_6 = auto()
    REMOTE_CONTROL_8 = auto()
    OPEN_COLLECTOR_8_MODULE = auto()

class GroupType(AutoNameEnum):
    GROUP = auto()
    EXTENDED_LINKED_SHUTTER = auto()
    SHUTTER_WIND_PROTECTION_RULE = auto()
    LOCK_OUT_PROTECTION_RULE = auto()
    SMOKE_ALARM_DETECTION_RULE = auto()
    OVER_HEAT_PROTECTION_RULE = auto()
    SWITCHING_PROFILE = auto()
    HEATING_COOLING_DEMAND_PUMP = auto()
    HEATING_COOLING_DEMAND_BOILER = auto()
    HEATING_DEHUMIDIFIER = auto()
    HEATING_EXTERNAL_CLOCK = auto()
    HEATING_COOLING_DEMAND = auto()
    HEATING = auto()
    SECURITY_ZONE = auto()
    INBOX = auto()
    HEATING_CHANGEOVER = auto()
    HEATING_TEMPERATURE_LIMITER = auto()
    HEATING_HUMIDITY_LIMITER = auto()
    ALARM_SWITCHING = auto()
    LINKED_SWITCHING = auto()
    EXTENDED_LINKED_SWITCHING = auto()
    SWITCHING = auto()
    SECURITY = auto()
    ENVIRONMENT = auto()
    SECURITY_BACKUP_ALARM_SWITCHING = auto()

class SecurityEventType(AutoNameEnum):
    SENSOR_EVENT = auto()
    ACCESS_POINT_DISCONNECTED = auto()
    ACCESS_POINT_CONNECTED = auto()
    ACTIVATION_CHANGED = auto()
    SILENCE_CHANGED = auto()
    SABOTAGE = auto()
    MOISTURE_DETECTION_EVENT = auto()
    SMOKE_ALARM = auto()
    EXTERNAL_TRIGGERED = auto()
    OFFLINE_ALARM = auto()
    WATER_DETECTION_EVENT = auto()
    MAINS_FAILURE_EVENT = auto()
    OFFLINE_WATER_DETECTION_EVENT = auto()

class AutomationRuleType(AutoNameEnum):
    SIMPLE = auto()

class FunctionalHomeType(AutoNameEnum):
    INDOOR_CLIMATE = auto()
    LIGHT_AND_SHADOW = auto()
    SECURITY_AND_ALARM = auto()
    WEATHER_AND_ENVIRONMENT = auto()

class EventType(AutoNameEnum):
    SECURITY_JOURNAL_CHANGED = auto()
    GROUP_ADDED = auto()
    GROUP_REMOVED = auto()
    DEVICE_REMOVED = auto()
    DEVICE_CHANGED = auto()
    DEVICE_ADDED = auto()
    CLIENT_REMOVED = auto()
    CLIENT_CHANGED = auto()
    CLIENT_ADDED = auto()
    HOME_CHANGED = auto()
    GROUP_CHANGED = auto()


class MotionDetectionSendInterval(AutoNameEnum):
    SECONDS_30 = auto()
    SECONDS_60 = auto()
    SECONDS_120 = auto()
    SECONDS_240 = auto()
    SECONDS_480 = auto()

class SmokeDetectorAlarmType(AutoNameEnum):
    IDLE_OFF = auto()
    PRIMARY_ALARM = auto()
    INTRUSION_ALARM = auto()
    SECONDARY_ALARM = auto()

class LiveUpdateState(AutoNameEnum):
    UP_TO_DATE = auto()
    UPDATE_AVAILABLE = auto()
    UPDATE_INCOMPLETE = auto()
    LIVE_UPDATE_NOT_SUPPORTED = auto()

class OpticalAlarmSignal(AutoNameEnum):
    DISABLE_OPTICAL_SIGNAL = auto()
    BLINKING_ALTERNATELY_REPEATING = auto()
    BLINKING_BOTH_REPEATING = auto()
    DOUBLE_FLASHING_REPEATING = auto()
    FLASHING_BOTH_REPEATING = auto()
    CONFIRMATION_SIGNAL_0 = auto()
    CONFIRMATION_SIGNAL_1 = auto()
    CONFIRMATION_SIGNAL_2 = auto()

class WindValueType(AutoNameEnum):
    CURRENT_VALUE = auto()
    MIN_VALUE = auto()
    MAX_VALUE = auto()
    AVERAGE_VALUE = auto()

class FunctionalChannelType(AutoNameEnum):
    FUNCTIONAL_CHANNEL = auto()
    ALARM_SIREN_CHANNEL = auto()
    CLIMATE_SENSOR_CHANNEL = auto()
    DEHUMIDIFIER_DEMAND_CHANNEL = auto()
    DEVICE_BASE = auto()
    DEVICE_GLOBAL_PUMP_CONTROL = auto()
    DEVICE_INCORRECT_POSITIONED = auto()
    DEVICE_OPERATIONLOCK = auto()
    DEVICE_SABOTAGE = auto()
    DIMMER_CHANNEL = auto()
    FLOOR_TERMINAL_BLOCK_LOCAL_PUMP_CHANNEL = auto()
    FLOOR_TERMINAL_BLOCK_CHANNEL = auto()
    HEAT_DEMAND_CHANNEL = auto()
    HEATING_THERMOSTAT_CHANNEL = auto()
    MOTION_DETECTION_CHANNEL = auto()
    PRESENCE_DETECTION_CHANNEL = auto()
    ROTARY_HANDLE_CHANNEL = auto()
    SHUTTER_CHANNEL = auto()
    SHUTTER_CONTACT_CHANNEL = auto()
    SINGLE_KEY_CHANNEL = auto()
    SMOKE_DETECTOR_CHANNEL = auto()
    SWITCH_CHANNEL = auto()
    SWITCH_MEASURING_CHANNEL = auto()
    WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL = auto()
    WALL_MOUNTED_THERMOSTAT_WITHOUT_DISPLAY_CHANNEL = auto()
    WATER_SENSOR_CHANNEL = auto()
    WEATHER_SENSOR_CHANNEL = auto()
    WEATHER_SENSOR_PRO_CHANNEL = auto()

class HeatingLoadType(AutoNameEnum):
    LOAD_BALANCING = auto()
    LOAD_COLLECTION = auto()
