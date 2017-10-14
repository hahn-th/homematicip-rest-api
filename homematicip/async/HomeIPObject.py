import asyncio
import logging

from homematicip import EventHook
from .connection import Connection

_LOGGER = logging.getLogger(__name__)


class HomeMaticIPobject:
    """This class represents a generic ASYNC homematic ip object

     Makes basic requests to the access point"""

    def __init__(self, connection: Connection):
        self._connection = connection
        self.onUpdate = None

    def _restCall(self, path, body=None):
        """Shadows the original _restCall so another method can be used for
        making an async request."""
        return path, body

    def update(self, js):
        if self.onUpdate is not None:
            self.onUpdate(js)
        else:
            _LOGGER.warning(
                'onUpdate event not fired as has no method is assigned to it.')

            # def from_json(self, js):
            #     pass

            # def __repr__(self):
            #     return "id({}) {}".format(self.id, self.__str__())
            #
            # def __str__(self):
            #     return 'id({})'.format(self.id)

            # def __str__(self):
            #     if sys.version_info >= (3, 0):
            #         return self.__unicode__()
            #     else:
            #         return unicode(self).encode('utf-8')
