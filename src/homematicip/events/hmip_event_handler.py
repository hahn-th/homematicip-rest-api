import logging

from pydantic import BaseModel
from homematicip.events.event_manager import EventManager
from homematicip.events.event_manager import ModelUpdateEvent
from homematicip.events.event_types import EventType
from homematicip.model.client import Client
from homematicip.model.devices import Device
from homematicip.model.model import Model

LOGGER = logging.getLogger(__name__)


class HmipEventHandler:
    """Take an incoming event from homematicip-cloud websocket and update model."""

    def __init__(self, event_manager: EventManager, model: Model):
        self._model = model
        self._event_manager = event_manager

    def process_event(self, event_json):
        for event in event_json["events"].values():

            LOGGER.info(f"Processing event {event['pushEventType']}")

            event_type = EventType[event['pushEventType']]
            if event_type == EventType.CLIENT_ADDED:
                data = event['client']
                client_id = data['id']
                client = Client.model_validate_json(data, strict=False)
                self._model.clients[client_id] = client
                self._event_manager.publish(ModelUpdateEvent.ITEM_CREATED, client)

            elif event_type == EventType.CLIENT_CHANGED:
                data = event['client']
                if data['id'] in self._model.clients:
                    client: BaseModel = self._model.clients[data['id']]
                    self._model.clients[data['id']] = client.model_copy(update={**data})
                    self._event_manager.publish(ModelUpdateEvent.ITEM_UPDATED, client)

            elif event_type == EventType.CLIENT_REMOVED:
                data = event['client']

                client = self._model.clients.pop(data['id'], None)
                if client is not None:
                    self._event_manager.publish(ModelUpdateEvent.ITEM_REMOVED, client)

            elif event_type == EventType.DEVICE_ADDED:
                data = event['device']
                if data['id'] not in self._model.devices:
                    device = Device.model_validate_json(data, strict=False)
                    self._model.devices[data['id']] = device
                    self._event_manager.publish(ModelUpdateEvent.ITEM_CREATED, device)

            elif event_type == EventType.DEVICE_CHANGED:
                data = event['device']
                if data['id'] in self._model.devices:
                    device: BaseModel = self._model.devices[data['id']]
                    self._model.devices[data['id']] = device.model_copy(update={**data})
                    self._event_manager.publish(ModelUpdateEvent.ITEM_UPDATED, device)

            elif event_type == EventType.DEVICE_REMOVED:
                data = event['device']

                device = self._model.devices.pop(data['id'], None)
                if device is not None:
                    self._event_manager.publish(ModelUpdateEvent.ITEM_REMOVED, device)

            elif event_type == EventType.GROUP_ADDED:
                pass
            elif event_type == EventType.GROUP_CHANGED:
                pass
            elif event_type == EventType.GROUP_REMOVED:
                data = event['group']

                group = self._model.groups.pop(data['id'], None)
                if group is not None:
                    self._event_manager.publish(ModelUpdateEvent.ITEM_REMOVED, group)

            elif event_type == EventType.HOME_CHANGED:
                data = event['home']

                home = self._model.home.model_copy(update={**data})
                self._model.home = home
                self._event_manager.publish(ModelUpdateEvent.ITEM_UPDATED, home)

            elif event_type == EventType.SECURITY_JOURNAL_CHANGED:
                pass

    def _get_device_from_model(self, model: Model, id: str):
        if id in model.clients:
            return model.clients[id]
