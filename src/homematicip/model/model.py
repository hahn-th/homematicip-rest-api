"""This module provides the model class.

Pydantic v1 must be used because of limitations in homeassistant."""
import logging

try:
    from pydantic.v1 import ValidationError  # type: ignore # noqa F401 # pragma: no cover
except ImportError:
    from pydantic import ValidationError  # type: ignore # pragma: no cover

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
        return Model(**data)
    except ValidationError as e:
        LOGGER.fatal("Error while building model from json.", exc_info=e)
