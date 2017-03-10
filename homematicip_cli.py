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
    group.add_argument("--list-firmware", action="store_true", dest="list_firmware", help="list the firmware of all devices")
    

    parser.add_argument("--list-security-journal", action="store_true", dest="list_security_journal", help="display the security journal")
    parser.add_argument("-d", "--device", dest="device", help="the device you want to modify (see \"Device Settings\")")

    group = parser.add_argument_group("Device Settings")
    group.add_argument("--turn_on", action="store_true", dest="device_switch_state", help="turn the switch on")
    group.add_argument("--turn_off", action="store_false", dest="device_switch_state", help="turn the switch off")
    group.add_argument("--set-label", dest="device_new_label", help="set a new label")
    group.add_argument("--set-display", dest="device_display", action="store", help="set the display mode", choices=["actual","setpoint", "actual_humidity"])
      

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


    if args.list_devices:
        sortedDevices = sorted(home.devices, key=attrgetter('deviceType', 'label'))
        for d in sortedDevices:
            print d.id, unicode(d)

    elif args.list_groups:
        sortedGroups = sorted(home.groups, key=attrgetter('groupType', 'label'))
        for g in sortedGroups:
            print unicode(g)
       
    elif args.list_firmware:
        sortedDevices = sorted(home.devices, key=attrgetter('deviceType', 'label'))
        for d in sortedDevices:
            print unicode(u"{:45s} - Firmware: {:6s} - Available Firmware: {} UpdateState: {}".format(d.label, d.firmwareVersion,
                                                                                      d.availableFirmwareVersion, d.updateState))
    elif args.list_security_journal:
        journal = home.get_security_journal()
        for entry in journal:
            print unicode(entry)
    elif args.device:
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

        if not command_entered:
            parser.print_help()
    else:
        parser.print_help()



if __name__ == "__main__":
    main()