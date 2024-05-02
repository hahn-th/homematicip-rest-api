import logging

from pydantic import ValidationError

from homematicip.model.model import Model

LOGGER = logging.getLogger(__name__)


def build_model_from_json(data) -> Model:
    LOGGER.debug("Build model from json.")
    try:
        return Model.model_validate(data, strict=False)
    except ValidationError as e:
        LOGGER.fatal("Error while building model from json.", exc_info=e)
