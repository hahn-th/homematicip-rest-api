import asyncio
import json
import logging

from homematicip.aio.class_maps import TYPE_CLASS_MAP, TYPE_GROUP_MAP, TYPE_SECURITY_EVENT_MAP
from homematicip.aio.connection import AsyncConnection
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

    async def activate_absence_with_duration(self, duration):
        return await self._connection.api_call(*super().activate_absence_with_duration(duration))

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

    async def get_security_journal(self):
        journal = await self._connection.api_call(
            'home/security/getSecurityJournal', json.dumps(self._connection.clientCharacteristics))
        if (journal is None or "errorCode" in journal):
            LOGGER.error("Could not get the security journal. Error: %s", journal["errorCode"])
            return None
        ret = []
        for entry in journal["entries"]:
            eventType = entry["eventType"]
            if eventType in self._typeSecurityEventMap:
                j = self._typeSecurityEventMap[eventType](self._connection)
                j.from_json(entry)
                ret.append(j)
            else:
                j = SecurityEvent(self._connection)
                j.from_json(entry)
                ret.append(j)
                LOGGER.warning("There is no class for %s yet", eventType)
        return ret

    async def activate_absence_with_period(self, endtime):
        return await self._connection.api_call(*super().activate_absence_with_period(endtime))

    async def deactivate_absence(self):
        return await self._connection.api_call(*super().deactivate_absence())

    async def activate_vacation(self, endtime, temperature):
        return await self._connection.api_call(*super().activate_vacation(endtime, temperature))

    async def deactivate_vacation(self):
        return await self._connection.api_call(*super().deactivate_vacation())

    def set_zone_activation_delay(self, delay):
        pass

    async def set_security_zones_activation(self, internal=True, external=True):
        return await self._connection.api_call(*super().set_security_zones_activation(internal, external))

    def delete_group(self, group):
        pass

    async def set_location(self, city, latitude, longitude):
        return await self._connection.api_call(*super().set_location(city, latitude, longitude))
