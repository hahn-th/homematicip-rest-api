import asyncio
import json
import logging

from homematicip.aio.class_maps import (
    TYPE_CLASS_MAP,
    TYPE_GROUP_MAP,
    TYPE_RULE_MAP,
    TYPE_SECURITY_EVENT_MAP,
)
from homematicip.aio.connection import AsyncConnection
from homematicip.aio.securityEvent import AsyncSecurityEvent
from homematicip.base.enums import *
from homematicip.home import Home, OAuthOTK

LOGGER = logging.getLogger(__name__)


class AsyncHome(Home):
    """this class represents the 'Async Home' of the homematic ip"""

    _typeClassMap = TYPE_CLASS_MAP
    _typeGroupMap = TYPE_GROUP_MAP
    _typeSecurityEventMap = TYPE_SECURITY_EVENT_MAP
    _typeRuleMap = TYPE_RULE_MAP

    def __init__(self, loop, websession=None):
        super().__init__(connection=AsyncConnection(loop, websession))

    async def init(self, access_point_id, lookup=True):
        await self._connection.init(access_point_id, lookup)

    async def get_current_state(self, clearConfig: bool = False):
        """downloads the current configuration and parses it into self

        Args:
            clearConfig(bool): if set to true, this function will remove all old objects
            from self.devices, self.client, ... to have a fresh config instead of reparsing them
        """
        json_state = await self.download_configuration()
        return self.update_home(json_state, clearConfig)

    async def download_configuration(self):
        return await self._connection.api_call(*super().download_configuration())

    async def enable_events(self) -> asyncio.Task:
        """Connects to the websocket. Returns a listening task."""
        return await self._connection.ws_connect(
            on_message=self._ws_on_message, on_error=self._ws_on_error
        )

    async def disable_events(self):
        await self._connection.close_websocket_connection()

    async def get_OAuth_OTK(self):
        token = OAuthOTK(self._connection)
        token.from_json(await self._connection.api_call("home/getOAuthOTK"))
        return token

    async def activate_absence_with_duration(self, duration):
        return await self._connection.api_call(
            *super().activate_absence_with_duration(duration)
        )

    async def set_powermeter_unit_price(self, price):
        return await self._connection.api_call(
            *super().set_powermeter_unit_price(price)
        )

    async def set_intrusion_alert_through_smoke_detectors(self, activate=True):
        return await self._connection.api_call(
            *super().set_intrusion_alert_through_smoke_detectors(activate)
        )

    async def set_timezone(self, timezone):
        return await self._connection.api_call(*super().set_timezone(timezone))

    async def set_zones_device_assignment(self, internal_devices, external_devices):
        return await self._connection.api_call(
            *super().set_zones_device_assignment(internal_devices, internal_devices)
        )

    async def set_pin(self, newPin, oldPin=None):
        if newPin is None:
            newPin = ""
        data = {"pin": newPin}
        if oldPin:
            self._connection.headers["PIN"] = str(oldPin)
        result = await self._connection.api_call("home/setPin", body=json.dumps(data))
        if oldPin:
            del self._connection.headers["PIN"]
        return result

    async def get_security_journal(self):
        journal = await self._connection.api_call(
            "home/security/getSecurityJournal",
            json.dumps(self._connection.clientCharacteristics),
        )
        if journal is None or "errorCode" in journal:
            LOGGER.error(
                "Could not get the security journal. Error: %s", journal["errorCode"]
            )
            return None
        ret = []
        for entry in journal["entries"]:
            try:
                eventType = SecurityEventType(entry["eventType"])
                if eventType in self._typeSecurityEventMap:
                    j = self._typeSecurityEventMap[eventType](self._connection)
            except:
                j = AsyncSecurityEvent(self._connection)
                LOGGER.warning("There is no class for %s yet", entry["eventType"])
            j.from_json(entry)
            ret.append(j)

        return ret

    async def activate_absence_with_period(self, endtime):
        return await self._connection.api_call(
            *super().activate_absence_with_period(endtime)
        )

    async def activate_absence_permanent(self):
        return await self._connection.api_call(*super().activate_absence_permanent())

    async def deactivate_absence(self):
        return await self._connection.api_call(*super().deactivate_absence())

    async def activate_vacation(self, endtime, temperature):
        return await self._connection.api_call(
            *super().activate_vacation(endtime, temperature)
        )

    async def deactivate_vacation(self):
        return await self._connection.api_call(*super().deactivate_vacation())

    async def set_zone_activation_delay(self, delay):
        return await self._connection.api_call(
            *super().set_zone_activation_delay(delay)
        )

    async def set_security_zones_activation(self, internal=True, external=True):
        return await self._connection.api_call(
            *super().set_security_zones_activation(internal, external)
        )

    async def delete_group(self, group):
        return await group.delete()

    async def set_location(self, city, latitude, longitude):
        return await self._connection.api_call(
            *super().set_location(city, latitude, longitude)
        )
