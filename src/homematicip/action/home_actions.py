import json
from datetime import datetime

from homematicip.action.action import Action
from homematicip.action.registry import ActionTarget
from homematicip.connection.rest_connection import RestConnection
from homematicip.model.model import Model


async def action_set_security_zones_activation(rest_connection: RestConnection, internal: bool = True,
                                               external: bool = True):
    """this function will set the alarm system to armed or disable it

    Examples:
    arming while being at home:
    > home.set_security_zones_activation(False,True)

    arming without being at home
    > home.set_security_zones_activation(True,True)

    disarming the alarm system
    > home.set_security_zones_activation(False,False)

    :param rest_connection: the rest connection
    :param internal: activates/deactivates the internal zone
    :param external: activates/deactivates the external zone
    """
    data = {"zonesActivation": {"EXTERNAL": external, "INTERNAL": internal}}
    return await rest_connection.async_post("home/security/setZonesActivation", data)


@Action.target_type(ActionTarget.HOME)
def get_security_zones_activation(model: Model) -> (bool, bool):
    """returns the value of the security zones if they are armed or not.

    :return: internal, external - True if the zone is armed
    """
    internal_active: bool = False
    external_active: bool = False

    security_zones = [g for g in model.groups.values() if g.type == "SECURITY_ZONE"]
    for g in security_zones:
        if g.label == "EXTERNAL":
            external_active = g.active
        elif g.label == "INTERNAL":
            internal_active = g.active
    return internal_active, external_active


async def action_set_silent_alarm(rest_connection: RestConnection, internal: bool = True, external: bool = True):
    """this function will set the silent alarm for interal or external

    :param rest_connection: the rest connection
    :param internal: activates/deactivates the silent alarm for internal zone
    :param external: activates/deactivates the silent alarm for the external zone
    """
    data = {"zonesSilentAlarm": {"EXTERNAL": external, "INTERNAL": internal}}
    return rest_connection.async_post("home/security/setZonesSilentAlarm", data)


async def action_set_location(rest_connection: RestConnection, city, latitude, longitude):
    """sets the location of the home

    :param rest_connection: the rest connection
    :param city: the city
    :param latitude: the latitude
    :param longitude: the longitude
    """
    data = {"city": city, "latitude": latitude, "longitude": longitude}
    return await rest_connection.async_post("home/setLocation", data)


async def action_set_intrusion_alert_through_smoke_detectors(rest_connection: RestConnection, activate: bool = True):
    """activate or deactivate if smoke detectors should "ring" during an alarm

    :param rest_connection: the rest connection
    :param activate: True will let the smoke detectors "ring" during an alarm
    """
    data = {"intrusionAlertThroughSmokeDetectors": activate}
    return await rest_connection.async_post(
        "home/security/setIntrusionAlertThroughSmokeDetectors", data
    )


async def action_activate_absence_with_period(rest_connection: RestConnection, endtime: datetime):
    """activates the absence mode until the given time

    :param rest_connection: the rest connection
    :param endtime: the time when the absence should automatically be disabled
    """
    data = {"endTime": endtime.strftime("%Y_%m_%d %H:%M")}
    return await rest_connection.async_post(
        "home/heating/activateAbsenceWithPeriod", data
    )


async def action_activate_absence_permanent(rest_connection: RestConnection):
    """activates the absence forever

    :param rest_connection: the rest connection
    """
    return await rest_connection.async_post("home/heating/activateAbsencePermanent")


async def action_activate_absence_with_duration(rest_connection: RestConnection, duration: int):
    """activates the absence mode for a given time

    :param rest_connection: the rest connection
    :param duration: the absence duration in minutes
    """
    data = {"duration": duration}
    return await rest_connection.async_post(
        "home/heating/activateAbsenceWithDuration", data
    )


async def action_deactivate_absence(rest_connection: RestConnection):
    """deactivates the absence mode immediately"""
    return await rest_connection.async_post("home/heating/deactivateAbsence")


async def action_activate_vacation(rest_connection: RestConnection, endtime: datetime, temperature: float):
    """activates the vatation mode until the given time

    :param rest_connection: the rest connection
    :param endtime: the time when the vatation mode should automatically be disabled
    :param temperature: the settemperature during the vacation mode
    """
    data = {
        "endTime": endtime.strftime("%Y_%m_%d %H:%M"),
        "temperature": temperature,
    }
    return await rest_connection.async_post("home/heating/activateVacation", data)


async def action_deactivate_vacation(rest_connection: RestConnection):
    """deactivates the vacation mode immediately"""
    return await rest_connection.async_post("home/heating/deactivateVacation")


#
# async def action_set_pin(rest_connection: RestConnection, newPin: str, oldPin: str = None) -> dict:
#     """sets a new pin for the home
#
#     :param rest_connection: the rest connection
#     :param newPin: the new pin
#     :param oldPin: optional, if there is currently a pin active it must be given here.
#                     Otherwise it will not be possible to set the new pin
#     """
#     if newPin is None:
#         newPin = ""
#     data = {"pin": newPin}
#     if oldPin:
#         self._connection.headers["PIN"] = str(oldPin)
#     result = await rest_connection.async_post("home/setPin", data)
#     if oldPin:
#         del self._connection.headers["PIN"]
#     return result


async def action_set_zone_activation_delay(rest_connection: RestConnection, delay):
    """sets the delay for the zone activation

    :param rest_connection: the rest connection
    :param delay: the delay in seconds
    """
    data = {"zoneActivationDelay": delay}
    return await rest_connection.async_post(
        "home/security/setZoneActivationDelay", data
    )


# async def action_get_security_journal(rest_connection: RestConnection):
#     journal = self._rest_call("home/security/getSecurityJournal")
#     if "errorCode" in journal:
#         LOGGER.error(
#             "Could not get the security journal. Error: %s", journal["errorCode"]
#         )
#         return None
#     ret = []
#     for entry in journal["entries"]:
#         try:
#             eventType = SecurityEventType(entry["eventType"])
#             if eventType in self._typeSecurityEventMap:
#                 j = self._typeSecurityEventMap[eventType](self._connection)
#         except:
#             j = SecurityEvent(self._connection)
#             LOGGER.warning("There is no class for %s yet", entry["eventType"])
#
#         j.from_json(entry)
#         ret.append(j)
#
#     return ret


async def action_set_timezone(rest_connection: RestConnection, timezone: str):
    """sets the timezone for the AP. e.g. "Europe/Berlin"
    Args:
        timezone(str): the new timezone
    """
    data = {"timezoneId": timezone}
    return await rest_connection.async_post("home/setTimezone", data)


async def action_set_powermeter_unit_price(rest_connection: RestConnection, price):
    data = {"powerMeterUnitPrice": price}
    return await rest_connection.async_post("home/setPowerMeterUnitPrice", data)


async def action_set_zones_device_assignment(rest_connection: RestConnection, internal_devices,
                                             external_devices) -> dict:
    """sets the devices for the security zones

    :param rest_connection: the rest connection
    :param internal_devices: the devices which should be used for the internal zone
    :param external_devices: the devices which should be used for the external(hull) zone
    """
    internal = [x.id for x in internal_devices]
    external = [x.id for x in external_devices]
    data = {"zonesDeviceAssignment": {"INTERNAL": internal, "EXTERNAL": external}}
    result = await rest_connection.async_post(
        "home/security/setZonesDeviceAssignment", data
    )

    if result.json:
        return json.dump(result.json)

    return {}


async def action_start_inclusion(rest_connection: RestConnection, deviceId):
    """start inclusion mode for specific device
    Args:
        deviceId: sgtin of device
    """
    data = {"deviceId": deviceId}
    return await rest_connection.async_post("home/startInclusionModeForDevice", data)
