import logging

from homematicip.base.enums import *
from homematicip.device import *

ERROR_CODE = "errorCode"

_LOGGER = logging.getLogger(__name__)


class AsyncDevice(Device):
    """Async implementation of a genereric homematic ip device"""

    async def set_label(self, label):
        return await self._connection.api_call(*super().set_label(label))

    async def authorizeUpdate(self):
        return await self._connection.api_call(*super().authorizeUpdate())

    async def delete(self):
        return await self._connection.api_call(*super().delete())

    async def set_router_module_enabled(self, enabled=True):
        return await self._connection.api_call(
            *super().set_router_module_enabled(enabled)
        )

    async def is_update_applicable(self):
        return await self._connection.api_call(*super().is_update_applicable())


class AsyncSwitch(Switch, AsyncDevice):
    """Generic async switch"""

    async def set_switch_state(self, on=True, channelIndex=1):
        _LOGGER.debug("Async switch set_switch_state")
        url, data = super().set_switch_state(on, channelIndex)
        return await self._connection.api_call(url, data)

    async def turn_on(self, channelIndex=1):
        _LOGGER.debug("Async switch turn_on")
        return await self.set_switch_state(True, channelIndex)

    async def turn_off(self, channelIndex=1):
        _LOGGER.debug("Async switch turn_off")
        return await self.set_switch_state(False, channelIndex)


class AsyncSwitchMeasuring(SwitchMeasuring, AsyncSwitch):
    """Generic async switch measuring"""

    async def reset_energy_counter(self):
        return await self._connection.api_call(*super().reset_energy_counter())


class AsyncHeatingSwitch2(HeatingSwitch2, AsyncSwitch):
    """HMIP-WHS2 (Switch Actuator for heating systems – 2x channels)"""


class AsyncPlugableSwitch(PlugableSwitch, AsyncSwitch):
    """Async implementation of HMIP-PS (Pluggable Switch)"""


class AsyncPrintedCircuitBoardSwitchBattery(
    PrintedCircuitBoardSwitchBattery, AsyncSwitch
):
    """HMIP-PCBS-BAT (Printed Circuit Board Switch Battery)"""


class AsyncPrintedCircuitBoardSwitch2(PrintedCircuitBoardSwitch2, AsyncSwitch):
    """Async implementation of HMIP-PCBS2 (Switch Circuit Board - 2x channels)"""


class AsyncLightSensor(LightSensor, AsyncDevice):
    """Async implementation of HMIP-SLO (Light Sensor outdoor)"""


class AsyncSabotageDevice(SabotageDevice, AsyncDevice):
    """Async implementation sabotage signaling devices"""


class AsyncOpenCollector8Module(OpenCollector8Module, AsyncSwitch):
    """Async implementation of HMIP-MOD-OC8 ( Open Collector Module )"""


class AsyncOperationLockableDevice(OperationLockableDevice, AsyncDevice):
    async def set_operation_lock(self, operationLock=True):
        return await self._connection.api_call(
            *super().set_operation_lock(operationLock=operationLock)
        )


class AsyncBrandSwitchNotificationLight(BrandSwitchNotificationLight, AsyncSwitch):
    """HMIP-BSL (Switch Actuator for brand switches – with signal lamp)"""

    async def set_rgb_dim_level(
        self, channelIndex: int, rgb: RGBColorState, dimLevel: float
    ):
        return await self._connection.api_call(
            *super().set_rgb_dim_level(channelIndex, rgb, dimLevel)
        )

    async def set_rgb_dim_level_with_time(
        self,
        channelIndex: int,
        rgb: RGBColorState,
        dimLevel: float,
        onTime: float,
        rampTime: float,
    ):
        return await self._connection.api_call(
            *super().set_rgb_dim_level_with_time(
                channelIndex, rgb, dimLevel, onTime, rampTime
            )
        )


class AsyncPlugableSwitchMeasuring(PlugableSwitchMeasuring, AsyncSwitchMeasuring):
    """HMIP-PSM (Pluggable Switch and Meter)"""


class AsyncBrandSwitchMeasuring(BrandSwitchMeasuring, AsyncSwitchMeasuring):
    """HMIP-BSM (Brand Switch and Meter)"""


class AsyncFullFlushSwitchMeasuring(FullFlushSwitchMeasuring, AsyncSwitchMeasuring):
    """HMIP-FSM (Full flush Switch and Meter)"""


class AsyncShutterContact(ShutterContact, AsyncSabotageDevice):
    """HMIP-SWDO (Door / Window Contact - optical) /
    HMIP-SWDO-I (Door / Window Contact Invisible - optical)"""


class AsyncShutterContactOpticalPlus(ShutterContactOpticalPlus, AsyncShutterContact):
    """HmIP-SWDO-PL ( Window / Door Contact – optical, plus )"""


class AsyncShutterContactMagnetic(ShutterContactMagnetic, AsyncDevice):
    """HMIP-SWDM /  HMIP-SWDM-B2  (Door / Window Contact - magnetic"""


class AsyncContactInterface(ContactInterface, AsyncSabotageDevice):
    """HMIP-SCI (Contact Interface Sensor)"""


class AsyncRotaryHandleSensor(RotaryHandleSensor, AsyncSabotageDevice):
    """HMIP-SRH"""


class AsyncTemperatureHumiditySensorOutdoor(
    TemperatureHumiditySensorOutdoor, AsyncDevice
):
    """HMIP-STHO (Temperature and Humidity Sensor outdoor)"""


class AsyncHeatingThermostat(HeatingThermostat, AsyncOperationLockableDevice):
    """HMIP-eTRV (Radiator Thermostat)"""


class AsyncHeatingThermostatCompact(HeatingThermostatCompact, AsyncSabotageDevice):
    """HMIP-eTRV-C (Heating-thermostat compact without display)"""


class AsyncHeatingThermostatEvo(HeatingThermostatEvo, AsyncSabotageDevice):
    """HMIP-eTRV-E (Heating-thermostat new evo version)"""


class AsyncTemperatureHumiditySensorWithoutDisplay(
    TemperatureHumiditySensorWithoutDisplay, AsyncDevice
):
    """HMIP-STH (Temperature and Humidity Sensor without display - indoor)"""


class AsyncTemperatureHumiditySensorDisplay(
    TemperatureHumiditySensorDisplay, AsyncDevice
):
    """HMIP-STHD (Temperature and Humidity Sensor with display - indoor)"""

    async def set_display(
        self, display: ClimateControlDisplay = ClimateControlDisplay.ACTUAL
    ):
        await self._connection.api_call(*super().set_display(display=display))


class AsyncWallMountedThermostatPro(
    WallMountedThermostatPro,
    AsyncTemperatureHumiditySensorDisplay,
    AsyncOperationLockableDevice,
):
    """HMIP-WTH, HMIP-WTH-2 (Wall Thermostat with Humidity Sensor)
    / HMIP-BWTH (Brand Wall Thermostat with Humidity Sensor)"""


class AsyncWallMountedThermostatBasicHumidity(AsyncWallMountedThermostatPro):
    """HMIP-WTH-B (Wall Thermostat – basic)"""


class AsyncSmokeDetector(SmokeDetector, AsyncDevice):
    """HMIP-SWSD (Smoke Alarm with Q label)"""


class AsyncFloorTerminalBlock6(FloorTerminalBlock6, AsyncDevice):
    """HMIP-FAL230-C6 (Floor Heating Actuator - 6 channels, 230 V)"""


class AsyncFloorTerminalBlock10(FloorTerminalBlock10, AsyncFloorTerminalBlock6):
    """HMIP-FAL24-C10  (Floor Heating Actuator – 10x channels, 24V)"""


class AsyncFloorTerminalBlock12(FloorTerminalBlock12, AsyncDevice):
    """HMIP-FALMOT-C12 (Floor Heating Actuator – 12x channels, motorised)"""

    async def set_minimum_floor_heating_valve_position(
        self, minimumFloorHeatingValvePosition: float
    ):
        """sets the minimum floot heating valve position

        Args:
            minimumFloorHeatingValvePosition(float): the minimum valve position. must be between 0.0 and 1.0

        Returns:
            the result of the _restCall
        """
        await self._connection.api_call(
            *super().set_minimum_floor_heating_valve_position(
                minimumFloorHeatingValvePosition=minimumFloorHeatingValvePosition
            )
        )


class AsyncPushButton(PushButton, AsyncDevice):
    """HMIP-WRC2 (Wall-mount Remote Control - 2-button)"""


class AsyncPushButton6(PushButton6, AsyncPushButton):
    """HMIP-WRC6 (Wall-mount Remote Control - 6-button)"""


class AsyncPushButtonFlat(PushButtonFlat, AsyncPushButton):
    """HMIP-WRCC2 (Wall-mount Remote Control – flat)"""


class AsyncBrandPushButton(BrandPushButton, AsyncPushButton):
    """HMIP-BRC2 (Remote Control for brand switches – 2x channels)"""


class AsyncKeyRemoteControl4(KeyRemoteControl4, AsyncPushButton):
    """HMIP-KRC4 (Key Ring Remote Control - 4 buttons)"""


class AsyncRemoteControl8(RemoteControl8, AsyncPushButton):
    """HMIP-RC8 (Remote Control - 8 buttons)"""


class AsyncRemoteControl8Module(RemoteControl8Module, AsyncRemoteControl8):
    """HMIP-MOD-RC8 (Open Collector Module Sender - 8x)"""


class AsyncAlarmSirenIndoor(AlarmSirenIndoor, AsyncSabotageDevice):
    """HMIP-ASIR (Alarm Siren)"""


class AsyncAlarmSirenOutdoor(AlarmSirenOutdoor, AsyncAlarmSirenIndoor):
    """HMIP-ASIR-O (Alarm Siren Outdoor)"""


class AsyncMotionDetectorIndoor(MotionDetectorIndoor, AsyncSabotageDevice):
    """HMIP-SMI (Motion Detector with Brightness Sensor - indoor)"""


class AsyncMotionDetectorOutdoor(MotionDetectorOutdoor, AsyncDevice):
    """HMIP-SMO-A (Motion Detector with Brightness Sensor - outdoor)"""


class AsyncMotionDetectorPushButton(MotionDetectorPushButton, AsyncDevice):
    """HMIP-SMI55 (Motion Detector with Brightness Sensor and Remote Control - 2-button)"""


class AsyncPresenceDetectorIndoor(PresenceDetectorIndoor, AsyncSabotageDevice):
    """HMIP-SPI (Presence Sensor - indoor)"""


class AsyncPassageDetector(PassageDetector, AsyncSabotageDevice):
    """HMIP-SPDR (Passage Detector)"""


class AsyncKeyRemoteControlAlarm(KeyRemoteControlAlarm, AsyncDevice):
    """HMIP-KRCA (Key Ring Remote Control - alarm)"""


class AsyncFullFlushContactInterface(FullFlushContactInterface, AsyncDevice):
    """HMIP-FCI1 (Contact Interface flush-mount – 1 channel)"""


class AsyncFullFlushContactInterface6(FullFlushContactInterface6, AsyncDevice):
    """HMIP-FCI6 (Contact Interface flush-mount – 6 channels)"""


class AsyncFullFlushInputSwitch(FullFlushInputSwitch, AsyncSwitch):
    """HMIP-FSI16 (Switch Actuator with Push-button Input 230V, 16A)"""


class AsyncDinRailSwitch(DinRailSwitch, AsyncFullFlushInputSwitch):
    """HMIP-DRSI1 (Switch Actuator for DIN rail mount – 1x channel)"""


class AsyncShutter(Shutter, AsyncDevice):
    """Base class for async shutter devices"""

    async def set_shutter_level(self, level=0.0, channelIndex=1):
        return await self._connection.api_call(
            *super().set_shutter_level(level, channelIndex)
        )

    async def set_shutter_stop(self, channelIndex=1):
        return await self._connection.api_call(*super().set_shutter_stop(channelIndex))


class AsyncBlind(Blind, AsyncShutter):
    """Base class for async blind devices"""

    async def set_slats_level(self, slatsLevel=0.0, shutterLevel=None, channelIndex=1):
        return await self._connection.api_call(
            *super().set_slats_level(slatsLevel, shutterLevel, channelIndex)
        )


class AsyncFullFlushShutter(FullFlushShutter, AsyncShutter):
    """HMIP-FROLL (Shutter Actuator - flush-mount) / HMIP-BROLL (Shutter Actuator - Brand-mount)"""
    
    
class AsyncBrandSwitch2(BrandSwitch2, AsyncSwitch):
    """ELV-SH-BS2 (ELV Smart Home ARR-Bausatz Schaltaktor für Markenschalter – 2-fach powered by Homematic IP)"""


class AsyncFullFlushBlind(FullFlushBlind, AsyncBlind):
    """HMIP-FBL (Blind Actuator - flush-mount)"""


class AsyncBrandBlind(BrandBlind, AsyncFullFlushBlind):
    """HMIP-BBL (Blind Actuator for brand switches)"""


class AsyncDinRailBlind4(DinRailBlind4, AsyncBlind):
    """HmIP-DRBLI4 (Blind Actuator for DIN rail mount – 4 channels)"""


class AsyncDimmer(Dimmer, AsyncDevice):
    """Base dimmer device class"""

    async def set_dim_level(self, dimLevel=0.0, channelIndex=1):
        return await self._connection.api_call(
            *super().set_dim_level(dimLevel=dimLevel, channelIndex=channelIndex)
        )


class AsyncPluggableDimmer(AsyncDimmer):
    """HMIP-PDT Pluggable Dimmer"""


class AsyncBrandDimmer(AsyncDimmer):
    """HMIP-BDT Brand Dimmer"""


class AsyncFullFlushDimmer(AsyncDimmer):
    """HMIP-FDT Dimming Actuator flush-mount"""


class AsyncWeatherSensor(WeatherSensor, AsyncDevice):
    """HMIP-SWO-B"""


class AsyncWeatherSensorPlus(WeatherSensorPlus, AsyncDevice):
    """HMIP-SWO-PL"""


class AsyncWeatherSensorPro(WeatherSensorPro, AsyncDevice):
    """HMIP-SWO-PR"""


class AsyncMultiIOBox(MultiIOBox, AsyncSwitch):
    """HMIP-MIOB (Multi IO Box for floor heating & cooling)"""


class AsyncWaterSensor(WaterSensor, AsyncDevice):
    """HMIP-SWD"""

    async def set_acoustic_alarm_signal(self, acousticAlarmSignal: AcousticAlarmSignal):
        return await self._connection.api_call(
            *super().set_acoustic_alarm_signal(acousticAlarmSignal=acousticAlarmSignal)
        )

    async def set_acoustic_alarm_timing(self, acousticAlarmTiming: AcousticAlarmTiming):
        return await self._connection.api_call(
            *super().set_acoustic_alarm_timing(acousticAlarmTiming=acousticAlarmTiming)
        )

    async def set_acoustic_water_alarm_trigger(
        self, acousticWaterAlarmTrigger: WaterAlarmTrigger
    ):
        return await self._connection.api_call(
            *super().set_acoustic_water_alarm_trigger(
                acousticWaterAlarmTrigger=acousticWaterAlarmTrigger
            )
        )

    async def set_inapp_water_alarm_trigger(
        self, inAppWaterAlarmTrigger: WaterAlarmTrigger
    ):
        return await self._connection.api_call(
            *super().set_inapp_water_alarm_trigger(
                inAppWaterAlarmTrigger=inAppWaterAlarmTrigger
            )
        )

    async def set_siren_water_alarm_trigger(
        self, sirenWaterAlarmTrigger: WaterAlarmTrigger
    ):
        return await self._connection.api_call(
            *super().set_siren_water_alarm_trigger(
                sirenWaterAlarmTrigger=sirenWaterAlarmTrigger
            )
        )


class AsyncAccelerationSensor(AccelerationSensor, AsyncDevice):
    """HMIP-SAM"""

    async def set_acceleration_sensor_mode(
        self, mode: AccelerationSensorMode, channelIndex=1
    ):
        return await self._connection.api_call(
            *super().set_acceleration_sensor_mode(mode, channelIndex)
        )

    async def set_acceleration_sensor_neutral_position(
        self, neutralPosition: AccelerationSensorNeutralPosition, channelIndex=1
    ):
        return await self._connection.api_call(
            *super().set_acceleration_sensor_neutral_position(
                neutralPosition, channelIndex
            )
        )

    async def set_acceleration_sensor_sensitivity(
        self, sensitivity: AccelerationSensorSensitivity, channelIndex=1
    ):
        return await self._connection.api_call(
            *super().set_acceleration_sensor_sensitivity(sensitivity, channelIndex)
        )

    async def set_acceleration_sensor_trigger_angle(self, angle: int, channelIndex=1):
        return await self._connection.api_call(
            *super().set_acceleration_sensor_trigger_angle(angle, channelIndex)
        )

    async def set_acceleration_sensor_event_filter_period(
        self, period: float, channelIndex=1
    ):
        return await self._connection.api_call(
            *super().set_acceleration_sensor_event_filter_period(period, channelIndex)
        )

    async def set_notification_sound_type(
        self, soundType: NotificationSoundType, isHighToLow: bool, channelIndex=1
    ):
        return await self._connection.api_call(
            *super().set_notification_sound_type(soundType, isHighToLow, channelIndex)
        )


class AsyncDoorModule(DoorModule, AsyncDevice):
    """Generic Door Module class"""

    async def send_door_command(self, doorCommand=DoorCommand.STOP):
        return await self._connection.api_call(*super().send_door_command(doorCommand))


class AsyncGarageDoorModuleTormatic(GarageDoorModuleTormatic, AsyncDoorModule):
    """HMIP-MOD-TM (Garage Door Module Tormatic)"""


class AsyncHoermannDrivesModule(HoermannDrivesModule, AsyncDoorModule):
    """HMIP-MOD-HO (Garage Door Module for Hörmann)"""


class AsyncPluggableMainsFailureSurveillance(
    PluggableMainsFailureSurveillance, AsyncDevice
):
    """[HMIP-PMFS] (Plugable Power Supply Monitoring)"""


class AsyncRoomControlDevice(RoomControlDevice, AsyncWallMountedThermostatPro):
    """ALPHA-IP-RBG    (Alpha IP Wall Thermostat Display)"""


class AsyncRoomControlDeviceAnalog(AsyncDevice):
    """ALPHA-IP-RBGa   (ALpha IP Wall Thermostat Display analog)"""

    def __init__(self, connection):
        super().__init__(connection)
        self.actualTemperature = 0.0
        self.setPointTemperature = 0.0
        self.temperatureOffset = 0.0

    def from_json(self, js):
        super().from_json(js)
        c = get_functional_channel("ANALOG_ROOM_CONTROL_CHANNEL", js)
        if c:
            self.set_attr_from_dict("actualTemperature", c)
            self.set_attr_from_dict("setPointTemperature", c)
            self.set_attr_from_dict("temperatureOffset", c)


class AsyncWiredDimmer3(WiredDimmer3, AsyncDimmer):
    """HMIPW-DRD3 (Homematic IP Wired Dimming Actuator – 3x channels)"""


class AsyncWiredInput32(WiredInput32, AsyncFullFlushContactInterface):
    """HMIPW-DRI32 (Homematic IP Wired Inbound module – 32x channels)"""


class AsyncWiredSwitch8(WiredSwitch8, AsyncSwitch):
    """HMIPW-DRS8 (Homematic IP Wired Switch Actuator – 8x channels)"""


class AsyncDinRailSwitch4(DinRailSwitch4, AsyncSwitch):
    """HMIP-DRSI4 (Homematic IP Switch Actuator for DIN rail mount – 4x channels)"""


class AsyncTiltVibrationSensor(TiltVibrationSensor, AsyncDevice):
    """HMIP-STV (Inclination and vibration Sensor)"""

    async def set_acceleration_sensor_mode(
        self, mode: AccelerationSensorMode, channelIndex=1
    ):
        return await self._connection.api_call(
            *super().set_acceleration_sensor_mode(mode, channelIndex)
        )

    async def set_acceleration_sensor_sensitivity(
        self, sensitivity: AccelerationSensorSensitivity, channelIndex=1
    ):
        return await self._connection.api_call(
            *super().set_acceleration_sensor_sensitivity(sensitivity, channelIndex)
        )

    async def set_acceleration_sensor_trigger_angle(self, angle: int, channelIndex=1):
        return await self._connection.api_call(
            *super().set_acceleration_sensor_trigger_angle(angle, channelIndex)
        )

    async def set_acceleration_sensor_event_filter_period(
        self, period: float, channelIndex=1
    ):
        return await self._connection.api_call(
            *super().set_acceleration_sensor_event_filter_period(period, channelIndex)
        )


class AsyncHomeControlAccessPoint(HomeControlAccessPoint, AsyncDevice):
    """HMIP-HAP"""


class AsyncBlindModule(BlindModule, AsyncDevice):
    """HMIP-HDM1 (Hunter Douglas & erfal window blinds)"""

    async def set_primary_shading_level(self, primaryShadingLevel: float):
        return await self._connection.api_call(
            *super().set_primary_shading_level(primaryShadingLevel)
        )

    async def set_secondary_shading_level(
        self, primaryShadingLevel: float, secondaryShadingLevel: float
    ):
        return await self._connection.api_call(
            *super().set_secondary_shading_level(
                primaryShadingLevel, secondaryShadingLevel
            )
        )

    async def stop(self):
        return await self._connection.api_call(*super().stop())


class AsyncRainSensor(RainSensor, AsyncDevice):
    """HMIP-SRD (Rain Sensor)"""


class AsyncTemperatureDifferenceSensor2(TemperatureDifferenceSensor2, AsyncDevice):
    """HmIP-STE2-PCB (Temperature Difference Sensors - 2x sensors)"""


class AsyncWallMountedGarageDoorController(
    WallMountedGarageDoorController, AsyncDevice
):
    """HmIP-WGC (Garage Door Controller)"""

    async def send_start_impulse(self):
        return await self._connection.api_call(*super().send_start_impulse())

class AsyncDoorLockDrive(DoorLockDrive, AsyncDevice):
    """HmIP-DLD (DoorLockDrive)"""

    async def set_lock_state(self, doorLockState: LockState, pin="", channelIndex=1):
        """sets the door lock state

        Args:
            doorLockState(float): the state of the door. See LockState from base/enums.py
            pin(string): Pin, if specified.
            channelIndex(int): the channel to control
        Returns:
            the result of the _restCall
        """
        return await self._connection.api_call(
            *super().set_lock_state(doorLockState, pin, channelIndex)
        )


class AsyncDoorLockSensor(DoorLockSensor, AsyncDevice):
    """HmIP-DLS"""
