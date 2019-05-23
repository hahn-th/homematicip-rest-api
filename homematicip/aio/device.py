import logging

from homematicip.device import *
from homematicip.base.enums import *

ERROR_CODE = "errorCode"

_LOGGER = logging.getLogger(__name__)


class AsyncDevice(Device):
    """ Async implementation of a genereric homematic ip device """

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
    """ Generic async switch """

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


class AsyncPlugableSwitch(PlugableSwitch, AsyncSwitch):
    """ Async implementation of HMIP-PS (Pluggable Switch) """


class AsyncPrintedCircuitBoardSwitchBattery(
    PrintedCircuitBoardSwitchBattery, AsyncSwitch
):
    """ HmIP-PCBS-BAT (Printed Curcuit Board Switch Battery) """


class AsyncPrintedCircuitBoardSwitch2(PrintedCircuitBoardSwitch2, AsyncSwitch):
    """ Async implementation of HMIP-PCBS2 (Switch Circuit Board - 2x channels) """


class AsyncLightSensor(LightSensor, AsyncDevice):
    """ Async implementation of HMIP-SLO (Light Sensor outdoor) """


class AsyncSabotageDevice(SabotageDevice, AsyncDevice):
    pass


class AsyncOpenCollector8Module(OpenCollector8Module, AsyncSwitch):
    """ Async implementation of HmIP-MOD-OC8 ( Open Collector Module ) """


class AsyncOperationLockableDevice(OperationLockableDevice, AsyncDevice):
    async def set_operation_lock(self, operationLock=True):
        return await self._connection.api_call(
            *super().set_operation_lock(operationLock=operationLock)
        )


class AsyncBrandSwitchNotificationLight(BrandSwitchNotificationLight, AsyncSwitch):
    """ HMIP-BSL (Switch Actuator for brand switches – with signal lamp) """

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


class AsyncPlugableSwitchMeasuring(PlugableSwitchMeasuring, AsyncSwitch):
    """ HMIP-PSM (Pluggable Switch and Meter) """

    async def reset_energy_counter(self):
        return await self._connection.api_call(*super().reset_energy_counter())


class AsyncBrandSwitchMeasuring(BrandSwitchMeasuring, AsyncSwitch):
    """ HMIP-BSM (Brand Switch and Meter) """


class AsyncFullFlushSwitchMeasuring(FullFlushSwitchMeasuring, AsyncSwitch):
    """ HmIP-FSM (Full flush Switch and Meter) """


class AsyncShutterContact(ShutterContact, AsyncSabotageDevice):
    """ HMIP-SWDO (Door / Window Contact - optical) /
    HMIP-SWDO-I (Door / Window Contact Invisible - optical) / 
    HmIP-SWDM /  HmIP-SWDM-B2  (Door / Window Contact - magnetic"""

    pass


class AsyncRotaryHandleSensor(RotaryHandleSensor, AsyncSabotageDevice):
    """ HmIP-SRH """


class AsyncTemperatureHumiditySensorOutdoor(
    TemperatureHumiditySensorOutdoor, AsyncDevice
):
    """ HmIP-STHO (Temperature and Humidity Sensor outdoor) """


class AsyncHeatingThermostat(HeatingThermostat, AsyncOperationLockableDevice):
    """ HMIP-eTRV (Radiator Thermostat) """

    pass


class AsyncHeatingThermostatCompact(HeatingThermostatCompact, AsyncSabotageDevice):
    """ HmIP-eTRV-C (Heating-thermostat compact without display) """

    pass


class AsyncTemperatureHumiditySensorWithoutDisplay(
    TemperatureHumiditySensorWithoutDisplay, AsyncDevice
):
    """ HMIP-STH (Temperature and Humidity Sensor without display - indoor) """

    pass


class AsyncTemperatureHumiditySensorDisplay(
    TemperatureHumiditySensorDisplay, AsyncDevice
):
    """ HMIP-STHD (Temperature and Humidity Sensor with display - indoor) """

    async def set_display(
        self, display: ClimateControlDisplay = ClimateControlDisplay.ACTUAL
    ):
        await self._connection.api_call(*super().set_display(display=display))


class AsyncWallMountedThermostatPro(
    WallMountedThermostatPro,
    AsyncTemperatureHumiditySensorDisplay,
    AsyncOperationLockableDevice,
):
    """ HMIP-WTH, HMIP-WTH-2 (Wall Thermostat with Humidity Sensor)
    / HMIP-BWTH (Brand Wall Thermostat with Humidity Sensor)"""

    pass


class AsyncSmokeDetector(SmokeDetector, AsyncDevice):
    """ HMIP-SWSD (Smoke Alarm with Q label) """

    pass


class AsyncFloorTerminalBlock6(FloorTerminalBlock6, AsyncDevice):
    """ HMIP-FAL230-C6 (Floor Heating Actuator - 6 channels, 230 V) """

    pass


class AsyncFloorTerminalBlock10(FloorTerminalBlock10, AsyncFloorTerminalBlock6):
    """ HMIP-FAL24-C10  (Floor Heating Actuator – 10x channels, 24V) """


class AsyncPushButton(PushButton, AsyncDevice):
    """ HMIP-WRC2 (Wall-mount Remote Control - 2-button) """


class AsyncPushButton6(PushButton6, AsyncPushButton):
    """ HMIP-WRC6 (Wall-mount Remote Control - 6-button)  """


class AsyncBrandPushButton(BrandPushButton, AsyncPushButton):
    """ HMIP-BRC2 (Remote Control for brand switches – 2x channels) """


class AsyncKeyRemoteControl4(KeyRemoteControl4, AsyncPushButton):
    """ HMIP-KRC4 (Key Ring Remote Control - 4 buttons) """


class AsyncRemoteControl8(RemoteControl8, AsyncPushButton):
    """ HmIP-RC8 (Remote Control - 8 buttons) """


class AsyncAlarmSirenIndoor(AlarmSirenIndoor, AsyncSabotageDevice):
    """ HMIP-ASIR (Alarm Siren) """


class AsyncMotionDetectorIndoor(MotionDetectorIndoor, AsyncSabotageDevice):
    """ HMIP-SMI (Motion Detector with Brightness Sensor - indoor) """

    pass


class AsyncMotionDetectorOutdoor(MotionDetectorOutdoor, AsyncDevice):
    """ HmIP-SMO-A (Motion Detector with Brightness Sensor - outdoor) """

    pass


class AsyncMotionDetectorPushButton(MotionDetectorPushButton, AsyncSabotageDevice):
    """ HMIP-SMI55 (Motion Detector with Brightness Sensor and Remote Control - 2-button) """

    pass


class AsyncPresenceDetectorIndoor(PresenceDetectorIndoor, AsyncSabotageDevice):
    """ HMIP-SPI (Presence Sensor - indoor) """

    pass


class AsyncPassageDetector(PassageDetector, AsyncSabotageDevice):
    """ HMIP-SPDR (Passage Detector) """

    pass


class AsyncKeyRemoteControlAlarm(KeyRemoteControlAlarm, AsyncDevice):
    """ HMIP-KRCA (Key Ring Remote Control - alarm) """

    pass


class AsyncFullFlushContactInterface(FullFlushContactInterface, AsyncDevice):
    """ HMIP-FCI1 (Contact Interface flush-mount – 1 channel) """

    pass


class AsyncFullFlushShutter(FullFlushShutter, AsyncDevice):
    """ HMIP-FROLL (Shutter Actuator - flush-mount) / HMIP-BROLL (Shutter Actuator - Brand-mount) """

    async def set_shutter_level(self, level):
        return await self._connection.api_call(*super().set_shutter_level(level))

    async def set_shutter_stop(self):
        return await self._connection.api_call(*super().set_shutter_stop())


class AsyncFullFlushBlind(FullFlushBlind, AsyncFullFlushShutter):
    """HMIP-FBL (Blind Actuator - flush-mount)"""

    async def set_slats_level(self, slatsLevel=0.0, shutterLevel=None):
        return await self._connection.api_call(
            *super().set_slats_level(slatsLevel, shutterLevel)
        )


class AsyncBrandBlind(BrandBlind, AsyncFullFlushBlind):
    """ HMIP-BBL (Blind Actuator for brand switches) """


class AsyncDimmer(Dimmer, AsyncDevice):
    """Base dimmer device class"""

    async def set_dim_level(self, dimLevel=0.0):
        return await self._connection.api_call(
            *super().set_dim_level(dimLevel=dimLevel)
        )


class AsyncPluggableDimmer(AsyncDimmer):
    """HmIP-PDT Pluggable Dimmer"""


class AsyncBrandDimmer(AsyncDimmer):
    """HmIP-BDT Brand Dimmer"""


class AsyncFullFlushDimmer(AsyncDimmer):
    """HmIP-FDT Dimming Actuator flush-mount"""


class AsyncWeatherSensor(WeatherSensor, AsyncDevice):
    """ HmIP-SWO-B """


class AsyncWeatherSensorPlus(WeatherSensorPlus, AsyncDevice):
    """ HmIP-SWO-PL """


class AsyncWeatherSensorPro(WeatherSensorPro, AsyncDevice):
    """ HmIP-SWO-PR """


class AsyncMultiIOBox(MultiIOBox, AsyncSwitch):
    """ HMIP-MIOB (Multi IO Box for floor heating & cooling)  """


class AsyncWaterSensor(WaterSensor, AsyncDevice):
    """ HmIP-SWD """

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
