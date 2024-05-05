import logging

from homematicip.action.action import Action
from homematicip.model.enums import ProfileMode, ClimateControlMode
from homematicip.model.hmip_base import HmipBaseModel
from homematicip.runner import Runner

LOGGER = logging.getLogger(__name__)


@Action.allowed_types("HEATING")
async def action_set_boost(runner: Runner, group: HmipBaseModel, enable):
    data = {"groupId": group.id, "boost": enable}
    return await runner.rest_connection.async_post("group/heating/setBoost", data)


@Action.allowed_types("EXTENDED_LINKED_SHUTTER", "SHUTTER_PROFILE", "SWITCHING")
async def action_set_shutter_level_group(runner: Runner, group: HmipBaseModel, shutter_level):
    data = {"groupId": group.id, "shutterLevel": shutter_level}
    return await runner.rest_connection.async_post("group/switching/setShutterLevel", data)


@Action.allowed_types("EXTENDED_LINKED_SHUTTER", "SHUTTER_PROFILE", "SWITCHING")
async def action_set_stop_group(runner: Runner, group: HmipBaseModel):
    data = {"groupId": group.id}
    return await runner.rest_connection.async_post("group/switching/stop", data)


@Action.allowed_types("EXTENDED_LINKED_SHUTTER", "SHUTTER_PROFILE", "SWITCHING")
async def action_set_slats_level_group(runner: Runner, group: HmipBaseModel, slats_level, shutter_level=None):
    LOGGER.info(f"Run 'action_set_slats_level_group'. Setting slats level to {slats_level} and shutter level to {shutter_level or '<None>'}")
    if shutter_level is None:
        shutter_level = group.shutterLevel

    data = {
        "groupId": group.id,
        "slatsLevel": slats_level,
        "shutterLevel": shutter_level
    }
    return await runner.rest_connection.async_post("group/switching/setSlatsLevel", data)


@Action.allowed_types("HEATING")
async def action_set_point_temperature(runner: Runner, group: HmipBaseModel, temperature):
    data = {"groupId": group.id, "setPointTemperature": temperature}
    return await runner.rest_connection.async_post("group/heating/setSetPointTemperature", data)


@Action.allowed_types("HEATING")
async def action_set_boost_duration(runner: Runner, group: HmipBaseModel, duration: int):
    data = {"groupId": group.id, "boostDuration": duration}
    return await runner.rest_connection.async_post("group/heating/setBoostDuration", data)


@Action.allowed_types("HEATING")
async def action_set_active_profile(runner: Runner, group: HmipBaseModel, index):
    data = {"groupId": group.id, "profileIndex": index}
    return await runner.rest_connection.async_post("group/heating/setActiveProfile", data)


@Action.allowed_types("HEATING")
async def action_set_control_mode(runner: Runner, group: HmipBaseModel, mode=ClimateControlMode.AUTOMATIC):
    data = {"groupId": group.id, "controlMode": str(mode)}
    return await runner.rest_connection.async_post("group/heating/setControlMode", data)


@Action.allowed_types("SWITCHING_PROFILE")
async def set_profile_mode(runner: Runner, group: HmipBaseModel, profile_mode: ProfileMode):
    devices = [runner.model.devices[d] for d in group.devices]
    channels = []
    for d in devices:
        channels.append({"channelIndex": 1, "deviceId": d.id})

    data = {
        "groupId": group.id,
        "channels": channels,
        "profileMode": str(profile_mode)
    }
    return await runner.rest_connection.async_post(
        "group/switching/profile/setProfileMode", data)
