from homematicip.events.event_types import ModelUpdateEvent


class EventManager:
    """Event manager to handle subscriptions and publish events. Events types are identified by ModelUpdateEvent."""
    def __init__(self):
        self._subscriptions = {event_type: [] for event_type in ModelUpdateEvent}

    def subscribe(self, event_type, callback):
        if event_type in self._subscriptions:
            self._subscriptions[event_type].append(callback)

    def unsubscribe(self, event_type, callback):
        if event_type in self._subscriptions:
            if callback in self._subscriptions[event_type]:
                self._subscriptions[event_type].remove(callback)

    def publish(self, event_type, event_args):
        if event_type in self._subscriptions:
            for callback in self._subscriptions[event_type]:
                callback(event_args)
