import homematicip
from homematicip.device import *
import requests

_typeClassMap = {"HEATING_THERMOSTAT": HeatingThermostat, "SHUTTER_CONTACT": ShutterContact,
                 "WALL_MOUNTED_THERMOSTAT_PRO": WallMountedThermostatPro, "SMOKE_DETECTOR": SmokeDetector,
                 "FLOOR_TERMINAL_BLOCK_6": FloorTerminalBlock6}


class Weather(HomeMaticIPObject.HomeMaticIPObject):
    temperature = None
    weatherCondition = None
    weatherDayTime = None

    def from_json(self, js):
        self.temperature = js["temperature"]
        self.weatherCondition = js["weatherCondition"]
        self.weatherDayTime = js["weatherDayTime"]


class Location(HomeMaticIPObject.HomeMaticIPObject):
    city = None
    latitude = None
    weatherDayTime = None

    def from_json(self, js):
        self.city = js["city"]
        self.latitude = js["latitude"]
        self.longitude = js["longitude"]


class Client(HomeMaticIPObject.HomeMaticIPObject):
    id = None
    label = None
    weatherDayTime = None

    def from_json(self, js):
        self.id = js["id"]
        self.label = js["label"]
        self.homeId = js["homeId"]


class Home(HomeMaticIPObject.HomeMaticIPObject):
    """this class represents the 'Home' of the homematic ip"""
    devices = None
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

    def get_current_state(self):
        state = self._restCall('home/getCurrentState', json.dumps(homematicip.get_clientCharacteristics()))
        json_state = json.loads(state)
        js_home = json_state["home"]

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

        self.devices = self.get_devices(json_state)
        self.clients = self.get_clients(json_state)

    def get_devices(self, json_state):
        ret = []
        data = json_state
        for k in data["devices"]:
            device = data["devices"][k]
            deviceType = device["type"]
            if _typeClassMap.has_key(deviceType):
                d = _typeClassMap[deviceType]()
                d.from_json(device)
                ret.append(d)
            else:
                print "There is no class for {} yet".format(deviceType)
        return ret

    def get_clients(self, json_state):
        ret = []
        data = json_state
        for k in data["clients"]:
            client = data["clients"][k]
            c = Client()
            c.from_json(client)
            ret.append(c)
        return ret

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
        data = {"endtime": endtime.strftime("%Y_%m_%d %H:%M")}
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
        data = { "pin" : newPin }
        headers = self.headers
        if oldPin:
            headers["PIN"] = oldPin
        result = requests.post('{}/hmip/home/setPin'.format(homematicip.get_urlREST()), data=json.dumps(data), headers=headers)
        return result.text
