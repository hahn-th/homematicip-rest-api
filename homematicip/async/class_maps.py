import homematicip.base.constants as cn

from homematicip.async.device import AsyncPlugableSwitch, \
    AsyncPlugableSwitchMeasuring, AsyncShutterContact
from homematicip.async.group import AsyncSecurityGroup, AsyncSwitchingGroup, \
    AsyncExtendedLinkedSwitchingGroup, AsyncLinkedSwitchingGroup, AsyncAlarmSwitchingGroup, \
    AsyncHeatingHumidyLimiterGroup, AsyncHeatingTemperatureLimiterGroup, \
    AsyncHeatingChangeoverGroup, AsyncInboxGroup, AsyncSecurityZoneGroup, AsyncHeatingGroup, \
    AsyncHeatingCoolingDemandGroup, AsyncHeatingExternalClockGroup, AsyncHeatingDehumidifierGroup, \
    AsyncHeatingCoolingDemandBoilerGroup, AsyncHeatingCoolingDemandPumpGroup, \
    AsyncSwitchingProfileGroup, AsyncOverHeatProtectionRule, AsyncSmokeAlarmDetectionRule, \
    AsyncLockOutProtectionRule, AsyncShutterWindProtectionRule, AsyncExtendedLinkedShutterGroup

TYPE_CLASS_MAP = {
    cn.PLUGABLE_SWITCH_MEASURING: AsyncPlugableSwitchMeasuring,
    cn.PLUGABLE_SWITCH: AsyncPlugableSwitch,
    cn.SHUTTER_CONTACT: AsyncShutterContact
}

TYPE_GROUP_MAP = {
    cn.SECURITY: AsyncSecurityGroup,
    cn.SWITCHING: AsyncSwitchingGroup,
    cn.EXTENDED_LINKED_SWITCHING: AsyncExtendedLinkedSwitchingGroup,
    cn.LINKED_SWITCHING: AsyncLinkedSwitchingGroup,
    cn.ALARM_SWITCHING: AsyncAlarmSwitchingGroup,
    cn.HEATING_HUMIDITY_LIMITER: AsyncHeatingHumidyLimiterGroup,
    cn.HEATING_TEMPERATURE_LIMITER: AsyncHeatingTemperatureLimiterGroup,
    cn.HEATING_CHANGEOVER: AsyncHeatingChangeoverGroup,
    cn.INBOX: AsyncInboxGroup,
    cn.SECURITY_ZONE: AsyncSecurityZoneGroup,
    cn.HEATING: AsyncHeatingGroup,
    cn.HEATING_COOLING_DEMAND: AsyncHeatingCoolingDemandGroup,
    cn.HEATING_EXTERNAL_CLOCK: AsyncHeatingExternalClockGroup,
    cn.HEATING_DEHUMIDIFIER: AsyncHeatingDehumidifierGroup,
    cn.HEATING_COOLING_DEMAND_BOILER: AsyncHeatingCoolingDemandBoilerGroup,
    cn.HEATING_COOLING_DEMAND_PUMP: AsyncHeatingCoolingDemandPumpGroup,
    cn.SWITCHING_PROFILE: AsyncSwitchingProfileGroup,
    cn.OVER_HEAT_PROTECTION_RULE: AsyncOverHeatProtectionRule,
    cn.SMOKE_ALARM_DETECTION_RULE: AsyncSmokeAlarmDetectionRule,
    cn.LOCK_OUT_PROTECTION_RULE: AsyncLockOutProtectionRule,
    cn.SHUTTER_WIND_PROTECTION_RULE: AsyncShutterWindProtectionRule,
    cn.EXTENDED_LINKED_SHUTTER: AsyncExtendedLinkedShutterGroup
}

TYPE_SECURITY_EVENT_MAP = {

}
