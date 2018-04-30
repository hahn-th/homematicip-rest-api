import homematicip.base.constants as cn

from homematicip.device import *

from homematicip.group import *

from homematicip.securityEvent import *
from homematicip.rule import *


TYPE_CLASS_MAP = {
    cn.DEVICE: Device,
    cn.HEATING_THERMOSTAT: HeatingThermostat,
    cn.SHUTTER_CONTACT: ShutterContact,
    cn.SHUTTER_CONTACT_INVISIBLE: ShutterContact,
    cn.WALL_MOUNTED_THERMOSTAT_PRO: WallMountedThermostatPro,
    cn.BRAND_WALL_MOUNTED_THERMOSTAT: WallMountedThermostatPro,
    cn.SMOKE_DETECTOR: SmokeDetector,
    cn.FLOOR_TERMINAL_BLOCK_6: FloorTerminalBlock6,
    cn.PLUGABLE_SWITCH_MEASURING: PlugableSwitchMeasuring,
    cn.TEMPERATURE_HUMIDITY_SENSOR_DISPLAY: TemperatureHumiditySensorDisplay,
    cn.ROOM_CONTROL_DEVICE: TemperatureHumiditySensorDisplay,
    cn.TEMPERATURE_HUMIDITY_SENSOR: TemperatureHumiditySensorWithoutDisplay,
    cn.PUSH_BUTTON: PushButton,
    cn.ALARM_SIREN_INDOOR: AlarmSirenIndoor,
    cn.MOTION_DETECTOR_INDOOR: MotionDetectorIndoor,
    cn.KEY_REMOTE_CONTROL_ALARM: KeyRemoteControlAlarm,
    cn.PLUGABLE_SWITCH: PlugableSwitch,
    cn.FULL_FLUSH_SHUTTER: FullFlushShutter,
    cn.BRAND_SHUTTER: FullFlushShutter,
    cn.PRECENCE_DETECTOR_INDOOR: PresenceDetectorIndoor,
    cn.PLUGGABLE_DIMMER: PluggableDimmer,
    cn.BRAND_DIMMER: BrandDimmer,
    cn.BRAND_SWITCH_MEASURING: BrandSwitchMeasuring,
    cn.PRINTED_CIRCUIT_BOARD_SWITCH_BATTERY: PrintedCircuitBoardSwitchBattery,
    cn.TEMPERATURE_HUMIDITY_SENSOR_OUTDOOR: TemperatureHumiditySensorOutdoor,
    cn.WEATHER_SENSOR: WeatherSensor,
    cn.WEATHER_SENSOR_PRO: WeatherSensorPro,
    cn.ROTARY_HANDLE_SENSOR: RotaryHandleSensor,
    cn.FULL_FLUSH_SWITCH_MEASURING: FullFlushSwitchMeasuring
}

TYPE_GROUP_MAP = {
    cn.SECURITY: SecurityGroup,
    cn.SWITCHING: SwitchingGroup,
    cn.EXTENDED_LINKED_SWITCHING: ExtendedLinkedSwitchingGroup,
    cn.LINKED_SWITCHING: LinkedSwitchingGroup,
    cn.ALARM_SWITCHING: AlarmSwitchingGroup,
    cn.HEATING_HUMIDITY_LIMITER: HeatingHumidyLimiterGroup,
    cn.HEATING_TEMPERATURE_LIMITER: HeatingTemperatureLimiterGroup,
    cn.HEATING_CHANGEOVER: HeatingChangeoverGroup,
    cn.INBOX: InboxGroup,
    cn.SECURITY_ZONE: SecurityZoneGroup,
    cn.HEATING: HeatingGroup,
    cn.HEATING_COOLING_DEMAND: HeatingCoolingDemandGroup,
    cn.HEATING_EXTERNAL_CLOCK: HeatingExternalClockGroup,
    cn.HEATING_DEHUMIDIFIER: HeatingDehumidifierGroup,
    cn.HEATING_COOLING_DEMAND_BOILER: HeatingCoolingDemandBoilerGroup,
    cn.HEATING_COOLING_DEMAND_PUMP: HeatingCoolingDemandPumpGroup,
    cn.SWITCHING_PROFILE: SwitchingProfileGroup,
    cn.OVER_HEAT_PROTECTION_RULE: OverHeatProtectionRule,
    cn.SMOKE_ALARM_DETECTION_RULE: SmokeAlarmDetectionRule,
    cn.LOCK_OUT_PROTECTION_RULE: LockOutProtectionRule,
    cn.SHUTTER_WIND_PROTECTION_RULE: ShutterWindProtectionRule,
    cn.EXTENDED_LINKED_SHUTTER: ExtendedLinkedShutterGroup,
    cn.ENVIRONMENT:EnvironmentGroup
}

TYPE_SECURITY_EVENT_MAP = {
    cn.SILENCE_CHANGED: SilenceChangedEvent,
    cn.ACTIVATION_CHANGED: ActivationChangedEvent,
    cn.ACCESS_POINT_CONNECTED: AccessPointConnectedEvent,
    cn.ACCESS_POINT_DISCONNECTED: AccessPointDisconnectedEvent,
    cn.SENSOR_EVENT: SensorEvent
}

TYPE_RULE_MAP = {
    cn.SIMPLE_RULE : SimpleRule
}
