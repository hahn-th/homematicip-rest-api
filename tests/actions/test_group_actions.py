import pytest

from homematicip.action.group_actions import async_set_switch_state_group
from homematicip.connection.rest_connection import RestConnection, RestResult
from homematicip.model.model_components import Group
from homematicip.runner import Runner


@pytest.fixture
def runner(mocker, filled_model):
    conn = mocker.Mock(spec=RestConnection)
    conn.async_post.return_value = RestResult(status=200)
    runner = Runner(_rest_connection=conn, model=filled_model)
    return runner


@pytest.fixture
def sample_group() -> Group:
    return Group(id="00000000-0000-0000-0000-000000000001", type="", channels=[])


@pytest.mark.asyncio
async def test_wrong_group_type(runner, sample_group):
    sample_group.type = "ASDF"
    with pytest.raises(ValueError):
        await async_set_switch_state_group(runner.rest_connection, sample_group, True)

@pytest.mark.asyncio
async def test_group_set_switch_state(runner, sample_group):
    sample_group.type = "SWITCHING"
    await async_set_switch_state_group(runner.rest_connection, sample_group, True)
    runner.rest_connection.async_post.assert_called_once_with("group/switching/setState",
                                                              {"groupId": sample_group.id, "on": True})

#
# from homematicip.action.group_actions import SetPointTemperatureGroupAction, SetBoostGroupAction, \
#     SetBoostDurationGroupAction, SetActiveProfileGroupAction, SetControlModeGroupAction, \
#     SetHeatingProfileModeGroupAction
# from homematicip.connection.rest_connection import RestConnection, ConnectionContext
# from homematicip.model.enums import ProfileMode
#
#
# @pytest.mark.asyncio
# async def test_heating_set_point_temperature(filled_model, mocker):
#     connection = RestConnection(ConnectionContext())
#     patched = mocker.patch("homematicip.connection.rest_connection.RestConnection.async_post")
#     patched.return_value = "OK"
#     group_id = "00000000-0000-0000-0000-000000000010"
#     group = filled_model.groups[group_id]
#
#     action = SetPointTemperatureGroupAction(connection)
#     result = await action.run(group, temperature=22)
#
#     assert result == "OK"
#     assert patched.call_args.args[0] == "group/heating/setPointTemperature"
#     assert patched.call_args.args[1] == {"groupId": group_id, "setPointTemperature": 22}
#
#
# @pytest.mark.asyncio
# async def test_heating_set_boost(filled_model, mocker):
#     connection = RestConnection(ConnectionContext())
#     patched = mocker.patch("homematicip.connection.rest_connection.RestConnection.async_post")
#     patched.return_value = "OK"
#     group_id = "00000000-0000-0000-0000-000000000010"
#     group = filled_model.groups[group_id]
#
#     action = SetBoostGroupAction(connection)
#     result = await action.run(group, enable=True)
#
#     assert result == "OK"
#     assert patched.call_args.args[0] == "group/heating/setBoost"
#     assert patched.call_args.args[1] == {"groupId": group_id, "boost": True}
#
#
# @pytest.mark.asyncio
# async def test_heating_set_boost_duration(filled_model, mocker):
#     connection = RestConnection(ConnectionContext())
#     patched = mocker.patch("homematicip.connection.rest_connection.RestConnection.async_post")
#     patched.return_value = "OK"
#     group_id = "00000000-0000-0000-0000-000000000010"
#     group = filled_model.groups[group_id]
#
#     action = SetBoostDurationGroupAction(connection)
#     result = await action.run(group, duration=10)
#
#     assert result == "OK"
#     assert patched.call_args.args[0] == "group/heating/setBoostDuration"
#     assert patched.call_args.args[1] == {"groupId": group_id, "boostDuration": 10}
#
#
# @pytest.mark.asyncio
# async def test_heating_set_active_profile(filled_model, mocker):
#     connection = RestConnection(ConnectionContext())
#     patched = mocker.patch("homematicip.connection.rest_connection.RestConnection.async_post")
#     patched.return_value = "OK"
#     group_id = "00000000-0000-0000-0000-000000000010"
#     group = filled_model.groups[group_id]
#
#     action = SetActiveProfileGroupAction(connection)
#     result = await action.run(group, index=12345)
#
#     assert result == "OK"
#     assert patched.call_args.args[0] == "group/heating/setActiveProfile"
#     assert patched.call_args.args[1] == {"groupId": group_id, "profileIndex": 12345}
#
#
# @pytest.mark.asyncio
# async def test_heating_set_control_mode(filled_model, mocker):
#     connection = RestConnection(ConnectionContext())
#     patched = mocker.patch("homematicip.connection.rest_connection.RestConnection.async_post")
#     patched.return_value = "OK"
#     group_id = "00000000-0000-0000-0000-000000000010"
#     group = filled_model.groups[group_id]
#
#     action = SetControlModeGroupAction(connection)
#     result = await action.run(group, mode=ClimateControlMode.MANUAL)
#
#     assert result == "OK"
#     assert patched.call_args.args[0] == "group/heating/setControlMode"
#     assert patched.call_args.args[1] == {"groupId": group_id, "controlMode": ClimateControlMode.MANUAL.value}
#
#
# @pytest.mark.asyncio
# async def test_heating_set_heating_profile_mode(filled_model, mocker):
#     connection = RestConnection(ConnectionContext())
#     patched = mocker.patch("homematicip.connection.rest_connection.RestConnection.async_post")
#     patched.return_value = "OK"
#     group_id = "00000000-0000-0000-0000-000000000010"
#     group = filled_model.groups[group_id]
#
#     action = SetHeatingProfileModeGroupAction(connection)
#     result = await action.run(group, profile_mode=ProfileMode.AUTOMATIC)
#
#     assert result == "OK"
#     assert patched.call_args.args[0] == "group/heating/setProfileMode"
#     assert patched.call_args.args[1] == {"groupId": group_id, "profileMode": str(ProfileMode.AUTOMATIC)}
