# coding=utf-8
import logging

from aenum import Enum, auto

logger = logging.getLogger(__name__)


class AutoNameEnum(str, Enum):
    """auto() will generate the name of the attribute as value"""

    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self):
        return self.value

    @classmethod
    def from_str(cls, text: str, default=None):
        """this function will create the enum object based on its string value

        Args:
            text(str): the string value of the enum
            default(AutoNameEnum): a default value if text could not be used
        Returns:
            the enum object or None if the text is None or the default value
        """
        if text is None:
            return None
        try:
            return cls(text)
        except:
            logger.warning(
                "'%s' isn't a valid option for class '%s'", text, cls.__name__
            )
            return default


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
    LOW_BATTERY = auto()
    DISARMED = auto()
    INTERNALLY_ARMED = auto()
    EXTERNALLY_ARMED = auto()
    DELAYED_INTERNALLY_ARMED = auto()
    DELAYED_EXTERNALLY_ARMED = auto()
    EVENT = auto()
    ERROR = auto()


class AlarmContactType(AutoNameEnum):
    PASSIVE_GLASS_BREAKAGE_DETECTOR = auto()
    WINDOW_DOOR_CONTACT = auto()


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


class ContactType(AutoNameEnum):
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
    STRONG_WIND = auto()
    UNKNOWN = auto()


class WeatherDayTime(AutoNameEnum):
    DAY = auto()
    TWILIGHT = auto()
    NIGHT = auto()


class ClimateControlMode(AutoNameEnum):
    AUTOMATIC = auto()
    MANUAL = auto()
    ECO = auto()


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
    ACCELERATION_SENSOR = auto()
    ALARM_SIREN_INDOOR = auto()
    ALARM_SIREN_OUTDOOR = auto()
    BLIND_MODULE = auto()
    BRAND_BLIND = auto()
    BRAND_DIMMER = auto()
    BRAND_PUSH_BUTTON = auto()
    BRAND_SHUTTER = auto()
    BRAND_SWITCH_2 = auto()
    BRAND_SWITCH_MEASURING = auto()
    BRAND_SWITCH_NOTIFICATION_LIGHT = auto()
    BRAND_WALL_MOUNTED_THERMOSTAT = auto()
    DIN_RAIL_BLIND_4 = auto()
    DIN_RAIL_SWITCH = auto()
    DIN_RAIL_SWITCH_4 = auto()
    DIN_RAIL_DIMMER_3 = auto()
    DOOR_LOCK_DRIVE = auto()
    DOOR_LOCK_SENSOR = auto()
    FLOOR_TERMINAL_BLOCK_6 = auto()
    FLOOR_TERMINAL_BLOCK_10 = auto()
    FLOOR_TERMINAL_BLOCK_12 = auto()
    FULL_FLUSH_BLIND = auto()
    FULL_FLUSH_CONTACT_INTERFACE = auto()
    FULL_FLUSH_CONTACT_INTERFACE_6 = auto()
    FULL_FLUSH_DIMMER = auto()
    FULL_FLUSH_INPUT_SWITCH = auto()
    FULL_FLUSH_SHUTTER = auto()
    FULL_FLUSH_SWITCH_MEASURING = auto()
    HEATING_SWITCH_2 = auto()
    HEATING_THERMOSTAT = auto()
    HEATING_THERMOSTAT_COMPACT = auto()
    HEATING_THERMOSTAT_EVO = auto()
    HOME_CONTROL_ACCESS_POINT = auto()
    HOERMANN_DRIVES_MODULE = auto()
    KEY_REMOTE_CONTROL_4 = auto()
    KEY_REMOTE_CONTROL_ALARM = auto()
    LIGHT_SENSOR = auto()
    MOTION_DETECTOR_INDOOR = auto()
    MOTION_DETECTOR_OUTDOOR = auto()
    MOTION_DETECTOR_PUSH_BUTTON = auto()
    MULTI_IO_BOX = auto()
    OPEN_COLLECTOR_8_MODULE = auto()
    PASSAGE_DETECTOR = auto()
    PLUGGABLE_MAINS_FAILURE_SURVEILLANCE = auto()
    PLUGABLE_SWITCH = auto()
    PLUGABLE_SWITCH_MEASURING = auto()
    PLUGGABLE_DIMMER = auto()
    PRESENCE_DETECTOR_INDOOR = auto()
    PRINTED_CIRCUIT_BOARD_SWITCH_BATTERY = auto()
    PRINTED_CIRCUIT_BOARD_SWITCH_2 = auto()
    PUSH_BUTTON = auto()
    PUSH_BUTTON_6 = auto()
    PUSH_BUTTON_FLAT = auto()
    RAIN_SENSOR = auto()
    REMOTE_CONTROL_8 = auto()
    REMOTE_CONTROL_8_MODULE = auto()
    ROOM_CONTROL_DEVICE = auto()
    ROOM_CONTROL_DEVICE_ANALOG = auto()
    ROTARY_HANDLE_SENSOR = auto()
    SHUTTER_CONTACT = auto()
    SHUTTER_CONTACT_INTERFACE = auto()
    SHUTTER_CONTACT_INVISIBLE = auto()
    SHUTTER_CONTACT_MAGNETIC = auto()
    SHUTTER_CONTACT_OPTICAL_PLUS = auto()
    SMOKE_DETECTOR = auto()
    TEMPERATURE_HUMIDITY_SENSOR = auto()
    TEMPERATURE_HUMIDITY_SENSOR_DISPLAY = auto()
    TEMPERATURE_HUMIDITY_SENSOR_OUTDOOR = auto()
    TEMPERATURE_SENSOR_2_EXTERNAL_DELTA = auto()
    TILT_VIBRATION_SENSOR = auto()
    TORMATIC_MODULE = auto()
    WALL_MOUNTED_THERMOSTAT_BASIC_HUMIDITY = auto()
    WALL_MOUNTED_THERMOSTAT_PRO = auto()
    WALL_MOUNTED_GARAGE_DOOR_CONTROLLER = auto()
    WATER_SENSOR = auto()
    WEATHER_SENSOR = auto()
    WEATHER_SENSOR_PLUS = auto()
    WEATHER_SENSOR_PRO = auto()
    WIRED_DIMMER_3 = auto()
    WIRED_INPUT_32 = auto()
    WIRED_SWITCH_8 = auto()


class GroupType(AutoNameEnum):
    GROUP = auto()
    ACCESS_AUTHORIZATION_PROFILE = auto()
    ACCESS_CONTROL = auto()
    ALARM_SWITCHING = auto()
    ENVIRONMENT = auto()
    EXTENDED_LINKED_GARAGE_DOOR = auto()
    EXTENDED_LINKED_SHUTTER = auto()
    EXTENDED_LINKED_SWITCHING = auto()
    HEATING = auto()
    HEATING_CHANGEOVER = auto()
    HEATING_COOLING_DEMAND = auto()
    HEATING_COOLING_DEMAND_BOILER = auto()
    HEATING_COOLING_DEMAND_PUMP = auto()
    HEATING_DEHUMIDIFIER = auto()
    HEATING_EXTERNAL_CLOCK = auto()
    HEATING_FAILURE_ALERT_RULE_GROUP = auto()
    HEATING_HUMIDITY_LIMITER = auto()
    HEATING_TEMPERATURE_LIMITER = auto()
    HOT_WATER = auto()
    HUMIDITY_WARNING_RULE_GROUP = auto()
    INBOX = auto()
    INDOOR_CLIMATE = auto()
    LINKED_SWITCHING = auto()
    LOCK_OUT_PROTECTION_RULE = auto()
    OVER_HEAT_PROTECTION_RULE = auto()
    SECURITY = auto()
    SECURITY_BACKUP_ALARM_SWITCHING = auto()
    SECURITY_ZONE = auto()
    SHUTTER_PROFILE = auto()
    SHUTTER_WIND_PROTECTION_RULE = auto()
    SMOKE_ALARM_DETECTION_RULE = auto()
    SWITCHING = auto()
    SWITCHING_PROFILE = auto()


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
    ACCESS_CONTROL = auto()
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
    ACCELERATION_SENSOR_CHANNEL = auto()
    ACCESS_AUTHORIZATION_CHANNEL = auto()
    ACCESS_CONTROLLER_CHANNEL = auto()
    ALARM_SIREN_CHANNEL = auto()
    ANALOG_OUTPUT_CHANNEL = auto()
    ANALOG_ROOM_CONTROL_CHANNEL = auto()
    BLIND_CHANNEL = auto()
    CHANGE_OVER_CHANNEL = auto()
    CLIMATE_SENSOR_CHANNEL = auto()
    CONTACT_INTERFACE_CHANNEL = auto()
    DEHUMIDIFIER_DEMAND_CHANNEL = auto()
    DEVICE_BASE = auto()
    DEVICE_BASE_FLOOR_HEATING = auto()
    DEVICE_GLOBAL_PUMP_CONTROL = auto()
    DEVICE_INCORRECT_POSITIONED = auto()
    DEVICE_OPERATIONLOCK = auto()
    DEVICE_PERMANENT_FULL_RX = auto()
    DEVICE_RECHARGEABLE_WITH_SABOTAGE = auto()
    DEVICE_SABOTAGE = auto()
    DIMMER_CHANNEL = auto()
    DOOR_CHANNEL = auto()
    DOOR_LOCK_CHANNEL = auto()
    DOOR_LOCK_SENSOR_CHANNEL = auto()
    FLOOR_TERMINAL_BLOCK_CHANNEL = auto()
    FLOOR_TERMINAL_BLOCK_LOCAL_PUMP_CHANNEL = auto()
    FLOOR_TERMINAL_BLOCK_MECHANIC_CHANNEL = auto()
    GENERIC_INPUT_CHANNEL = auto()
    HEAT_DEMAND_CHANNEL = auto()
    HEATING_THERMOSTAT_CHANNEL = auto()
    IMPULSE_OUTPUT_CHANNEL = auto()
    INTERNAL_SWITCH_CHANNEL = auto()
    LIGHT_SENSOR_CHANNEL = auto()
    MAINS_FAILURE_CHANNEL = auto()
    MOTION_DETECTION_CHANNEL = auto()
    MULTI_MODE_INPUT_BLIND_CHANNEL = auto()
    MULTI_MODE_INPUT_CHANNEL = auto()
    MULTI_MODE_INPUT_DIMMER_CHANNEL = auto()
    MULTI_MODE_INPUT_SWITCH_CHANNEL = auto()
    NOTIFICATION_LIGHT_CHANNEL = auto()
    PASSAGE_DETECTOR_CHANNEL = auto()
    PRESENCE_DETECTION_CHANNEL = auto()
    RAIN_DETECTION_CHANNEL = auto()
    ROTARY_HANDLE_CHANNEL = auto()
    SHADING_CHANNEL = auto()
    SHUTTER_CHANNEL = auto()
    SHUTTER_CONTACT_CHANNEL = auto()
    SINGLE_KEY_CHANNEL = auto()
    SMOKE_DETECTOR_CHANNEL = auto()
    SWITCH_CHANNEL = auto()
    SWITCH_MEASURING_CHANNEL = auto()
    TEMPERATURE_SENSOR_2_EXTERNAL_DELTA_CHANNEL = auto()
    TILT_VIBRATION_SENSOR_CHANNEL = auto()
    WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL = auto()
    WALL_MOUNTED_THERMOSTAT_WITHOUT_DISPLAY_CHANNEL = auto()
    WATER_SENSOR_CHANNEL = auto()
    WEATHER_SENSOR_CHANNEL = auto()
    WEATHER_SENSOR_PLUS_CHANNEL = auto()
    WEATHER_SENSOR_PRO_CHANNEL = auto()


class HeatingLoadType(AutoNameEnum):
    LOAD_BALANCING = auto()
    LOAD_COLLECTION = auto()


class DeviceUpdateState(AutoNameEnum):
    UP_TO_DATE = auto()
    TRANSFERING_UPDATE = auto()
    UPDATE_AVAILABLE = auto()
    UPDATE_AUTHORIZED = auto()
    BACKGROUND_UPDATE_NOT_SUPPORTED = auto()


class PassageDirection(AutoNameEnum):
    LEFT = auto()
    RIGHT = auto()


class MultiModeInputMode(AutoNameEnum):
    KEY_BEHAVIOR = auto()
    SWITCH_BEHAVIOR = auto()
    BINARY_BEHAVIOR = auto()


class BinaryBehaviorType(AutoNameEnum):
    NORMALLY_CLOSE = auto()
    NORMALLY_OPEN = auto()


class HeatingFailureValidationType(AutoNameEnum):
    NO_HEATING_FAILURE = auto()
    HEATING_FAILURE_WARNING = auto()
    HEATING_FAILURE_ALARM = auto()


class HumidityValidationType(AutoNameEnum):
    LESSER_LOWER_THRESHOLD = auto()
    GREATER_UPPER_THRESHOLD = auto()
    GREATER_LOWER_LESSER_UPPER_THRESHOLD = auto()


class AccelerationSensorMode(AutoNameEnum):
    ANY_MOTION = auto()
    FLAT_DECT = auto()


class AccelerationSensorNeutralPosition(AutoNameEnum):
    HORIZONTAL = auto()
    VERTICAL = auto()


class AccelerationSensorSensitivity(AutoNameEnum):
    SENSOR_RANGE_16G = auto()
    SENSOR_RANGE_8G = auto()
    SENSOR_RANGE_4G = auto()
    SENSOR_RANGE_2G = auto()
    SENSOR_RANGE_2G_PLUS_SENS = auto()
    SENSOR_RANGE_2G_2PLUS_SENSE = auto()


class NotificationSoundType(AutoNameEnum):
    SOUND_NO_SOUND = auto()
    SOUND_SHORT = auto()
    SOUND_SHORT_SHORT = auto()
    SOUND_LONG = auto()


class DoorState(AutoNameEnum):
    CLOSED = auto()
    OPEN = auto()
    VENTILATION_POSITION = auto()
    POSITION_UNKNOWN = auto()


class DoorCommand(AutoNameEnum):
    OPEN = auto()
    STOP = auto()
    CLOSE = auto()
    PARTIAL_OPEN = auto()


class ShadingStateType(AutoNameEnum):
    NOT_POSSIBLE = auto()
    NOT_EXISTENT = auto()
    POSITION_USED = auto()
    TILT_USED = auto()
    NOT_USED = auto()
    MIXED = auto()


class GroupVisibility(AutoNameEnum):
    INVISIBLE_GROUP_AND_CONTROL = auto()
    INVISIBLE_CONTROL = auto()
    VISIBLE = auto()


class ProfileMode(AutoNameEnum):
    AUTOMATIC = auto()
    MANUAL = auto()


class AlarmSignalType(AutoNameEnum):
    NO_ALARM = auto()
    SILENT_ALARM = auto()
    FULL_ALARM = auto()


class ConnectionType(AutoNameEnum):
    HMIP_RF = auto()
    HMIP_WIRED = auto()
    HMIP_LAN = auto()
    HMIP_WLAN = auto()


class ShadingStateType(AutoNameEnum):
    NOT_POSSIBLE = auto()
    NOT_EXISTENT = auto()
    POSITION_USED = auto()
    TILT_USED = auto()
    NOT_USED = auto()
    MIXED = auto()


class DriveSpeed(AutoNameEnum):
    CREEP_SPEED = auto()
    SLOW_SPEED = auto()
    NOMINAL_SPEED = auto()
    OPTIONAL_SPEED = auto()


class ShadingPackagePosition(AutoNameEnum):
    LEFT = auto()
    RIGHT = auto()
    CENTER = auto()
    SPLIT = auto()
    TOP = auto()
    BOTTOM = auto()
    TDBU = auto()
    NOT_USED = auto()


class LockState(AutoNameEnum):
    OPEN = auto()
    UNLOCKED = auto()
    LOCKED = auto()
    NONE = auto()


class MotorState(AutoNameEnum):
    STOPPED = auto()
    CLOSING = auto()
    OPENING = auto()
