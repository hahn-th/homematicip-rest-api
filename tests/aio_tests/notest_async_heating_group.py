import pytest

from homematicip.aio.group import AsyncHeatingGroup


@pytest.mark.asyncio
async def test_set_point_temperature(fake_connection):
    heating_group = AsyncHeatingGroup(fake_connection)
    resp = await heating_group.set_point_temperature(10)
    assert resp == "called"
    fake_connection.api_call.mock.assert_called_once_with(
        "group/heating/setSetPointTemperature",
        '{"groupId": null, "setPointTemperature": 10}',
    )


# @pytest.mark.asyncio
# async def test_set_boost(self, enable=True):
#     return await self._connection.api_call(*super().set_boost(enable=enable))
#
# @pytest.mark.asyncio
# async def test_set_active_profile(self, index):
#     return await self._connection.api_call(*super().set_active_profile(index))
