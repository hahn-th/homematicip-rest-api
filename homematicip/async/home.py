# coding=utf-8
import json
import logging

from homematicip.async import HomeIPObject
from homematicip.async.connection import Connection

from homematicip.async import device

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

_typeClassMap = {'HEATING_THERMOSTAT': device.HeatingThermostat,
                 'SHUTTER_CONTACT': device.ShutterContact,
                 'WALL_MOUNTED_THERMOSTAT_PRO': device.WallMountedThermostatPro,
                 'SMOKE_DETECTOR': device.SmokeDetector,
                 'FLOOR_TERMINAL_BLOCK_6': device.FloorTerminalBlock6,
                 'PLUGABLE_SWITCH_MEASURING': device.PlugableSwitchMeasuring,
                 'TEMPERATURE_HUMIDITY_SENSOR_DISPLAY': device.TemperatureHumiditySensorDisplay,
                 'PUSH_BUTTON': device.PushButton,
                 'ALARM_SIREN_INDOOR': device.AlarmSirenIndoor,
                 'MOTION_DETECTOR_INDOOR': device.MotionDetectorIndoor,
                 'KEY_REMOTE_CONTROL_ALARM': device.KeyRemoteControlAlarm,
                 'PLUGABLE_SWITCH': device.PlugableSwitch,
                 'FULL_FLUSH_SHUTTER': device.FullFlushShutter}

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

        
    def from_json(self, js):
        home.Home.from_json(self, js)

    def start_incoming_websocket_data(self):
        """Starts listening for incoming websocket data."""
        self._connection.listen_for_websocket_data(
            self._parse_incoming_socket_data)

    def stop_incoming_websocket_data(self):
        """Stops listening for incoming websocket data."""
        self._connection.close_websocket_connection()

    def _parse_incoming_socket_data(self, js):
        for eID in js["events"]:
            event = js["events"][eID]
            pushEventType = event["pushEventType"]
            obj = None
            if pushEventType == "DEVICE_CHANGED":
                data = event["device"]
                obj = self.search_device_by_id(data["id"])
                if obj:
                    obj.from_json(data)
            else:
                LOGGER.warning(
                    "Uknown EventType '{}' Data: {}".format(
                        pushEventType, event))


    async def get_current_state(self):
        json_state = await self._connection._apiCall(
            URL_GET_CURRENT_STATE,
            json.dumps(self._connection.client_characteristics))

        js_home = json_state[HOME]

        self.from_json(js_home)

        self.devices = self._get_devices(json_state)

        return True

    def _get_devices(self, json_state):
        ret = []
        data = json_state
        for k in data["devices"]:
            _device = data["devices"][k]
            deviceType = _device["type"]
            if deviceType in _typeClassMap:
                d = _typeClassMap[deviceType](self._connection)
                d.from_json(_device)
                ret.append(d)
            else:
                d = device.Device(self._connection)
                d.from_json(_device)
                ret.append(d)
                LOGGER.warning(
                    "There is no class for {} yet".format(deviceType))
        return ret


    def set_pin(self, newPin, oldPin=None):
        LOGGER.warning('set_pin not implemented')

    async def get_OAuth_OTK(self):
        token = OAuthOTK()
        token.from_json(await self._connection._apiCall("home/getOAuthOTK"))
        return token

    def set_timezone(self, timezone):
        LOGGER.warning("set_timezone not implemented.")

    async def set_powermeter_unit_price(self, price):
        LOGGER.warning('set_powermeter_unit_price not implemented.')

    async def set_zones_device_assignment(self, internal_devices,
                                          external_devices):
        LOGGER.warning('set_zones_device_assignment not implemented.')
