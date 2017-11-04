from homematicip.base.constants import HEATING_THERMOSTAT, SHUTTER_CONTACT, \
    WALL_MOUNTED_THERMOSTAT_PRO, SMOKE_DETECTOR, FLOOR_TERMINAL_BLOCK_6, \
    PLUGABLE_SWITCH, PLUGABLE_SWITCH_MEASURING, \
    TEMPERATURE_HUMIDITY_SENSOR_DISPLAY, PUSH_BUTTON, ALARM_SIREN_INDOOR, \
    KEY_REMOTE_CONTROL_ALARM, MOTION_DETECTOR_INDOOR, FULL_FLUSH_SHUTTER
from homematicip.device import HeatingThermostat, ShutterContact, \
    WallMountedThermostatPro, SmokeDetector, FloorTerminalBlock6, \
    PlugableSwitch, PlugableSwitchMeasuring, TemperatureHumiditySensorDisplay, \
    PushButton, AlarmSirenIndoor, MotionDetectorIndoor, KeyRemoteControlAlarm, \
    FullFlushShutter

TYPE_CLASS_MAP = {HEATING_THERMOSTAT: HeatingThermostat,
                 SHUTTER_CONTACT: ShutterContact,
                 WALL_MOUNTED_THERMOSTAT_PRO: WallMountedThermostatPro,
                 SMOKE_DETECTOR: SmokeDetector,
                 FLOOR_TERMINAL_BLOCK_6: FloorTerminalBlock6,
                 PLUGABLE_SWITCH_MEASURING: PlugableSwitchMeasuring,
                 TEMPERATURE_HUMIDITY_SENSOR_DISPLAY: TemperatureHumiditySensorDisplay,
                 PUSH_BUTTON: PushButton,
                 ALARM_SIREN_INDOOR: AlarmSirenIndoor,
                 MOTION_DETECTOR_INDOOR: MotionDetectorIndoor,
                 KEY_REMOTE_CONTROL_ALARM: KeyRemoteControlAlarm,
                 PLUGABLE_SWITCH: PlugableSwitch,
                 FULL_FLUSH_SHUTTER: FullFlushShutter}

# _typeGroupMap = {"SECURITY": SecurityGroup, "SWITCHING": SwitchingGroup,
#                  "EXTENDED_LINKED_SWITCHING": ExtendedLinkedSwitchingGroup
#     , "LINKED_SWITCHING": LinkedSwitchingGroup,
#                  "ALARM_SWITCHING": AlarmSwitchingGroup,
#                  "HEATING_HUMIDITY_LIMITER": HeatingHumidyLimiterGroup
#     , "HEATING_TEMPERATURE_LIMITER": HeatingTemperatureLimiterGroup,
#                  "HEATING_CHANGEOVER": HeatingChangeoverGroup,
#                  "INBOX": InboxGroup
#     , "SECURITY_ZONE": SecurityZoneGroup, "HEATING": HeatingGroup,
#                  "HEATING_COOLING_DEMAND": HeatingCoolingDemandGroup
#     , "HEATING_EXTERNAL_CLOCK": HeatingExternalClockGroup,
#                  "HEATING_DEHUMIDIFIER": HeatingDehumidifierGroup
#     , "HEATING_COOLING_DEMAND_BOILER": HeatingCoolingDemandBoilerGroup,
#                  "HEATING_COOLING_DEMAND_PUMP": HeatingCoolingDemandPumpGroup
#     , "SWITCHING_PROFILE": SwitchingProfileGroup,
#                  "OVER_HEAT_PROTECTION_RULE": OverHeatProtectionRule,
#                  "SMOKE_ALARM_DETECTION_RULE": SmokeAlarmDetectionRule,
#                  "LOCK_OUT_PROTECTION_RULE": LockOutProtectionRule,
#                  "SHUTTER_WIND_PROTECTION_RULE": ShutterWindProtectionRule}
#
# _typeSecurityEventMap = {"SILENCE_CHANGED": SilenceChangedEvent,
#                          "ACTIVATION_CHANGED": ActivationChangedEvent,
#                          "ACCESS_POINT_CONNECTED": AccessPointConnectedEvent,
#                          "ACCESS_POINT_DISCONNECTED": AccessPointDisconnectedEvent,
#                          "SENSOR_EVENT": SensorEvent}
