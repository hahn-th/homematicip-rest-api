#!/usr/bin/env python3
import logging
import sys
import time
import re
from argparse import ArgumentParser
from collections import namedtuple
from logging.handlers import TimedRotatingFileHandler

import homematicip
from homematicip.device import *
from homematicip.group import *
from homematicip.rule import *
from homematicip.home import Home

logger = None


def create_logger(level, file_name):
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = TimedRotatingFileHandler(file_name, when='midnight', backupCount=5) if file_name else logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger

def convert_config2ini():
    """converts the old config.py to ./config.ini"""
    try:
        import config
        print('converting config.py to config.ini')
        _config = configparser.ConfigParser()
        _config.add_section("AUTH")
        _config.add_section('LOGGING')
        _config['AUTH'] = { 'AuthToken' : config.AUTH_TOKEN, 'AccessPoint': config.ACCESS_POINT }
        _config.set('LOGGING','Level', str(config.LOGGING_LEVEL))
        _config.set('LOGGING', 'FileName', str(config.LOGGING_FILENAME))
        with open('./config.ini', 'w') as configfile:
            _config.write(configfile)
        os.remove('./config.py')
    except ImportError:
        pass 

def anonymizeConfig(config, pattern, format):
    m = re.findall(pattern, config, flags=re.IGNORECASE)
    if m == None:
        return config
    map = {}
    i = 0
    for s in m:
        if s in map.keys():
            continue
        map[s] = format.format(i)
        i = i + 1

    for k,v in map.items():
        config = config.replace(k,v)
    return config
    


def main():
    parser = ArgumentParser(description="a cli wrapper for the homematicip API")
    parser.add_argument("--config_file", type=str, help="the configuration file. If nothing is specified the script will search for it.")
    parser.add_argument("--debug-level", dest="debug_level", type=int, help="the debug level which should get used(Critical=50, DEBUG=10)")

    group = parser.add_argument_group("Display Configuration")
    group.add_argument("--dump-configuration", action="store_true", dest="dump_config",help="dumps the current configuration from the AP")
    group.add_argument("--anonymize", action="store_true", dest="anonymize",help="used together with --dump-configuration to anonymize the output")
    group.add_argument("--list-devices", action="store_true", dest="list_devices", help="list all devices")
    group.add_argument("--list-groups", action="store_true", dest="list_groups", help="list all groups")
    group.add_argument("--list-group-ids", action="store_true", dest="list_group_ids",help="list all groups and their ids")
    group.add_argument("--list-firmware", action="store_true", dest="list_firmware", help="list the firmware of all devices")
    group.add_argument("--list-rssi", action="store_true", dest="list_rssi", help="list the reception quality of all devices")
    group.add_argument("--list-events", action="store_true", dest="list_events", help="prints all the events")
    group.add_argument("--list-last-status-update", action="store_true", dest="list_last_status_update", help="prints the last status update of all systems")

    parser.add_argument("--list-security-journal", action="store_true", dest="list_security_journal", help="display the security journal")
    parser.add_argument("--list-rules", action="store_true", dest="list_rules", help="display all automation rules")

    parser.add_argument("-d", "--device", dest="device", action='append', 
                        help="the device you want to modify (see \"Device Settings\").\nYou can use * to modify all devices or enter the parameter multiple times to modify more devices")
    parser.add_argument("-g", "--group", dest="group", help="the group you want to modify (see \"Group Settings\")")
    parser.add_argument("-r", "--rule", dest="rules", action='append', 
                        help="the automation you want to modify (see \"Automation Rule Settings\").\nYou can use * to modify all automations or enter the parameter multiple times to modify more automations")

    group = parser.add_argument_group("Device Settings")
    group.add_argument("--turn-on", action="store_true", dest="device_switch_state", help="turn the switch on", default=None)
    group.add_argument("--turn-off", action="store_false", dest="device_switch_state", help="turn the switch off", default=None)
    group.add_argument("--set-shutter-level", action="store", dest="device_shutter_level", help="set shutter to level (0..1)")
    group.add_argument("--set-shutter-stop", action="store_true", dest="device_shutter_stop", help="stop shutter", default=None)
    group.add_argument("--set-label", dest="device_new_label", help="set a new label")
    group.add_argument("--set-display", dest="device_display", action="store", help="set the display mode", choices=["actual", "setpoint", "actual_humidity"])
    group.add_argument("--enable-router-module", action="store_true", dest="device_enable_router_module", help="enables the router module of the device", default=None)
    group.add_argument("--disable-router-module", action="store_false", dest="device_enable_router_module", help="disables the router module of the device", default=None)

    group = parser.add_argument_group("Home Settings")
    group.add_argument("--set-protection-mode", dest="protectionmode", action="store", help="set the protection mode", choices=["presence", "absence", "disable"])
    group.add_argument("--set-pin", dest="new_pin", action="store", help="set a new pin")
    group.add_argument("--delete-pin", dest="delete_pin", action="store_true", help="deletes the pin")
    group.add_argument("--old-pin", dest="old_pin", action="store", help="the current pin. used together with --set-pin or --delete-pin", default=None)
    group.add_argument("--set-zones-device-assignment", dest="set_zones_device_assignment", action="store_true", help="sets the zones devices assignment")
    group.add_argument("--external-devices", dest="external_devices", nargs='+', help="sets the devices for the external zone")
    group.add_argument("--internal-devices", dest="internal_devices", nargs='+', help="sets the devices for the internal zone")
    group.add_argument("--activate-absence", dest="activate_absence", action="store", help="activates absence for provided amount of minutes", default=None, type=int)
    group.add_argument("--deactivate-absence", action="store_true", dest="deactivate_absence", help="deactivates absence")

    group = parser.add_argument_group("Group Settings")
    group.add_argument("--list-profiles", dest="group_list_profiles", action="store_true", help="displays all profiles for a group")
    group.add_argument("--activate-profile", dest="group_activate_profile", help="activates a profile by using its index or its name")
    group.add_argument("--set-group-shutter-level", action="store", dest="group_shutter_level", help="set all shutters in group to level (0..1)")
    group.add_argument("--set-group-shutter-stop", action="store_true", dest="group_shutter_stop", help="stop all shutters in group", default=None)
    group.add_argument("--set-point-temperature", action="store", dest="group_set_point_temperature", help="sets the temperature for the given group. The group must be of the type \"HEATING\"", default=None, type=float)

    group.add_argument("--set-boost", action="store_true", dest="group_boost", help="activates the boost mode for a HEATING group", default=None)
    group.add_argument("--set-boost-stop", action="store_false", dest="group_boost", help="deactivates the boost mode for a HEATING group", default=None)

    group = parser.add_argument_group("Automation Rule Settings")
    group.add_argument("--enable-rule", action="store_true", dest="rule_activation", help="activates the automation rules", default=None)
    group.add_argument("--disable-rule", action="store_false", dest="rule_activation", help="deactivates the automation rules", default=None)

    if len(sys.argv) == 1:
        parser.print_help()
        return

    try:
        args = parser.parse_args()
    except:
        print('could not parse arguments')
        parser.print_help()
        return

    _config = None

    if args.config_file:
        try:
            _config = homematicip.load_config_file(args.config_file)
        except FileNotFoundError:
            print("##### CONFIG FILE NOT FOUND: {} #####".format(args.config_file))
            return
    else:
        convert_config2ini()
        _config = homematicip.find_and_load_config_file()


    if _config is None:
        print("Could not find configuration file. Script will exit")
        return

    global logger
    logger = create_logger(args.debug_level if args.debug_level else _config.log_level, _config.log_file)


    home = Home()
    home.set_auth_token(_config.auth_token)
    home.init(_config.access_point)

    command_entered = False

    if args.dump_config:
        command_entered = True
        json_state = home.download_configuration()
        if "errorCode" in json_state:
            logger.error("Could not get the current configuration. Error: %s",json_state["errorCode"])
        else:
            c = json.dumps(json_state, indent=4, sort_keys=True)
            if args.anonymize:
                # generate dummy guids
                c = anonymizeConfig(c,'[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}','00000000-0000-0000-0000-{0:0>12}')
                #generate dummy SGTIN
                c = anonymizeConfig(c,'3014F711[A-Z0-9]{16}','3014F711{0:0>16}')
                #remove refresh Token
                c = anonymizeConfig(c,'"refreshToken": ?"[^"]+"','"refreshToken": null')
                #location
                c = anonymizeConfig(c,'"city": ?"[^"]+"','"city": "1010, Vienna, Austria"')
                c = anonymizeConfig(c,'"latitude": ?"[^"]+"','"latitude": "48.208088"')
                c = anonymizeConfig(c,'"longitude": ?"[^"]+"','"longitude": "16.358608"')

            print(c)


    if not home.get_current_state():
        return

    if args.list_devices:
        command_entered = True
        sortedDevices = sorted(home.devices, key=attrgetter('deviceType', 'label'))
        for d in sortedDevices:
            print('{} {}'.format(d.id, str(d)))

    if args.list_groups:
        command_entered = True
        sortedGroups = sorted(home.groups, key=attrgetter('groupType', 'label'))
        for g in sortedGroups:
            print(g)

    if args.list_last_status_update:
        command_entered = True
        print('Devices:')
        sortedDevices = sorted(home.devices, key=attrgetter('deviceType', 'label'))
        for d in sortedDevices:
            print('\t{}\t{}\t{}'.format(d.id, d.label, d.lastStatusUpdate))
        print('Groups:')
        sortedGroups = sorted(home.groups, key=attrgetter('groupType', 'label'))
        for g in sortedGroups:
            print('\t{}\t{}\t{}'.format(g.groupType, g.label, g.lastStatusUpdate))

    if args.list_group_ids:
        command_entered = True
        sortedGroups = sorted(home.groups, key=attrgetter('groupType', 'label'))
        for g in sortedGroups:
            print("Id: {} - Type: {} - Label: {}".format(g.id, g.groupType, g.label))

    if args.protectionmode:
        command_entered = True
        if args.protectionmode == "presence":
            home.set_security_zones_activation(False, True)
        elif args.protectionmode == "absence":
            home.set_security_zones_activation(True, True)
        elif args.protectionmode == "disable":
            home.set_security_zones_activation(False, False)

    if args.new_pin:
        command_entered = True
        home.set_pin(args.new_pin, args.old_pin)
    if args.delete_pin:
        command_entered = True
        home.set_pin(None, args.old_pin)

    if args.list_security_journal:
        command_entered = True
        journal = home.get_security_journal()
        for entry in journal:
            print(entry)

    if args.list_firmware:
        command_entered = True
        print("{:45s} - Firmware: {:6} - Available Firmware: {:6} UpdateState: {}".format("HmIP AccessPoint",
                                                                                              home.currentAPVersion if home.currentAPVersion is not None else "None",
                                                                                              home.availableAPVersion if home.availableAPVersion is not None else "None",
                                                                                              home.updateState))
        sortedDevices = sorted(home.devices, key=attrgetter('deviceType', 'label'))
        for d in sortedDevices:
            print("{:45s} - Firmware: {:6} - Available Firmware: {:6} UpdateState: {}".format(d.label, d.firmwareVersion,
                                                                                            d.availableFirmwareVersion if d.availableFirmwareVersion is not None else "None",
                                                                                            d.updateState))

    if args.list_rssi:
        command_entered = True

        print("{:45s} - Duty cycle: {:2}".format("HmIP AccessPoint",
                                                     home.dutyCycle if home.dutyCycle is not None else "None"))

        sortedDevices = sorted(home.devices, key=attrgetter('deviceType', 'label'))
        for d in sortedDevices:
            print("{:45s} - RSSI: {:4} {} - Peer RSSI: {:4} - {} {}".format(d.label,
                                                                                d.rssiDeviceValue if d.rssiDeviceValue is not None else "None",
                                                                                getRssiBarString(d.rssiDeviceValue),
                                                                                d.rssiPeerValue if d.rssiPeerValue is not None else "None",
                                                                                getRssiBarString(d.rssiPeerValue),
                                                                                "Unreachable" if d.unreach else ""))
    if args.list_rules:
        command_entered = True
        sortedRules = sorted(home.rules, key=attrgetter('ruleType', 'label'))
        for d in sortedRules:
            print('{} {}'.format(d.id, str(d)))

    if args.device:
        command_entered = False
        devices = []
        for argdevice in args.device:
            if argdevice == '*':
                devices = home.devices
                break
            else:
                d = home.search_device_by_id(argdevice)
                if d == None:
                    logger.error("Could not find device %s", argdevice)
                else:
                    devices.append(d)

        for device in devices:

            if args.device_new_label:
                device.set_label(args.device_new_label)
                command_entered = True
            if args.device_switch_state != None:
                if isinstance(device, Switch):
                    device.set_switch_state(args.device_switch_state)
                    command_entered = True
                else:
                    logger.error("can't turn on/off device %s of type %s", device.id, device.deviceType)

            if args.device_shutter_level is not None:
                if isinstance(device, FullFlushShutter):
                    device.set_shutter_level(args.device_shutter_level)
                    command_entered = True
                else:
                    logger.error("can't set shutter level of device %s of type %s", device.id, device.deviceType)

            if args.device_shutter_stop is not None:
                if isinstance(device, FullFlushShutter):
                    device.set_shutter_stop()
                    command_entered = True
                else:
                    logger.error("can't stop shutter of device %s of type %s", device.id, device.deviceType)

            if args.device_display != None:
                if isinstance(device, TemperatureHumiditySensorDisplay):
                    device.set_display(args.device_display.upper())
                    command_entered = True
                else:
                    logger.error("can't set display of device %s of type %s", device.id, device.deviceType)

            if args.device_enable_router_module != None:
                if device.routerModuleSupported:
                    device.set_router_module_enabled(args.device_enable_router_module)
                    print("{} the router module for device {}". format("Enabled" if args.device_enable_router_module else "Disabled", device.id))
                    command_entered = True
                else:
                    logger.error("the device %s doesn't support the router module", device.id)

    if args.set_zones_device_assignment:
        internal = []
        external = []
        error = False
        command_entered = True
        for id in args.external_devices:
            d = home.search_device_by_id(id)
            if d == None:
                logger.error("Device %s is not registered on this Access Point",id)
                error = True
            else:
                external.append(d)

        for id in args.internal_devices:
            d = home.search_device_by_id(id)
            if d == None:
                logger.error("Device %s is not registered on this Access Point",id)
                error = True
            else:
                internal.append(d)
        if not error:
            home.set_zones_device_assignment(internal, external)

    if args.activate_absence:
        command_entered = True
        home.activate_absence_with_duration(args.activate_absence)

    if args.deactivate_absence:
        command_entered = True
        home.deactivate_absence()

    if args.group:
        command_entered = False
        group = None
        for g in home.groups:
            if g.id == args.group:
                group = g
                break
        if group == None:
            logger.error("Could not find group %s",args.group)
            return

        if args.group_list_profiles:
            command_entered = True
            for p in group.profiles:
                isActive = p.id == group.activeProfile.id
                print("Index: {} - Id: {} - Name: {} - Active: {}".format(p.index, p.id, p.name, isActive))

        if args.group_shutter_level:
            command_entered = True
            group.set_shutter_level(args.group_shutter_level)

        if args.group_shutter_stop:
            command_entered = True
            group.set_shutter_stop()

        if args.group_set_point_temperature:
            command_entered = True
            if isinstance(group, HeatingGroup):
                group.set_point_temperature(args.group_set_point_temperature)
            else:
                logger.error("Group %s isn't a HEATING group", g.id)

        if args.group_activate_profile:
            command_entered = True
            if isinstance(group, HeatingGroup):
                index = args.group_activate_profile
                for p in group.profiles:
                    if p.name == args.group_activate_profile:
                        index = p.index
                        break
                group.set_active_profile(index)
            else:
                logger.error("Group %s isn't a HEATING group", g.id)

        if args.group_boost is not None:
            command_entered = True
            if isinstance(group, HeatingGroup):
                group.set_boost(args.group_boost)
            else:
                logger.error("Group %s isn't a HEATING group", g.id)



    if args.rules:
        command_entered = False
        rules = []
        for argrule in args.rules:
            if argrule == '*':
                rules = home.rules
                break
            else:
                r = home.search_rule_by_id(argrule)
                if r == None:
                    logger.error("Could not find automation rule %s", argrule)
                else:
                    rules.append(r)

        for rule in rules:
             if args.rule_activation != None:
                if isinstance(rule, SimpleRule):
                    rule.set_rule_enabled_state(args.rule_activation)
                    command_entered = True  
                else:
                    logger.error("can't enable/disable rule %s of type %s", rule.id, rule.ruleType)         



    if args.list_events:
        command_entered = True
        home.onEvent += printEvents
        home.enable_events()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            return

    if not command_entered:
        parser.print_help()


def printEvents(eventList):
    for event in eventList:
        print("EventType: {} Data: {}".format(event["eventType"], event["data"]))


def getRssiBarString(rssiValue):
    # Observerd values: -93..-47
    width = 10
    dots = 0
    if rssiValue:
        dots = int(round((100 + rssiValue) / 5))
        dots = max(0, min(width, dots))

    return "[{}{}]".format('*' * dots, '_' * (width - dots))


if __name__ == "__main__":
    main()

