import homematicip.base.constants as cn

from homematicip.device import HeatingThermostat, ShutterContact, \
    WallMountedThermostatPro, SmokeDetector, FloorTerminalBlock6, \
    PlugableSwitchMeasuring, TemperatureHumiditySensorDisplay, PushButton, \
    AlarmSirenIndoor, MotionDetectorIndoor, KeyRemoteControlAlarm, \
    PlugableSwitch, FullFlushShutter, TemperatureHumiditySensorWithoutDisplay, \
    PresenceDetectorIndoor, PluggableDimmer
from homematicip.group import SecurityGroup, SwitchingGroup, \
    ExtendedLinkedSwitchingGroup, LinkedSwitchingGroup, AlarmSwitchingGroup, \
    HeatingHumidyLimiterGroup, HeatingTemperatureLimiterGroup, \
    HeatingChangeoverGroup, InboxGroup, SecurityZoneGroup, HeatingGroup, \
    HeatingCoolingDemandGroup, HeatingExternalClockGroup, \
    HeatingDehumidifierGroup, HeatingCoolingDemandBoilerGroup, \
    HeatingCoolingDemandPumpGroup, SwitchingProfileGroup, \
    OverHeatProtectionRule, SmokeAlarmDetectionRule, LockOutProtectionRule, \
    ShutterWindProtectionRule, ExtendedLinkedShutterGroup
from homematicip.securityEvent import SilenceChangedEvent, \
    ActivationChangedEvent, AccessPointConnectedEvent, \
    AccessPointDisconnectedEvent, SensorEvent

TYPE_CLASS_MAP = {
    cn.HEATING_THERMOSTAT: HeatingThermostat,
    cn.SHUTTER_CONTACT: ShutterContact,
    cn.SHUTTER_CONTACT_INVISIBLE: ShutterContact,
    cn.WALL_MOUNTED_THERMOSTAT_PRO: WallMountedThermostatPro,
    cn.BRAND_WALL_MOUNTED_THERMOSTAT: WallMountedThermostatPro,
    cn.SMOKE_DETECTOR: SmokeDetector,
    cn.FLOOR_TERMINAL_BLOCK_6: FloorTerminalBlock6,
    cn.PLUGABLE_SWITCH_MEASURING: PlugableSwitchMeasuring,
    cn.TEMPERATURE_HUMIDITY_SENSOR_DISPLAY: TemperatureHumiditySensorDisplay,
    cn.TEMPERATURE_HUMIDITY_SENSOR: TemperatureHumiditySensorWithoutDisplay,
    cn.PUSH_BUTTON: PushButton,
    cn.ALARM_SIREN_INDOOR: AlarmSirenIndoor,
    cn.MOTION_DETECTOR_INDOOR: MotionDetectorIndoor,
    cn.KEY_REMOTE_CONTROL_ALARM: KeyRemoteControlAlarm,
    cn.PLUGABLE_SWITCH: PlugableSwitch,
    cn.FULL_FLUSH_SHUTTER: FullFlushShutter,
    cn.BRAND_SHUTTER: FullFlushShutter,
    cn.PRECENCE_DETECTOR_INDOOR: PresenceDetectorIndoor,
    cn.PLUGGABLE_DIMMER: PluggableDimmer
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
    cn.EXTENDED_LINKED_SHUTTER: ExtendedLinkedShutterGroup
}

TYPE_SECURITY_EVENT_MAP = {
    "SILENCE_CHANGED": SilenceChangedEvent,
    "ACTIVATION_CHANGED": ActivationChangedEvent,
    "ACCESS_POINT_CONNECTED": AccessPointConnectedEvent,
    "ACCESS_POINT_DISCONNECTED": AccessPointDisconnectedEvent,
    "SENSOR_EVENT": SensorEvent
}
