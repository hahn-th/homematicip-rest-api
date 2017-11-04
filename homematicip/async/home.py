# coding=utf-8
import json
import logging

from homematicip.async.async_class_map import TYPE_CLASS_MAP
from homematicip.async.connection import Connection
from homematicip.base.base_home import BaseHome
from homematicip.base.constants import HOME
from homematicip.base.oauth_otk import OAuthOTK

LOGGER = logging.getLogger(__name__)


class Home(BaseHome):
    """this class represents the 'Home' of the homematic ip"""
    _type_class_map = TYPE_CLASS_MAP

    def __init__(self, connection: Connection):
        super().__init__(connection)

    def start_incoming_websocket_data(self):
        """Starts listening for incoming websocket data."""
        self.connection.listen_for_websocket_data(
            self._parse_incoming_socket_data)

    def stop_incoming_websocket_data(self):
        """Stops listening for incoming websocket data."""
        self.connection.close_websocket_connection()


    async def get_current_state(self):
        json_state = await self.connection._rest_call(
            *self._get_current_state())

        js_home = json_state[HOME]

        self.from_json(js_home)
        self._get_devices(json_state)

    async def get_OAuth_OTK(self):
        token = OAuthOTK()
        token.from_json(
            await self.connection._rest_call(*self._get_OAuth_OTK()))
        return token
