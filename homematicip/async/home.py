import asyncio
import json
import logging

from homematicip.async.class_maps import TYPE_CLASS_MAP, TYPE_GROUP_MAP, TYPE_SECURITY_EVENT_MAP
from homematicip.async.connection import AsyncConnection
from homematicip.home import Home

LOGGER = logging.getLogger(__name__)


class AsyncHome(Home):
    """this class represents the 'Async Home' of the homematic ip"""
    _typeClassMap = TYPE_CLASS_MAP
    _typeGroupMap = TYPE_GROUP_MAP
    _typeSecurityEventMap = TYPE_SECURITY_EVENT_MAP

    def __init__(self, loop, websession=None):
        super().__init__(connection=AsyncConnection(loop, websession))

    async def init(self, access_point_id, lookup=True):
        await self._connection.init(access_point_id, lookup)

    async def get_current_state(self):
        # todo: a download_configuration method has been added. This can simplify this one.
        json_state = await self._connection.api_call(
            'home/getCurrentState', json.dumps(self._connection.clientCharacteristics))
        if "errorCode" in json_state:
            LOGGER.error(
                "Could not get the current configuration. Error: %s", json_state["errorCode"])
            return False

        js_home = json_state["home"]

        self.from_json(js_home)

        self._get_devices(json_state)
        self._get_clients(json_state)
        self._get_groups(json_state)

        return True

    async def enable_events(self) -> asyncio.Task:
        """Connects to the websocket. Returns a listening task."""
        return await self._connection.ws_connect(
            on_message=self._ws_on_message, on_error=self._ws_on_error)

    async def disable_events(self):
        await self._connection.close_websocket_connection()

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

    def set_location(self, city, latitude, longitude):
        LOGGER.warning('set_location not implemented.')
        pass
