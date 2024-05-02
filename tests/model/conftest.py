import pytest

from homematicip.model import build_model_from_json, Model


@pytest.fixture
def filled_model(sample_data_complete) -> Model:
    return build_model_from_json(sample_data_complete)
