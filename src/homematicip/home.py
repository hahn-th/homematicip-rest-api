from homematicip.aio.home import AsyncHome
from homematicip.group import *
from homematicip.securityEvent import *

LOGGER = logging.getLogger(__name__)


class Home(AsyncHome):
    """this class represents the 'Home' of the homematic ip"""

    def activate_absence_permanent(self):
        return self._run_non_async(self.activate_absence_permanent_async)

    def activate_absence_with_duration(self, duration: int):
        return self._run_non_async(self.activate_absence_with_duration_async, duration)

    def activate_absence_with_period(self, endtime: datetime):
        return self._run_non_async(self.activate_absence_with_period_async, endtime)

    def activate_vacation(self, endtime: datetime, temperature: float):
        return self._run_non_async(self.activate_vacation_async, endtime, temperature)

    def deactivate_absence(self):
        return self._run_non_async(self.deactivate_absence_async)

    def deactivate_vacation(self):
        return self._run_non_async(self.deactivate_vacation_async)

    def download_configuration(self) -> dict:
        return self._run_non_async(self.download_configuration_async)

    def get_OAuth_OTK(self):
        return self._run_non_async(self.get_OAuth_OTK_async)

    def get_security_journal(self):
        return self._run_non_async(self.get_security_journal_async)

    def set_cooling(self, cooling):
        return self._run_non_async(self.set_cooling_async, cooling)

    def set_intrusion_alert_through_smoke_detectors(self, activate: bool = True):
        return self._run_non_async(self.set_intrusion_alert_through_smoke_detectors_async, activate)

    def set_location(self, city, latitude, longitude):
        return self._run_non_async(self.set_location_async, city, latitude, longitude)

    def set_pin(self, newPin: str, oldPin: str = None) -> dict:
        return self._run_non_async(self.set_pin_async, newPin, oldPin)

    def set_powermeter_unit_price(self, price):
        return self._run_non_async(self.set_powermeter_unit_price_async, price)

    def set_security_zones_activation(self, internal=True, external=True):
        return self._run_non_async(self.set_security_zones_activation_async, internal, external)

    def set_silent_alarm(self, internal=True, external=True):
        return self._run_non_async(self.set_silent_alarm_async, internal, external)

    def set_timezone(self, timezone: str):
        return self._run_non_async(self.set_timezone_async, timezone)

    def set_zone_activation_delay(self, delay):
        return self._run_non_async(self.set_zone_activation_delay_async, delay)

    def start_inclusion(self, deviceId):
        return self._run_non_async(self.start_inclusion_async, deviceId)

    def set_zones_device_assignment(self, internal_devices, external_devices) -> dict:
        return self._run_non_async(self.set_zones_device_assignment_async, internal_devices, external_devices)

    #
    # def _clear_configuration(self):
    #     """Clears all objects from the home"""
    #     self.devices = []
    #     self.clients = []
    #     self.groups = []
    #     self.channels = []
    #
    # def from_json(self, js_home):
    #     super().from_json(js_home)
    #
    #     self.weather = Weather(self._connection)
    #     self.weather.from_json(js_home["weather"])
    #     if js_home["location"] != None:
    #         self.location = Location(self._connection)
    #         self.location.from_json(js_home["location"])
    #
    #     self.connected = js_home["connected"]
    #     self.currentAPVersion = js_home["currentAPVersion"]
    #     self.availableAPVersion = js_home["availableAPVersion"]
    #     self.timeZoneId = js_home["timeZoneId"]
    #     self.pinAssigned = js_home["pinAssigned"]
    #     self.dutyCycle = js_home["dutyCycle"]
    #     self.updateState = HomeUpdateState.from_str(js_home["updateState"])
    #     self.powerMeterUnitPrice = js_home["powerMeterUnitPrice"]
    #     self.powerMeterCurrency = js_home["powerMeterCurrency"]
    #     self.deviceUpdateStrategy = DeviceUpdateStrategy.from_str(
    #         js_home["deviceUpdateStrategy"]
    #     )
    #     self.lastReadyForUpdateTimestamp = js_home["lastReadyForUpdateTimestamp"]
    #     self.apExchangeClientId = js_home["apExchangeClientId"]
    #     self.apExchangeState = ApExchangeState.from_str(js_home["apExchangeState"])
    #     self.id = js_home["id"]
    #     self.carrierSense = js_home["carrierSense"]
    #
    #     for ap, state in js_home["accessPointUpdateStates"].items():
    #         ap_state = AccessPointUpdateState(self._connection)
    #         ap_state.from_json(state)
    #         self.accessPointUpdateStates[ap] = ap_state
    #
    #     self._get_rules(js_home)
    #
    # def on_create(self, handler):
    #     """Adds an event handler to the create method. Fires when a device
    #     is created."""
    #     self._on_create.append(handler)
    #
    # def fire_create_event(self, *args, **kwargs):
    #     """Trigger the method tied to _on_create"""
    #     for _handler in self._on_create:
    #         _handler(*args, **kwargs)
    #
    # def fire_channel_event(self, *args, **kwargs):
    #     """Trigger the method tied to _on_channel_event"""
    #     for _handler in self._on_channel_event:
    #         _handler(*args, **kwargs)
    #
    # def remove_callback(self, handler):
    #     """Remove event handler."""
    #     super().remove_callback(handler)
    #     if handler in self._on_create:
    #         self._on_create.remove(handler)
    #
    # def on_channel_event(self, handler):
    #     """Adds an event handler to the channel event method. Fires when a channel event
    #     is received."""
    #     self._on_channel_event.append(handler)
    #
    # def remove_channel_event_handler(self, handler):
    #     """Remove event handler."""
    #     if handler in self._on_channel_event:
    #         self._on_channel_event.remove(handler)
    #
    # def download_configuration(self) -> dict:
    #     """downloads the current configuration from the cloud
    #
    #     Returns
    #         the downloaded configuration as json
    #     """
    #     if self._connection_context is None:
    #         raise Exception("Home not initialized. Run init() first.")
    #
    #     client_characteristics = ClientCharacteristicsBuilder.get(self._connection_context.accesspoint_id)
    #     result = self._rest_call(
    #         "home/getCurrentState", client_characteristics
    #     )
    #
    #     if not result.success:
    #         raise Exception("Could not get the current configuration. Error: %s", result.status_text)
    #
    #     return result.json
    #
    # def get_current_state(self, clear_config: bool = False):
    #     """downloads the current configuration and parses it into self
    #
    #     Args:
    #         clear_config(bool): if set to true, this function will remove all old objects
    #         from self.devices, self.client, ... to have a fresh config instead of reparsing them
    #     """
    #     json_state = self.download_configuration()
    #     return self.update_home(json_state, clear_config)
    #
    # def update_home(self, json_state, clear_config: bool = False):
    #     """parse a given json configuration into self.
    #     This will update the whole home including devices, clients and groups.
    #
    #     Args:
    #         json_state(dict): the json configuration as dictionary
    #         clear_config(bool): if set to true, this function will remove all old objects
    #         from self.devices, self.client, ... to have a fresh config instead of reparsing them
    #     """
    #
    #     if clear_config:
    #         self._clear_configuration()
    #
    #     self._get_devices(json_state)
    #     self._get_clients(json_state)
    #     self._get_groups(json_state)
    #     self._load_functionalChannels()
    #
    #     js_home = json_state["home"]
    #
    #     return self.update_home_only(js_home, clear_config)
    #
    # def update_home_only(self, js_home, clear_config: bool = False):
    #     """parse a given home json configuration into self.
    #     This will update only the home without updating devices, clients and groups.
    #
    #     Args:
    #         js_home(dict): the json configuration as dictionary
    #         clear_config(bool): if set to true, this function will remove all old objects
    #         from self.devices, self.client, ... to have a fresh config instead of reparsing them
    #     """
    #
    #     if clear_config:
    #         self.rules = []
    #         self.functionalHomes = []
    #
    #     self.from_json(js_home)
    #     self._get_functionalHomes(js_home)
    #
    #     return True
    #
    # def _get_devices(self, json_state):
    #     self.devices = [x for x in self.devices if x.id in json_state["devices"].keys()]
    #     for id_, raw in json_state["devices"].items():
    #         try:
    #             _device = self.search_device_by_id(id_)
    #             if _device:
    #                 _device.from_json(raw)
    #             else:
    #                 self.devices.append(self._parse_device(raw))
    #         except Exception as err:
    #             LOGGER.error(
    #                 f"An exception in _get_devices (device-id {id_}) of type {type(err).__name__} occurred: {err}"
    #             )
    #             return None
    #
    # def _parse_device(self, json_state):
    #     try:
    #         deviceType = DeviceType.from_str(json_state["type"])
    #         d = self._typeClassMap[deviceType](self._connection)
    #         d.from_json(json_state)
    #         return d
    #     except:
    #         d = self._typeClassMap[DeviceType.BASE_DEVICE](self._connection)
    #         d.from_json(json_state)
    #         LOGGER.warning("There is no class for device '%s' yet", json_state["type"])
    #         return d
    #
    # def _get_rules(self, json_state):
    #     self.rules = [
    #         x for x in self.rules if x.id in json_state["ruleMetaDatas"].keys()
    #     ]
    #     for id_, raw in json_state["ruleMetaDatas"].items():
    #         _rule = self.search_rule_by_id(id_)
    #         if _rule:
    #             _rule.from_json(raw)
    #         else:
    #             self.rules.append(self._parse_rule(raw))
    #
    # def _parse_rule(self, json_state):
    #     try:
    #         ruleType = AutomationRuleType.from_str(json_state["type"])
    #         r = self._typeRuleMap[ruleType](self._connection)
    #         r.from_json(json_state)
    #         return r
    #     except:
    #         r = Rule(self._connection)
    #         r.from_json(json_state)
    #         LOGGER.warning("There is no class for rule  '%s' yet", json_state["type"])
    #         return r
    #
    # def _get_clients(self, json_state):
    #     self.clients = [x for x in self.clients if x.id in json_state["clients"].keys()]
    #     for id_, raw in json_state["clients"].items():
    #         _client = self.search_client_by_id(id_)
    #         if _client:
    #             _client.from_json(raw)
    #         else:
    #             c = Client(self._connection)
    #             c.from_json(raw)
    #             self.clients.append(c)
    #
    # def _parse_group(self, json_state):
    #     g = None
    #     if json_state["type"] == "META":
    #         g = MetaGroup(self._connection)
    #         g.from_json(json_state, self.devices, self.groups)
    #     else:
    #         try:
    #             groupType = GroupType.from_str(json_state["type"])
    #             g = self._typeGroupMap[groupType](self._connection)
    #             g.from_json(json_state, self.devices)
    #         except:
    #             g = self._typeGroupMap[GroupType.GROUP](self._connection)
    #             g.from_json(json_state, self.devices)
    #             LOGGER.warning(
    #                 "There is no class for group '%s' yet", json_state["type"]
    #             )
    #     return g
    #
    # def _get_groups(self, json_state):
    #     self.groups = [x for x in self.groups if x.id in json_state["groups"].keys()]
    #     metaGroups = []
    #     for id_, raw in json_state["groups"].items():
    #         _group = self.search_group_by_id(id_)
    #         if _group:
    #             if isinstance(_group, MetaGroup):
    #                 _group.from_json(raw, self.devices, self.groups)
    #             else:
    #                 _group.from_json(raw, self.devices)
    #         else:
    #             group_type = raw["type"]
    #             if group_type == "META":
    #                 metaGroups.append(raw)
    #             else:
    #                 self.groups.append(self._parse_group(raw))
    #     for mg in metaGroups:
    #         self.groups.append(self._parse_group(mg))
    #
    # def _get_functionalHomes(self, json_state):
    #     for solution, functionalHome in json_state["functionalHomes"].items():
    #         try:
    #             solutionType = FunctionalHomeType.from_str(solution)
    #             h = None
    #             for fh in self.functionalHomes:
    #                 if fh.solution == solution:
    #                     h = fh
    #                     break
    #             if h is None:
    #                 h = self._typeFunctionalHomeMap[solutionType](self._connection)
    #                 self.functionalHomes.append(h)
    #             h.from_json(functionalHome, self.groups)
    #         except:
    #             h = FunctionalHome(self._connection)
    #             h.from_json(functionalHome, self.groups)
    #             LOGGER.warning(
    #                 "There is no class for functionalHome '%s' yet", solution
    #             )
    #             self.functionalHomes.append(h)
    #
    # def _load_functionalChannels(self):
    #     for d in self.devices:
    #         d.load_functionalChannels(self.groups, self.channels)
    #
    # def get_functionalHome(self, functionalHomeType: type) -> FunctionalHome:
    #     """gets the specified functionalHome
    #
    #     Args:
    #         functionalHome(type): the type of the functionalHome which should be returned
    #
    #     Returns:
    #         the FunctionalHome or None if it couldn't be found
    #     """
    #     for x in self.functionalHomes:
    #         if isinstance(x, functionalHomeType):
    #             return x
    #
    #     return None
    #
    # def search_device_by_id(self, deviceID) -> Device:
    #     """searches a device by given id
    #
    #     Args:
    #       deviceID(str): the device to search for
    #
    #     Returns
    #       the Device object or None if it couldn't find a device
    #     """
    #     for d in self.devices:
    #         if d.id == deviceID:
    #             return d
    #     return None
    #
    # def search_channel(self, deviceID, channelIndex) -> FunctionalChannel:
    #     """searches a channel by given deviceID and channelIndex"""
    #     foundD = [d for d in self.devices if d.id == deviceID]
    #     d = foundD[0] if foundD else None
    #     if d is not None:
    #         foundC = [ch for ch in d.functionalChannels if ch.index == channelIndex]
    #         return foundC[0] if foundC else None
    #     return None
    #
    # def search_group_by_id(self, groupID) -> Group:
    #     """searches a group by given id
    #
    #     Args:
    #       groupID(str): groupID the group to search for
    #
    #     Returns
    #       the group object or None if it couldn't find a group
    #     """
    #     for g in self.groups:
    #         if g.id == groupID:
    #             return g
    #     return None
    #
    # def search_client_by_id(self, clientID) -> Client:
    #     """searches a client by given id
    #
    #     Args:
    #       clientID(str): the client to search for
    #
    #     Returns
    #       the client object or None if it couldn't find a client
    #     """
    #     for c in self.clients:
    #         if c.id == clientID:
    #             return c
    #     return None
    #
    # def search_rule_by_id(self, ruleID) -> Rule:
    #     """searches a rule by given id
    #
    #     Args:
    #       ruleID(str): the rule to search for
    #
    #     Returns
    #       the rule object or None if it couldn't find a rule
    #     """
    #     for r in self.rules:
    #         if r.id == ruleID:
    #             return r
    #     return None
    #
    # def get_security_zones_activation(self) -> (bool, bool):
    #     """returns the value of the security zones if they are armed or not
    #
    #     Returns
    #         internal
    #           True if the internal zone is armed
    #         external
    #           True if the external zone is armed
    #     """
    #     internal_active = False
    #     external_active = False
    #     for g in self.groups:
    #         if isinstance(g, SecurityZoneGroup):
    #             if g.label == "EXTERNAL":
    #                 external_active = g.active
    #             elif g.label == "INTERNAL":
    #                 internal_active = g.active
    #     return internal_active, external_active
    #
    # def set_security_zones_activation(self, internal=True, external=True):
    #     """this function will set the alarm system to armed or disable it
    #
    #     Args:
    #       internal(bool): activates/deactivates the internal zone
    #       external(bool): activates/deactivates the external zone
    #
    #     Examples:
    #       arming while being at home
    #       home.set_security_zones_activation(False,True)
    #
    #       arming without being at home
    #       home.set_security_zones_activation(True,True)
    #
    #       disarming the alarm system
    #       home.set_security_zones_activation(False,False)
    #     """
    #     data = {"zonesActivation": {"EXTERNAL": external, "INTERNAL": internal}}
    #     return self._rest_call("home/security/setZonesActivation", data)
    #
    # def set_silent_alarm(self, internal=True, external=True):
    #     """this function will set the silent alarm for interal or external
    #
    #     Args:
    #       internal(bool): activates/deactivates the silent alarm for internal zone
    #       external(bool): activates/deactivates the silent alarm for the external zone
    #     """
    #     data = {"zonesSilentAlarm": {"EXTERNAL": external, "INTERNAL": internal}}
    #     return self._rest_call("home/security/setZonesSilentAlarm", json.dumps(data))
    #
    # def set_location(self, city, latitude, longitude):
    #     data = {"city": city, "latitude": latitude, "longitude": longitude}
    #     return self._rest_call("home/setLocation", data)
    #
    # def set_cooling(self, cooling):
    #     data = {"cooling": cooling}
    #     return self._rest_call("home/heating/setCooling", data)
    #
    # def set_intrusion_alert_through_smoke_detectors(self, activate: bool = True):
    #     """activate or deactivate if smoke detectors should "ring" during an alarm
    #
    #     Args:
    #         activate(bool): True will let the smoke detectors "ring" during an alarm
    #     """
    #     data = {"intrusionAlertThroughSmokeDetectors": activate}
    #     return self._rest_call(
    #         "home/security/setIntrusionAlertThroughSmokeDetectors", data
    #     )
    #
    # def activate_absence_with_period(self, endtime: datetime):
    #     """activates the absence mode until the given time
    #
    #     Args:
    #         endtime(datetime): the time when the absence should automatically be disabled
    #     """
    #     data = {"endTime": endtime.strftime("%Y_%m_%d %H:%M")}
    #     return self._rest_call(
    #         "home/heating/activateAbsenceWithPeriod", data
    #     )
    #
    # def activate_absence_permanent(self):
    #     """activates the absence forever"""
    #     return self._rest_call("home/heating/activateAbsencePermanent")
    #
    # def activate_absence_with_duration(self, duration: int):
    #     """activates the absence mode for a given time
    #
    #     Args:
    #         duration(int): the absence duration in minutes
    #     """
    #     data = {"duration": duration}
    #     return self._rest_call(
    #         "home/heating/activateAbsenceWithDuration", data
    #     )
    #
    # def deactivate_absence(self):
    #     """deactivates the absence mode immediately"""
    #     return self._rest_call("home/heating/deactivateAbsence")
    #
    # def activate_vacation(self, endtime: datetime, temperature: float):
    #     """activates the vatation mode until the given time
    #
    #     Args:
    #         endtime(datetime): the time when the vatation mode should automatically be disabled
    #         temperature(float): the settemperature during the vacation mode
    #     """
    #     data = {
    #         "endTime": endtime.strftime("%Y_%m_%d %H:%M"),
    #         "temperature": temperature,
    #     }
    #     return self._rest_call("home/heating/activateVacation", data)
    #
    # def deactivate_vacation(self):
    #     """deactivates the vacation mode immediately"""
    #     return self._rest_call("home/heating/deactivateVacation")
    #
    # def set_pin(self, newPin: str, oldPin: str = None) -> dict:
    #     """sets a new pin for the home
    #
    #     Args:
    #         newPin(str): the new pin
    #         oldPin(str): optional, if there is currently a pin active it must be given here.
    #                     Otherwise it will not be possible to set the new pin
    #
    #     Returns:
    #         the result of the call
    #     """
    #     custom_header = None
    #     if newPin is None:
    #         newPin = ""
    #
    #     if oldPin:
    #         custom_header = {"PIN": str(oldPin)}
    #
    #     result = self._rest_call("home/setPin", body={"pin": newPin}, custom_header=custom_header)
    #
    #     if not result.success:
    #         LOGGER.error("Could not set the pin. Error: %s", result.status_text)
    #
    #     return result.json
    #
    # def set_zone_activation_delay(self, delay):
    #     data = {"zoneActivationDelay": delay}
    #     return self._rest_call(
    #         "home/security/setZoneActivationDelay", body=data
    #     )
    #
    # def get_security_journal(self):
    #     journal = self._rest_call("home/security/getSecurityJournal")
    #
    #     if not journal.success:
    #         LOGGER.error(
    #             "Could not get the security journal. Error: %s", journal.status_text
    #         )
    #         return None
    #     ret = []
    #     for entry in journal.json["entries"]:
    #         journal_entry = None
    #         try:
    #             event_type = SecurityEventType(entry["eventType"])
    #             if event_type in self._typeSecurityEventMap:
    #                 journal_entry = self._typeSecurityEventMap[event_type](self._connection)
    #         except:
    #             journal_entry = SecurityEvent(self._connection)
    #             LOGGER.warning("There is no class for %s yet", entry["eventType"])
    #
    #         if journal_entry is not None:
    #             journal_entry.from_json(entry)
    #             ret.append(journal_entry)
    #
    #     return ret
    #
    # def delete_group(self, group: Group):
    #     """deletes the given group from the cloud
    #
    #     Args:
    #         group(Group):the group to delete
    #     """
    #     return group.delete()
    #
    # def get_OAuth_OTK(self):
    #     token = OAuthOTK(self._connection)
    #     result = self._rest_call("home/getOAuthOTK")
    #     token.from_json(result.json)
    #     return token
    #
    # def set_timezone(self, timezone: str):
    #     """sets the timezone for the AP. e.g. "Europe/Berlin"
    #     Args:
    #         timezone(str): the new timezone
    #     """
    #     data = {"timezoneId": timezone}
    #     return self._rest_call("home/setTimezone", body=data)
    #
    # def set_powermeter_unit_price(self, price):
    #     data = {"powerMeterUnitPrice": price}
    #     return self._rest_call("home/setPowerMeterUnitPrice", body=data)
    #
    # def set_zones_device_assignment(self, internal_devices, external_devices) -> dict:
    #     """sets the devices for the security zones
    #     Args:
    #         internal_devices(List[Device]): the devices which should be used for the internal zone
    #         external_devices(List[Device]):  the devices which should be used for the external(hull) zone
    #
    #     Returns:
    #         the result of _restCall
    #     """
    #     internal = [x.id for x in internal_devices]
    #     external = [x.id for x in external_devices]
    #     data = {"zonesDeviceAssignment": {"INTERNAL": internal, "EXTERNAL": external}}
    #     result = self._rest_call(
    #         "home/security/setZonesDeviceAssignment", body=data
    #     )
    #     return result.json
    #
    # def start_inclusion(self, deviceId):
    #     """start inclusion mode for specific device
    #     Args:
    #         deviceId: sgtin of device
    #     """
    #     data = {"deviceId": deviceId}
    #     return self._rest_call(
    #         "home/startInclusionModeForDevice", body=data
    #     )
    #
    # async def enable_events(self, additional_message_handler: Callable = None):
    #     """Connect to Websocket and listen for events"""
    #     if self._websocket_client and self._websocket_client.is_connected():
    #         return
    #
    #     self._websocket_client = WebSocketHandler()
    #     self._websocket_client.add_on_message_handler(self._ws_on_message)
    #     if additional_message_handler:
    #         self._websocket_client.add_on_message_handler(additional_message_handler)
    #
    #     await self._websocket_client.listen(self._connection_context)
    #
    # def disable_events(self):
    #     """Stop Websocket Connection"""
    #     if self._websocket_client:
    #         self._websocket_client.stop_listening()
    #         self._websocket_client = None
    #
    # async def _ws_on_message(self, message):
    #     LOGGER.debug(message)
    #     js = json.loads(message)
    #     event_list = []
    #     for event in js["events"].values():
    #         try:
    #             pushEventType = EventType(event["pushEventType"])
    #             LOGGER.debug(pushEventType)
    #             obj = None
    #             if pushEventType == EventType.GROUP_CHANGED:
    #                 data = event["group"]
    #                 obj = self.search_group_by_id(data["id"])
    #                 if obj is None:
    #                     obj = self._parse_group(data)
    #                     self.groups.append(obj)
    #                     pushEventType = EventType.GROUP_ADDED
    #                     self.fire_create_event(obj, event_type=pushEventType, obj=obj)
    #                 if type(obj) is MetaGroup:
    #                     obj.from_json(data, self.devices, self.groups)
    #                 else:
    #                     obj.from_json(data, self.devices)
    #                 obj.fire_update_event(data, event_type=pushEventType, obj=obj)
    #             elif pushEventType == EventType.HOME_CHANGED:
    #                 data = event["home"]
    #                 obj = self
    #                 obj.update_home_only(data)
    #                 obj.fire_update_event(data, event_type=pushEventType, obj=obj)
    #             elif pushEventType == EventType.CLIENT_ADDED:
    #                 data = event["client"]
    #                 obj = Client(self._connection)
    #                 obj.from_json(data)
    #                 self.clients.append(obj)
    #             elif pushEventType == EventType.CLIENT_CHANGED:
    #                 data = event["client"]
    #                 obj = self.search_client_by_id(data["id"])
    #                 obj.from_json(data)
    #             elif pushEventType == EventType.CLIENT_REMOVED:
    #                 obj = self.search_client_by_id(event["id"])
    #                 self.clients.remove(obj)
    #             elif pushEventType == EventType.DEVICE_ADDED:
    #                 data = event["device"]
    #                 obj = self._parse_device(data)
    #                 obj.load_functionalChannels(self.groups, self.channels)
    #                 self.devices.append(obj)
    #                 self.fire_create_event(data, event_type=pushEventType, obj=obj)
    #             elif pushEventType == EventType.DEVICE_CHANGED:
    #                 data = event["device"]
    #                 obj = self.search_device_by_id(data["id"])
    #                 if obj is None:  # no DEVICE_ADDED Event?
    #                     obj = self._parse_device(data)
    #                     self.devices.append(obj)
    #                     pushEventType = EventType.DEVICE_ADDED
    #                     self.fire_create_event(data, event_type=pushEventType, obj=obj)
    #                 else:
    #                     obj.from_json(data)
    #                 obj.load_functionalChannels(self.groups, self.channels)
    #                 obj.fire_update_event(data, event_type=pushEventType, obj=obj)
    #             elif pushEventType == EventType.DEVICE_REMOVED:
    #                 obj = self.search_device_by_id(event["id"])
    #                 obj.fire_remove_event(obj, event_type=pushEventType, obj=obj)
    #                 self.devices.remove(obj)
    #             elif pushEventType == EventType.DEVICE_CHANNEL_EVENT:
    #                 channel_event = ChannelEvent(**event)
    #                 self.fire_channel_event(channel_event)
    #             elif pushEventType == EventType.GROUP_REMOVED:
    #                 obj = self.search_group_by_id(event["id"])
    #                 obj.fire_remove_event(obj, event_type=pushEventType, obj=obj)
    #                 self.groups.remove(obj)
    #             elif pushEventType == EventType.GROUP_ADDED:
    #                 group = event["group"]
    #                 obj = self._parse_group(group)
    #                 self.groups.append(obj)
    #                 self.fire_create_event(obj, event_type=pushEventType, obj=obj)
    #             elif pushEventType == EventType.SECURITY_JOURNAL_CHANGED:
    #                 pass  # data is just none so nothing to do here
    #
    #             # TODO: implement INCLUSION_REQUESTED, NONE
    #             event_list.append({"eventType": pushEventType, "data": obj})
    #         except ValueError as valerr:  # pragma: no cover
    #             LOGGER.warning(
    #                 "Uknown EventType '%s' Data: %s", event["pushEventType"], event
    #             )
    #
    #         except Exception as err:  # pragma: no cover
    #             LOGGER.exception(err)
    #     self.onEvent.fire(event_list)
