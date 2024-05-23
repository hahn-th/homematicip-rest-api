import pytest

from homematicip.model.model import Model,build_model_from_json


@pytest.fixture
def filled_model(sample_data_complete) -> Model:
    return build_model_from_json(sample_data_complete)
