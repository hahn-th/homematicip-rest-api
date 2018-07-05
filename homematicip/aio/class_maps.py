import homematicip.base.constants as cn

from homematicip.aio.device import *
from homematicip.aio.group import *
from homematicip.aio.securityEvent import *

TYPE_CLASS_MAP = {
    cn.DEVICE: AsyncDevice,
    cn.HEATING_THERMOSTAT: AsyncHeatingThermostat,
    cn.SHUTTER_CONTACT: AsyncShutterContact,
    cn.SHUTTER_CONTACT_INVISIBLE: AsyncShutterContact,
    cn.WALL_MOUNTED_THERMOSTAT_PRO: AsyncWallMountedThermostatPro,
    cn.BRAND_WALL_MOUNTED_THERMOSTAT: AsyncWallMountedThermostatPro,
    cn.SMOKE_DETECTOR: AsyncSmokeDetector,
    cn.FLOOR_TERMINAL_BLOCK_6: AsyncFloorTerminalBlock6,
    cn.PLUGABLE_SWITCH_MEASURING: AsyncPlugableSwitchMeasuring,
    cn.BRAND_SWITCH_MEASURING:AsyncBrandSwitchMeasuring,
    cn.TEMPERATURE_HUMIDITY_SENSOR_DISPLAY: AsyncTemperatureHumiditySensorDisplay,
    cn.TEMPERATURE_HUMIDITY_SENSOR: AsyncTemperatureHumiditySensorWithoutDisplay,
    cn.PUSH_BUTTON: AsyncPushButton,
    cn.ALARM_SIREN_INDOOR: AsyncAlarmSirenIndoor,
    cn.MOTION_DETECTOR_INDOOR: AsyncMotionDetectorIndoor,
    cn.KEY_REMOTE_CONTROL_ALARM: AsyncKeyRemoteControlAlarm,
    cn.PLUGABLE_SWITCH: AsyncPlugableSwitch,
    cn.FULL_FLUSH_SHUTTER: AsyncFullFlushShutter,
    cn.BRAND_SHUTTER: AsyncFullFlushShutter,
    cn.PRECENCE_DETECTOR_INDOOR: AsyncPresenceDetectorIndoor,
    cn.PLUGGABLE_DIMMER: AsyncPluggableDimmer,
    cn.FULL_FLUSH_SWITCH_MEASURING: AsyncFullFlushSwitchMeasuring,
    cn.WEATHER_SENSOR: AsyncWeatherSensor,
    cn.WEATHER_SENSOR_PRO: AsyncWeatherSensorPro,
    cn.TEMPERATURE_HUMIDITY_SENSOR_OUTDOOR: AsyncTemperatureHumiditySensorOutdoor,
    cn.BRAND_DIMMER: AsyncBrandDimmer,
    cn.ROTARY_HANDLE_SENSOR: AsyncRotaryHandleSensor,
    cn.MOTION_DETECTOR_PUSH_BUTTON: AsyncMotionDetectorPushButton,
    cn.WATER_SENSOR: AsyncWaterSensor
}

TYPE_GROUP_MAP = {
    cn.SECURITY: AsyncSecurityGroup,
    cn.SWITCHING: AsyncSwitchingGroup,
    cn.EXTENDED_LINKED_SWITCHING: AsyncExtendedLinkedSwitchingGroup,
    cn.LINKED_SWITCHING: AsyncLinkedSwitchingGroup,
    cn.ALARM_SWITCHING: AsyncAlarmSwitchingGroup,
    cn.HEATING_HUMIDITY_LIMITER: AsyncHeatingHumidyLimiterGroup,
    cn.HEATING_TEMPERATURE_LIMITER: AsyncHeatingTemperatureLimiterGroup,
    cn.HEATING_CHANGEOVER: AsyncHeatingChangeoverGroup,
    cn.INBOX: AsyncInboxGroup,
    cn.SECURITY_ZONE: AsyncSecurityZoneGroup,
    cn.HEATING: AsyncHeatingGroup,
    cn.HEATING_COOLING_DEMAND: AsyncHeatingCoolingDemandGroup,
    cn.HEATING_EXTERNAL_CLOCK: AsyncHeatingExternalClockGroup,
    cn.HEATING_DEHUMIDIFIER: AsyncHeatingDehumidifierGroup,
    cn.HEATING_COOLING_DEMAND_BOILER: AsyncHeatingCoolingDemandBoilerGroup,
    cn.HEATING_COOLING_DEMAND_PUMP: AsyncHeatingCoolingDemandPumpGroup,
    cn.SWITCHING_PROFILE: AsyncSwitchingProfileGroup,
    cn.OVER_HEAT_PROTECTION_RULE: AsyncOverHeatProtectionRule,
    cn.SMOKE_ALARM_DETECTION_RULE: AsyncSmokeAlarmDetectionRule,
    cn.LOCK_OUT_PROTECTION_RULE: AsyncLockOutProtectionRule,
    cn.SHUTTER_WIND_PROTECTION_RULE: AsyncShutterWindProtectionRule,
    cn.EXTENDED_LINKED_SHUTTER: AsyncExtendedLinkedShutterGroup,
    cn.ENVIRONMENT: AsyncEnvironmentGroup
}

TYPE_SECURITY_EVENT_MAP = {
    cn.SILENCE_CHANGED: AsyncSilenceChangedEvent,
    cn.ACTIVATION_CHANGED: AsyncActivationChangedEvent,
    cn.ACCESS_POINT_CONNECTED: AsyncAccessPointConnectedEvent,
    cn.ACCESS_POINT_DISCONNECTED: AsyncAccessPointDisconnectedEvent,
    cn.SENSOR_EVENT: AsyncSensorEvent
}
