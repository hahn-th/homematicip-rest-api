import json
import logging

from homematicip.async.class_maps import TYPE_CLASS_MAP, TYPE_GROUP_MAP, \
    TYPE_SECURITY_EVENT_MAP
from homematicip.async.connection import AsyncConnection
from homematicip.home import Home

LOGGER = logging.getLogger(__name__)


class AsyncHome(Home):
    """this class represents the 'Home' of the homematic ip"""
    _typeClassMap = TYPE_CLASS_MAP
    _typeGroupMap = TYPE_GROUP_MAP
    _typeSecurityEventMap = TYPE_SECURITY_EVENT_MAP

    def __init__(self,loop):
        super().__init__(AsyncConnection(loop))

    async def init(self, access_point_id, lookup=True):
        await self._connection.init(access_point_id, lookup)

    async def get_current_state(self):
        json_state = await self._connection.api_call(
            'home/getCurrentState',
            json.dumps(self._connection.clientCharacteristics))
        if "errorCode" in json_state:
            LOGGER.error(
                "Could not get the current configuration. Error: {}".format(
                    json_state["errorCode"]))
            return False

        js_home = json_state["home"]

        self.from_json(js_home)

        self.devices = self._get_devices(json_state)
        self.clients = self._get_clients(json_state)
        self.groups = self._get_groups(json_state)

        return True

    def enable_events(self):
        """Starts listening for incoming websocket data."""
        self._connection.listen_for_websocket_data(
            self._ws_on_message)

    def disable_events(self):
        self._connection.close_websocket_connection()

    def get_OAuth_OTK(self):
        pass

    def activate_absence_with_duration(self, duration):
        pass

    def set_powermeter_unit_price(self, price):
        pass

    def set_intrusion_alert_through_smoke_detectors(self, activate=True):
        pass

    def set_timezone(self, timezone):
        pass

    def set_zones_device_assignment(self, internal_devices, external_devices):
        pass

    def set_pin(self, newPin, oldPin=None):
        pass

    def get_security_journal(self):
        pass

    def activate_absence_with_period(self, endtime):
        pass

    def deactivate_absence(self):
        pass

    def activate_vacation(self, endtime, temperature):
        pass

    def deactivate_vacation(self):
        pass

    def set_zone_activation_delay(self, delay):
        pass

    def set_security_zones_activation(self, internal=True, external=True):
        pass

    def delete_group(self, group):
        pass



    # def start_incoming_websocket_data(self):
    #     """Starts listening for incoming websocket data."""
    #     self.connection.listen_for_websocket_data(
    #         self._parse_incoming_socket_data)
    #
    # def stop_incoming_websocket_data(self):
    #     """Stops listening for incoming websocket data."""
    #     self.connection.close_websocket_connection()

    def set_location(self, city, latitude, longitude):
        LOGGER.warning('set_location not implemented.')
        pass


