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

