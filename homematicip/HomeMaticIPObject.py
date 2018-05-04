import logging

LOGGER = logging.getLogger(__name__)


class HomeMaticIPObject:
    """This class represents a generic homematic ip object to make
    basic requests to the access point"""

    def __init__(self, connection):
        self._connection = connection
        # List with update handlers.
        self._on_update = []
        self._rawJSONData = {}

    def on_update(self, handler):
        """Adds an event handler to the update method. Fires when a device
        is updated."""
        self._on_update.append(handler)

    def fire_update_event(self, *args, **kwargs):
        """Trigger the method tied to _on_update"""
        for _handler in self._on_update:
            _handler(*args, **kwargs)

    def _restCall(self, path, body=None):
        return self._connection._restCall(path, body)

    def from_json(self, js):
        #LOGGER.debug("from_json call HomeMaticIpObject")
        self._rawJSONData = js
        pass

    def __str__(self):
        return 'id({})'.format(self.id)
