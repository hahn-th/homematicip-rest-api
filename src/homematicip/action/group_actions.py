import logging

from homematicip.action.action import Action
from homematicip.action.registry import ActionTarget
from homematicip.connection.rest_connection import RestConnection
from homematicip.model.enums import ProfileMode, ClimateControlMode
from homematicip.model.hmip_base import HmipBaseModel
from homematicip.model.model_components import Group
from homematicip.runner import Runner

LOGGER = logging.getLogger(__name__)


@Action.allowed_types("HEATING")
@Action.cli_commands("set_boost")
@Action.target_type(ActionTarget.GROUP)
async def async_set_boost_group(rest_connection: RestConnection, group: HmipBaseModel, enable):
    data = {"groupId": group.id, "boost": enable}
    return await rest_connection.async_post("group/heating/setBoost", data)


@Action.allowed_types("HEATING")
@Action.cli_commands("set_boost_duration")
@Action.target_type(ActionTarget.GROUP)
async def async_set_boost_duration_group(rest_connection: RestConnection, group: HmipBaseModel, duration: int):
    data = {"groupId": group.id, "boostDuration": duration}
    return await rest_connection.async_post("group/heating/setBoostDuration", data)


@Action.allowed_types("EXTENDED_LINKED_SHUTTER", "SHUTTER_PROFILE", "SWITCHING")
@Action.cli_commands("set_shutter_level")
@Action.target_type(ActionTarget.GROUP)
async def async_set_shutter_level_group(rest_connection: RestConnection, group: HmipBaseModel, shutter_level):
    data = {"groupId": group.id, "shutterLevel": shutter_level}
    return await rest_connection.async_post("group/switching/setShutterLevel", data)


@Action.allowed_types("EXTENDED_LINKED_SHUTTER", "SHUTTER_PROFILE", "SWITCHING")
@Action.cli_commands("set_shutter_stop")
@Action.target_type(ActionTarget.GROUP)
async def async_set_shutter_stop_group(rest_connection: RestConnection, group: HmipBaseModel):
    data = {"groupId": group.id}
    return await rest_connection.async_post("group/switching/stop", data)


@Action.allowed_types("EXTENDED_LINKED_SHUTTER", "SHUTTER_PROFILE", "SWITCHING")
@Action.cli_commands("set_slats_level")
@Action.target_type(ActionTarget.GROUP)
async def async_set_slats_level_group(rest_connection: RestConnection, group: HmipBaseModel, slats_level,
                                      shutter_level=None):
    LOGGER.info(
        f"Run 'action_set_slats_level_group'. Setting slats level to {slats_level} and shutter level to {shutter_level or '<None>'}")
    if shutter_level is None:
        shutter_level = group.shutterLevel

    data = {
        "groupId": group.id,
        "slatsLevel": slats_level,
        "shutterLevel": shutter_level
    }
    return await rest_connection.async_post("group/switching/setSlatsLevel", data)


@Action.allowed_types("HEATING")
@Action.cli_commands("set_point_temperature")
@Action.target_type(ActionTarget.GROUP)
async def async_set_point_temperature_group(rest_connection: RestConnection, group: HmipBaseModel, temperature):
    data = {"groupId": group.id, "setPointTemperature": temperature}
    return await rest_connection.async_post("group/heating/setSetPointTemperature", data)


@Action.allowed_types("HEATING")
@Action.cli_commands("set_active_profile")
@Action.target_type(ActionTarget.GROUP)
async def async_set_active_profile_group(rest_connection: RestConnection, group: HmipBaseModel, index):
    data = {"groupId": group.id, "profileIndex": index}
    return await rest_connection.async_post("group/heating/setActiveProfile", data)


@Action.allowed_types("HEATING")
@Action.cli_commands("set_control_mode")
@Action.target_type(ActionTarget.GROUP)
async def async_set_control_mode_group(rest_connection: RestConnection, group: HmipBaseModel,
                                       mode=ClimateControlMode.AUTOMATIC):
    data = {"groupId": group.id, "controlMode": str(mode)}
    return await rest_connection.async_post("group/heating/setControlMode", data)


@Action.allowed_types("EXTENDED_LINKED_SWITCHING", "SWITCHING")
@Action.cli_commands("set_switch_state", "turn_on", "turn_off")
@Action.target_type(ActionTarget.GROUP)
async def async_set_switch_state_group(rest_connection: RestConnection, group: Group, on):
    """Set switching state of group

    :param rest_connection: RestConnection
    :param group: The group to set the state
    :param on: True switches on, False switches off
    """
    data = {"groupId": group.id, "on": on}
    return await rest_connection.async_post("group/switching/setState", data)


@Action.allowed_types("EXTENDED_LINKED_SWITCHING", "ALARM_SWITCHING")
@Action.cli_commands("set_on_time")
@Action.target_type(ActionTarget.GROUP)
async def async_set_on_time_group(rest_connection: RestConnection, group: Group, on_time_seconds):
    data = {"groupId": group.id, "onTime": on_time_seconds}
    return await rest_connection.async_post("group/switching/alarm/setOnTime", data)
