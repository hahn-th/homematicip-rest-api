from homematicip.action.action import Action
from homematicip.model.enums import ProfileMode, ClimateControlMode
from homematicip.model.hmip_base import HmipBaseModel
from homematicip.runner import Runner


# class SetGroupChannelsAction(AbstractAction):
#
#     def get_target_type_names(self) -> list[str]:
#         return ["SWITCHING_PROFILE"]
#
#     async def run(self, target: HmipBaseModel, **kwargs):
#         """Set the channels of a group. (No Params)"""
#
#         if not isinstance(target, Group):
#             raise ValueError("target must be a Group")
#
#         channels = []
#         for d in target.devices:
#             channels.append({"channelIndex": 1, "deviceId": d.id})
#         data = {
#             "groupId": target.id,
#             "channels": channels
#         }
#         return await self.connection.async_post("group/switching/profile/setGroupChannels", data)
#
#
#     class SetProfileModeGroupAction(AbstractAction):
#
#         def get_target_type_names(self) -> list[str]:
#             return ["SWITCHING_PROFILE"]
#
#         async def run(self, target: HmipBaseModel, **kwargs):
#             """Set the profile mode of a group.
#
#             Optional: automatic"""
#             automatic = kwargs.get("automatic")
#
#             if not isinstance(target, Group):
#                 raise ValueError("target must be a Group")
#             if not isinstance(automatic, bool):
#                 raise ValueError("automatic must be a boolean")
#
#             channels = []
#             for d in target.devices:
#                 channels.append({"channelIndex": 1, "deviceId": d.id})
#             data = {
#                 "groupId": target.id,
#                 "channels": channels,
#                 "profileMode": "AUTOMATIC"

#
# def set_profile_mode(self, devices, automatic=True):
#     channels = []
#     for d in devices:
#         channels.append[{"channelIndex": 1, "deviceId": d.id}]
#     data = {
#         "groupId": self.id,
#         "channels": channels,
#         "profileMode": ProfileMode.AUTOMATIC if automatic else ProfileMode.MANUAL,
#     }
#     return self._rest_call(
#         "group/switching/profile/setProfileMode", body=json.dumps(data)
#     )
#
# def create(self, label):
#     data = {"label": label}
#     result = self._rest_call(
#         "group/switching/profile/createSwitchingProfileGroup", body=json.dumps(data)
#     )
#     if "groupId" in result:
#         self.id = result["groupId"]
#     return result

@Action.allowed_types("HEATING")
async def action_set_boost(runner: Runner, group: HmipBaseModel, enable):
    data = {"groupId": group.id, "boost": enable}
    return await runner.rest_connection.async_post("group/heating/setBoost", data)


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
        channels.append[{"channelIndex": 1, "deviceId": d.id}]

    data = {
        "groupId": group.id,
        "channels": channels,
        "profileMode": str(profile_mode)
    }
    return await runner.rest_connection.async_post(
        "group/switching/profile/setProfileMode", data)
