# coding=utf-8
import json
import logging

from homematicip.async import HomeIPObject
from homematicip.async.async_class_map import TYPE_CLASS_MAP
from homematicip.async.connection import Connection

from homematicip.async import device

from homematicip import home
from homematicip.base.base_home import BaseHome
from homematicip.home import OAuthOTK

TYPE = "type"
GROUPS = "groups"
URL_GET_CURRENT_STATE = 'home/getCurrentState'
URL_HOME_SET_LOCATION = "home/setLocation"
CLIENTS = "clients"
DEVICES = "devices"
ERROR_CODE = "errorCode"
ID = "id"
HOME = "home"
AP_EXCHANGE_STATE = "apExchangeState"
AP_EXCHANGE_CLIENT_ID = "apExchangeClientId"
DEVICE_UPDATE_STRATEGY = "deviceUpdateStrategy"
POWER_METER_CURRENCY = "powerMeterCurrency"
POWER_METER_UNIT_PRICE = "powerMeterUnitPrice"
UPDATE_STATE = "updateState"
DUTY_CYCLE = "dutyCycle"
PIN_ASSIGNED = "pinAssigned"
TIME_ZONE_ID = "timeZoneId"
AVAILABLE_AP_VERSION = "availableAPVersion"
CURRENT_AP_VERSION = "currentAPVersion"
CONNECTED = "connected"
LOCATION = "location"
WEATHER = "weather"

LOGGER = logging.getLogger(__name__)


class Home(BaseHome):
    """this class represents the 'Home' of the homematic ip"""
    _type_class_map = TYPE_CLASS_MAP

    def __init__(self, connection: Connection):
        super().__init__(connection)

    def from_json(self, js):
        home.Home.from_json(self, js)

    def start_incoming_websocket_data(self):
        """Starts listening for incoming websocket data."""
        self.connection.listen_for_websocket_data(
            self._parse_incoming_socket_data)

    def stop_incoming_websocket_data(self):
        """Stops listening for incoming websocket data."""
        self.connection.close_websocket_connection()

    # def _parse_incoming_socket_data(self, js):
    #     for eID in js["events"]:
    #         event = js["events"][eID]
    #         pushEventType = event["pushEventType"]
    #         obj = None
    #         if pushEventType == "DEVICE_CHANGED":
    #             data = event["device"]
    #             obj = self.search_device_by_id(data["id"])
    #             if obj:
    #                 obj.from_json(data)
    #         else:
    #             LOGGER.debug(
    #                 "Uknown EventType '{}' Data: {}".format(
    #                     pushEventType, event))

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
