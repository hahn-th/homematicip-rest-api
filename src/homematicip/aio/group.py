import json

from homematicip.base.enums import *
from homematicip.group import (
    AlarmSwitchingGroup,
    AccessAuthorizationProfileGroup,
    AccessControlGroup,
    EnvironmentGroup,
    ExtendedLinkedShutterGroup,
    ExtendedLinkedSwitchingGroup,
    ExtendedLinkedGarageDoorGroup,
    Group,
    HeatingChangeoverGroup,
    HeatingCoolingDemandBoilerGroup,
    HeatingCoolingDemandGroup,
    HeatingCoolingDemandPumpGroup,
    HeatingDehumidifierGroup,
    HeatingExternalClockGroup,
    HeatingFailureAlertRuleGroup,
    HeatingGroup,
    HeatingHumidyLimiterGroup,
    HeatingTemperatureLimiterGroup,
    HotWaterGroup,
    HumidityWarningRuleGroup,
    InboxGroup,
    IndoorClimateGroup,
    LinkedSwitchingGroup,
    LockOutProtectionRule,
    MetaGroup,
    OverHeatProtectionRule,
    SecurityGroup,
    SecurityZoneGroup,
    ShutterProfile,
    ShutterWindProtectionRule,
    SmokeAlarmDetectionRule,
    SwitchGroupBase,
    SwitchingGroup,
    SwitchingProfileGroup,
)


class AsyncGroup(Group):
    async def set_label(self, label):
        return await self._connection.api_call(*super().set_label(label))

    async def delete(self):
        return await self._connection.api_call(*super().delete())


class AsyncMetaGroup(MetaGroup, AsyncGroup):
    """a meta group is a "Room" inside the homematic configuration"""

    pass


class AsyncSecurityGroup(SecurityGroup, AsyncGroup):
    pass


class AsyncSwitchGroupBase(SwitchGroupBase, AsyncGroup):
    async def turn_on(self):
        return await self.set_switch_state(True)

    async def turn_off(self):
        return await self.set_switch_state(False)

    async def set_switch_state(self, on=True):
        url, data = super().set_switch_state(on=on)
        return await self._connection.api_call(url, data)


class AsyncSwitchingGroup(SwitchingGroup, AsyncSwitchGroupBase):
    async def set_shutter_level(self, level):
        url, data = super().set_shutter_level(level)
        return await self._connection.api_call(url, data)

    async def set_shutter_stop(self):
        url, data = super().set_shutter_stop()
        return await self._connection.api_call(url, data)

    async def set_slats_level(self, slatsLevel, shutterlevel):
        url, data = super().set_slats_level(slatsLevel, shutterlevel)
        return await self._connection.api_call(url, data)


class AsyncShutterProfile(ShutterProfile, AsyncGroup):
    async def set_shutter_level(self, level):
        url, data = super().set_shutter_level(level)
        return await self._connection.api_call(url, data)

    async def set_shutter_stop(self):
        url, data = super().set_shutter_stop()
        return await self._connection.api_call(url, data)

    async def set_slats_level(self, slatsLevel, shutterlevel):
        url, data = super().set_slats_level(slatsLevel, shutterlevel)
        return await self._connection.api_call(url, data)

    async def set_profile_mode(self, profileMode: ProfileMode):
        return await self._connection.api_call(*super().set_profile_mode(profileMode))


class AsyncLinkedSwitchingGroup(LinkedSwitchingGroup, AsyncGroup):
    async def set_light_group_switches(self, devices):
        url, data = super().set_light_group_switches(devices)
        return await self._connection.api_call(url, data)


class AsyncExtendedLinkedSwitchingGroup(
    ExtendedLinkedSwitchingGroup, AsyncSwitchGroupBase
):
    async def set_on_time(self, onTimeSeconds):
        url, data = super().set_on_time(onTimeSeconds)
        return await self._connection.api_call(url, data)


class AsyncExtendedGarageDoorGroup(ExtendedLinkedGarageDoorGroup, AsyncGroup):
    """Class which represents Extended Garage Door Group."""


class AsyncExtendedLinkedShutterGroup(ExtendedLinkedShutterGroup, AsyncGroup):
    async def set_shutter_level(self, level):
        url, data = super().set_shutter_level(level)
        return await self._connection.api_call(url, data)

    async def set_shutter_stop(self):
        url, data = super().set_shutter_stop()
        return await self._connection.api_call(url, data)

    async def set_slats_level(self, slatsLevel=0.0, shutterLevel=None):
        url, data = super().set_slats_level(slatsLevel, shutterLevel)
        return await self._connection.api_call(url, data)


class AsyncAlarmSwitchingGroup(AlarmSwitchingGroup, AsyncGroup):
    async def set_on_time(self, onTimeSeconds):
        url, data = super().set_on_time(onTimeSeconds)
        return await self._connection.api_call(url, data)

    async def test_signal_optical(
        self, signalOptical=OpticalAlarmSignal.BLINKING_ALTERNATELY_REPEATING
    ):
        url, data = super().test_signal_optical(signalOptical=signalOptical)
        return await self._connection.api_call(url, data)

    async def set_signal_optical(
        self, signalOptical=OpticalAlarmSignal.BLINKING_ALTERNATELY_REPEATING
    ):
        url, data = super().set_signal_optical(signalOptical=signalOptical)
        return await self._connection.api_call(url, data)

    async def test_signal_acoustic(
        self, signalAcoustic=AcousticAlarmSignal.FREQUENCY_FALLING
    ):
        url, data = super().test_signal_acoustic(signalAcoustic=signalAcoustic)
        return await self._connection.api_call(url, data)

    async def set_signal_acoustic(
        self, signalAcoustic=AcousticAlarmSignal.FREQUENCY_FALLING
    ):
        url, data = super().set_signal_acoustic(signalAcoustic=signalAcoustic)
        return await self._connection.api_call(url, data)


# at the moment it doesn't look like this class has any special properties/functions
# keep it as a placeholder in the meantime
class AsyncHeatingHumidyLimiterGroup(HeatingHumidyLimiterGroup, AsyncGroup):
    pass


# at the moment it doesn't look like this class has any special properties/functions
# keep it as a placeholder in the meantime
class AsyncHeatingTemperatureLimiterGroup(HeatingTemperatureLimiterGroup, AsyncGroup):
    pass


class AsyncHeatingChangeoverGroup(HeatingChangeoverGroup, AsyncGroup):
    pass


class AsyncHeatingFailureAlertRuleGroup(HeatingFailureAlertRuleGroup, AsyncGroup):
    pass


# at the moment it doesn't look like this class has any special properties/functions
# keep it as a placeholder in the meantime
class AsyncInboxGroup(InboxGroup, AsyncGroup):
    pass


class AsyncIndoorClimateGroup(IndoorClimateGroup, AsyncGroup):
    pass


class AsyncSecurityZoneGroup(SecurityZoneGroup, AsyncGroup):
    pass


class AsyncHeatingGroup(HeatingGroup, AsyncGroup):
    async def set_point_temperature(self, temperature):
        return await self._connection.api_call(
            *super().set_point_temperature(temperature)
        )

    async def set_boost(self, enable=True):
        return await self._connection.api_call(*super().set_boost(enable=enable))

    async def set_active_profile(self, index):
        return await self._connection.api_call(*super().set_active_profile(index))

    async def set_boost_duration(self, duration: int):
        return await self._connection.api_call(*super().set_boost_duration(duration))

    async def set_control_mode(self, mode=ClimateControlMode.AUTOMATIC):
        return await self._connection.api_call(*super().set_control_mode(mode=mode))


class AsyncHeatingDehumidifierGroup(HeatingDehumidifierGroup, AsyncGroup):
    pass


class AsyncHeatingCoolingDemandGroup(HeatingCoolingDemandGroup, AsyncGroup):
    pass


# at the moment it doesn't look like this class has any special properties/functions
# keep it as a placeholder in the meantime
class AsyncHeatingExternalClockGroup(HeatingExternalClockGroup, AsyncGroup):
    pass


class AsyncHeatingCoolingDemandBoilerGroup(HeatingCoolingDemandBoilerGroup, AsyncGroup):
    pass


class AsyncHeatingCoolingDemandPumpGroup(HeatingCoolingDemandPumpGroup, AsyncGroup):
    pass


class AsyncHumidityWarningRuleGroup(HumidityWarningRuleGroup, AsyncGroup):
    pass


class AsyncSwitchingProfileGroup(SwitchingProfileGroup, AsyncGroup):
    async def set_group_channels(self):
        return await self._connection.api_call(*super().set_group_channels())

    async def set_profile_mode(self, devices, automatic=True):
        return await self._connection.api_call(
            *super().set_profile_mode(devices, automatic=automatic)
        )

    async def create(self, label):
        data = {"label": label}
        result = await self._connection.api_call(
            "group/switching/profile/createSwitchingProfileGroup", body=json.dumps(data)
        )
        if "groupId" in result:
            self.id = result["groupId"]
        return result


class AsyncOverHeatProtectionRule(OverHeatProtectionRule, AsyncGroup):
    pass


class AsyncSmokeAlarmDetectionRule(SmokeAlarmDetectionRule, AsyncGroup):
    pass


class AsyncShutterWindProtectionRule(ShutterWindProtectionRule, AsyncGroup):
    pass


class AsyncLockOutProtectionRule(LockOutProtectionRule, AsyncGroup):
    pass


class AsyncEnvironmentGroup(EnvironmentGroup, AsyncGroup):
    pass


class AsyncHotWaterGroup(HotWaterGroup, AsyncGroup):
    async def set_profile_mode(self, profileMode: ProfileMode):
        return await self._connection.api_call(*super().set_profile_mode(profileMode))


class AsyncAccessAuthorizationProfileGroup(AccessAuthorizationProfileGroup, AsyncGroup):
    pass


class AsyncAccessControlGroup(AccessControlGroup, AsyncGroup):
    pass
