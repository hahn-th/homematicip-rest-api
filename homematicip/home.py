import logging
import threading
import websocket
from typing import List

from homematicip.EventHook import *
from homematicip.base.enums import *
from homematicip.class_maps import *
from homematicip.connection import Connection
from homematicip.group import *
from homematicip.device import *
from homematicip.securityEvent import *
from homematicip.rule import *
from homematicip.base.helpers import bytes2str

LOGGER = logging.getLogger(__name__)


class Weather(HomeMaticIPObject.HomeMaticIPObject):

    def __init__(self, connection):
        super().__init__(connection)
        self.temperature = 0.0
        self.weatherCondition = WeatherCondition.UNKNOWN
        self.weatherDayTime = "DAY"
        self.minTemperature = 0.0
        self.maxTemperature = 0.0
        self.humidity = 0
        self.windSpeed = 0.0
        self.windDirection = 0

    def from_json(self, js):
        super().from_json(js)
        self.temperature = js["temperature"]
        self.weatherCondition = WeatherCondition.from_str(js["weatherCondition"])
        self.weatherDayTime = WeatherDayTime.from_str(js["weatherDayTime"])
        self.minTemperature = js["minTemperature"]
        self.maxTemperature = js["maxTemperature"]
        self.humidity = js["humidity"]
        self.windSpeed = js["windSpeed"]
        self.windDirection = js["windDirection"]
    def __str__(self):
        return "temperature({}) weatherCondition({}) weatherDayTime({}) minTemperature({}) maxTemperature({}) humidity({}) windSpeed({}) windDirection({})".format(self.temperature,
                                                                                                                                                                    self.weatherCondition,
                                                                                                                                                                    self.weatherDayTime,
                                                                                                                                                                    self.minTemperature,
                                                                                                                                                                    self.maxTemperature,
                                                                                                                                                                    self.humidity,
                                                                                                                                                                    self.windSpeed,
                                                                                                                                                                    self.windDirection)


class Location(HomeMaticIPObject.HomeMaticIPObject):
    def __init__(self, connection):
        super().__init__(connection)
        self.city = "London"
        self.latitude = "51.509865"
        self.longitude = "-0.118092"

    def from_json(self, js):
        super().from_json(js)
        self.city = js["city"]
        self.latitude = js["latitude"]
        self.longitude = js["longitude"]

    def __str__(self):
        return "city({}) latitude({}) longitude({})".format(self.city,
                                                            self.latitude,
                                                            self.longitude)


class Client(HomeMaticIPObject.HomeMaticIPObject):

    def __init__(self, connection):
        super().__init__(connection)
        self.id = ""
        self.label = ""
        self.homeId = ""
        self.c2cServiceIdentifier = ""
        self.clientType = ClientType.APP

    def from_json(self, js):
        super().from_json(js)
        self.id = js["id"]
        self.label = js["label"]
        self.homeId = js["homeId"]
        self.clientType = ClientType.from_str(js["clientType"])
        if "c2cServiceIdentifier" in js:
            self.c2cServiceIdentifier = js["c2cServiceIdentifier"]

    def __str__(self):
        return "label({})".format(self.label)


class OAuthOTK(HomeMaticIPObject.HomeMaticIPObject):

    def __init__(self, connection):
        super().__init__(connection)
        self.authToken = None
        self.expirationTimestamp = None

    def from_json(self, js):
        super().from_json(js)
        self.authToken = js["authToken"]
        self.expirationTimestamp = self.fromtimestamp(js["expirationTimestamp"])

class Home(HomeMaticIPObject.HomeMaticIPObject):
    """this class represents the 'Home' of the homematic ip"""
    _typeClassMap = TYPE_CLASS_MAP
    _typeGroupMap = TYPE_GROUP_MAP
    _typeSecurityEventMap = TYPE_SECURITY_EVENT_MAP
    _typeRuleMap = TYPE_RULE_MAP
    _typeFunctionalHomeMap = TYPE_FUNCTIONALHOME_MAP

    def __init__(self, connection=None):
        if connection is None:
            connection = Connection()
        super().__init__(connection)

        self.apExchangeClientId = None
        self.apExchangeState = ApExchangeState.NONE
        self.availableAPVersion = None
        self.carrierSense = None
        self.connected = None
        self.currentAPVersion = None
        self.deviceUpdateStrategy = DeviceUpdateStrategy.MANUALLY
        self.dutyCycle = None
        self.id = None
        self.lastReadyForUpdateTimestamp = None
        self.location = None
        self.pinAssigned = None
        self.powerMeterCurrency = None
        self.powerMeterUnitPrice = None
        self.timeZoneId = None
        self.updateState = HomeUpdateState.UP_TO_DATE
        self.weather = None

        self.__webSocket = None
        self.__webSocketThread = None
        self.onEvent = EventHook()

        self.devices = []
        self.clients = []
        self.groups = []
        self.rules = []
        self.functionalHomes = []

    def init(self, access_point_id, lookup=True):
        self._connection.init(access_point_id, lookup)

    def set_auth_token(self, auth_token):
        self._connection.set_auth_token(auth_token)

    def from_json(self, js_home):
        super().from_json(js_home)

        self.weather = Weather(self._connection)
        self.weather.from_json(js_home["weather"])
        self.location = Location(self._connection)
        self.location.from_json(js_home["location"])

        self.connected = js_home["connected"]
        self.currentAPVersion = js_home["currentAPVersion"]
        self.availableAPVersion = js_home["availableAPVersion"]
        self.timeZoneId = js_home["timeZoneId"]
        self.pinAssigned = js_home["pinAssigned"]
        self.dutyCycle = js_home["dutyCycle"]
        self.updateState = HomeUpdateState.from_str(js_home["updateState"])
        self.powerMeterUnitPrice = js_home["powerMeterUnitPrice"]
        self.powerMeterCurrency = js_home["powerMeterCurrency"]
        self.deviceUpdateStrategy = DeviceUpdateStrategy.from_str(js_home["deviceUpdateStrategy"])
        self.lastReadyForUpdateTimestamp = js_home["lastReadyForUpdateTimestamp"]
        self.apExchangeClientId = js_home["apExchangeClientId"]
        self.apExchangeState = ApExchangeState.from_str(js_home["apExchangeState"])
        self.id = js_home["id"]
        self.carrierSense = js_home["carrierSense"]

        
        self._get_rules(js_home)

    def download_configuration(self):
        return self._restCall('home/getCurrentState',
                              json.dumps(self._connection.clientCharacteristics))

    def get_current_state(self, clearConfig = False):

        json_state = self.download_configuration()

        if "errorCode" in json_state:
            LOGGER.error("Could not get the current configuration. Error: %s",
                         json_state["errorCode"])
            return False

        if clearConfig:
            self.devices = []
            self.clients = []
            self.groups = []
            self.rules = []
            self.functionalHomes = []

        js_home = json_state["home"]

        self.from_json(js_home)

        self._get_devices(json_state)
        self._get_clients(json_state)
        self._get_groups(json_state)

        self._get_functionalHomes(js_home)
        self._load_functionalChannels()

        return True

    def _get_devices(self, json_state):
        self.devices = [x for x in self.devices if x.id in json_state["devices"].keys()]
        for id_, raw in json_state["devices"].items():
            _device = self.search_device_by_id(id_)
            if _device:
                _device.from_json(raw)
            else:
                self.devices.append(self._parse_device(raw))

    def _parse_device(self, json_state):
        try:
            deviceType = DeviceType.from_str(json_state["type"])
            d = self._typeClassMap[deviceType](self._connection)
            d.from_json(json_state)
            return d
        except:
            d = self._typeClassMap[DeviceType.DEVICE](self._connection)
            d.from_json(json_state)
            LOGGER.warning("There is no class for %s yet", json_state["type"])
            return d

    def _get_rules(self, json_state):
        self.rules = [x for x in self.rules if x.id in json_state["ruleMetaDatas"].keys()]
        for id_, raw in json_state["ruleMetaDatas"].items():
            _rule = self.search_rule_by_id(id_)
            if _rule:
                _rule.from_json(raw)
            else:
                self.rules.append(self._parse_rule(raw))

    def _parse_rule(self, json_state):
        try:
            ruleType = AutomationRuleType.from_str(json_state["type"])
            r = self._typeRuleMap[ruleType](self._connection)
            r.from_json(json_state)
            return r
        except:
            r = Rule(self._connection)
            r.from_json(json_state)
            LOGGER.warning("There is no class for %s yet", json_state["type"])
            return r

    def _get_clients(self, json_state):
        self.clients = [x for x in self.clients if x.id in json_state["clients"].keys()]
        for id_, raw in json_state["clients"].items():
            _client = self.search_client_by_id(id_)
            if _client:
                _client.from_json(raw)
            else:
                c = Client(self._connection)
                c.from_json(raw)
                self.clients.append(c)

    def _parse_group(self, json_state):
        g = None
        if json_state["type"] == "META":
            g = MetaGroup(self._connection)
            g.from_json(json_state, self.devices, self.groups)
        else:
            try:
                groupType = GroupType.from_str(json_state["type"])
                g = self._typeGroupMap[groupType](self._connection)
                g.from_json(json_state, self.devices)
            except:
                g = self._typeGroupMap[GroupType.GROUP](self._connection)
                g.from_json(json_state, self.devices)
                LOGGER.warning("There is no class for %s yet", json_state["type"])
        return g

    def _get_groups(self, json_state):
        self.groups = [x for x in self.groups if x.id in json_state["groups"].keys()]
        metaGroups = []
        for id_, raw in json_state["groups"].items():
            _group = self.search_group_by_id(id_)
            if _group:
                if isinstance(_group, MetaGroup):
                    _group.from_json(raw, self.devices, self.groups)
                else:
                    _group.from_json(raw, self.devices)
            else:
                group_type = raw["type"]
                if group_type == "META":
                    metaGroups.append(raw)
                else:
                    self.groups.append(self._parse_group(raw))
        for mg in metaGroups:
            self.groups.append(self._parse_group(mg))

    def _get_functionalHomes(self, json_state):
        for solution, functionalHome in json_state["functionalHomes"].items():
            try:
                solutionType = FunctionalHomeType.from_str(solution)
                h = None
                for fh in self.functionalHomes:
                    if fh.solution == solution:
                        h = fh
                        break
                if h is None:
                    h = self._typeFunctionalHomeMap[solutionType](self._connection)
                    self.functionalHomes.append(h)
                h.from_json(functionalHome, self.groups)
            except:
                h = FunctionalHome(self._connection)
                h.from_json(functionalHome, self.groups)
                LOGGER.warning("There is no class for %s yet", solution)
                self.functionalHomes.append(h)

    def _load_functionalChannels(self):
        for d in self.devices:
            d.load_functionalChannels(self.groups)

    def get_functionalHome(self, functionalHomeType ):
        """ returns the functionalHome from the given type or None if the functional home couldn't be found"""
        for x in self.functionalHomes:
            if isinstance(x, functionalHomeType):
                return x

        return None

    def search_device_by_id(self, deviceID) -> Device:
        """ searches a device by given id
        :param deviceID the device to search for
        :return the Device object or None if it couldn't find a device
        """
        for d in self.devices:
            if d.id == deviceID:
                return d
        return None

    def search_group_by_id(self, groupID) -> Group:
        """ searches a group by given id
        :param groupID the device to search for
        :return the group object or None if it couldn't find a group
        """
        for g in self.groups:
            if g.id == groupID:
                return g
        return None

    def search_client_by_id(self, clientID) -> Client:
        """ searches a client by given id
        :param clientID the device to search for
        :return the client object or None if it couldn't find a client
        """
        for c in self.clients:
            if c.id == clientID:
                return c
        return None

    def search_rule_by_id(self, ruleID) -> Rule:
        """ searches a rule by given id
        :param ruleID the device to search for
        :return the rule object or None if it couldn't find a rule
        """
        for r in self.rules:
            if r.id == ruleID:
                return r
        return None

    def get_security_zones_activation(self):
        internal_active = False
        external_active = False
        for g in self.groups:
            if isinstance(g, SecurityZoneGroup):
                if g.label == 'EXTERNAL':
                    external_active = g.active
                elif g.label == 'INTERNAL':
                    internal_active = g.active
        return internal_active, external_active

    def set_security_zones_activation(self, internal=True, external=True):
        data = {"zonesActivation": {"EXTERNAL": external, "INTERNAL": internal}}
        return self._restCall("home/security/setZonesActivation", json.dumps(data))

    def set_location(self, city, latitude, longitude):
        data = {"city": city, "latitude": latitude, "longitude": longitude}
        return self._restCall("home/setLocation", json.dumps(data))

    def set_intrusion_alert_through_smoke_detectors(self, activate=True):
        data = {"intrusionAlertThroughSmokeDetectors": activate}
        return self._restCall("home/security/setIntrusionAlertThroughSmokeDetectors",
                              json.dumps(data))

    def activate_absence_with_period(self, endtime : datetime):
        data = {"endTime": endtime.strftime("%Y_%m_%d %H:%M")}
        return self._restCall("home/heating/activateAbsenceWithPeriod", json.dumps(data))

    def activate_absence_with_duration(self, duration):
        data = {"duration": duration}
        return self._restCall("home/heating/activateAbsenceWithDuration", json.dumps(data))

    def deactivate_absence(self):
        return self._restCall("home/heating/deactivateAbsence")

    def activate_vacation(self, endtime : datetime, temperature):
        data = {"endtime": endtime.strftime("%Y_%m_%d %H:%M"),
                "temperature": temperature}
        return self._restCall("home/heating/activateVacation",
                              json.dumps(data))

    def deactivate_vacation(self):
        return self._restCall("home/heating/deactivateVacation")

    def set_pin(self, newPin, oldPin=None):
        if newPin == None:
            newPin = ""
        data = {"pin": newPin}
        if oldPin:
            self._connection.headers["PIN"] = str(oldPin)
        result = self._restCall('home/setPin', body=json.dumps(data))
        if oldPin:
            del self._connection.headers["PIN"]
        return result

    def set_zone_activation_delay(self, delay):
        data = {"zoneActivationDelay": delay}
        return self._restCall("home/security/setZoneActivationDelay",
                              body=json.dumps(data))

    def get_security_journal(self):
        journal = self._restCall("home/security/getSecurityJournal")
        if "errorCode" in journal:
            LOGGER.error("Could not get the security journal. Error: %s", journal["errorCode"])
            return None
        ret = []
        for entry in journal["entries"]:
            try:
                eventType = SecurityEventType(entry["eventType"])
                if eventType in self._typeSecurityEventMap:
                    j = self._typeSecurityEventMap[eventType](self._connection)
            except:
                j = SecurityEvent(self._connection)
                LOGGER.warning("There is no class for %s yet", entry["eventType"])
            
            j.from_json(entry)
            ret.append(j)

        return ret

    def delete_group(self, group):
        """this function will delete the given group from the cloud"""
        return group.delete()

    def get_OAuth_OTK(self):
        token = OAuthOTK(self._connection)
        token.from_json(self._restCall("home/getOAuthOTK"))
        return token

    def set_timezone(self, timezone):
        """ sets the timezone for the AP. e.g. "Europe/Berlin" """
        data = {"timezoneId": timezone}
        return self._restCall("home/setTimezone", body=json.dumps(data))

    def set_powermeter_unit_price(self, price):
        data = {"powerMeterUnitPrice": price}
        return self._restCall("home/setPowerMeterUnitPrice",
                              body=json.dumps(data))

    def set_zones_device_assignment(self, internal_devices, external_devices):
        """ sets the devices for the security zones
        :param internal_devices the devices which should be used for the internal zone
        :param external_devices the devices which should be used for the external(hull) zone
        :return the result of _restCall
        """
        internal = [x.id for x in internal_devices]
        external = [x.id for x in external_devices]
        data = {"zonesDeviceAssignment": {"INTERNAL": internal,
                                          "EXTERNAL": external}}
        return self._restCall("home/security/setZonesDeviceAssignment",
                              body=json.dumps(data))

    def enable_events(self):
        websocket.enableTrace(True)
        self.__webSocket = websocket.WebSocketApp(self._connection.urlWebSocket, header=['AUTHTOKEN: {}'.format(self._connection.auth_token),
                'CLIENTAUTH: {}'.format(self._connection.clientauth_token)],
            on_message=self._ws_on_message,
            on_error=self._ws_on_error)
        self.__webSocketThread = threading.Thread(target=self.__webSocket.run_forever)
        self.__webSocketThread.daemon = True
        self.__webSocketThread.start()

    def disable_events(self):
        self.__webSocket.close()

    def _ws_on_error(self, message):
        LOGGER.error("Websocket error: %s", bytes2str(message))

    def _ws_on_message(self, message ):
        #json.loads doesn't support bytes as parameter before python 3.6
        js = json.loads(bytes2str(message))
        # LOGGER.debug(js)
        eventList = []
        for event in js["events"].values():
            try:
                pushEventType = EventType(event["pushEventType"])
                LOGGER.debug(pushEventType)
                obj = None
                if pushEventType == EventType.GROUP_CHANGED:
                    data = event["group"]
                    obj = self.search_group_by_id(data["id"])
                    if type(obj) is MetaGroup:
                        obj.from_json(data, self.devices, self.groups)
                    else:
                        obj.from_json(data, self.devices)
                    obj.fire_update_event(data, event_type=pushEventType, obj=obj)
                elif pushEventType == EventType.HOME_CHANGED:
                    data = event["home"]
                    obj = self
                    obj.from_json(data)
                    obj.fire_update_event(data, event_type=pushEventType, obj=obj)
                elif pushEventType == EventType.CLIENT_ADDED:
                    data = event["client"]
                    obj = Client(self._connection)
                    obj.from_json(data)
                    self.clients.append(obj)
                elif pushEventType == EventType.CLIENT_CHANGED:
                    data = event["client"]
                    obj = self.search_client_by_id(data["id"])
                    obj.from_json(data)
                elif pushEventType == EventType.CLIENT_REMOVED:
                    obj = self.search_client_by_id(event["id"])
                    self.clients.remove(obj)
                elif pushEventType == EventType.DEVICE_ADDED:
                    data = event["device"]
                    obj = self._parse_device(data)
                    obj.load_functionalChannels(self.groups)
                    self.devices.append(obj)
                elif pushEventType == EventType.DEVICE_CHANGED:
                    data = event["device"]
                    obj = self.search_device_by_id(data["id"])
                    if obj is None:  # no DEVICE_ADDED Event?
                        obj = self._parse_device(data)
                        self.devices.append(obj)
                    else:
                        obj.from_json(data)
                    obj.load_functionalChannels(self.groups)
                    obj.fire_update_event(data, event_type=pushEventType, obj=obj)
                elif pushEventType == EventType.DEVICE_REMOVED:
                    obj = self.search_device_by_id(event["id"])
                    self.devices.remove(obj)
                elif pushEventType == EventType.GROUP_REMOVED:
                    obj = self.search_group_by_id(event["id"])
                    self.groups.remove(obj)
                elif pushEventType == EventType.GROUP_ADDED:
                    group = event["group"]
                    obj = self._parse_group(group)
                    self.groups.append(obj)
                elif pushEventType == EventType.SECURITY_JOURNAL_CHANGED:
                    pass  # data is just none so nothing to do here

                # TODO: implement INCLUSION_REQUESTED, NONE
                eventList.append({"eventType": pushEventType, "data": obj})
            except ValueError as valerr:
                    LOGGER.warning("Uknown EventType '%s' Data: %s", event["pushEventType"], event)

            except Exception as err:
                LOGGER.exception(err)
        self.onEvent.fire(eventList)
