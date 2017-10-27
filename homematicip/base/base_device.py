from datetime import datetime

import logging

from homematicip.base.base_connection import BaseConnection
from homematicip.base.hmip_ip_object import HmipIpObject

_LOGGER = logging.getLogger(__name__)


class BaseDevice(HmipIpObject):
    _raw_data = None
    id = None
    homeId = None
    label = None
    lastStatusUpdate = None
    deviceType = None
    updateState = None
    firmwareVersion = None
    availableFirmwareVersion = None
    unreach = None
    lowBat = None
    routerModuleSupported = False
    routerModuleEnabled = False

    on_update = None

    def __init__(self, connection: BaseConnection):
        self.connection = connection

    def from_json(self, js):
        self.id = js["id"]
        self.homeId = js["homeId"]
        self.label = js["label"]
        time = js["lastStatusUpdate"]
        if time > 0:
            self.lastStatusUpdate = datetime.fromtimestamp(time / 1000.0)
        else:
            self.lastStatusUpdate = None

        self.deviceType = js["type"]
        self.updateState = js["updateState"]
        self.firmwareVersion = js["firmwareVersion"]
        self.availableFirmwareVersion = js["availableFirmwareVersion"]
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "DEVICE_BASE":
                self.unreach = c["unreach"]
                self.lowBat = c["lowBat"]
                self.routerModuleSupported = c["routerModuleSupported"]
                self.routerModuleEnabled = c["routerModuleEnabled"]
                break
        self.update()

    def set_label(self, label):
        raise NotImplementedError()

    def _set_label(self, label):
        data = {"deviceId": self.id, "label": label}
        return "device/setDeviceLabel", data

    def is_update_applicable(self):
        raise NotImplementedError()

    def _is_update_applicable(self):
        data = {"deviceId": self.id}
        return "device/isUpdateApplicable", data

    def authorizeUpdate(self):
        raise NotImplementedError()

    def _authorizeUpdate(self):
        data = {"deviceId": self.id}
        return "device/authorizeUpdate", data

    def delete(self):
        raise NotImplementedError()

    def _delete(self):
        data = {"deviceId": self.id}
        return "device/deleteDevice", data

    def set_router_module_enabled(self, enabled=True):
        raise NotImplementedError()

    def _set_router_module_enabled(self, enabled=True):
        data = {"deviceId": self.id, "channelIndex": 0,
                "routerModuleEnabled": enabled}
        return "device/configuration/setRouterModuleEnabled", data


class BasePluggableSwitch(BaseDevice):
    on = None

    def from_json(self, js):
        super().from_json(js)
        for cid in js["functionalChannels"]:
            c = js["functionalChannels"][cid]
            type = c["functionalChannelType"]
            if type == "SWITCH_CHANNEL":
                self.on = c["on"]

    def _set_switch_state(self, on=True):
        """Return set_switch_state data"""
        data = {"channelIndex": 1, "deviceId": self.id, "on": on}
        return ("device/control/setSwitchState", data)

    def _turn_on(self):
        """Switch the device on."""
        return self._set_switch_state(True)

    def turn_on(self):
        raise NotImplementedError()

    def _turn_off(self):
        """Switch the device off."""
        return self._set_switch_state(False)

    def turn_off(self):
        raise NotImplementedError()
