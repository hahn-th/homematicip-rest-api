import json

from homematicip.aio.class_maps import (
    TYPE_CLASS_MAP,
    TYPE_GROUP_MAP,
    TYPE_RULE_MAP,
    TYPE_SECURITY_EVENT_MAP,
)
from homematicip.aio.securityEvent import AsyncSecurityEvent
from homematicip.base.enums import *
from homematicip.connection_v2.client_characteristics_builder import ClientCharacteristicsBuilder
from homematicip.home import Home, OAuthOTK

LOGGER = logging.getLogger(__name__)


class AsyncHome(Home):
    """this class represents the 'Async Home' of the homematic ip"""

    _typeClassMap = TYPE_CLASS_MAP
    _typeGroupMap = TYPE_GROUP_MAP
    _typeSecurityEventMap = TYPE_SECURITY_EVENT_MAP
    _typeRuleMap = TYPE_RULE_MAP

    def __init__(self, loop, websession=None):
        super().__init__(None)

    async def get_current_state(self, clear_config: bool = False):
        """downloads the current configuration and parses it into self

        Args:
            clear_config(bool): if set to true, this function will remove all old objects
            from self.devices, self.client, ... to have a fresh config instead of reparsing them
        """
        LOGGER.debug("get_current_state")
        json_state = await self.download_configuration()
        return self.update_home(json_state, clear_config)

    async def download_configuration(self):
        if self._connection_context is None:
            raise Exception("Home not initialized. Run init() first.")

        client_characteristics = ClientCharacteristicsBuilder.get(self._connection_context.accesspoint_id)
        result = await self._rest_call_async(
            "home/getCurrentState", client_characteristics
        )
        return result.json
        # return await self._connection.async_post().api_call(*super().download_configuration())

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
        result = await self._connection.api_call("home/setPin", body=data)
        if oldPin:
            del self._connection.headers["PIN"]
        return result

    async def get_security_journal(self):
        journal = await self._connection.api_call(
            "home/security/getSecurityJournal",
            self._connection.clientCharacteristics,
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

    async def set_cooling(self, cooling):
        return await self._connection.api_call(*super().set_cooling(cooling))