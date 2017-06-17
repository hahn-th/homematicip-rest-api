# coding=utf-8
import homematicip
import threading
from homematicip.device import *
from homematicip.group import *
from homematicip.securityEvent import *
from homematicip.EventHook import *

from datetime import datetime
import requests
import websocket
import logging
import sys

logger = logging.getLogger(__name__)

_typeClassMap = {"HEATING_THERMOSTAT" : HeatingThermostat, "SHUTTER_CONTACT" : ShutterContact,
                 "WALL_MOUNTED_THERMOSTAT_PRO" : WallMountedThermostatPro, "SMOKE_DETECTOR" : SmokeDetector,
                 "FLOOR_TERMINAL_BLOCK_6": FloorTerminalBlock6, "PLUGABLE_SWITCH_MEASURING": PlugableSwitchMeasuring,
                 "TEMPERATURE_HUMIDITY_SENSOR_DISPLAY": TemperatureHumiditySensorDisplay, "PUSH_BUTTON": PushButton,
                 "ALARM_SIREN_INDOOR": AlarmSirenIndoor, "MOTION_DETECTOR_INDOOR": MotionDetectorIndoor,
                 "KEY_REMOTE_CONTROL_ALARM": KeyRemoteControlAlarm, "PLUGABLE_SWITCH" : PlugableSwitch}

_typeGroupMap = { "SECURITY" : SecurityGroup, "SWITCHING" : SwitchingGroup, "EXTENDED_LINKED_SWITCHING" : ExtendedLinkedSwitchingGroup
                , "LINKED_SWITCHING" : LinkedSwitchingGroup, "ALARM_SWITCHING" : AlarmSwitchingGroup, "HEATING_HUMIDITY_LIMITER" : HeatingHumidyLimiterGroup
                , "HEATING_TEMPERATURE_LIMITER" : HeatingTemperatureLimiterGroup, "HEATING_CHANGEOVER" : HeatingChangeoverGroup, "INBOX" : InboxGroup
                , "SECURITY_ZONE" : SecurityZoneGroup, "HEATING" : HeatingGroup, "HEATING_COOLING_DEMAND" : HeatingCoolingDemandGroup
                , "HEATING_EXTERNAL_CLOCK" : HeatingExternalClockGroup, "HEATING_DEHUMIDIFIER" : HeatingDehumidifierGroup
                , "HEATING_COOLING_DEMAND_BOILER" : HeatingCoolingDemandBoilerGroup, "HEATING_COOLING_DEMAND_PUMP" : HeatingCoolingDemandPumpGroup  
                , "SWITCHING_PROFILE" : SwitchingProfileGroup }

_typeSecurityEventMap = { "SILENCE_CHANGED" : SilenceChangedEvent, "ACTIVATION_CHANGED" : ActivationChangedEvent,  "ACCESS_POINT_CONNECTED" : AccessPointConnectedEvent,
                         "ACCESS_POINT_DISCONNECTED" : AccessPointDisconnectedEvent, "SENSOR_EVENT" : SensorEvent }

class Weather(HomeMaticIPObject.HomeMaticIPObject):
    temperature = 0.0
    weatherCondition = "CLEAR"
    weatherDayTime = "DAY"
    minTemperature = 0.0
    maxTemperature = 0.0
    humidity = 0
    windSpeed = 0.0
    windDirection = 0


    def from_json(self, js):
        self.temperature = js["temperature"]
        self.weatherCondition = js["weatherCondition"]
        self.weatherDayTime = js["weatherDayTime"]
        self.minTemperature = js["minTemperature"]
        self.maxTemperature = js["maxTemperature"]
        self.humidity = js["humidity"]
        self.windSpeed = js["windSpeed"]
        self.windDirection = js["windDirection"]


class Location(HomeMaticIPObject.HomeMaticIPObject):
    city = "London"
    latitude = "51.509865"
    longitude = "-0.118092"

    def from_json(self, js):
        self.city = js["city"]
        self.latitude = js["latitude"]
        self.longitude = js["longitude"]

    def __unicode__(self):
        return u"city({}) latitude({}) longitude({})".format(self.city,self.latitude,self.longitude)


class Client(HomeMaticIPObject.HomeMaticIPObject):
    id = None
    label = None
    homeId = None

    def from_json(self, js):
        self.id = js["id"]
        self.label = js["label"]
        self.homeId = js["homeId"]

    def __unicode__(self):
        return u"label({})".format(self.label)

class OAuthOTK(HomeMaticIPObject.HomeMaticIPObject):
    authToken = None
    expirationTimestamp = None

    def from_json(self, js):
        self.authToken = js["authToken"]
        time = js["expirationTimestamp"]
        if time > 0:
            self.expirationTimestamp = datetime.fromtimestamp(time / 1000.0)
        else:
            self.expirationTimestamp = None

class Home(HomeMaticIPObject.HomeMaticIPObject):
    """this class represents the 'Home' of the homematic ip"""
    devices = None
    groups = None
    weather = None
    location = None
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

    __webSocket = None
    __webSocketThread = None
    onEvent = EventHook()

    def from_json(self, js_home):
        super(Home, self).from_json(js_home)
        self.weather = Weather()
        self.weather.from_json(js_home["weather"])
        self.location = Location()
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
        self.lastReadyForUpdateTimestamp = js_home["lastReadyForUpdateTimestamp"]
        self.apExchangeClientId = js_home["apExchangeClientId"]
        self.apExchangeState = js_home["apExchangeState"]
        self.id = js_home["id"]

    def get_current_state(self):
        json_state = self._restCall('home/getCurrentState', json.dumps(homematicip.get_clientCharacteristics()))
        if "errorCode" in json_state:
            logger.error("Could not get the current configuration. Error: {}".format(json_state["errorCode"]))
            return False

        js_home = json_state["home"]

        self.from_json(js_home)

        self.devices = self._get_devices(json_state)
        self.clients = self._get_clients(json_state)
        self.groups = self._get_groups(json_state)

        return True

    def _get_devices(self, json_state):
        ret = []
        data = json_state
        for k in data["devices"]:
            device = data["devices"][k]
            deviceType = device["type"]
            if deviceType in _typeClassMap:
                d = _typeClassMap[deviceType]()
                d.from_json(device)
                ret.append(d)
            else:
                d = Device()
                d.from_json(device)
                ret.append(d)
                logger.warn("There is no class for {} yet".format(deviceType))
        return ret
    
    def _get_clients(self, json_state):
        ret = []
        data = json_state
        for k in data["clients"]:
            client = data["clients"][k]
            c = Client()
            c.from_json(client)
            ret.append(c)
        return ret

    def _get_groups(self, json_state):
        ret = []
        data = json_state
        metaGroups = []
        for k in data["groups"]:
            group = data["groups"][k]
            groupType = group["type"]
            if groupType in _typeGroupMap:
                g = _typeGroupMap[groupType]()
                g.from_json(group,self.devices)
                ret.append(g)
            elif groupType == "META":
                metaGroups.append(group)
            else:
                g = Group()
                g.from_json(group,self.devices)
                ret.append(g)
                logger.warn("There is no class for {} yet".format(groupType))

        for mg in metaGroups:
            g = MetaGroup()
            g.from_json(mg,self.devices,ret)
            ret.append(g)
        return ret

    def search_device_by_id(self, deviceID):
        """ searches a device by given id
        :param deviceID the device to search for
        :return the Device object or None if it couldn't find a device
        """
        for d in self.devices:
            if d.id == deviceID:
                return d
        return None

    def search_group_by_id(self, groupID):
        """ searches a group by given id
        :param groupID the device to search for
        :return the group object or None if it couldn't find a group
        """
        for g in self.groups:
            if g.id == groupID:
                return g
        return None

    def search_client_by_id(self, clientID):
        """ searches a client by given id
        :param clientID the device to search for
        :return the client object or None if it couldn't find a client
        """
        for c in self.clients:
            if c.id == clientID:
                return c
        return None

    def set_security_zones_activation(self, internal=True, external=True):
        data = {"zonesActivation": {"EXTERNAL": external, "INTERNAL": internal}}
        return self._restCall("home/security/setZonesActivation", json.dumps(data))

    def set_location(self, city, latitude, longitude):
        data = {"city": city, "latitude": latitude, "longitude": longitude}
        return self._restCall("home/setLocation", json.dumps(data))

    def set_intrusion_alert_through_smoke_detectors(self, activate=True):
        data = {"intrusionAlertThroughSmokeDetectors": activate}
        return self._restCall("home/security/setIntrusionAlertThroughSmokeDetectors", json.dumps(data))

    def activate_absence_with_period(self, endtime):
        data = {"endTime": endtime.strftime("%Y_%m_%d %H:%M")}
        return self._restCall("home/heating/activateAbsenceWithPeriod", json.dumps(data))

    def activate_absence_with_duration(self, duration):
        data = {"duration": duration}
        return self._restCall("home/heating/activateAbsenceWithDuration", json.dumps(data))

    def deactivate_absence(self):
        return self._restCall("home/heating/deactivateAbsence")

    def activate_vacation(self, endtime, temperature):
        data = {"endtime": endtime.strftime("%Y_%m_%d %H:%M"), "temperature": temperature}
        return self._restCall("home/heating/activateVacation", json.dumps(data))

    def deactivate_vacation(self):
        return self._restCall("home/heating/deactivateVacation")

    def set_pin(self,newPin,oldPin=None):
        if newPin == None:
            newPin = ""
        data = { "pin" : newPin }
        if oldPin:
            self.headers["PIN"] = oldPin
        result = self._restCall('home/setPin', body=json.dumps(data))
        if oldPin:
            del self.headers["PIN"]
        return result

    def set_zone_activation_delay( self, delay):
        data = { "zoneActivationDelay":delay }
        return self._restCall("home/security/setZoneActivationDelay", body=json.dumps(data))

    def get_security_journal(self):
        journal = self._restCall("home/security/getSecurityJournal")
        if "errorCode" in journal:
            logger.error("Could not get the security journal. Error: {}".format(journal["errorCode"]))
            return None
        ret = []
        for entry in journal["entries"]:
            eventType = entry["eventType"]
            if eventType in _typeSecurityEventMap:
                j = _typeSecurityEventMap[eventType]()
                j.from_json(entry)
                ret.append(j)
            else:
                j = SecurityEvent()
                j.from_json(entry)
                ret.append(j)
                logger.warn("There is no class for {} yet".format(eventType))
        return ret

    def delete_group(self, group):
        data = { "groupId" : group.id }
        return self._restCall("home/group/deleteGroup", body = json.dumps(data))

    def get_OAuth_OTK(self):
        token = OAuthOTK()
        token.from_json(self._restCall("home/getOAuthOTK" ))
        return token

    def set_timezone(self, timezone):
        """ sets the timezone for the AP. e.g. "Europe/Berlin" """
        data = { "timezoneId" : timezone }
        return self._restCall("home/setTimezone", body = json.dumps(data))

    def set_powermeter_unit_price(self, price):
        data = { "powerMeterUnitPrice" : price }
        return self._restCall("home/setPowerMeterUnitPrice", body = json.dumps(data))

    def set_zones_device_assignment(self, internal_devices, external_devices):
        """ sets the devices for the security zones
        :param internal_devices the devices which should be used for the internal zone
        :param external_devices the devices which should be used for the external(hull) zone
        :return the result of _restCall
        """
        internal = [x.id for x in internal_devices]
        external = [x.id for x in external_devices]
        data = { "zonesDeviceAssignment" : { "INTERNAL":internal, "EXTERNAL":external } }
        return self._restCall("home/security/setZonesDeviceAssignment", body = json.dumps(data))

    def enable_events(self):
        websocket.enableTrace(True)
        self.__webSocket = websocket.WebSocketApp(homematicip.get_urlWebSocket(), header=['AUTHTOKEN: {}'.format(homematicip.get_auth_token()), 'CLIENTAUTH: {}'.format(homematicip.get_clientauth_token())], on_message=self.__ws_on_message, on_error=self.__ws_on_error)
        self.__webSocketThread = threading.Thread(target=self.__webSocket.run_forever)
        self.__webSocketThread.daemon = True
        self.__webSocketThread.start()

    def disable_events(self):
        self.__webSocket.close()

    def __ws_on_error(self,ws,message):
        logger.error("Websocket error: {}".format(message))
        
    def __ws_on_message(self,ws, message):
        js = json.loads(message)
        eventList=[]
        try:
            for eID in js["events"]:
                event = js["events"][eID]
                pushEventType = event["pushEventType"]
                obj = None 
                if pushEventType == "GROUP_CHANGED":
                    data = event["group"]
                    obj=self.search_group_by_id(data["id"])
                    obj.from_json(data,self.devices)
                elif pushEventType == "HOME_CHANGED":
                    data = event["home"]
                    obj = self
                    obj.from_json(data)
                elif pushEventType == "CLIENT_ADDED":
                    data = event["client"]
                    obj=Client()
                    obj.from_json(data)
                    self.clients.append(obj)                             
                elif pushEventType == "CLIENT_CHANGED":
                    data = event["client"]
                    obj=self.search_client_by_id(data["id"])
                    obj.from_json(data)
                elif pushEventType == "CLIENT_REMOVED":
                    obj=self.search_client_by_id(event["id"])
                    self.clients.remove(obj)
                elif pushEventType == "DEVICE_ADDED":
                    data = event["device"]
                    obj=Device() #TODO:implement typecheck
                    obj.from_json(data)
                    self.devices.append(obj)                             
                elif pushEventType == "DEVICE_CHANGED":
                    data = event["device"]
                    obj=self.search_device_by_id(data["id"])
                    obj.from_json(data)
                elif pushEventType == "DEVICE_REMOVED":
                    obj=self.search_device_by_id(event["id"])
                    self.devices.remove(obj)
                elif pushEventType == "GROUP_REMOVED":
                    obj=self.search_group_by_id(event["id"])
                    self.groups.remove(obj)
                elif pushEventType == "GROUP_ADDED":
                    data = event["group"]
                    obj=Group() #TODO:implement typecheck
                    obj.from_json(data)
                    self.groups.append(obj)
                elif pushEventType == "SECURITY_JOURNAL_CHANGED":
                    pass # data is just none so nothing to do here

                #TODO: implement INCLUSION_REQUESTED, NONE
                else:
                    logger.warn("Uknown EventType '{}' Data: {}".format(pushEventType,event))
                eventList.append({"eventType":pushEventType, "data" : obj})
        except:
            logger.error("Unexpected error: {}".format(sys.exc_info()[0]))
        self.onEvent.fire(eventList)