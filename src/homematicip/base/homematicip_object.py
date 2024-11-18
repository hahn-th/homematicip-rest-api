import asyncio
import logging
from datetime import datetime

from homematicip.base.enums import AutoNameEnum
from homematicip.connection_v2.rest_connection import RestConnection, RestResult

LOGGER = logging.getLogger(__name__)


class HomeMaticIPObject:
    """This class represents a generic homematic ip object to make
    basic requests to the access point"""

    def __init__(self, connection):
        self._connection: RestConnection = connection
        #: List with remove handlers.
        self._on_remove = []
        #: List with update handlers.
        self._on_update = []

        #:the raw json data of the object
        self._rawJSONData = {}

        # list[str]:List of all attributes which were added via set_attr_from_dict
        self._dictAttributes = []

    def on_remove(self, handler):
        """Adds an event handler to the remove method. Fires when a device
        is removed."""
        self._on_remove.append(handler)

    def fire_remove_event(self, *args, **kwargs):
        """Trigger the method tied to _on_remove"""
        for _handler in self._on_remove:
            _handler(*args, **kwargs)

    def on_update(self, handler):
        """Adds an event handler to the update method. Fires when a device
        is updated."""
        self._on_update.append(handler)

    def fire_update_event(self, *args, **kwargs):
        """Trigger the method tied to _on_update"""
        for _handler in self._on_update:
            _handler(*args, **kwargs)

    def remove_callback(self, handler):
        """Remove event handler."""
        if handler in self._on_remove:
            self._on_remove.remove(handler)
        if handler in self._on_update:
            self._on_update.remove(handler)

    def _rest_call(self, path, body=None, custom_header: dict = None) -> RestResult:
        """Run a rest call non async.

        Args:
            path (str): the path to call without base url
            body (dict): the body to send
            custom_header (dict): the custom header to send. This will be merged with the default header
        """
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._connection.async_post(path, body, custom_header))

    async def _rest_call_async(self, path, body=None, custom_header: dict = None):
        """Run a rest call async

        Args:
            path (str): the path to call without base url
            body (dict): the body to send
            custom_header (dict): the custom header to send. This will be merged with the default header
        """
        return await self._connection.async_post(path, body, custom_header)

    def from_json(self, js):
        """this method will parse the homematicip object from a json object

        Args:
          js: the json object to parse
        """
        # LOGGER.debug("from_json call HomeMaticIpObject")
        self._rawJSONData = js
        pass

    def fromtimestamp(self, timestamp):
        """internal helper function which will create a datetime object from a timestamp"""
        if timestamp is None or timestamp <= 0:
            return None
        return datetime.fromtimestamp(timestamp / 1000.0)

    def set_attr_from_dict(
            self,
            attr: str,
            dict,
            type: AutoNameEnum = None,
            dict_attr=None,
            addToStrOutput=True,
    ):
        """this method will add the value from dict to the given attr name

        Args:
            attr(str): the attribute which value should be changed
            dict(dict): the dictionary from which the value should be extracted
            type(AutoNameEnum): this will call type.from_str(value), if a type gets provided
            dict_attr: the name of the attribute in the dict. Set this to None(default) to use attr
            addToStrOutput(str): should the attribute be returned via __str__()
        """
        if not dict_attr:
            dict_attr = attr

        if dict_attr not in dict:
            return None

        value = dict[dict_attr]
        if type:
            value = type.from_str(value)

        self.__dict__[attr] = value
        if addToStrOutput and attr not in self._dictAttributes:
            self._dictAttributes.append(attr)

    def str_from_attr_map(self) -> str:
        """this method will return a string with all key/values which were added via the set_attr_from_dict method"""
        return "".join([f"{x}({self.__dict__[x]}) " for x in self._dictAttributes])[:-1]

    def _run_non_async(self, method, *args, **kwargs):
        """Run an async method in a sync way"""
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(method(*args, **kwargs))
