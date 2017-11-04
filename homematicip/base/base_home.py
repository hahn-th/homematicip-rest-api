# coding=utf-8
import homematicip
import threading

from homematicip.base.base_connection import BaseConnection
from homematicip.base.base_device import BaseDevice
from homematicip.base.client import Client
from homematicip.base.hmip_ip_object import HmipIpObject
from homematicip.base.location import Location
from homematicip.base.weather import Weather
from homematicip.group import *
from homematicip.securityEvent import *

import logging
import sys

_LOGGER = logging.getLogger(__name__)


class BaseHome(HmipIpObject):
    """this class represents the base 'Home' of the homematic ip"""
    devices = None
    clients = None
    weather = None
    connected = None
    currentAPVersion = None
    availableAPVersion = None
    timeZoneId = None
    pinAssigned = None
    dutyCycle = None
    updateState = None
    powerMeterUnitPrice = None
    powerMeterCurrency = None
    deviceUpdateStrategy = None
    lastReadyForUpdateTimestamp = None
    apExchangeClientId = None
    apExchangeState = None
    id = None

    _type_class_map = None
    _type_group_map = None

    def __init__(self, connection: BaseConnection):
        self.connection = connection
        self.location = Location()
        self.weather = Weather()

    def from_json(self, js_home):
        self.weather.from_json(js_home["weather"])
        self.location.from_json(js_home["location"])
        self.connected = js_home["connected"]
        self.currentAPVersion = js_home["currentAPVersion"]
        self.availableAPVersion = js_home["availableAPVersion"]
        self.timeZoneId = js_home["timeZoneId"]
        self.pinAssigned = js_home["pinAssigned"]
        self.dutyCycle = js_home["dutyCycle"]
        self.updateState = js_home["updateState"]
        self.powerMeterUnitPrice = js_home["powerMeterUnitPrice"]
        self.powerMeterCurrency = js_home["powerMeterCurrency"]
        self.deviceUpdateStrategy = js_home["deviceUpdateStrategy"]
        self.lastReadyForUpdateTimestamp = js_home[
            "lastReadyForUpdateTimestamp"]
        self.apExchangeClientId = js_home["apExchangeClientId"]
        self.apExchangeState = js_home["apExchangeState"]
        self.id = js_home["id"]
        self.update()

    def _get_current_state(self):
        return 'home/getCurrentState', self.connection.client_characteristics

    def get_current_state(self):
        raise NotImplementedError()

    def _get_devices(self, json_state):
        self.devices = {}
        data = json_state
        for device_data in data["devices"].values():
            self._add_device(device_data)

    def _add_device(self, device_data):
        deviceType = device_data["type"]
        device_class = self._type_class_map.get(deviceType, None)
        if device_class:
            d = device_class(self.connection)
            d.from_json(device_data)
            self.devices[d.id] = d
        else:
            _LOGGER.debug('No implementation for device %s', deviceType)

    def _get_clients(self, json_state):
        self.clients = {}
        data = json_state
        for client_data in data["clients"].values():
            self._add_client(client_data)

    def _add_client(self, client_data):
        c = Client()
        c.from_json(client_data)
        self.clients[c.id] = c

    def _get_groups(self, json_state):
        self.groups = {}
        data = json_state
        metaGroups = []
        for group in data["groups"].values():
            groupType = group["type"]
            group_class = self._type_group_map.get(groupType)
            if group_class:
                g = group_class()
                g.from_json(group, self.devices)
                self.groups[g.id] = g
            elif groupType == "META":
                metaGroups.append(group)
            else:
                _LOGGER.debug('No implementation for group %s', groupType)

        for mg in metaGroups:
            g = MetaGroup()
            g.from_json(mg, self.devices, self.groups)
            self.groups[g.id] = g

    def search_device_by_id(self, device_id):
        """ searches a device by given id
        :param device_id the device to search for
        :return the Device object or None if it couldn't find a device
        """
        return self.devices.get(device_id, None)

    def search_group_by_id(self, group_id):
        """ searches a group by given id
        :param group_id the device to search for
        :return the group object or None if it couldn't find a group
        """
        return self.groups.get(group_id, None)

    def search_client_by_id(self, client_id):
        """ searches a client by given id
        :param client_id the device to search for
        :return the client object or None if it couldn't find a client
        """
        return self.clients.get(client_id, None)

    def _set_security_zones_activation(self, internal=True, external=True):
        data = {
            "zonesActivation": {"EXTERNAL": external, "INTERNAL": internal}}
        return "home/security/setZonesActivation", data

    def set_security_zones_activation(self, internal=True, external=True):
        raise NotImplementedError()

    def _set_location(self, city, latitude, longitude):
        data = {"city": city, "latitude": latitude, "longitude": longitude}
        return "home/setLocation", data

    def set_location(self, city, latitude, longitude):
        raise NotImplementedError()

    def _set_intrusion_alert_through_smoke_detectors(self, activate=True):
        data = {"intrusionAlertThroughSmokeDetectors": activate}
        return "home/security/setIntrusionAlertThroughSmokeDetectors", data

    def set_intrusion_alert_through_smoke_detectors(self, activate=True):
        raise NotImplementedError()

    def _activate_absence_with_period(self, endtime):
        data = {"endTime": endtime.strftime("%Y_%m_%d %H:%M")}
        return "home/heating/activateAbsenceWithPeriod", data

    def activate_absence_with_period(self, endtime):
        raise NotImplementedError()

    def _activate_absence_with_duration(self, duration):
        # todo: what is the duration? datetime object ? integer ?
        data = {"duration": duration}
        return "home/heating/activateAbsenceWithDuration", data

    def activate_absence_with_duration(self, duration):
        raise NotImplementedError()

    def _deactivate_absence(self):
        return "home/heating/deactivateAbsence", None

    def deactivate_absence(self):
        raise NotImplementedError()

    def _activate_vacation(self, endtime, temperature):
        """

        :param endtime: datetime object
        :param temperature: temperature setpoint
        :return:
        """
        data = {"endtime": endtime.strftime("%Y_%m_%d %H:%M"),
                "temperature": temperature}
        return "home/heating/activateVacation", data

    def activate_vacation(self, endtime, temperature):
        raise NotImplementedError()

    def _deactivate_vacation(self):
        return "home/heating/deactivateVacation", None

    def deactivate_vacation(self):
        raise NotImplementedError()

    def _set_pin(self, newPin, oldPin=None):
        if newPin == None:
            newPin = ""
        data = {"pin": newPin}
        if oldPin:
            self.connection.headers["PIN"] = oldPin
        return 'home/setPin', data

    def set_pin(self, newPin, oldPin=None):
        raise NotImplementedError()

    def _set_zone_activation_delay(self, delay):
        # todo: what type is delay ? Datetime, integer ?
        data = {"zoneActivationDelay": delay}
        return "home/security/setZoneActivationDelay", data

    def set_zone_activation_delay(self, delay):
        raise NotImplementedError

    def get_security_journal(self):
        raise NotImplementedError

    def _get_security_journal(self):
        return "home/security/getSecurityJournal", None

    def delete_group(self, group):
        raise NotImplementedError

    def _delete_group(self, group):
        data = {"groupId": group.id}
        return "home/group/deleteGroup", data

    def get_OAuth_OTK(self):
        raise NotImplementedError

    def _get_OAuth_OTK(self):
        return "home/getOAuthOTK", None

    def set_timezone(self, timezone):
        """ sets the timezone for the AP. e.g. "Europe/Berlin" """
        raise NotImplementedError

    def _set_timezone(self, timezone):
        data = {"timezoneId": timezone}
        return "home/setTimezone", data

    def _set_powermeter_unit_price(self, price):
        return "home/setPowerMeterUnitPrice", {"powerMeterUnitPrice": price}

    def set_powermeter_unit_price(self, price):
        raise NotImplementedError

    def set_zones_device_assignment(self, internal_devices, external_devices):
        """ sets the devices for the security zones
                :param internal_devices the devices which should be used for the internal zone
                :param external_devices the devices which should be used for the external(hull) zone
                :return the result of _restCall
                """
        raise NotImplementedError

    def _set_zones_device_assignment(self, internal_devices,
                                     external_devices):

        internal = [x.id for x in internal_devices]
        external = [x.id for x in external_devices]
        data = {"zonesDeviceAssignment": {"INTERNAL": internal,
                                          "EXTERNAL": external}}
        return "home/security/setZonesDeviceAssignment", data

    def enable_events(self):
        websocket.enableTrace(True)
        self.__webSocket = websocket.WebSocketApp(
            homematicip.get_urlWebSocket(),
            header=['AUTHTOKEN: {}'.format(homematicip.get_auth_token()),
                    'CLIENTAUTH: {}'.format(
                        homematicip.get_clientauth_token())],
            on_message=self.__ws_on_message, on_error=self.__ws_on_error)
        self.__webSocketThread = threading.Thread(
            target=self.__webSocket.run_forever)
        self.__webSocketThread.daemon = True
        self.__webSocketThread.start()

    def disable_events(self):
        self.__webSocket.close()

    def __ws_on_error(self, ws, message):
        _LOGGER.error("Websocket error: {}".format(message))

    def __ws_on_message(self, ws, message):
        js = json.loads(message)
        eventList = []
        try:
            for eID in js["events"]:
                event = js["events"][eID]
                pushEventType = event["pushEventType"]
                obj = None
                if pushEventType == "GROUP_CHANGED":
                    data = event["group"]
                    obj = self.search_group_by_id(data["id"])
                    obj.from_json(data, self.devices)
                elif pushEventType == "HOME_CHANGED":
                    data = event["home"]
                    obj = self
                    obj.from_json(data)
                elif pushEventType == "CLIENT_ADDED":
                    data = event["client"]
                    self._add_client(data)
                elif pushEventType == "CLIENT_CHANGED":
                    data = event["client"]
                    obj = self.search_client_by_id(data["id"])
                    obj.from_json(data)
                elif pushEventType == "CLIENT_REMOVED":
                    self.clients.pop(event['id'], None)
                elif pushEventType == "DEVICE_ADDED":
                    data = event["device"]
                    self._add_device(data)
                elif pushEventType == "DEVICE_CHANGED":
                    data = event["device"]
                    obj = self.search_device_by_id(data["id"])
                    obj.from_json(data)
                elif pushEventType == "DEVICE_REMOVED":
                    self.devices.pop(event['id'], None)
                elif pushEventType == "GROUP_REMOVED":
                    obj = self.search_group_by_id(event["id"])
                    self.groups.pop(event['id'])
                elif pushEventType == "GROUP_ADDED":
                    data = event["group"]

                    obj = Group()  # TODO:implement typecheck
                    obj.from_json(data)
                    self.groups.append(obj)
                elif pushEventType == "SECURITY_JOURNAL_CHANGED":
                    pass  # data is just none so nothing to do here

                # TODO: implement INCLUSION_REQUESTED, NONE
                else:
                    _LOGGER.warning(
                        "Uknown EventType '{}' Data: {}".format(pushEventType,
                                                                event))
                eventList.append({"eventType": pushEventType, "data": obj})
        except:
            _LOGGER.error("Unexpected error: {}".format(sys.exc_info()[0]))
        self.onEvent.fire(eventList)
