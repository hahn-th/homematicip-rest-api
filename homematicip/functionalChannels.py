from homematicip.group import Group
from homematicip.base.enums import *

from typing import Iterable

class FunctionalChannel():
    """ this is the base class for the functional channels """

    def __init__(self):
        self.index = -1
        self.groupIndex = -1
        self.label = ""
        self.groupIndex = -1

        self.groups = Iterable[Group]

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        self.index = js["index"]
        self.groupIndex = js["groupIndex"]
        self.label = js["label"]

        self.groups = []
        for id in js["groups"]:
            for g in groups:
                if g.id == id:
                    self.groups.append(g)
                    break

class DeviceBaseChannel(FunctionalChannel):
    """ this is the representive of the DEVICE_BASE channel"""
    def __init__(self):
        super().__init__()
        self.unreach = None
        self.lowBat = None
        self.routerModuleSupported = False
        self.routerModuleEnabled = False
        self.rssiDeviceValue = 0
        self.rssiPeerValue = 0
        self.dutyCycle = False
        self.configPending = False

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.unreach = js["unreach"]
        self.lowBat = js["lowBat"]
        self.routerModuleSupported = js["routerModuleSupported"]
        self.routerModuleEnabled = js["routerModuleEnabled"]
        self.rssiDeviceValue = js["rssiDeviceValue"]
        self.rssiPeerValue = js["rssiPeerValue"]
        self.dutyCycle = js["dutyCycle"]
        self.configPending = js["configPending"]

class DeviceSabotageChannel(DeviceBaseChannel):
    """ this is the representive of the DEVICE_SABOTAGE channel"""
    def __init__(self):
        super().__init__()
        self.sabotage = False

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.sabotage = js["sabotage"]

class DeviceOperationLockChannel(DeviceBaseChannel):
    """ this is the representive of the DEVICE_OPERATIONLOCK channel"""
    def __init__(self):
        super().__init__()
        self.operationLockActive = False

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.operationLockActive = js["operationLockActive"]

class DeviceIncorrectPositionedChannel(DeviceBaseChannel):
    """ this is the representive of the DEVICE_INCORRECT_POSITIONED channel"""
    def __init__(self):
        super().__init__()
        self.incorrectPositioned = False

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.incorrectPositioned = js["incorrectPositioned"]

class WaterSensorChannel(FunctionalChannel):
    """ this is the representive of the WATER_SENSOR_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.acousticAlarmSignal = AcousticAlarmSignal.DISABLE_ACOUSTIC_SIGNAL
        self.acousticAlarmTiming = AcousticAlarmTiming.PERMANENT
        self.acousticWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.inAppWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.moistureDetected = False
        self.sirenWateralarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.waterlevelDetected = False

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.acousticAlarmSignal = AcousticAlarmSignal.from_str(js["acousticAlarmSignal"])
        self.acousticAlarmTiming = AcousticAlarmTiming.from_str(js["acousticAlarmTiming"])
        self.acousticWaterAlarmTrigger = WaterAlarmTrigger.from_str(js["acousticWaterAlarmTrigger"])
        self.inAppWaterAlarmTrigger = WaterAlarmTrigger.from_str(js["inAppWaterAlarmTrigger"])
        self.moistureDetected = js["moistureDetected"]
        self.sirenWaterAlarmTrigger = WaterAlarmTrigger.from_str(js["sirenWaterAlarmTrigger"])
        self.waterlevelDetected = js["waterlevelDetected"]


class HeatingThermostatChannel(FunctionalChannel):
    """ this is the representive of the HEATING_THERMOSTAT_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.temperatureOffset = 0
        self.valvePosition = 0.0
        self.valveState = ValveState.ERROR_POSITION
        self.setPointTemperature = 0.0
        self.automaticValveAdaptionNeeded = False

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.temperatureOffset = js["temperatureOffset"]
        self.valvePosition = js["valvePosition"]
        self.valveState = ValveState.from_str(js["valveState"])
        self.setPointTemperature = js["setPointTemperature"]

class ShutterContactChannel(FunctionalChannel):
    """ this is the representive of the SHUTTER_CONTACT_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.windowState = WindowState.CLOSED
        self.eventDelay = None

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.windowState = WindowState.from_str(js["windowState"])
        self.eventDelay = js["eventDelay"]

class RotaryHandleChannel(ShutterContactChannel):
    """ this is the representive of the ROTARY_HANDLE_CHANNEL channel"""

class ClimateSensorChannel(FunctionalChannel):
    """ this is the representive of the CLIMATE_SENSOR_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.actualTemperature = 0
        self.humidity = 0

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.actualTemperature = js["actualTemperature"]
        self.humidity = js["humidity"]

class WallMountedThermostatWithoutDisplayChannel(ClimateSensorChannel):
    """ this is the representive of the WALL_MOUNTED_THERMOSTAT_WITHOUT_DISPLAY_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.temperatureOffset = 0

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.temperatureOffset = js["temperatureOffset"]

class WallMountedThermostatProChannel(WallMountedThermostatWithoutDisplayChannel):
    """ this is the representive of the WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.display = ClimateControlDisplay.ACTUAL
        self.setPointTemperature = 0

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.setPointTemperature = js["setPointTemperature"]
        self.display = ClimateControlDisplay.from_str(js["display"])

class SmokeDetectorChannel(FunctionalChannel):
    """ this is the representive of the SMOKE_DETECTOR_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.smokeDetectorAlarmType = SmokeDetectorAlarmType.IDLE_OFF

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.smokeDetectorAlarmType = SmokeDetectorAlarmType.from_str(js["smokeDetectorAlarmType"])



class SwitchChannel(FunctionalChannel):
    """ this is the representive of the SWITCH_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.on = False
        self.profileMode = None
        self.userDesiredProfileMode = None

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.on = js["on"]
        self.profileMode = js["profileMode"]
        self.userDesiredProfileMode = js["userDesiredProfileMode"]



class SwitchMeasuringChannel(SwitchChannel):
    """ this is the representive of the SWITCH_MEASURING_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.energyCounter = 0
        self.currentPowerConsumption = 0

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.energyCounter = js["energyCounter"]
        self.currentPowerConsumption = js["currentPowerConsumption"]

class DeviceGlobalPumpControlChannel(DeviceBaseChannel):
    """ this is the representive of the DEVICE_GLOBAL_PUMP_CONTROL channel"""
    def __init__(self):
        super().__init__()
        self.globalPumpControl = None
        self.heatingValveType = HeatingValveType.NORMALLY_CLOSE

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.globalPumpControl = js["globalPumpControl"]
        self.heatingValveType = HeatingValveType.from_str(js["heatingValveType"])
        self.heatingLoadType = HeatingLoadType.from_str(js["heatingLoadType"])
        self.coolingEmergencyValue = js["coolingEmergencyValue"]
            
        self.frostProtectionTemperature = js["frostProtectionTemperature"]
        self.heatingEmergencyValue = js["heatingEmergencyValue"]
        self.valveProtectionDuration = js["valveProtectionDuration"]
        self.valveProtectionSwitchingInterval = js["valveProtectionSwitchingInterval"]

class MotionDetectionChannel(FunctionalChannel):
    """ this is the representive of the MOTION_DETECTION_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.currentIllumination = None
        self.motionDetected = None
        self.illumination = None
        self.motionBufferActive = False
        self.motionDetected = False
        self.motionDetectionSendInterval = MotionDetectionSendInterval.SECONDS_30
        self.numberOfBrightnessMeasurements = 0

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.motionDetected = js["motionDetected"]
        self.illumination = js["illumination"]
        self.motionBufferActive = js["motionBufferActive"]
        self.motionDetected = js["motionDetected"]
        self.motionDetectionSendInterval = MotionDetectionSendInterval.from_str(js["motionDetectionSendInterval"])
        self.numberOfBrightnessMeasurements = js["numberOfBrightnessMeasurements"]
        self.currentIllumination = js["currentIllumination"]


class PresenceDetectionChannel(FunctionalChannel):
    """ this is the representive of the PRESENCE_DETECTION_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.presenceDetected = False
        self.currentIllumination = None
        self.illumination = 0
        self.motionBufferActive = False
        self.motionDetectionSendInterval = MotionDetectionSendInterval.SECONDS_30
        self.numberOfBrightnessMeasurements = 0

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.presenceDetected = js["presenceDetected"]
        self.currentIllumination = js["currentIllumination"]
        self.illumination = js["illumination"]
        self.motionBufferActive = js["motionBufferActive"]
        self.motionDetectionSendInterval = MotionDetectionSendInterval.from_str(js["motionDetectionSendInterval"])
        self.numberOfBrightnessMeasurements = js["numberOfBrightnessMeasurements"]

class ShutterChannel(FunctionalChannel):
    """ this is the representive of the SHUTTER_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.shutterLevel = 0
        self.changeOverDelay = 0.0
        self.bottomToTopReferenceTime = 0.0
        self.topToBottomReferenceTime = 0.0
        self.delayCompensationValue = 0
        self.endpositionAutoDetectionEnabled = False
        self.previousShutterLevel = None
        self.processing = False
        self.profileMode = "AUTOMATIC"
        self.selfCalibrationInProgress = None
        self.supportingDelayCompensation = False
        self.supportingEndpositionAutoDetection = False
        self.supportingSelfCalibration = False
        self.userDesiredProfileMode = "AUTOMATIC"

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.shutterLevel = js["shutterLevel"]
        self.changeOverDelay = js["changeOverDelay"]
        self.delayCompensationValue = js["delayCompensationValue"]
        self.bottomToTopReferenceTime = js["bottomToTopReferenceTime"]
        self.topToBottomReferenceTime = js["topToBottomReferenceTime"]
        self.endpositionAutoDetectionEnabled = js["endpositionAutoDetectionEnabled"]
        self.previousShutterLevel = js["previousShutterLevel"]
        self.processing = js["processing"]
        self.profileMode = js["profileMode"]
        self.selfCalibrationInProgress = js["selfCalibrationInProgress"]
        self.supportingDelayCompensation = js["supportingDelayCompensation"]
        self.supportingEndpositionAutoDetection = js["supportingEndpositionAutoDetection"]
        self.supportingSelfCalibration = js["supportingSelfCalibration"]
        self.userDesiredProfileMode = js["userDesiredProfileMode"]

class DimmerChannel(FunctionalChannel):
    """ this is the representive of the DIMMER_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.dimLevel = 0
        self.profileMode = None
        self.userDesiredProfileMode = None

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.dimLevel = js["dimLevel"]
        self.profileMode = js["profileMode"]
        self.userDesiredProfileMode = js["userDesiredProfileMode"]

class WeatherSensorChannel(FunctionalChannel):
    """ this is the representive of the WEATHER_SENSOR_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.actualTemperature = 0
        self.humidity = 0
        self.illumination = 0
        self.illuminationThresholdSunshine = 0
        self.storm = False
        self.sunshine = False
        self.todaySunshineDuration = 0
        self.totalSunshineDuration = 0
        self.windSpeed = 0
        self.windValueType = WindValueType.AVERAGE_VALUE
        self.yesterdaySunshineDuration = 0

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.actualTemperature = js["actualTemperature"]
        self.humidity = js["humidity"]
        self.illumination = js["illumination"]
        self.illuminationThresholdSunshine = js["illuminationThresholdSunshine"]
        self.storm = js["storm"]
        self.sunshine = js["sunshine"]
        self.todaySunshineDuration = js["todaySunshineDuration"]
        self.totalSunshineDuration = js["totalSunshineDuration"]
        self.windSpeed = js["windSpeed"]
        self.windValueType = WindValueType.from_str(js["windValueType"])
        self.yesterdaySunshineDuration = js["yesterdaySunshineDuration"]

class WeatherSensorPlusChannel(WeatherSensorChannel):
    """ this is the representive of the WEATHER_SENSOR_PLUS_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.raining = False
        self.todayRainCounter = 0
        self.totalRainCounter = 0
        self.yesterdayRainCounter = 0

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.raining = js["raining"]
        self.todayRainCounter = js["todayRainCounter"]
        self.totalRainCounter = js["totalRainCounter"]
        self.yesterdayRainCounter = js["yesterdayRainCounter"]

class WeatherSensorProChannel(WeatherSensorPlusChannel):
    """ this is the representive of the WEATHER_SENSOR_PRO_CHANNEL channel"""
    def __init__(self):
        super().__init__()
        self.weathervaneAlignmentNeeded = False
        self.windDirection = 0
        self.windDirectionVariation = 0

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.weathervaneAlignmentNeeded = js["weathervaneAlignmentNeeded"]
        self.windDirection = js["windDirection"]
        self.windDirectionVariation = js["windDirectionVariation"]

class SingleKeyChannel(FunctionalChannel):
    """ this is the representive of the SINGLE_KEY_CHANNEL channel"""

class AlarmSirenChannel(FunctionalChannel):
    """ this is the representive of the ALARM_SIREN_CHANNEL channel"""

class FloorTeminalBlockChannel(FunctionalChannel):
    """ this is the representive of the FLOOR_TERMINAL_BLOCK_CHANNEL channel"""

class FloorTerminalBlockLocalPumpChannel(FunctionalChannel):
    """ this is the representive of the FLOOR_TERMINAL_BLOCK_LOCAL_PUMP_CHANNEL  channel"""
    def __init__(self):
        super().__init__()
        self.pumpFollowUpTime = 0
        self.pumpLeadTime = 0
        self.pumpProtectionDuration = 0
        self.pumpProtectionSwitchingInterval = 20

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups """
        super().from_json(js,groups)
        self.pumpFollowUpTime = js["pumpFollowUpTime"]
        self.pumpLeadTime = js["pumpLeadTime"]
        self.pumpProtectionDuration = js["pumpProtectionDuration"]
        self.pumpProtectionSwitchingInterval = js["pumpProtectionSwitchingInterval"]

class HeatDemandChannel(FunctionalChannel):
    """ this is the representive of the HEAT_DEMAND_CHANNEL channel"""

class DehumidifierDemandChannel(FunctionalChannel):
    """ this is the representive of the DEHUMIDIFIER_DEMAND_CHANNEL channel"""

