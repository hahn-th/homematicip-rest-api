import sys

import logging

LOGGER = logging.getLogger(__name__)

class HomeMaticIPObject:
    """This class represents a generic homematic ip object to make
    basic requests to the access point"""

    def __init__(self, connection):
        self._connection = connection

    def _restCall(self, path, body=None):
        return self._connection._restCall(path, body)

    def from_json(self, js):
        LOGGER.debug("from_json call HomeMaticIpObject")

    def __str__(self):
        return 'id({})'.format(self.id)
