import pytest
from click.testing import CliRunner

from homematicip.cli import hmip
from homematicip.cli.hmip import _model_update_event_handler
from homematicip.events.event_types import ModelUpdateEvent
from homematicip.model.model import Model, build_model_from_json


@pytest.fixture
def filled_model(sample_data_complete) -> Model:
    return build_model_from_json(sample_data_complete)

#
# def test_version():
#     result = CliRunner().invoke(hmip.cli, ["version"])
#     assert result.exit_code == 0
#     assert "HomematicIP-Rest-Api" in result.output
#
# def test_list_devices(mocker):
#     result = CliRunner().invoke(hmip.cli, ["list", "devices"])
#     assert result.exit_code == 0

@pytest.mark.asyncio
async def test_model_update_event_handler(filled_model: Model):
    device = filled_model.devices["3014F7110000RAIN_SENSOR"]

    await _model_update_event_handler(ModelUpdateEvent.ITEM_UPDATED, device)