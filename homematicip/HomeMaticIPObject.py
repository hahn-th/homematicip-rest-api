import sys

import logging

LOGGER = logging.getLogger(__name__)


class HomeMaticIPObject:
    """This class represents a generic homematic ip object to make
    basic requests to the access point"""

    _on_update = None

    def __init__(self, connection):
        self._connection = connection

    def on_update(self, handler):
        """Adds an event handler to the update method. Fires when a device
        is updated."""
        self._on_update = handler

    def fire_update_event(self, *args, **kwargs):
        """Trigger the method tied to _on_update"""
        if self._on_update is not None:
            self._on_update(*args, **kwargs)
        else:
            LOGGER.debug('on-update event not fired. on-update is None')

    def _restCall(self, path, body=None):
        return self._connection._restCall(path, body)

    def from_json(self, js):
        LOGGER.debug("from_json call HomeMaticIpObject")

    def __str__(self):
        return 'id({})'.format(self.id)
