# coding=utf-8
import json
import logging
import asyncio
import aiohttp

from datetime import datetime
from homematicip.async import HomeIPObject
from homematicip.async.connection import Connection
from homematicip.async.device import HeatingThermostat, ShutterContact, \
    WallMountedThermostatPro, SmokeDetector, FloorTerminalBlock6, \
    PlugableSwitchMeasuring, TemperatureHumiditySensorDisplay, PushButton, \
    AlarmSirenIndoor, MotionDetectorIndoor, KeyRemoteControlAlarm, \
    PlugableSwitch, FullFlushShutter, Device

from homematicip import home
from homematicip.home import OAuthOTK

TYPE = "type"
GROUPS = "groups"
URL_GET_CURRENT_STATE = 'home/getCurrentState'
URL_HOME_SET_LOCATION = "home/setLocation"
CLIENTS = "clients"
DEVICES = "devices"
ERROR_CODE = "errorCode"
ID = "id"
HOME = "home"
AP_EXCHANGE_STATE = "apExchangeState"
AP_EXCHANGE_CLIENT_ID = "apExchangeClientId"
DEVICE_UPDATE_STRATEGY = "deviceUpdateStrategy"
POWER_METER_CURRENCY = "powerMeterCurrency"
POWER_METER_UNIT_PRICE = "powerMeterUnitPrice"
UPDATE_STATE = "updateState"
DUTY_CYCLE = "dutyCycle"
PIN_ASSIGNED = "pinAssigned"
TIME_ZONE_ID = "timeZoneId"
AVAILABLE_AP_VERSION = "availableAPVersion"
CURRENT_AP_VERSION = "currentAPVersion"
CONNECTED = "connected"
LOCATION = "location"
WEATHER = "weather"

LOGGER = logging.getLogger(__name__)


# c = {"HEATING_THERMOSTAT": HeatingThermostat,
#                  "SHUTTER_CONTACT": ShutterContact,
#                  "WALL_MOUNTED_THERMOSTAT_PRO": WallMountedThermostatPro,
#                  "SMOKE_DETECTOR": SmokeDetector,
#                  "FLOOR_TERMINAL_BLOCK_6": FloorTerminalBlock6,
#                  "PLUGABLE_SWITCH_MEASURING": PlugableSwitchMeasuring,
#                  "TEMPERATURE_HUMIDITY_SENSOR_DISPLAY": TemperatureHumiditySensorDisplay,
#                  "PUSH_BUTTON": PushButton,
#                  "ALARM_SIREN_INDOOR": AlarmSirenIndoor,
#                  "MOTION_DETECTOR_INDOOR": MotionDetectorIndoor,
#                  "KEY_REMOTE_CONTROL_ALARM": KeyRemoteControlAlarm,
#                  "PLUGABLE_SWITCH": PlugableSwitch,
#                  "FULL_FLUSH_SHUTTER": FullFlushShutter}


# _typeGroupMap = {"SECURITY": SecurityGroup, "SWITCHING": SwitchingGroup,
#                  "EXTENDED_LINKED_SWITCHING": ExtendedLinkedSwitchingGroup
#     , "LINKED_SWITCHING": LinkedSwitchingGroup,
#                  "ALARM_SWITCHING": AlarmSwitchingGroup,
#                  "HEATING_HUMIDITY_LIMITER": HeatingHumidyLimiterGroup
#     , "HEATING_TEMPERATURE_LIMITER": HeatingTemperatureLimiterGroup,
#                  "HEATING_CHANGEOVER": HeatingChangeoverGroup,
#                  "INBOX": InboxGroup
#     , "SECURITY_ZONE": SecurityZoneGroup, "HEATING": HeatingGroup,
#                  "HEATING_COOLING_DEMAND": HeatingCoolingDemandGroup
#     , "HEATING_EXTERNAL_CLOCK": HeatingExternalClockGroup,
#                  "HEATING_DEHUMIDIFIER": HeatingDehumidifierGroup
#     , "HEATING_COOLING_DEMAND_BOILER": HeatingCoolingDemandBoilerGroup,
#                  "HEATING_COOLING_DEMAND_PUMP": HeatingCoolingDemandPumpGroup
#     , "SWITCHING_PROFILE": SwitchingProfileGroup,
#                  "OVER_HEAT_PROTECTION_RULE": OverHeatProtectionRule,
#                  "SMOKE_ALARM_DETECTION_RULE": SmokeAlarmDetectionRule,
#                  "LOCK_OUT_PROTECTION_RULE": LockOutProtectionRule,
#                  "SHUTTER_WIND_PROTECTION_RULE": ShutterWindProtectionRule}
#
# _typeSecurityEventMap = {"SILENCE_CHANGED": SilenceChangedEvent,
#                          "ACTIVATION_CHANGED": ActivationChangedEvent,
#                          "ACCESS_POINT_CONNECTED": AccessPointConnectedEvent,
#                          "ACCESS_POINT_DISCONNECTED": AccessPointDisconnectedEvent,
#                          "SENSOR_EVENT": SensorEvent}


class Weather(HomeIPObject.HomeMaticIPobject):
    temperature = 0.0
    weatherCondition = "CLEAR"
    weatherDayTime = "DAY"
    minTemperature = 0.0
    maxTemperature = 0.0
    humidity = 0
    windSpeed = 0.0
    windDirection = 0

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        self.temperature = js["temperature"]
        self.weatherCondition = js["weatherCondition"]
        self.weatherDayTime = js["weatherDayTime"]
        self.minTemperature = js["minTemperature"]
        self.maxTemperature = js["maxTemperature"]
        self.humidity = js["humidity"]
        self.windSpeed = js["windSpeed"]
        self.windDirection = js["windDirection"]


class Location(HomeIPObject.HomeMaticIPobject):
    city = "London"
    latitude = "51.509865"
    longitude = "-0.118092"

    def __init__(self, connection):
        super().__init__(connection)

    def from_json(self, js):
        self.city = js["city"]
        self.latitude = js["latitude"]
        self.longitude = js["longitude"]

    def __unicode__(self):
        return u"city({}) latitude({}) longitude({})".format(self.city,
                                                             self.latitude,
                                                             self.longitude)


class Client(HomeIPObject.HomeMaticIPobject):
    def __init__(self, connection):
        super().__init__(connection)

    id = None
    label = None
    homeId = None

    def from_json(self, js):
        self.id = js["id"]
        self.label = js["label"]
        self.homeId = js["homeId"]


class Home(HomeIPObject.HomeMaticIPobject, home.Home):
    """this class represents the 'Home' of the homematic ip"""

    def __init__(self, connection: Connection):
        super().__init__(connection)
        self._connection._loop.create_task(self.websocket())

    @asyncio.coroutine
    def websocket(self):
        try:
            ws = yield from self._connection.websession.ws_connect(
                self._connection.urlWebSocket,
                headers={'AUTHTOKEN': self._connection.auth_token,
                         'CLIENTAUTH': self._connection.clientauth_token}
            )
            while True:
                msg = yield from ws.receive()
                if msg.tp == aiohttp.WSMsgType.BINARY:
                    js = json.loads(msg.data)
                    LOGGER.debug("incoming: {}".format(js))
                    eventList = []
                    try:
                        for eID in js["events"]:
                            event = js["events"][eID]
                            pushEventType = event["pushEventType"]
                            obj = None
                            if pushEventType == "GROUP_CHANGED":
                                LOGGER.debug(pushEventType)
                                # data = event["group"]
                                # obj = self.search_group_by_id(data["id"])
                                # obj.from_json(data, self.devices)
                            elif pushEventType == "HOME_CHANGED":
                                data = event["home"]
                                obj = self
                                obj.from_json(data)
                            # elif pushEventType == "CLIENT_ADDED":
                            #     data = event["client"]
                            #     obj = Client()
                            #     obj.from_json(data)
                            #     self.clients.append(obj)
                            elif pushEventType == "CLIENT_CHANGED":
                                data = event["client"]
                                obj = self.search_client_by_id(data["id"])
                                obj.from_json(data)
                            elif pushEventType == "CLIENT_REMOVED":
                                obj = self.search_client_by_id(event["id"])
                                self.clients.remove(obj)
                            # elif pushEventType == "DEVICE_ADDED":
                            #     data = event["device"]
                            #     obj = Device()  # TODO:implement typecheck
                            #     obj.from_json(data)
                            #     self.devices.append(obj)
                            elif pushEventType == "DEVICE_CHANGED":
                                data = event["device"]
                                obj = self.search_device_by_id(data["id"])
                                obj.from_json(data)
                            elif pushEventType == "DEVICE_REMOVED":
                                obj = self.search_device_by_id(event["id"])
                                self.devices.remove(obj)
                            # elif pushEventType == "GROUP_REMOVED":
                            #     obj = self.search_group_by_id(event["id"])
                            #     self.groups.remove(obj)
                            # elif pushEventType == "GROUP_ADDED":
                            #     data = event["group"]
                            #     obj=Group() #TODO:implement typecheck
                            #     obj.from_json(data)
                            #     self.groups.append(obj)
                            elif pushEventType == "SECURITY_JOURNAL_CHANGED":
                                pass  # data is just none so nothing to do here

                            # TODO: implement INCLUSION_REQUESTED, NONE
                            else:
                                LOGGER.warning(
                                    "Uknown EventType '{}' Data: {}".format(
                                        pushEventType, event))
                            eventList.append(
                                {"eventType": pushEventType, "data": obj})
                    except Exception as e:
                        LOGGER.exception(e)
                        # LOGGER.error("Unexpected error: {}".format(sys.exc_info()[0]))


                elif msg.tp == aiohttp.WSMsgType.CLOSED:
                    LOGGER.warning("websocket connection closed")
                    break
                elif msg.tp == aiohttp.WSMsgType.ERROR:
                    LOGGER.warning("websocket connection error")
                    break
        except Exception as e:
            LOGGER.exception(e)

    async def get_current_state(self):
        json_state = await self._apiCall(
            URL_GET_CURRENT_STATE,
            json.dumps(self._connection.client_characteristics))
        if ERROR_CODE in json_state:
            LOGGER.error(
                "Could not get the current configuration. Error: {}".format(
                    json_state[ERROR_CODE]))
            return False

        js_home = json_state[HOME]

        self.from_json(js_home)

        self.devices = self._get_devices(json_state)
        self.clients = self._get_clients(json_state)
        self.groups = self._get_groups(json_state)

        return True

    # def set_security_zones_activation(self, internal=True, external=True):
    #     data = {
    #         "zonesActivation": {"EXTERNAL": external, "INTERNAL": internal}}
    #     return self._restCall("home/security/setZonesActivation",
    #                           json.dumps(data))
    #
    # def set_location(self, city, latitude, longitude):
    #     data = {"city": city, "latitude": latitude, "longitude": longitude}
    #     return self._restCall(URL_HOME_SET_LOCATION, json.dumps(data))
    #
    # def set_intrusion_alert_through_smoke_detectors(self, activate=True):
    #     data = {"intrusionAlertThroughSmokeDetectors": activate}
    #     return self._restCall(
    #         "home/security/setIntrusionAlertThroughSmokeDetectors",
    #         json.dumps(data))

    # def activate_absence_with_period(self, endtime):
    #     data = {"endTime": endtime.strftime("%Y_%m_%d %H:%M")}
    #     return self._restCall("home/heating/activateAbsenceWithPeriod",
    #                           json.dumps(data))
    #
    # def activate_absence_with_duration(self, duration):
    #     data = {"duration": duration}
    #     return self._restCall("home/heating/activateAbsenceWithDuration",
    #                           json.dumps(data))
    #
    # def deactivate_absence(self):
    #     return self._restCall("home/heating/deactivateAbsence")
    #
    # def activate_vacation(self, endtime, temperature):
    #     data = {"endtime": endtime.strftime("%Y_%m_%d %H:%M"),
    #             "temperature": temperature}
    #     return self._restCall("home/heating/activateVacation",
    #                           json.dumps(data))
    #
    # def deactivate_vacation(self):
    #     return self._restCall("home/heating/deactivateVacation")
    #
    def set_pin(self, newPin, oldPin=None):
        LOGGER.warning('Not implemented')

    # def set_zone_activation_delay(self, delay):
    #     data = {"zoneActivationDelay": delay}
    #     return self._restCall("home/security/setZoneActivationDelay",
    #                           body=json.dumps(data))

    # async def get_security_journal(self):
    #     journal = await self._restCall("home/security/getSecurityJournal")
    #     if "errorCode" in journal:
    #         LOGGER.error(
    #             "Could not get the security journal. Error: {}".format(
    #                 journal["errorCode"]))
    #         return None
    #     ret = []
    #     for entry in journal["entries"]:
    #         eventType = entry["eventType"]
    #         if eventType in _typeSecurityEventMap:
    #             j = _typeSecurityEventMap[eventType]()
    #             j.from_json(entry)
    #             ret.append(j)
    #         else:
    #             j = SecurityEvent()
    #             j.from_json(entry)
    #             ret.append(j)
    #             LOGGER.warning("There is no class for {} yet".format(eventType))
    #     return ret

    # def delete_group(self, group):
    #     data = {"groupId": group.id}
    #     return self._restCall("home/group/deleteGroup", body=json.dumps(data))

    async def get_OAuth_OTK(self):
        token = OAuthOTK()
        token.from_json(await self._apiCall("home/getOAuthOTK"))
        return token

    def set_timezone(self, timezone):
        """ sets the timezone for the AP. e.g. "Europe/Berlin" """
        url, data = super().set_timezone(timezone)
        return self._apiCall(url, data)

    async def set_powermeter_unit_price(self, price):
        url, data = super().set_powermeter_unit_price(price)

        return await self._apiCall(url, data)

    async def set_zones_device_assignment(self, internal_devices,
                                          external_devices):
        """ sets the devices for the security zones
                :param internal_devices the devices which should be used for the internal zone
                :param external_devices the devices which should be used for the external(hull) zone
                :return the result of _restCall
                """
        url, data = super().set_zones_device_assignment(internal_devices,
                                                        external_devices)

        return await self._apiCall(url, data)
