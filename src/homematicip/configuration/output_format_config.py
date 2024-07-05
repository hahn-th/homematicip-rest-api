from dataclasses import dataclass, field
from typing import List


def _default_functional_channel_attributes() -> List[str]:
    return [
        "accelerationSensorEventFilterPeriod",
        "accelerationSensorMode",
        "accelerationSensorNeutralPosition",
        "accelerationSensorSensitivity",
        "accelerationSensorTriggerAngle",
        "accelerationSensorTriggered",
        "actualTemperature",
        "alarmContactType",
        "authorized",
        "averageIllumination",
        "binaryBehaviorType",
        "blindModeActive",
        "colorTemperature",
        "currentIllumination",
        "currentPowerConsumption",
        "dimLevel",
        "display",
        "doorHandleType",
        "doorLockDirection",
        "doorState",
        "energyCounter",
        "genericAlarmSignal",
        "highestIllumination",
        "humidity",
        "illumination",
        "impulseDuration",
        "leftCounter",
        "leftRightCounterDelta",
        "lowBat",
        "lowestIllumination",
        "moistureDetected",
        "motionBufferActive",
        "motionDetected",
        "motorState",
        "multiModeInputMode",
        "notificationSoundTypeHighToLow",
        "notificationSoundTypeLowToHigh",
        "on",
        "passageBlindtime",
        "passageDirection",
        "passageSensorSensitivity",
        "powerMainsFailure",
        "previousShutterLevel",
        "previousSlatsLevel",
        "primaryShadingLevel",
        "processing",
        "profileMode",
        "pumpFollowUpTime",
        "pumpLeadTime",
        "pumpProtectionDuration",
        "pumpProtectionSwitchingInterval",
        "raining",
        "rightCounter",
        "rssiDeviceValue",
        "rssiPeerValue",
        "saturationLevel",
        "secondaryShadingLevel",
        "selfCalibrationInProgress",
        "setPointTemperature",
        "shutterLevel",
        "simpleRGBColorState",
        "slatsLevel",
        "smokeDetectorAlarmType",
        "storm",
        "sunshine",
        "temperatureExternalDelta",
        "temperatureExternalOne",
        "temperatureExternalTwo",
        "temperatureOffset",
        "todayRainCounter",
        "todaySunshineDuration",
        "totalRainCounter",
        "totalSunshineDuration",
        "unreach",
        "valveActualTemperature",
        "valvePosition",
        "valveState",
        "vaporAmount",
        "waterlevelDetected",
        "windSpeed",
        "windowState",
        "yesterdayRainCounter",
        "yesterdaySunshineDuration"
    ]


def _default_group_attributes() -> List[str]:
    return [
        "activeProfile",
        "actualTemperature",
        "boostDuration",
        "boostMode",
        "humidity",
        "partyMode",
        "valvePosition",
        "windowState",
        "motionDetected",
        "presenceDetected",
        "on",
        "triggered",
        "primaryShadingLevel",
        "secondaryShadingLevel",
        "shutterLevel",
        "slatsLevel",
        "moistureDetected",
        "waterLevelDetected",
        "signalAcoustic",
        "signalOptical",
        "illumination",
        "enabled",
        "ventilationLevel"
    ]


def _default_device_attributes() -> List[str]:
    return [
        "connectionType",
        "modelType",
        "permanentlyReachable",
        "externalService"
    ]


@dataclass
class OutputFormatConfig:
    functional_channel_attributes: List[str] = field(default_factory=_default_functional_channel_attributes)
    group_attributes: List[str] = field(default_factory=_default_group_attributes)
    device_attributes: List[str] = field(default_factory=_default_device_attributes)
