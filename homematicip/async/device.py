import logging
from homematicip.device import Device, PlugableSwitch, PlugableSwitchMeasuring, \
    SabotageDevice, ShutterContact

ERROR_CODE = "errorCode"

_LOGGER = logging.getLogger(__name__)


class AsyncDevice(Device):
    """ Async implementation of a genereric homematic ip device """

    def set_label(self, label):
        pass

    def authorizeUpdate(self):
        pass

    def delete(self):
        pass

    def set_router_module_enabled(self, enabled=True):
        pass

    def is_update_applicable(self):
        pass


class AsyncPlugableSwitch(PlugableSwitch, AsyncDevice):
    """ Async implementation of HMIP-PS (Pluggable Switch) """

    async def turn_on(self):
        url, data = super().turn_on()
        return await self._connection.api_call(url, data)

    async def turn_off(self):
        url, data = super().turn_off()
        return await self._connection.api_call(url, data)


class AsyncPlugableSwitchMeasuring(PlugableSwitchMeasuring, AsyncPlugableSwitch):
    """ HMIP-PSM (Pluggable Switch and Meter) """
    pass


class AsyncSabotageDevice(SabotageDevice, AsyncDevice):
    pass


class AsyncShutterContact(ShutterContact, AsyncSabotageDevice):
    """ HMIP-SWDO (Door / Window Contact - optical) /
    HMIP-SWDO-I (Door / Window Contact Invisible - optical)"""

    pass
