"""This module provides the model class.

Pydantic v1 must be used because of limitations in homeassistant."""
import logging

from homematicip.events.event_manager import EventManager
from homematicip.events.event_types import ModelUpdateEvent

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


def update_model_from_json(model: Model, event_manager: EventManager, data):
    """Update a model from json data.

    :param model: The model to update.
    :param event_manager: The event manager to publish events.
    :param data: The json data to update the model."""

    LOGGER.debug("Update model from json.")

    try:
        for key in data:
            if key == "home":
                if model.home.update_from_dict(data[key]):
                    event_manager.publish(ModelUpdateEvent.ITEM_UPDATED, model.home)
            elif key == "clients":
                for client_json in data[key].items():
                    client_id = client_json[0]
                    client_data = client_json[1]
                    if client_id in model.clients:
                        if model.clients[client_id].update_from_dict(client_data):
                            event_manager.publish(ModelUpdateEvent.ITEM_UPDATED, model.clients[client_id])
                    else:
                        model.clients[client_id] = Client(**client_data)
                        event_manager.publish(ModelUpdateEvent.ITEM_CREATED, model.clients[client_id])
            elif key == "devices":
                for device_json in data[key].items():
                    device_id = device_json[0]
                    device_data = device_json[1]
                    if device_id in model.devices:
                        if model.devices[device_id].update_from_dict(device_data):
                            event_manager.publish(ModelUpdateEvent.ITEM_UPDATED, model.devices[device_id])
                    else:
                        model.devices[device_id] = Device(**device_data)
                        event_manager.publish(ModelUpdateEvent.ITEM_CREATED, model.devices[device_id])
            elif key == "groups":
                for group_json in data[key].items():
                    group_id = group_json[0]
                    group_data = group_json[1]
                    if group_id in model.groups:
                        if model.groups[group_id].update_from_dict(group_data):
                            event_manager.publish(ModelUpdateEvent.ITEM_UPDATED, model.groups[group_id])
                    else:
                        model.groups[group_id] = Group(**group_data)
                        event_manager.publish(ModelUpdateEvent.ITEM_CREATED, model.groups[group_id])

    except ValidationError as e:
        LOGGER.fatal("Error while updating model from json.", exc_info=e)
