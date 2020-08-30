import logging
import ssl
import sys
import threading
from typing import List

import websocket

from homematicip.base.enums import *
from homematicip.base.helpers import bytes2str
from homematicip.class_maps import *
from homematicip.connection import Connection
from homematicip.device import *
from homematicip.EventHook import *
from homematicip.group import *
from homematicip.rule import *
from homematicip.securityEvent import *

LOGGER = logging.getLogger(__name__)


class Weather(HomeMaticIPObject):
    """ this class represents the weather of the home location"""

    def __init__(self, connection):
        super().__init__(connection)
        #:float: the current temperature
        self.temperature = 0.0
        #:WeatherCondition: the current weather
        self.weatherCondition = WeatherCondition.UNKNOWN
        #:datetime: the current datime
        self.weatherDayTime = WeatherDayTime.DAY
        #:float: the minimum temperature of the day
        self.minTemperature = 0.0
        #:float: the maximum temperature of the day
        self.maxTemperature = 0.0
        #:float: the current humidity
        self.humidity = 0
        #:float: the current windspeed
        self.windSpeed = 0.0
        #:int: the current wind direction in 360° where 0° is north
        self.windDirection = 0
        #:float: the current vapor
        self.vaporAmount = 0.0

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
        self.vaporAmount = js["vaporAmount"]

    def __str__(self):
        return "temperature({}) weatherCondition({}) weatherDayTime({}) minTemperature({}) maxTemperature({}) humidity({}) vaporAmount({}) windSpeed({}) windDirection({})".format(
            self.temperature,
            self.weatherCondition,
            self.weatherDayTime,
            self.minTemperature,
            self.maxTemperature,
            self.humidity,
            self.vaporAmount,
            self.windSpeed,
            self.windDirection,
        )


class Location(HomeMaticIPObject):
    """This class represents the possible location"""

    def __init__(self, connection):
        super().__init__(connection)
        #:str: the name of the city
        self.city = "London"
        #:float: the latitude of the location
        self.latitude = 51.509865
        #:float: the longitue of the location
        self.longitude = -0.118092

    def from_json(self, js):
        super().from_json(js)
        self.city = js["city"]
        self.latitude = js["latitude"]
        self.longitude = js["longitude"]

    def __str__(self):
        return "city({}) latitude({}) longitude({})".format(
            self.city, self.latitude, self.longitude
        )


class Client(HomeMaticIPObject):
    """A client is an app which has access to the access point. 
    e.g. smartphone, 3th party apps, google home, conrad connect
    """

    def __init__(self, connection):
        super().__init__(connection)
        #:str: the unique id of the client
        self.id = ""
        #:str: a human understandable name of the client
        self.label = ""
        #:str: the home where the client belongs to
        self.homeId = ""
        #:str: the c2c service name
        self.c2cServiceIdentifier = ""
        #:ClientType: the type of this client
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


class OAuthOTK(HomeMaticIPObject):
    def __init__(self, connection):
        super().__init__(connection)
        self.authToken = None
        self.expirationTimestamp = None

    def from_json(self, js):
        super().from_json(js)
        self.authToken = js["authToken"]
        self.expirationTimestamp = self.fromtimestamp(js["expirationTimestamp"])


class AccessPointUpdateState(HomeMaticIPObject):
    def __init__(self, connection):
        super().__init__(connection)
        self.accessPointUpdateState = DeviceUpdateState.UP_TO_DATE
        self.successfulUpdateTimestamp = None
        self.updateStateChangedTimestamp = None

    def from_json(self, js):
        self.accessPointUpdateState = js["accessPointUpdateState"]
        self.successfulUpdateTimestamp = self.fromtimestamp(
            js["successfulUpdateTimestamp"]
        )
        self.updateStateChangedTimestamp = self.fromtimestamp(
            js["updateStateChangedTimestamp"]
        )


class Home(HomeMaticIPObject):
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

        # List with create handlers.
        self._on_create = []

        self.apExchangeClientId = None
        self.apExchangeState = ApExchangeState.NONE
        self.availableAPVersion = None
        self.carrierSense = None
        #:bool:displays if the access point is connected to the hmip cloud or
        # not
        self.connected = None
        #:str:the current version of the access point
        self.currentAPVersion = None
        self.deviceUpdateStrategy = DeviceUpdateStrategy.MANUALLY
        self.dutyCycle = None
        #:str:the SGTIN of the access point
        self.id = None
        self.lastReadyForUpdateTimestamp = None
        #:Location:the location of the AP
        self.location = None
        #:bool:determines if a pin is set on this access point
        self.pinAssigned = None
        self.powerMeterCurrency = None
        self.powerMeterUnitPrice = None
        self.timeZoneId = None
        self.updateState = HomeUpdateState.UP_TO_DATE
        #:Weather:the current weather
        self.weather = None

        self.__webSocket = None
        self.__webSocketThread = None
        self.onEvent = EventHook()
        self.onWsError = EventHook()
        #:bool:switch to enable/disable automatic reconnection of the websocket (default=True)
        self.websocket_reconnect_on_error = True

        #:List[Device]: a collection of all devices in home
        self.devices = []
        #:List[Client]: a collection of all clients in home
        self.clients = []
        #:List[Group]: a collection of all groups in the home
        self.groups = []
        #:List[Rule]: a collection of all rules in the home
        self.rules = []
        #: a collection of all functionalHomes in the home
        self.functionalHomes = []
        #:Map: a map of all access points and their updateStates
        self.accessPointUpdateStates = {}

    def init(self, access_point_id, lookup=True):
        self._connection.init(access_point_id, lookup)

    def set_auth_token(self, auth_token):
        self._connection.set_auth_token(auth_token)

    def from_json(self, js_home):
        super().from_json(js_home)

        self.weather = Weather(self._connection)
        self.weather.from_json(js_home["weather"])
        if js_home["location"] != None:
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
        self.deviceUpdateStrategy = DeviceUpdateStrategy.from_str(
            js_home["deviceUpdateStrategy"]
        )
        self.lastReadyForUpdateTimestamp = js_home["lastReadyForUpdateTimestamp"]
        self.apExchangeClientId = js_home["apExchangeClientId"]
        self.apExchangeState = ApExchangeState.from_str(js_home["apExchangeState"])
        self.id = js_home["id"]
        self.carrierSense = js_home["carrierSense"]

        for ap, state in js_home["accessPointUpdateStates"].items():
            ap_state = AccessPointUpdateState(self._connection)
            ap_state.from_json(state)
            self.accessPointUpdateStates[ap] = ap_state

        self._get_rules(js_home)

    def on_create(self, handler):
        """Adds an event handler to the create method. Fires when a device
        is created."""
        self._on_create.append(handler)

    def fire_create_event(self, *args, **kwargs):
        """Trigger the method tied to _on_create"""
        for _handler in self._on_create:
            _handler(*args, **kwargs)

    def remove_callback(self, handler):
        """Remove event handler."""
        super().remove_callback(handler)
        if handler in self._on_create:
            self._on_create.remove(handler)

    def download_configuration(self) -> str:
        """downloads the current configuration from the cloud

        Returns
            the downloaded configuration or an errorCode
        """
        return self._restCall(
            "home/getCurrentState", json.dumps(self._connection.clientCharacteristics)
        )

    def get_current_state(self, clearConfig: bool = False):
        """downloads the current configuration and parses it into self
           
        Args:
            clearConfig(bool): if set to true, this function will remove all old objects 
            from self.devices, self.client, ... to have a fresh config instead of reparsing them
        """
        json_state = self.download_configuration()
        return self.update_home(json_state, clearConfig)

    def update_home(self, json_state, clearConfig: bool = False):
        """parse a given json configuration into self.
        This will update the whole home including devices, clients and groups.

        Args:
            clearConfig(bool): if set to true, this function will remove all old objects
            from self.devices, self.client, ... to have a fresh config instead of reparsing them
        """
        if "errorCode" in json_state:
            LOGGER.error(
                "Could not get the current configuration. Error: %s",
                json_state["errorCode"],
            )
            return False

        if clearConfig:
            self.devices = []
            self.clients = []
            self.groups = []

        self._get_devices(json_state)
        self._get_clients(json_state)
        self._get_groups(json_state)

        js_home = json_state["home"]

        return self.update_home_only(js_home, clearConfig)

    def update_home_only(self, js_home, clearConfig: bool = False):
        """parse a given home json configuration into self.
        This will update only the home without updating devices, clients and groups.

        Args:
            clearConfig(bool): if set to true, this function will remove all old objects
            from self.devices, self.client, ... to have a fresh config instead of reparsing them
        """
        if "errorCode" in js_home:
            LOGGER.error(
                "Could not get the current configuration. Error: %s",
                js_home["errorCode"],
            )
            return False

        if clearConfig:
            self.rules = []
            self.functionalHomes = []

        self.from_json(js_home)
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
            LOGGER.warning("There is no class for device '%s' yet", json_state["type"])
            return d

    def _get_rules(self, json_state):
        self.rules = [
            x for x in self.rules if x.id in json_state["ruleMetaDatas"].keys()
        ]
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
            LOGGER.warning("There is no class for rule  '%s' yet", json_state["type"])
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
                LOGGER.warning(
                    "There is no class for group '%s' yet", json_state["type"]
                )
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
                LOGGER.warning(
                    "There is no class for functionalHome '%s' yet", solution
                )
                self.functionalHomes.append(h)

    def _load_functionalChannels(self):
        for d in self.devices:
            d.load_functionalChannels(self.groups)

    def get_functionalHome(self, functionalHomeType: type) -> FunctionalHome:
        """ gets the specified functionalHome
        
        Args:
            functionalHome(type): the type of the functionalHome which should be returned

        Returns:
            the FunctionalHome or None if it couldn't be found
        """
        for x in self.functionalHomes:
            if isinstance(x, functionalHomeType):
                return x

        return None

    def search_device_by_id(self, deviceID) -> Device:
        """ searches a device by given id
        
        Args:
          deviceID(str): the device to search for
          
        Returns
          the Device object or None if it couldn't find a device
        """
        for d in self.devices:
            if d.id == deviceID:
                return d
        return None

    def search_group_by_id(self, groupID) -> Group:
        """ searches a group by given id
        
        Args:
          groupID(str): groupID the group to search for
          
        Returns
          the group object or None if it couldn't find a group
        """
        for g in self.groups:
            if g.id == groupID:
                return g
        return None

    def search_client_by_id(self, clientID) -> Client:
        """ searches a client by given id
        
        Args:
          clientID(str): the client to search for
        
        Returns
          the client object or None if it couldn't find a client
        """
        for c in self.clients:
            if c.id == clientID:
                return c
        return None

    def search_rule_by_id(self, ruleID) -> Rule:
        """ searches a rule by given id
        
        Args:
          ruleID(str): the rule to search for
        
        Returns
          the rule object or None if it couldn't find a rule
        """
        for r in self.rules:
            if r.id == ruleID:
                return r
        return None

    def get_security_zones_activation(self) -> (bool, bool):
        """ returns the value of the security zones if they are armed or not
        
        Returns
            internal
              True if the internal zone is armed
            external
              True if the external zone is armed
        """
        internal_active = False
        external_active = False
        for g in self.groups:
            if isinstance(g, SecurityZoneGroup):
                if g.label == "EXTERNAL":
                    external_active = g.active
                elif g.label == "INTERNAL":
                    internal_active = g.active
        return internal_active, external_active

    def set_security_zones_activation(self, internal=True, external=True):
        """ this function will set the alarm system to armed or disable it
        
        Args:
          internal(bool): activates/deactivates the internal zone
          external(bool): activates/deactivates the external zone
        
        Examples:
          arming while being at home
          
          >>> home.set_security_zones_activation(False,True)
          
          arming without being at home
          
          >>> home.set_security_zones_activation(True,True)
          
          disarming the alarm system
          
          >>> home.set_security_zones_activation(False,False)
        """
        data = {"zonesActivation": {"EXTERNAL": external, "INTERNAL": internal}}
        return self._restCall("home/security/setZonesActivation", json.dumps(data))

    def set_location(self, city, latitude, longitude):
        data = {"city": city, "latitude": latitude, "longitude": longitude}
        return self._restCall("home/setLocation", json.dumps(data))

    def set_intrusion_alert_through_smoke_detectors(self, activate: bool = True):
        """ activate or deactivate if smoke detectors should "ring" during an alarm

        Args:
            activate(bool): True will let the smoke detectors "ring" during an alarm
        """
        data = {"intrusionAlertThroughSmokeDetectors": activate}
        return self._restCall(
            "home/security/setIntrusionAlertThroughSmokeDetectors", json.dumps(data)
        )

    def activate_absence_with_period(self, endtime: datetime):
        """ activates the absence mode until the given time

        Args:
            endtime(datetime): the time when the absence should automatically be disabled
        """
        data = {"endTime": endtime.strftime("%Y_%m_%d %H:%M")}
        return self._restCall(
            "home/heating/activateAbsenceWithPeriod", json.dumps(data)
        )

    def activate_absence_with_duration(self, duration: int):
        """ activates the absence mode for a given time

        Args:
            duration(int): the absence duration in minutes
        """
        data = {"duration": duration}
        return self._restCall(
            "home/heating/activateAbsenceWithDuration", json.dumps(data)
        )

    def deactivate_absence(self):
        """ deactivates the absence mode immediately"""
        return self._restCall("home/heating/deactivateAbsence")

    def activate_vacation(self, endtime: datetime, temperature: float):
        """ activates the vatation mode until the given time

        Args:
            endtime(datetime): the time when the vatation mode should automatically be disabled
            temperature(float): the settemperature during the vacation mode
        """
        data = {
            "endTime": endtime.strftime("%Y_%m_%d %H:%M"),
            "temperature": temperature,
        }
        return self._restCall("home/heating/activateVacation", json.dumps(data))

    def deactivate_vacation(self):
        """ deactivates the vacation mode immediately"""
        return self._restCall("home/heating/deactivateVacation")

    def set_pin(self, newPin: str, oldPin: str = None) -> dict:
        """ sets a new pin for the home

        Args:
            newPin(str): the new pin
            oldPin(str): optional, if there is currently a pin active it must be given here.
                        Otherwise it will not be possible to set the new pin

        Returns:
            the result of the call
        """
        if newPin is None:
            newPin = ""
        data = {"pin": newPin}
        if oldPin:
            self._connection.headers["PIN"] = str(oldPin)
        result = self._restCall("home/setPin", body=json.dumps(data))
        if oldPin:
            del self._connection.headers["PIN"]
        return result

    def set_zone_activation_delay(self, delay):
        data = {"zoneActivationDelay": delay}
        return self._restCall(
            "home/security/setZoneActivationDelay", body=json.dumps(data)
        )

    def get_security_journal(self):
        journal = self._restCall("home/security/getSecurityJournal")
        if "errorCode" in journal:
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
                j = SecurityEvent(self._connection)
                LOGGER.warning("There is no class for %s yet", entry["eventType"])

            j.from_json(entry)
            ret.append(j)

        return ret

    def delete_group(self, group: Group):
        """deletes the given group from the cloud
        
        Args:
            group(Group):the group to delete
        """
        return group.delete()

    def get_OAuth_OTK(self):
        token = OAuthOTK(self._connection)
        token.from_json(self._restCall("home/getOAuthOTK"))
        return token

    def set_timezone(self, timezone: str):
        """ sets the timezone for the AP. e.g. "Europe/Berlin" 
        Args:
            timezone(str): the new timezone
        """
        data = {"timezoneId": timezone}
        return self._restCall("home/setTimezone", body=json.dumps(data))

    def set_powermeter_unit_price(self, price):
        data = {"powerMeterUnitPrice": price}
        return self._restCall("home/setPowerMeterUnitPrice", body=json.dumps(data))

    def set_zones_device_assignment(self, internal_devices, external_devices) -> dict:
        """ sets the devices for the security zones
        Args:
            internal_devices(List[Device]): the devices which should be used for the internal zone
            external_devices(List[Device]):  the devices which should be used for the external(hull) zone
        
        Returns:
            the result of _restCall
        """
        internal = [x.id for x in internal_devices]
        external = [x.id for x in external_devices]
        data = {"zonesDeviceAssignment": {"INTERNAL": internal, "EXTERNAL": external}}
        return self._restCall(
            "home/security/setZonesDeviceAssignment", body=json.dumps(data)
        )

    def start_inclusion(self, deviceId):
        """ start inclusion mode for specific device
        Args:
            deviceId: sgtin of device        
        """
        data = {"deviceId": deviceId}
        return self._restCall("home/startInclusionModeForDevice", body=json.dumps(data))

    def enable_events(self):
        websocket.enableTrace(True)

        self.__webSocket = websocket.WebSocketApp(
            self._connection.urlWebSocket,
            header=[
                "AUTHTOKEN: {}".format(self._connection.auth_token),
                "CLIENTAUTH: {}".format(self._connection.clientauth_token),
            ],
            on_message=self._ws_on_message,
            on_error=self._ws_on_error,
            on_close=self._ws_on_close,
        )

        websocket_kwargs = {"ping_interval": 3}
        if hasattr(sys, "_called_from_test"):  # disable ssl during a test run
            sslopt = {"cert_reqs": ssl.CERT_NONE}
            websocket_kwargs = {"sslopt": sslopt, "ping_interval": 2, "ping_timeout": 1}

        self.__webSocketThread = threading.Thread(
            name="hmip-websocket",
            target=self.__webSocket.run_forever,
            kwargs=websocket_kwargs,
        )
        self.__webSocketThread.setDaemon(True)
        self.__webSocketThread.start()

    def disable_events(self):
        if self.__webSocket:
            self.__webSocket.close()
            self.__webSocket = None

    def _ws_on_close(self):
        self.__webSocket = None

    def _ws_on_error(self, err):
        LOGGER.exception(err)
        self.onWsError.fire(err)
        if self.websocket_reconnect_on_error:
            logger.debug("Trying to reconnect websocket")
            self.disable_events()
            self.enable_events()

    def _ws_on_message(self, message):
        # json.loads doesn't support bytes as parameter before python 3.6
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
                    if obj is None:
                        obj = self._parse_group(data)
                        self.groups.append(obj)
                        pushEventType = EventType.GROUP_ADDED
                        self.fire_create_event(obj, event_type=pushEventType, obj=obj)
                    if type(obj) is MetaGroup:
                        obj.from_json(data, self.devices, self.groups)
                    else:
                        obj.from_json(data, self.devices)
                    obj.fire_update_event(data, event_type=pushEventType, obj=obj)
                elif pushEventType == EventType.HOME_CHANGED:
                    data = event["home"]
                    obj = self
                    obj.update_home_only(data)
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
                    self.fire_create_event(data, event_type=pushEventType, obj=obj)
                elif pushEventType == EventType.DEVICE_CHANGED:
                    data = event["device"]
                    obj = self.search_device_by_id(data["id"])
                    if obj is None:  # no DEVICE_ADDED Event?
                        obj = self._parse_device(data)
                        self.devices.append(obj)
                        pushEventType = EventType.DEVICE_ADDED
                        self.fire_create_event(data, event_type=pushEventType, obj=obj)
                    else:
                        obj.from_json(data)
                    obj.load_functionalChannels(self.groups)
                    obj.fire_update_event(data, event_type=pushEventType, obj=obj)
                elif pushEventType == EventType.DEVICE_REMOVED:
                    obj = self.search_device_by_id(event["id"])
                    obj.fire_remove_event(obj, event_type=pushEventType, obj=obj)
                    self.devices.remove(obj)
                elif pushEventType == EventType.GROUP_REMOVED:
                    obj = self.search_group_by_id(event["id"])
                    obj.fire_remove_event(obj, event_type=pushEventType, obj=obj)
                    self.groups.remove(obj)
                elif pushEventType == EventType.GROUP_ADDED:
                    group = event["group"]
                    obj = self._parse_group(group)
                    self.groups.append(obj)
                    self.fire_create_event(obj, event_type=pushEventType, obj=obj)
                elif pushEventType == EventType.SECURITY_JOURNAL_CHANGED:
                    pass  # data is just none so nothing to do here

                # TODO: implement INCLUSION_REQUESTED, NONE
                eventList.append({"eventType": pushEventType, "data": obj})
            except ValueError as valerr:  # pragma: no cover
                LOGGER.warning(
                    "Uknown EventType '%s' Data: %s", event["pushEventType"], event
                )

            except Exception as err:  # pragma: no cover
                LOGGER.exception(err)
        self.onEvent.fire(eventList)
