from typing import Iterable

from homematicip.base.enums import *
from homematicip.base.HomeMaticIPObject import HomeMaticIPObject
from homematicip.group import Group


class FunctionalChannel(HomeMaticIPObject):
    """ this is the base class for the functional channels """

    def __init__(self):
        super().__init__(None)
        self.index = -1
        self.groupIndex = -1
        self.label = ""
        self.groupIndex = -1
        self.functionalChannelType = ""
        self.groups = Iterable[Group]

        # we don't need a connection in this object (at the moment)
        self._connection = None

    def from_json(self, js, groups: Iterable[Group]):
        """ this function will load the functional channel object 
        from a json object and the given groups 
        
        Args:
            js(dict): the json object
            groups(Iterable[Group]): the groups for referencing
        """
        self.index = js["index"]
        self.groupIndex = js["groupIndex"]
        self.label = js["label"]
        self.functionalChannelType = FunctionalChannelType.from_str(
            js["functionalChannelType"], js["functionalChannelType"]
        )
        self.groups = []
        for id in js["groups"]:
            for g in groups:
                if g.id == id:
                    self.groups.append(g)
                    break

        super().from_json(js)


class DeviceBaseChannel(FunctionalChannel):
    """ this is the representative of the DEVICE_BASE channel"""

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
        self.coProFaulty = None
        self.coProRestartNeeded = None
        self.coProUpdateFailure = None
        self.deviceOverheated = None
        self.deviceOverloaded = None
        self.deviceUndervoltage = None
        self.temperatureOutOfRange = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.unreach = js["unreach"]
        self.lowBat = js["lowBat"]
        self.routerModuleSupported = js["routerModuleSupported"]
        self.routerModuleEnabled = js["routerModuleEnabled"]
        self.rssiDeviceValue = js["rssiDeviceValue"]
        self.rssiPeerValue = js["rssiPeerValue"]
        self.dutyCycle = js["dutyCycle"]
        self.configPending = js["configPending"]
        sof = js["supportedOptionalFeatures"]
        if sof:
            if sof["IFeatureDeviceCoProError"]:
                self.coProFaulty = js["coProFaulty"]
            if sof["IFeatureDeviceCoProRestart"]:
                self.coProRestartNeeded = js["coProRestartNeeded"]
            if sof["IFeatureDeviceCoProUpdate"]:
                self.coProUpdateFailure = js["coProUpdateFailure"]
            if sof["IFeatureDeviceOverheated"]:
                self.deviceOverheated = js["deviceOverheated"]
            if sof["IFeatureDeviceOverloaded"]:
                self.deviceOverloaded = js["deviceOverloaded"]
            if sof["IFeatureDeviceTemperatureOutOfRange"]:
                self.temperatureOutOfRange = js["temperatureOutOfRange"]
            if sof["IFeatureDeviceUndervoltage"]:
                self.deviceUndervoltage = js["deviceUndervoltage"]


class AccessControllerChannel(DeviceBaseChannel):
    """ this is the representative of the ACCESS_CONTROLLER_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.dutyCycleLevel = 0.0
        self.accessPointPriority = 0
        self.signalBrightness = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("dutyCycleLevel", js)
        self.set_attr_from_dict("accessPointPriority", js)
        self.set_attr_from_dict("signalBrightness", js)


class DeviceSabotageChannel(DeviceBaseChannel):
    """ this is the representative of the DEVICE_SABOTAGE channel"""

    def __init__(self):
        super().__init__()
        self.sabotage = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.sabotage = js["sabotage"]


class DeviceOperationLockChannel(DeviceBaseChannel):
    """ this is the representative of the DEVICE_OPERATIONLOCK channel"""

    def __init__(self):
        super().__init__()
        self.operationLockActive = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.operationLockActive = js["operationLockActive"]


class DeviceIncorrectPositionedChannel(DeviceBaseChannel):
    """ this is the representative of the DEVICE_INCORRECT_POSITIONED channel"""

    def __init__(self):
        super().__init__()
        self.incorrectPositioned = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.incorrectPositioned = js["incorrectPositioned"]


class DevicePermanentFullRxChannel(DeviceBaseChannel):
    """ this is the representative of the DEVICE_PERMANENT_FULL_RX channel"""

    def __init__(self):
        super().__init__()
        self.permanentFullRx = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.permanentFullRx = js["permanentFullRx"]


class WaterSensorChannel(FunctionalChannel):
    """ this is the representative of the WATER_SENSOR_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.acousticAlarmSignal = AcousticAlarmSignal.DISABLE_ACOUSTIC_SIGNAL
        self.acousticAlarmTiming = AcousticAlarmTiming.PERMANENT
        self.acousticWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.inAppWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.moistureDetected = False
        self.sirenWaterAlarmTrigger = WaterAlarmTrigger.NO_ALARM
        self.waterlevelDetected = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.acousticAlarmSignal = AcousticAlarmSignal.from_str(
            js["acousticAlarmSignal"]
        )
        self.acousticAlarmTiming = AcousticAlarmTiming.from_str(
            js["acousticAlarmTiming"]
        )
        self.acousticWaterAlarmTrigger = WaterAlarmTrigger.from_str(
            js["acousticWaterAlarmTrigger"]
        )
        self.inAppWaterAlarmTrigger = WaterAlarmTrigger.from_str(
            js["inAppWaterAlarmTrigger"]
        )
        self.moistureDetected = js["moistureDetected"]
        self.sirenWaterAlarmTrigger = WaterAlarmTrigger.from_str(
            js["sirenWaterAlarmTrigger"]
        )
        self.waterlevelDetected = js["waterlevelDetected"]


class HeatingThermostatChannel(FunctionalChannel):
    """ this is the representative of the HEATING_THERMOSTAT_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        #:float: the offset temperature for the thermostat (+/- 3.5)
        self.temperatureOffset = 0.0
        #:float: the current position of the valve 0.0 = closed, 1.0 max opened
        self.valvePosition = 0.0
        #:ValveState: the current state of the valve
        self.valveState = ValveState.ERROR_POSITION
        #:float: the current temperature which should be reached in the room
        self.setPointTemperature = 0.0
        #:float: the current measured temperature at the valve
        self.valveActualTemperature = 0.0
        #:bool: must the adaption re-run?
        self.automaticValveAdaptionNeeded = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.temperatureOffset = js["temperatureOffset"]
        self.valvePosition = js["valvePosition"]
        self.valveState = ValveState.from_str(js["valveState"])
        self.setPointTemperature = js["setPointTemperature"]
        self.valveActualTemperature = js["valveActualTemperature"]


class ShutterContactChannel(FunctionalChannel):
    """ this is the representative of the SHUTTER_CONTACT_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.windowState = WindowState.CLOSED
        self.eventDelay = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.windowState = WindowState.from_str(js["windowState"])
        self.eventDelay = js["eventDelay"]


class RotaryHandleChannel(ShutterContactChannel):
    """ this is the representative of the ROTARY_HANDLE_CHANNEL channel"""


class ContactInterfaceChannel(ShutterContactChannel):
    """ this is the representative of the CONTACT_INTERFACE_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.alarmContactType = AlarmContactType.WINDOW_DOOR_CONTACT
        self.contactType = ContactType.NORMALLY_CLOSE

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.alarmContactType = AlarmContactType.from_str(js["alarmContactType"])
        self.contactType = ContactType.from_str(js["contactType"])


class ClimateSensorChannel(FunctionalChannel):
    """ this is the representative of the CLIMATE_SENSOR_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.actualTemperature = 0
        self.humidity = 0
        self.vaporAmount = 0.0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.actualTemperature = js["actualTemperature"]
        self.humidity = js["humidity"]
        self.vaporAmount = js["vaporAmount"]


class DoorChannel(FunctionalChannel):
    """ this is the representative of the DoorChannel channel"""

    def __init__(self):
        super().__init__()
        self.doorState = DoorState.POSITION_UNKNOWN
        self.on = False
        self.processing = False
        self.ventilationPositionSupported = True

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.doorState = js["doorState"]
        self.on = js["on"]
        self.processing = js["processing"]
        self.ventilationPositionSupported = js["ventilationPositionSupported"]


class WallMountedThermostatWithoutDisplayChannel(ClimateSensorChannel):
    """ this is the representative of the WALL_MOUNTED_THERMOSTAT_WITHOUT_DISPLAY_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.temperatureOffset = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.temperatureOffset = js["temperatureOffset"]


class AnalogRoomControlChannel(FunctionalChannel):
    """ this is the representative of the ANALOG_ROOM_CONTROL_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.actualTemperature = 0
        self.setPointTemperature = 0
        self.temperatureOffset = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("actualTemperature", js)
        self.set_attr_from_dict("setPointTemperature", js)
        self.set_attr_from_dict("temperatureOffset", js)


class WallMountedThermostatProChannel(WallMountedThermostatWithoutDisplayChannel):
    """ this is the representative of the WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.display = ClimateControlDisplay.ACTUAL
        self.setPointTemperature = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.setPointTemperature = js["setPointTemperature"]
        self.display = ClimateControlDisplay.from_str(js["display"])


class SmokeDetectorChannel(FunctionalChannel):
    """ this is the representative of the SMOKE_DETECTOR_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.smokeDetectorAlarmType = SmokeDetectorAlarmType.IDLE_OFF

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.smokeDetectorAlarmType = SmokeDetectorAlarmType.from_str(
            js["smokeDetectorAlarmType"]
        )


class SwitchChannel(FunctionalChannel):
    """ this is the representative of the SWITCH_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.on = False
        self.profileMode = None
        self.userDesiredProfileMode = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.on = js["on"]
        self.profileMode = js["profileMode"]
        self.userDesiredProfileMode = js["userDesiredProfileMode"]


class SwitchMeasuringChannel(SwitchChannel):
    """ this is the representative of the SWITCH_MEASURING_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.energyCounter = 0
        self.currentPowerConsumption = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.energyCounter = js["energyCounter"]
        self.currentPowerConsumption = js["currentPowerConsumption"]


class DeviceGlobalPumpControlChannel(DeviceBaseChannel):
    """ this is the representative of the DEVICE_GLOBAL_PUMP_CONTROL channel"""

    def __init__(self):
        super().__init__()
        self.globalPumpControl = False
        self.heatingValveType = HeatingValveType.NORMALLY_CLOSE
        self.heatingLoadType = HeatingLoadType.LOAD_BALANCING
        self.frostProtectionTemperature = 0.0
        self.heatingEmergencyValue = 0.0
        self.valveProtectionDuration = 0
        self.valveProtectionSwitchingInterval = 20
        self.coolingEmergencyValue = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.globalPumpControl = js["globalPumpControl"]
        self.heatingValveType = HeatingValveType.from_str(js["heatingValveType"])
        self.heatingLoadType = HeatingLoadType.from_str(js["heatingLoadType"])
        self.coolingEmergencyValue = js["coolingEmergencyValue"]

        self.frostProtectionTemperature = js["frostProtectionTemperature"]
        self.heatingEmergencyValue = js["heatingEmergencyValue"]
        self.valveProtectionDuration = js["valveProtectionDuration"]
        self.valveProtectionSwitchingInterval = js["valveProtectionSwitchingInterval"]


class DeviceBaseFloorHeatingChannel(DeviceBaseChannel):
    """ this is the representative of the DEVICE_BASE_FLOOR_HEATING channel"""

    def __init__(self):
        super().__init__()
        self.frostProtectionTemperature = 0.0
        self.valveProtectionDuration = 0
        self.valveProtectionSwitchingInterval = 20
        self.coolingEmergencyValue = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("coolingEmergencyValue", js)
        self.set_attr_from_dict("frostProtectionTemperature", js)
        self.set_attr_from_dict("valveProtectionDuration", js)
        self.set_attr_from_dict("valveProtectionSwitchingInterval", js)


class MotionDetectionChannel(FunctionalChannel):
    """ this is the representative of the MOTION_DETECTION_CHANNEL channel"""

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
        super().from_json(js, groups)
        self.motionDetected = js["motionDetected"]
        self.illumination = js["illumination"]
        self.motionBufferActive = js["motionBufferActive"]
        self.motionDetected = js["motionDetected"]
        self.motionDetectionSendInterval = MotionDetectionSendInterval.from_str(
            js["motionDetectionSendInterval"]
        )
        self.numberOfBrightnessMeasurements = js["numberOfBrightnessMeasurements"]
        self.currentIllumination = js["currentIllumination"]


class PresenceDetectionChannel(FunctionalChannel):
    """ this is the representative of the PRESENCE_DETECTION_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.presenceDetected = False
        self.currentIllumination = None
        self.illumination = 0
        self.motionBufferActive = False
        self.motionDetectionSendInterval = MotionDetectionSendInterval.SECONDS_30
        self.numberOfBrightnessMeasurements = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.presenceDetected = js["presenceDetected"]
        self.currentIllumination = js["currentIllumination"]
        self.illumination = js["illumination"]
        self.motionBufferActive = js["motionBufferActive"]
        self.motionDetectionSendInterval = MotionDetectionSendInterval.from_str(
            js["motionDetectionSendInterval"]
        )
        self.numberOfBrightnessMeasurements = js["numberOfBrightnessMeasurements"]


class ShutterChannel(FunctionalChannel):
    """ this is the representative of the SHUTTER_CHANNEL channel"""

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
        super().from_json(js, groups)
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
        self.supportingEndpositionAutoDetection = js[
            "supportingEndpositionAutoDetection"
        ]
        self.supportingSelfCalibration = js["supportingSelfCalibration"]
        self.userDesiredProfileMode = js["userDesiredProfileMode"]


class BlindChannel(ShutterChannel):
    """ this is the representative of the BLIND_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.slatsLevel = 0
        self.slatsReferenceTime = 0.0
        self.previousSlatsLevel = 0
        self.blindModeActive = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)

        self.slatsLevel = js["slatsLevel"]
        self.slatsReferenceTime = js["slatsReferenceTime"]
        self.previousSlatsLevel = js["previousSlatsLevel"]
        self.blindModeActive = js["blindModeActive"]


class MultiModeInputBlindChannel(BlindChannel):
    """ this is the representative of the MULTI_MODE_INPUT_BLIND_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.binaryBehaviorType = BinaryBehaviorType.NORMALLY_CLOSE
        self.multiModeInputMode = MultiModeInputMode.KEY_BEHAVIOR
        self.favoritePrimaryShadingPosition = 0.0
        self.favoriteSecondaryShadingPosition = 0.0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)

        self.binaryBehaviorType = BinaryBehaviorType.from_str(js["binaryBehaviorType"])
        self.multiModeInputMode = MultiModeInputMode.from_str(js["multiModeInputMode"])
        self.favoritePrimaryShadingPosition = js["favoritePrimaryShadingPosition"]
        self.favoriteSecondaryShadingPosition = js["favoriteSecondaryShadingPosition"]


class DimmerChannel(FunctionalChannel):
    """ this is the representative of the DIMMER_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.dimLevel = 0
        self.profileMode = None
        self.userDesiredProfileMode = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.dimLevel = js["dimLevel"]
        self.profileMode = js["profileMode"]
        self.userDesiredProfileMode = js["userDesiredProfileMode"]


class WeatherSensorChannel(FunctionalChannel):
    """ this is the representative of the WEATHER_SENSOR_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.actualTemperature = 0
        self.humidity = 0
        self.vaporAmount = 0.0
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
        super().from_json(js, groups)
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
        self.vaporAmount = js["vaporAmount"]


class WeatherSensorPlusChannel(WeatherSensorChannel):
    """ this is the representative of the WEATHER_SENSOR_PLUS_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.raining = False
        self.todayRainCounter = 0
        self.totalRainCounter = 0
        self.yesterdayRainCounter = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.raining = js["raining"]
        self.todayRainCounter = js["todayRainCounter"]
        self.totalRainCounter = js["totalRainCounter"]
        self.yesterdayRainCounter = js["yesterdayRainCounter"]


class WeatherSensorProChannel(WeatherSensorPlusChannel):
    """ this is the representative of the WEATHER_SENSOR_PRO_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.weathervaneAlignmentNeeded = False
        self.windDirection = 0
        self.windDirectionVariation = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.weathervaneAlignmentNeeded = js["weathervaneAlignmentNeeded"]
        self.windDirection = js["windDirection"]
        self.windDirectionVariation = js["windDirectionVariation"]


class SingleKeyChannel(FunctionalChannel):
    """ this is the representative of the SINGLE_KEY_CHANNEL channel"""


class AlarmSirenChannel(FunctionalChannel):
    """ this is the representative of the ALARM_SIREN_CHANNEL channel"""


class FloorTeminalBlockChannel(FunctionalChannel):
    """ this is the representative of the FLOOR_TERMINAL_BLOCK_CHANNEL channel"""


class FloorTerminalBlockLocalPumpChannel(FunctionalChannel):
    """ this is the representative of the FLOOR_TERMINAL_BLOCK_LOCAL_PUMP_CHANNEL  channel"""

    def __init__(self):
        super().__init__()
        self.pumpFollowUpTime = 0
        self.pumpLeadTime = 0
        self.pumpProtectionDuration = 0
        self.pumpProtectionSwitchingInterval = 20

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.pumpFollowUpTime = js["pumpFollowUpTime"]
        self.pumpLeadTime = js["pumpLeadTime"]
        self.pumpProtectionDuration = js["pumpProtectionDuration"]
        self.pumpProtectionSwitchingInterval = js["pumpProtectionSwitchingInterval"]


class HeatDemandChannel(FunctionalChannel):
    """ this is the representative of the HEAT_DEMAND_CHANNEL channel"""


class DehumidifierDemandChannel(FunctionalChannel):
    """ this is the representative of the DEHUMIDIFIER_DEMAND_CHANNEL channel"""


class PassageDetectorChannel(FunctionalChannel):
    """ this is the representative of the PASSAGE_DETECTOR_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.leftCounter = 0
        self.leftRightCounterDelta = 0
        self.passageBlindtime = 0.0
        self.passageDirection = PassageDirection.RIGHT
        self.passageSensorSensitivity = 0.0
        self.passageTimeout = 0.0
        self.rightCounter = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.leftCounter = js["leftCounter"]
        self.leftRightCounterDelta = js["leftRightCounterDelta"]
        self.passageBlindtime = js["passageBlindtime"]
        self.passageDirection = PassageDirection.from_str(js["passageDirection"])
        self.passageSensorSensitivity = js["passageSensorSensitivity"]
        self.passageTimeout = js["passageTimeout"]
        self.rightCounter = js["rightCounter"]


class InternalSwitchChannel(FunctionalChannel):
    """ this is the representative of the INTERNAL_SWITCH_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.frostProtectionTemperature = 0
        self.heatingValveType = HeatingValveType.NORMALLY_CLOSE
        self.internalSwitchOutputEnabled = False
        self.valveProtectionDuration = 0
        self.valveProtectionSwitchingInterval = 0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.frostProtectionTemperature = js["frostProtectionTemperature"]
        self.heatingValveType = HeatingValveType.from_str(js["heatingValveType"])
        self.internalSwitchOutputEnabled = js["internalSwitchOutputEnabled"]
        self.valveProtectionDuration = js["valveProtectionDuration"]
        self.valveProtectionSwitchingInterval = js["valveProtectionSwitchingInterval"]


class MultiModeInputChannel(FunctionalChannel):
    """ this is the representative of the MULTI_MODE_INPUT_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.binaryBehaviorType = BinaryBehaviorType.NORMALLY_OPEN
        self.multiModeInputMode = MultiModeInputMode.BINARY_BEHAVIOR
        self.windowState = WindowState.OPEN

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.binaryBehaviorType = BinaryBehaviorType.from_str(js["binaryBehaviorType"])
        self.multiModeInputMode = MultiModeInputMode.from_str(js["multiModeInputMode"])
        self.windowState = WindowState.from_str(js["windowState"])


class NotificationLightChannel(DimmerChannel):
    """ this is the representative of the NOTIFICATION_LIGHT_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        #:boolean: is the light turned on?
        self.on = False
        #:RGBColorState:the color of the light
        self.simpleRGBColorState = RGBColorState.BLACK

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.on = js["on"]
        self.simpleRGBColorState = RGBColorState.from_str(js["simpleRGBColorState"])


class LightSensorChannel(FunctionalChannel):
    """ this is the representative of the LIGHT_SENSOR_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        #:float:the average illumination value
        self.averageIllumination = 0.0
        #:float:the current illumination value
        self.currentIllumination = 0.0
        #:float:the highest illumination value
        self.highestIllumination = 0.0
        #:float:the lowest illumination value
        self.lowestIllumination = 0.0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.averageIllumination = js["averageIllumination"]
        self.currentIllumination = js["currentIllumination"]
        self.highestIllumination = js["highestIllumination"]
        self.lowestIllumination = js["lowestIllumination"]


class GenericInputChannel(FunctionalChannel):
    """ this is the representative of the GENERIC_INPUT_CHANNEL channel"""


class AnalogOutputChannel(FunctionalChannel):
    """ this is the representative of the ANALOG_OUTPUT_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        #:float:the analog output level (Volt?)
        self.analogOutputLevel = 0.0

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.analogOutputLevel = js["analogOutputLevel"]


class AccelerationSensorChannel(FunctionalChannel):
    """ this is the representative of the ACCELERATION_SENSOR_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        #:float:
        self.accelerationSensorEventFilterPeriod = 100.0
        #:AccelerationSensorMode:
        self.accelerationSensorMode = AccelerationSensorMode.ANY_MOTION
        #:AccelerationSensorNeutralPosition:
        self.accelerationSensorNeutralPosition = (
            AccelerationSensorNeutralPosition.HORIZONTAL
        )
        #:AccelerationSensorSensitivity:
        self.accelerationSensorSensitivity = (
            AccelerationSensorSensitivity.SENSOR_RANGE_2G
        )
        #:int:
        self.accelerationSensorTriggerAngle = 0
        #:bool:
        self.accelerationSensorTriggered = False
        #:NotificationSoundType:
        self.notificationSoundTypeHighToLow = NotificationSoundType.SOUND_NO_SOUND
        #:NotificationSoundType:
        self.notificationSoundTypeLowToHigh = NotificationSoundType.SOUND_NO_SOUND

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("accelerationSensorEventFilterPeriod", js)
        self.set_attr_from_dict("accelerationSensorMode", js, AccelerationSensorMode)
        self.set_attr_from_dict(
            "accelerationSensorNeutralPosition", js, AccelerationSensorNeutralPosition
        )
        self.set_attr_from_dict(
            "accelerationSensorSensitivity", js, AccelerationSensorSensitivity
        )
        self.set_attr_from_dict("accelerationSensorTriggerAngle", js)
        self.set_attr_from_dict("accelerationSensorTriggered", js)
        self.set_attr_from_dict(
            "notificationSoundTypeHighToLow", js, NotificationSoundType
        )
        self.set_attr_from_dict(
            "notificationSoundTypeLowToHigh", js, NotificationSoundType
        )


class DeviceRechargeableWithSabotage(DeviceSabotageChannel):
    """ this is the representative of the DEVICE_RECHARGEABLE_WITH_SABOTAGE channel"""

    def __init__(self):
        super().__init__()
        #:bool:is the battery in a bad condition
        self.badBatteryHealth = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("badBatteryHealth", js)


class FloorTerminalBlockMechanicChannel(FunctionalChannel):
    """ this is the representative of the class FLOOR_TERMINAL_BLOCK_MECHANIC_CHANNEL(FunctionalChannel) channel"""

    def __init__(self):
        super().__init__()
        #:ValveState:the current valve state
        self.valveState = ValveState.ADAPTION_DONE

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("valveState", js)


class ChangeOverChannel(FunctionalChannel):
    """ this is the representative of the CHANGE_OVER_CHANNEL channel"""


class MainsFailureChannel(FunctionalChannel):
    """ this is the representative of the MAINS_FAILURE_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.powerMainsFailure = False
        self.genericAlarmSignal = AlarmSignalType.NO_ALARM

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("powerMainsFailure", js)
        self.set_attr_from_dict("genericAlarmSignal", js, AlarmSignalType)


class MultiModeInputSwitchChannel(FunctionalChannel):
    """ this is the representative of the MULTI_MODE_INPUT_SWITCH_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.binaryBehaviorType = BinaryBehaviorType.NORMALLY_OPEN
        self.multiModeInputMode = MultiModeInputMode.SWITCH_BEHAVIOR
        self.on = False
        self.profileMode = ProfileMode.MANUAL
        self.userDesiredProfileMode = ProfileMode.MANUAL

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("binaryBehaviorType", js, BinaryBehaviorType)
        self.set_attr_from_dict("multiModeInputMode", js, MultiModeInputMode)
        self.set_attr_from_dict("on", js)
        self.set_attr_from_dict("profileMode", js, ProfileMode)
        self.set_attr_from_dict("userDesiredProfileMode", js, ProfileMode)


class MultiModeInputDimmerChannel(FunctionalChannel):
    """ this is the representative of the MULTI_MODE_INPUT_DIMMER_CHANNEL channel  """

    def __init__(self):
        super().__init__()
        self.binaryBehaviorType = BinaryBehaviorType.NORMALLY_CLOSE
        self.dimLevel = 0
        self.multiModeInputMode = MultiModeInputMode.KEY_BEHAVIOR
        self.on = False
        self.profileMode = ProfileMode.AUTOMATIC
        self.userDesiredProfileMode = ProfileMode.AUTOMATIC

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("binaryBehaviorType", js, BinaryBehaviorType)
        self.set_attr_from_dict("dimLevel", js)
        self.set_attr_from_dict("multiModeInputMode", js, MultiModeInputMode)
        self.set_attr_from_dict("on", js)
        self.set_attr_from_dict("profileMode", js, ProfileMode)
        self.set_attr_from_dict("userDesiredProfileMode", js, ProfileMode)


class TiltVibrationSensorChannel(FunctionalChannel):
    """ this is the representative of the TILT_VIBRATION_SENSOR_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        #:float:
        self.accelerationSensorEventFilterPeriod = 100.0
        #:AccelerationSensorMode:
        self.accelerationSensorMode = AccelerationSensorMode.ANY_MOTION
        #:AccelerationSensorSensitivity:
        self.accelerationSensorSensitivity = (
            AccelerationSensorSensitivity.SENSOR_RANGE_2G
        )
        #:int:
        self.accelerationSensorTriggerAngle = 0
        #:bool:
        self.accelerationSensorTriggered = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("accelerationSensorEventFilterPeriod", js)
        self.set_attr_from_dict("accelerationSensorMode", js, AccelerationSensorMode)
        self.set_attr_from_dict(
            "accelerationSensorSensitivity", js, AccelerationSensorSensitivity
        )
        self.set_attr_from_dict("accelerationSensorTriggerAngle", js)
        self.set_attr_from_dict("accelerationSensorTriggered", js)


class ShadingChannel(FunctionalChannel):
    """ this is the representative of the SHADING_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        self.automationDriveSpeed = DriveSpeed.CREEP_SPEED
        self.manualDriveSpeed = DriveSpeed.CREEP_SPEED
        self.favoritePrimaryShadingPosition = 0.0
        self.favoriteSecondaryShadingPosition = 0.0
        self.primaryShadingLevel = 0.0
        self.secondaryShadingLevel = 0.0
        self.previousPrimaryShadingLevel = 0.0
        self.previousSecondaryShadingLevel = 0.0
        self.identifyOemSupported = False
        self.productId = 0
        self.primaryCloseAdjustable = False
        self.primaryOpenAdjustable = False
        self.primaryShadingStateType = ShadingStateType.NOT_EXISTENT
        self.primaryCloseAdjustable = False
        self.primaryOpenAdjustable = False
        self.primaryShadingStateType = ShadingStateType.NOT_EXISTENT
        self.profileMode = ProfileMode.MANUAL
        self.userDesiredProfileMode = ProfileMode.MANUAL
        self.processing = False
        self.shadingDriveVersion = None
        self.shadingPackagePosition = ShadingPackagePosition.NOT_USED
        self.shadingPositionAdjustmentActive = None
        self.shadingPositionAdjustmentClientId = None

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)

        self.set_attr_from_dict("automationDriveSpeed", js, DriveSpeed)
        self.set_attr_from_dict("manualDriveSpeed", js, DriveSpeed)

        self.set_attr_from_dict("favoritePrimaryShadingPosition", js)
        self.set_attr_from_dict("favoriteSecondaryShadingPosition", js)

        self.set_attr_from_dict("primaryCloseAdjustable", js)
        self.set_attr_from_dict("primaryOpenAdjustable", js)
        self.set_attr_from_dict("primaryShadingStateType", js, ShadingStateType)
        self.set_attr_from_dict("secondaryCloseAdjustable", js)
        self.set_attr_from_dict("secondaryOpenAdjustable", js)
        self.set_attr_from_dict("secondaryShadingStateType", js, ShadingStateType)

        self.set_attr_from_dict("primaryShadingLevel", js)
        self.set_attr_from_dict("secondaryShadingLevel", js)

        self.set_attr_from_dict("previousPrimaryShadingLevel", js)
        self.set_attr_from_dict("previousSecondaryShadingLevel", js)

        self.set_attr_from_dict("identifyOemSupported", js)
        self.set_attr_from_dict("productId", js)

        self.set_attr_from_dict("profileMode", js, ProfileMode)
        self.set_attr_from_dict("userDesiredProfileMode", js, ProfileMode)

        self.set_attr_from_dict("shadingDriveVersion", js)
        self.set_attr_from_dict("shadingPackagePosition", js, ShadingPackagePosition)
        self.set_attr_from_dict("shadingPositionAdjustmentActive", js)
        self.set_attr_from_dict("shadingPositionAdjustmentClientId", js)


class RainDetectionChannel(FunctionalChannel):
    """ this is the representative of the TILT_VIBRATION_SENSOR_CHANNEL channel"""

    def __init__(self):
        super().__init__()
        #:float:
        self.rainSensorSensitivity = 0
        #:bool:
        self.raining = False

    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("rainSensorSensitivity", js)
        self.set_attr_from_dict("raining", js)

class TemperaturDifferenceSensor2Channel(FunctionalChannel):
    """ this is the representative of the TEMPERATURE_SENSOR_2_EXTERNAL_DELTA_CHANNEL channel """

    def __init__(self, connection):
        super().__init__(connection)
        #:float:
        self.temperatureExternalDelta = 0.0
        #:float:
        self.temperatureExternalOne = 0.0
        #:float:
        self.temperatureExternalTwo = 0.0
    def from_json(self, js, groups: Iterable[Group]):
        super().from_json(js, groups)
        self.set_attr_from_dict("temperatureExternalDelta", js)
        self.set_attr_from_dict("temperatureExternalOne", js)
        self.set_attr_from_dict("temperatureExternalTwo", js)