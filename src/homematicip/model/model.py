import logging

from pydantic import ValidationError

from homematicip.model.model_components import Group, Device, Client
from homematicip.model.hmip_base import HmipBaseModel
from homematicip.model.home import Home

LOGGER = logging.getLogger(__name__)


class Model(HmipBaseModel):
    """The model class represents the complete homematicip model."""
    clients: dict[str, Client] = {}
    devices: dict[str, Device] = {}
    groups: dict[str, Group] = {}
    home: Home


def build_model_from_json(data) -> Model:
    """Build a model from json data."""
    LOGGER.debug("Build model from json.")
    try:
        return Model.model_validate(data, strict=False)
    except ValidationError as e:
        LOGGER.fatal("Error while building model from json.", exc_info=e)
