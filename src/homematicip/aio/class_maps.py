from os import device_encoding
from homematicip.aio.device import *
from homematicip.aio.group import *
from homematicip.aio.rule import *
from homematicip.aio.securityEvent import *
from homematicip.base.enums import *

TYPE_CLASS_MAP = {
    DeviceType.DEVICE: AsyncDevice,
    DeviceType.BASE_DEVICE: AsyncBaseDevice,
    DeviceType.EXTERNAL: AsyncExternalDevice,
    DeviceType.ACCESS_POINT: AsyncHomeControlUnit,
    DeviceType.ACCELERATION_SENSOR: AsyncAccelerationSensor,
    DeviceType.ALARM_SIREN_INDOOR: AsyncAlarmSirenIndoor,
    DeviceType.ALARM_SIREN_OUTDOOR: AsyncAlarmSirenOutdoor,
    DeviceType.BLIND_MODULE: AsyncBlindModule,
    DeviceType.BRAND_BLIND: AsyncBrandBlind,
    DeviceType.BRAND_DIMMER: AsyncBrandDimmer,
    DeviceType.BRAND_PUSH_BUTTON: AsyncBrandPushButton,
    DeviceType.BRAND_SHUTTER: AsyncFullFlushShutter,
    DeviceType.BRAND_SWITCH_2: AsyncBrandSwitch2,
    DeviceType.BRAND_SWITCH_MEASURING: AsyncBrandSwitchMeasuring,
    DeviceType.BRAND_SWITCH_NOTIFICATION_LIGHT: AsyncBrandSwitchNotificationLight,
    DeviceType.BRAND_WALL_MOUNTED_THERMOSTAT: AsyncWallMountedThermostatPro,
    DeviceType.CARBON_DIOXIDE_SENSOR: AsyncCarbonDioxideSensor,
    DeviceType.DALI_GATEWAY: AsyncDaliGateway,
    DeviceType.DIN_RAIL_BLIND_4: AsyncDinRailBlind4,
    DeviceType.DIN_RAIL_DIMMER_3: AsyncDinRailDimmer3,
    DeviceType.DIN_RAIL_SWITCH: AsyncDinRailSwitch,
    DeviceType.DIN_RAIL_SWITCH_4: AsyncDinRailSwitch4,
    DeviceType.DOOR_BELL_BUTTON: AsyncDoorBellButton,
    DeviceType.DOOR_BELL_CONTACT_INTERFACE: AsyncDoorBellContactInterface,
    DeviceType.DOOR_LOCK_DRIVE: AsyncDoorLockDrive,
    DeviceType.DOOR_LOCK_SENSOR: AsyncDoorLockSensor,
    DeviceType.ENERGY_SENSORS_INTERFACE: AsyncEnergySensorsInterface,
    DeviceType.FLOOR_TERMINAL_BLOCK_10: AsyncFloorTerminalBlock10,
    DeviceType.FLOOR_TERMINAL_BLOCK_12: AsyncFloorTerminalBlock12,
    DeviceType.FLOOR_TERMINAL_BLOCK_6: AsyncFloorTerminalBlock6,
    DeviceType.FULL_FLUSH_BLIND: AsyncFullFlushBlind,
    DeviceType.FULL_FLUSH_CONTACT_INTERFACE: AsyncFullFlushContactInterface,
    DeviceType.FULL_FLUSH_CONTACT_INTERFACE_6: AsyncFullFlushContactInterface6,
    DeviceType.FULL_FLUSH_DIMMER: AsyncFullFlushDimmer,
    DeviceType.FULL_FLUSH_SHUTTER: AsyncFullFlushShutter,
    DeviceType.FULL_FLUSH_INPUT_SWITCH: AsyncFullFlushInputSwitch,
    DeviceType.FULL_FLUSH_SWITCH_MEASURING: AsyncFullFlushSwitchMeasuring,
    DeviceType.HEATING_SWITCH_2: AsyncHeatingSwitch2,
    DeviceType.HEATING_THERMOSTAT: AsyncHeatingThermostat,
    DeviceType.HEATING_THERMOSTAT_COMPACT: AsyncHeatingThermostatCompact,
    DeviceType.HEATING_THERMOSTAT_COMPACT_PLUS: AsyncHeatingThermostatCompact,
    DeviceType.HEATING_THERMOSTAT_EVO: AsyncHeatingThermostatEvo,
    DeviceType.HEATING_THERMOSTAT_THREE: AsyncHeatingThermostat,
    DeviceType.HEATING_THERMOSTAT_FLEX: AsyncHeatingThermostat,
    DeviceType.HOERMANN_DRIVES_MODULE: AsyncHoermannDrivesModule,
    DeviceType.HOME_CONTROL_ACCESS_POINT: AsyncHomeControlAccessPoint,
    DeviceType.KEY_REMOTE_CONTROL_4: AsyncKeyRemoteControl4,
    DeviceType.KEY_REMOTE_CONTROL_ALARM: AsyncKeyRemoteControlAlarm,
    DeviceType.LIGHT_SENSOR: AsyncLightSensor,
    DeviceType.MOTION_DETECTOR_INDOOR: AsyncMotionDetectorIndoor,
    DeviceType.MOTION_DETECTOR_OUTDOOR: AsyncMotionDetectorOutdoor,
    DeviceType.MOTION_DETECTOR_PUSH_BUTTON: AsyncMotionDetectorPushButton,
    DeviceType.MULTI_IO_BOX: AsyncMultiIOBox,
    DeviceType.OPEN_COLLECTOR_8_MODULE: AsyncOpenCollector8Module,
    DeviceType.PASSAGE_DETECTOR: AsyncPassageDetector,
    DeviceType.PLUGABLE_SWITCH: AsyncPlugableSwitch,
    DeviceType.PLUGABLE_SWITCH_MEASURING: AsyncPlugableSwitchMeasuring,
    DeviceType.PLUGGABLE_DIMMER: AsyncPluggableDimmer,
    DeviceType.PLUGGABLE_MAINS_FAILURE_SURVEILLANCE: AsyncPluggableMainsFailureSurveillance,
    DeviceType.PRESENCE_DETECTOR_INDOOR: AsyncPresenceDetectorIndoor,
    DeviceType.PRINTED_CIRCUIT_BOARD_SWITCH_2: AsyncPrintedCircuitBoardSwitch2,
    DeviceType.PRINTED_CIRCUIT_BOARD_SWITCH_BATTERY: AsyncPrintedCircuitBoardSwitchBattery,
    DeviceType.PUSH_BUTTON: AsyncPushButton,
    DeviceType.PUSH_BUTTON_6: AsyncPushButton6,
    DeviceType.PUSH_BUTTON_FLAT: AsyncPushButtonFlat,
    DeviceType.REMOTE_CONTROL_8: AsyncRemoteControl8,
    DeviceType.REMOTE_CONTROL_8_MODULE: AsyncRemoteControl8Module,
    DeviceType.RGBW_DIMMER: AsyncRgbwDimmer,
    DeviceType.ROOM_CONTROL_DEVICE: AsyncRoomControlDevice,
    DeviceType.ROOM_CONTROL_DEVICE_ANALOG: AsyncRoomControlDeviceAnalog,
    DeviceType.RAIN_SENSOR: AsyncRainSensor,
    DeviceType.ROTARY_HANDLE_SENSOR: AsyncRotaryHandleSensor,
    DeviceType.SHUTTER_CONTACT: AsyncShutterContact,
    DeviceType.SHUTTER_CONTACT_INTERFACE: AsyncContactInterface,
    DeviceType.SHUTTER_CONTACT_INVISIBLE: AsyncShutterContact,
    DeviceType.SHUTTER_CONTACT_MAGNETIC: AsyncShutterContactMagnetic,
    DeviceType.SHUTTER_CONTACT_OPTICAL_PLUS: AsyncShutterContactOpticalPlus,
    DeviceType.SMOKE_DETECTOR: AsyncSmokeDetector,
    DeviceType.TEMPERATURE_HUMIDITY_SENSOR: AsyncTemperatureHumiditySensorWithoutDisplay,
    DeviceType.TEMPERATURE_HUMIDITY_SENSOR_DISPLAY: AsyncTemperatureHumiditySensorDisplay,
    DeviceType.TEMPERATURE_HUMIDITY_SENSOR_OUTDOOR: AsyncTemperatureHumiditySensorOutdoor,
    DeviceType.TEMPERATURE_SENSOR_2_EXTERNAL_DELTA: AsyncTemperatureDifferenceSensor2,
    DeviceType.TILT_VIBRATION_SENSOR: AsyncTiltVibrationSensor,
    DeviceType.TORMATIC_MODULE: AsyncGarageDoorModuleTormatic,
    DeviceType.WALL_MOUNTED_THERMOSTAT_BASIC_HUMIDITY: AsyncWallMountedThermostatBasicHumidity,
    DeviceType.WALL_MOUNTED_THERMOSTAT_PRO: AsyncWallMountedThermostatPro,
    DeviceType.WALL_MOUNTED_GARAGE_DOOR_CONTROLLER: AsyncWallMountedGarageDoorController,
    DeviceType.WATER_SENSOR: AsyncWaterSensor,
    DeviceType.WEATHER_SENSOR: AsyncWeatherSensor,
    DeviceType.WEATHER_SENSOR_PLUS: AsyncWeatherSensorPlus,
    DeviceType.WEATHER_SENSOR_PRO: AsyncWeatherSensorPro,
    DeviceType.WIRED_BLIND_4: AsyncWiredDinRailBlind4,
    DeviceType.WIRED_DIMMER_3: AsyncWiredDimmer3,
    DeviceType.WIRED_DIN_RAIL_ACCESS_POINT: AsyncWiredDinRailAccessPoint,
    DeviceType.WIRED_FLOOR_TERMINAL_BLOCK_12: AsyncWiredFloorTerminalBlock12,
    DeviceType.WIRED_INPUT_32: AsyncWiredInput32,
    DeviceType.WIRED_INPUT_SWITCH_6: AsyncWiredInputSwitch6,
    DeviceType.WIRED_MOTION_DETECTOR_PUSH_BUTTON: AsyncWiredMotionDetectorPushButton,
    DeviceType.WIRED_PRESENCE_DETECTOR_INDOOR: AsyncPresenceDetectorIndoor,
    DeviceType.WIRED_PUSH_BUTTON_2: AsyncWiredPushButton,
    DeviceType.WIRED_PUSH_BUTTON_6: AsyncWiredPushButton,
    DeviceType.WIRED_SWITCH_8: AsyncWiredSwitch8,
    DeviceType.WIRED_SWITCH_4: AsyncWiredSwitch4,
    DeviceType.WIRED_WALL_MOUNTED_THERMOSTAT: AsyncWallMountedThermostatPro,
    DeviceType.WIRED_CARBON_TEMPERATURE_HUMIDITY_SENSOR_DISPLAY: AsyncWiredCarbonTemperatureHumiditySensorDisplay,
}

TYPE_GROUP_MAP = {
    GroupType.GROUP: AsyncGroup,
    GroupType.ALARM_SWITCHING: AsyncAlarmSwitchingGroup,
    GroupType.ACCESS_AUTHORIZATION_PROFILE: AsyncAccessAuthorizationProfileGroup,
    GroupType.ACCESS_CONTROL: AsyncAccessControlGroup,
    GroupType.ENERGY: AsyncEnergyGroup,
    GroupType.ENVIRONMENT: AsyncEnvironmentGroup,
    GroupType.EXTENDED_LINKED_SHUTTER: AsyncExtendedLinkedShutterGroup,
    GroupType.EXTENDED_LINKED_SWITCHING: AsyncExtendedLinkedSwitchingGroup,
    GroupType.EXTENDED_LINKED_GARAGE_DOOR: AsyncExtendedGarageDoorGroup,
    GroupType.HEATING: AsyncHeatingGroup,
    GroupType.HEATING_CHANGEOVER: AsyncHeatingChangeoverGroup,
    GroupType.HEATING_COOLING_DEMAND: AsyncHeatingCoolingDemandGroup,
    GroupType.HEATING_COOLING_DEMAND_BOILER: AsyncHeatingCoolingDemandBoilerGroup,
    GroupType.HEATING_COOLING_DEMAND_PUMP: AsyncHeatingCoolingDemandPumpGroup,
    GroupType.HEATING_DEHUMIDIFIER: AsyncHeatingDehumidifierGroup,
    GroupType.HEATING_EXTERNAL_CLOCK: AsyncHeatingExternalClockGroup,
    GroupType.HEATING_FAILURE_ALERT_RULE_GROUP: AsyncHeatingFailureAlertRuleGroup,
    GroupType.HEATING_HUMIDITY_LIMITER: AsyncHeatingHumidyLimiterGroup,
    GroupType.HEATING_TEMPERATURE_LIMITER: AsyncHeatingTemperatureLimiterGroup,
    GroupType.HOT_WATER: AsyncHotWaterGroup,
    GroupType.HUMIDITY_WARNING_RULE_GROUP: AsyncHumidityWarningRuleGroup,
    GroupType.INBOX: AsyncInboxGroup,
    GroupType.INDOOR_CLIMATE: AsyncIndoorClimateGroup,
    GroupType.LINKED_SWITCHING: AsyncLinkedSwitchingGroup,
    GroupType.LOCK_OUT_PROTECTION_RULE: AsyncLockOutProtectionRule,
    GroupType.OVER_HEAT_PROTECTION_RULE: AsyncOverHeatProtectionRule,
    GroupType.SECURITY: AsyncSecurityGroup,
    GroupType.SECURITY_BACKUP_ALARM_SWITCHING: AsyncAlarmSwitchingGroup,
    GroupType.SECURITY_ZONE: AsyncSecurityZoneGroup,
    GroupType.SHUTTER_PROFILE: AsyncShutterProfile,
    GroupType.SHUTTER_WIND_PROTECTION_RULE: AsyncShutterWindProtectionRule,
    GroupType.SMOKE_ALARM_DETECTION_RULE: AsyncSmokeAlarmDetectionRule,
    GroupType.SWITCHING: AsyncSwitchingGroup,
    GroupType.SWITCHING_PROFILE: AsyncSwitchingProfileGroup,
}

TYPE_SECURITY_EVENT_MAP = {
    SecurityEventType.ACCESS_POINT_CONNECTED: AsyncAccessPointConnectedEvent,
    SecurityEventType.ACCESS_POINT_DISCONNECTED: AsyncAccessPointDisconnectedEvent,
    SecurityEventType.ACTIVATION_CHANGED: AsyncActivationChangedEvent,
    SecurityEventType.EXTERNAL_TRIGGERED: AsyncExternalTriggeredEvent,
    SecurityEventType.MAINS_FAILURE_EVENT: AsyncMainsFailureEvent,
    SecurityEventType.MOISTURE_DETECTION_EVENT: AsyncMoistureDetectionEvent,
    SecurityEventType.OFFLINE_ALARM: AsyncOfflineAlarmEvent,
    SecurityEventType.OFFLINE_WATER_DETECTION_EVENT: AsyncOfflineWaterDetectionEvent,
    SecurityEventType.SABOTAGE: AsyncSabotageEvent,
    SecurityEventType.SENSOR_EVENT: AsyncSensorEvent,
    SecurityEventType.SILENCE_CHANGED: AsyncSilenceChangedEvent,
    SecurityEventType.SMOKE_ALARM: AsyncSmokeAlarmEvent,
    SecurityEventType.WATER_DETECTION_EVENT: AsyncWaterDetectionEvent,
}

TYPE_RULE_MAP = {AutomationRuleType.SIMPLE: AsyncSimpleRule}
