import logging

from homematicip.action.action import Action
from homematicip.connection.rest_connection import RestConnection
from homematicip.model.enums import ProfileMode, ClimateControlMode
from homematicip.model.hmip_base import HmipBaseModel
from homematicip.runner import Runner

LOGGER = logging.getLogger(__name__)


@Action.allowed_types("HEATING")
async def action_set_boost(rest_connection: RestConnection, group: HmipBaseModel, enable):
    data = {"groupId": group.id, "boost": enable}
    return await rest_connection.async_post("group/heating/setBoost", data)


@Action.allowed_types("EXTENDED_LINKED_SHUTTER", "SHUTTER_PROFILE", "SWITCHING")
async def action_set_shutter_level_group(rest_connection: RestConnection, group: HmipBaseModel, shutter_level):
    data = {"groupId": group.id, "shutterLevel": shutter_level}
    return await rest_connection.async_post("group/switching/setShutterLevel", data)


@Action.allowed_types("EXTENDED_LINKED_SHUTTER", "SHUTTER_PROFILE", "SWITCHING")
async def action_set_stop_group(rest_connection: RestConnection, group: HmipBaseModel):
    data = {"groupId": group.id}
    return await rest_connection.async_post("group/switching/stop", data)


@Action.allowed_types("EXTENDED_LINKED_SHUTTER", "SHUTTER_PROFILE", "SWITCHING")
async def action_set_slats_level_group(rest_connection: RestConnection, group: HmipBaseModel, slats_level,
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
async def action_set_point_temperature(rest_connection: RestConnection, group: HmipBaseModel, temperature):
    data = {"groupId": group.id, "setPointTemperature": temperature}
    return await rest_connection.async_post("group/heating/setSetPointTemperature", data)


@Action.allowed_types("HEATING")
async def action_set_boost_duration(rest_connection: RestConnection, group: HmipBaseModel, duration: int):
    data = {"groupId": group.id, "boostDuration": duration}
    return await rest_connection.async_post("group/heating/setBoostDuration", data)


@Action.allowed_types("HEATING")
async def action_set_active_profile(rest_connection: RestConnection, group: HmipBaseModel, index):
    data = {"groupId": group.id, "profileIndex": index}
    return await rest_connection.async_post("group/heating/setActiveProfile", data)


@Action.allowed_types("HEATING")
async def action_set_control_mode(rest_connection: RestConnection, group: HmipBaseModel,
                                  mode=ClimateControlMode.AUTOMATIC):
    data = {"groupId": group.id, "controlMode": str(mode)}
    return await rest_connection.async_post("group/heating/setControlMode", data)


#
# @Action.allowed_types("SWITCHING_PROFILE")
# async def set_profile_mode(rest_connection: RestConnection, group: HmipBaseModel, profile_mode: ProfileMode):
#     devices = [runner.model.devices[d] for d in group.devices]
#     channels = []
#     for d in devices:
#         channels.append({"channelIndex": 1, "deviceId": d.id})
#
#     data = {
#         "groupId": group.id,
#         "channels": channels,
#         "profileMode": str(profile_mode)
#     }
#     return await rest_connection.async_post(
#         "group/switching/profile/setProfileMode", data)

