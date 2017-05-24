import config
import logging
from operator import attrgetter
from argparse import ArgumentParser
import sys
import homematicip

def create_logger():
  logger = logging.getLogger()
  logger.setLevel(config.LOGGING_LEVEL)
  handler = logging.handlers.TimedRotatingFileHandler(config.LOGGING_FILENAME, when='midnight', backupCount=5) if config.LOGGING_FILENAME else logging.StreamHandler()
  handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
  logger.addHandler(handler)
  return logger

logger = create_logger();


def main():
    parser = ArgumentParser(description="a cli wrapper for the homematicip API")
    parser.add_argument("--debug-level", dest="debug_level", type=int, default=30, help="the debug level which should get used(Critical=50, DEBUG=10)")

    group = parser.add_argument_group("Display Configuration")
    group.add_argument("--list-devices", action="store_true", dest="list_devices", help="list all devices")
    group.add_argument("--list-groups", action="store_true", dest="list_groups", help="list all groups")
    group.add_argument("--list-group-ids", action="store_true", dest="list_group_ids", help="list all groups and their ids")
    group.add_argument("--list-firmware", action="store_true", dest="list_firmware", help="list the firmware of all devices")


    parser.add_argument("--list-security-journal", action="store_true", dest="list_security_journal", help="display the security journal")

    parser.add_argument("-d", "--device", dest="device", help="the device you want to modify (see \"Device Settings\")")
    parser.add_argument("-g", "--group", dest="group", help="the group you want to modify (see \"Group Settings\")")
    parser.add_argument("-p", "--profile-index", dest="profile_index", help="the index if the profile you want to modify (see \"Group Settings\")")

    group = parser.add_argument_group("Device Settings")
    group.add_argument("--turn_on", action="store_true", dest="device_switch_state", help="turn the switch on")
    group.add_argument("--turn_off", action="store_false", dest="device_switch_state", help="turn the switch off")
    group.add_argument("--set-label", dest="device_new_label", help="set a new label")
    group.add_argument("--set-display", dest="device_display", action="store", help="set the display mode", choices=["actual","setpoint", "actual_humidity"])

    group = parser.add_argument_group("Home Settings")
    group.add_argument("--set-protection-mode", dest="protectionmode", action="store", help="set the protection mode", choices=["presence","absence", "disable"])
    group.add_argument("--set-pin", dest="new_pin", action="store", help="set a new pin")
    group.add_argument("--delete-pin", dest="delete_pin", action="store_true", help="deletes the pin")
    group.add_argument("--old-pin", dest="old_pin", action="store", help="the current pin. used together with --set-pin or --delete-pin", default=None)
    group.add_argument("--set-zones-device-assignment", dest="set_zones_device_assignment", action="store_true", help="sets the zones devices assignment")
    group.add_argument("--external_devices", dest="external_devices", nargs='+', help="sets the devices for the external zone")
    group.add_argument("--internal_devices", dest="internal_devices", nargs='+', help="sets the devices for the internal zone")
    group.add_argument("--activate-absence", dest="activate_absence", action="store", help="activates absence for provided amount of minutes", default=None, type=int)
    group.add_argument("--deactivate-absence", action="store_true", dest="deactivate_absence", help="deactivates absence")

    group = parser.add_argument_group("Group Settings")
    group.add_argument("--list-profiles", dest="list_profiles", action="store_true", help="displays the all profile for a group")
    group.add_argument("--activate-profile", dest="activate_profile", help="activates a profile by using its index or its name")

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    logger.setLevel(args.debug_level)

    homematicip.init(config.ACCESS_POINT)
    homematicip.set_auth_token(config.AUTH_TOKEN)

    home = homematicip.Home()
    if not home.get_current_state():
        return

    command_entered = False

    if args.list_devices:
        command_entered = True
        sortedDevices = sorted(home.devices, key=attrgetter('deviceType', 'label'))
        for d in sortedDevices:
            print d.id, unicode(d)

    if args.list_groups:
        command_entered = True
        sortedGroups = sorted(home.groups, key=attrgetter('groupType', 'label'))
        for g in sortedGroups:
            print unicode(g)

    if args.list_group_ids:
        command_entered = True
        sortedGroups = sorted(home.groups, key=attrgetter('groupType', 'label'))
        for g in sortedGroups:
            print u"Id: {} - Type: {} - Label: {}".format(g.id, g.groupType, g.label)

    if args.protectionmode:
        command_entered = True
        if args.protectionmode == "presence":
            home.set_security_zones_activation(False,True)
        elif args.protectionmode == "absence":
            home.set_security_zones_activation(True,True)
        elif args.protectionmode == "disable":
            home.set_security_zones_activation(False,False)

    if args.new_pin:
        command_entered = True
        home.set_pin(args.new_pin,args.old_pin)
    if args.delete_pin:
        command_entered = True
        home.set_pin(None,args.old_pin)

    if args.list_security_journal:
        command_entered = True
        journal = home.get_security_journal()
        for entry in journal:
            print unicode(entry)

    if args.list_firmware:
        command_entered = True
        print unicode(u"{:45s} - Firmware: {:6s} - Available Firmware: {:6s} UpdateState: {}".format("HmIP AccessPoint",
                                                                                        home.currentAPVersion,
                                                                                        home.availableAPVersion,
                                                                                        home.updateState))
        sortedDevices = sorted(home.devices, key=attrgetter('deviceType', 'label'))
        for d in sortedDevices:
            print unicode(u"{:45s} - Firmware: {:6s} - Available Firmware: {:6s} UpdateState: {}".format(d.label, d.firmwareVersion,
                                                                                      d.availableFirmwareVersion, d.updateState))

    if args.device:
        command_entered = False
        device = None
        for d in home.devices:
            if d.id == args.device:
                device = d
                break
        if device == None:
            logger.error("Could not find device {}".format(args.device))
            return

        if args.device_new_label:
            device.set_label(args.device_new_label)
            command_entered = True
        if args.device_switch_state != None:
            if isinstance(device, homematicip.PlugableSwitch):
                device.set_switch_state(args.device_switch_state)
                command_entered = True
            else:
                logger.error("can't turn on/off device {} of type {}".format(device.id,device.deviceType))

        if args.device_display != None:
            if isinstance(device, homematicip.TemperatureHumiditySensorDisplay):
                device.set_display(args.device_display.upper())
                command_entered = True
            else:
                logger.error("can't set display of device {} of type {}".format(device.id,device.deviceType))


    if args.set_zones_device_assignment:
        internal = []
        external = []
        error = False
        command_entered = True
        for id in args.external_devices:
            d = home.search_device_by_id(id)
            if d == None:
                logger.error("Device {} is not registered on this Access Point".format(id))
                error = True
            else:
                external.append(d)

        for id in args.internal_devices:
            d = home.search_device_by_id(id)
            if d == None:
                logger.error("Device {} is not registered on this Access Point".format(id))
                error = True
            else:
                internal.append(d)
        if not error:
            home.set_zones_device_assignment(internal,external)


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
            logger.error("Could not find group {}".format(args.group))
            return

        if args.activate_profile:
            command_entered = True
            index = args.activate_profile
            for p in group.profiles:
                if p.name == args.activate_profile:
                    index = p.index
                    break
            group.set_active_profile(index)

        if args.list_profiles:
            command_entered = True
            for p in group.profiles:
                isActive = p.id == group.activeProfile.id
                print u"Index: {} - Id: {} - Name: {} - Active: {}".format(p.index, p.id, p.name, isActive)


    if not command_entered:
        parser.print_help()



if __name__ == "__main__":
    main()
