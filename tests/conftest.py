import json
import os
from pathlib import Path

import pytest
from homematicip.configuration.config import PersistentConfig, Config
from homematicip.connection.rest_connection import ConnectionContext
from homematicip.model.model import build_model_from_json, Model


@pytest.fixture
def path_to_sample_dir():
    return Path(__file__).parent.parent.joinpath("sample_data")


@pytest.fixture
def path_to_sample_home_json(path_to_sample_dir):
    return os.path.join(path_to_sample_dir, "json_data", "home.json")


@pytest.fixture
def config():
    return Config(
        lookup_url="https://localhost:4711/getHost",
        accesspoint_id="3014F711A000000BAD0C0DED",
        auth_token="8A45BAA53BE37E3FCA58E9976EFA4C497DAFE55DB997DB9FD685236E5E63ED7DE",
    )


@pytest.fixture
def connection_context(config: PersistentConfig):
    return ConnectionContext(
        accesspoint_id=config.accesspoint_id,
        auth_token=config.auth_token,
        client_auth_token="test",
        rest_url="https://localhost:4711",
        websocket_url="https://localhost:4711",
    )


@pytest.fixture
def sample_data_complete(path_to_sample_home_json):
    f = open(path_to_sample_home_json, "r")
    return json.load(f)


@pytest.fixture
def filled_model(sample_data_complete) -> Model:
    return build_model_from_json(sample_data_complete)
