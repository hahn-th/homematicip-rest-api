from homematicip.base.enums import *

from homematicip.aio.device import *
from homematicip.aio.group import *
from homematicip.aio.securityEvent import *

TYPE_CLASS_MAP = {
    DeviceType.DEVICE: AsyncDevice,
    DeviceType.HEATING_THERMOSTAT: AsyncHeatingThermostat,
    DeviceType.SHUTTER_CONTACT: AsyncShutterContact,
    DeviceType.SHUTTER_CONTACT_INVISIBLE: AsyncShutterContact,
    DeviceType.WALL_MOUNTED_THERMOSTAT_PRO: AsyncWallMountedThermostatPro,
    DeviceType.BRAND_WALL_MOUNTED_THERMOSTAT: AsyncWallMountedThermostatPro,
    DeviceType.SMOKE_DETECTOR: AsyncSmokeDetector,
    DeviceType.FLOOR_TERMINAL_BLOCK_6: AsyncFloorTerminalBlock6,
    DeviceType.PLUGABLE_SWITCH_MEASURING: AsyncPlugableSwitchMeasuring,
    DeviceType.BRAND_SWITCH_MEASURING:AsyncBrandSwitchMeasuring,
    DeviceType.TEMPERATURE_HUMIDITY_SENSOR_DISPLAY: AsyncTemperatureHumiditySensorDisplay,
    DeviceType.TEMPERATURE_HUMIDITY_SENSOR: AsyncTemperatureHumiditySensorWithoutDisplay,
    DeviceType.PUSH_BUTTON: AsyncPushButton,
    DeviceType.ALARM_SIREN_INDOOR: AsyncAlarmSirenIndoor,
    DeviceType.MOTION_DETECTOR_INDOOR: AsyncMotionDetectorIndoor,
    DeviceType.MOTION_DETECTOR_OUTDOOR: AsyncMotionDetectorOutdoor,
    DeviceType.KEY_REMOTE_CONTROL_ALARM: AsyncKeyRemoteControlAlarm,
    DeviceType.PLUGABLE_SWITCH: AsyncPlugableSwitch,
    DeviceType.FULL_FLUSH_SHUTTER: AsyncFullFlushShutter,
    DeviceType.BRAND_SHUTTER: AsyncFullFlushShutter,
    DeviceType.PRESENCE_DETECTOR_INDOOR: AsyncPresenceDetectorIndoor,
    DeviceType.PLUGGABLE_DIMMER: AsyncPluggableDimmer,
    DeviceType.FULL_FLUSH_SWITCH_MEASURING: AsyncFullFlushSwitchMeasuring,
    DeviceType.WEATHER_SENSOR: AsyncWeatherSensor,
    DeviceType.WEATHER_SENSOR_PRO: AsyncWeatherSensorPro,
    DeviceType.TEMPERATURE_HUMIDITY_SENSOR_OUTDOOR: AsyncTemperatureHumiditySensorOutdoor,
    DeviceType.BRAND_DIMMER: AsyncBrandDimmer,
    DeviceType.ROTARY_HANDLE_SENSOR: AsyncRotaryHandleSensor,
    DeviceType.MOTION_DETECTOR_PUSH_BUTTON: AsyncMotionDetectorPushButton,
    DeviceType.WATER_SENSOR: AsyncWaterSensor,
    DeviceType.SHUTTER_CONTACT_MAGNETIC: AsyncShutterContact,
    DeviceType.FULL_FLUSH_DIMMER : AsyncFullFlushDimmer,
    DeviceType.PUSH_BUTTON_6 : AsyncPushButton6,
    DeviceType.REMOTE_CONTROL_8 : AsyncRemoteControl8,
    DeviceType.OPEN_COLLECTOR_8_MODULE : AsyncOpenCollector8Module
}

TYPE_GROUP_MAP = {
    GroupType.GROUP: AsyncGroup,
    GroupType.SECURITY: AsyncSecurityGroup,
    GroupType.SWITCHING: AsyncSwitchingGroup,
    GroupType.EXTENDED_LINKED_SWITCHING: AsyncExtendedLinkedSwitchingGroup,
    GroupType.LINKED_SWITCHING: AsyncLinkedSwitchingGroup,
    GroupType.ALARM_SWITCHING: AsyncAlarmSwitchingGroup,
    GroupType.SECURITY_BACKUP_ALARM_SWITCHING: AsyncAlarmSwitchingGroup,
    GroupType.HEATING_HUMIDITY_LIMITER: AsyncHeatingHumidyLimiterGroup,
    GroupType.HEATING_TEMPERATURE_LIMITER: AsyncHeatingTemperatureLimiterGroup,
    GroupType.HEATING_CHANGEOVER: AsyncHeatingChangeoverGroup,
    GroupType.INBOX: AsyncInboxGroup,
    GroupType.SECURITY_ZONE: AsyncSecurityZoneGroup,
    GroupType.HEATING: AsyncHeatingGroup,
    GroupType.HEATING_COOLING_DEMAND: AsyncHeatingCoolingDemandGroup,
    GroupType.HEATING_EXTERNAL_CLOCK: AsyncHeatingExternalClockGroup,
    GroupType.HEATING_DEHUMIDIFIER: AsyncHeatingDehumidifierGroup,
    GroupType.HEATING_COOLING_DEMAND_BOILER: AsyncHeatingCoolingDemandBoilerGroup,
    GroupType.HEATING_COOLING_DEMAND_PUMP: AsyncHeatingCoolingDemandPumpGroup,
    GroupType.SWITCHING_PROFILE: AsyncSwitchingProfileGroup,
    GroupType.OVER_HEAT_PROTECTION_RULE: AsyncOverHeatProtectionRule,
    GroupType.SMOKE_ALARM_DETECTION_RULE: AsyncSmokeAlarmDetectionRule,
    GroupType.LOCK_OUT_PROTECTION_RULE: AsyncLockOutProtectionRule,
    GroupType.SHUTTER_WIND_PROTECTION_RULE: AsyncShutterWindProtectionRule,
    GroupType.EXTENDED_LINKED_SHUTTER: AsyncExtendedLinkedShutterGroup,
    GroupType.ENVIRONMENT: AsyncEnvironmentGroup
}

TYPE_SECURITY_EVENT_MAP = {
    SecurityEventType.SILENCE_CHANGED: AsyncSilenceChangedEvent,
    SecurityEventType.ACTIVATION_CHANGED: AsyncActivationChangedEvent,
    SecurityEventType.ACCESS_POINT_CONNECTED: AsyncAccessPointConnectedEvent,
    SecurityEventType.ACCESS_POINT_DISCONNECTED: AsyncAccessPointDisconnectedEvent,
    SecurityEventType.SENSOR_EVENT: AsyncSensorEvent,
    SecurityEventType.SABOTAGE: AsyncSabotageEvent,
    SecurityEventType.MOISTURE_DETECTION_EVENT : AsyncMoistureDetectionEvent,
    SecurityEventType.SMOKE_ALARM : AsyncSmokeAlarmEvent,
    SecurityEventType.EXTERNAL_TRIGGERED : AsyncExternalTriggeredEvent,
    SecurityEventType.OFFLINE_ALARM : AsyncOfflineAlarmEvent,
    SecurityEventType.WATER_DETECTION_EVENT : AsyncWaterDetectionEvent,
    SecurityEventType.MAINS_FAILURE_EVENT : AsyncMainsFailureEvent,
    SecurityEventType.OFFLINE_WATER_DETECTION_EVENT : AsyncOfflineWaterDetectionEvent
}

