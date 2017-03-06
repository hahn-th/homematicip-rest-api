import config
import logging
from operator import attrgetter
from optparse import OptionParser, OptionGroup
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
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("", "--debug-level", dest="debug_level", type="int", default=30, help="the debug level which should get used(Critical=50, DEBUG=10)")

    group = OptionGroup(parser,"Display Configuration")
    group.add_option("", "--list-devices", action="store_true", dest="list_devices", help="list all devices")
    group.add_option("", "--list-groups", action="store_true", dest="list_groups", help="list all groups")
    group.add_option("", "--list-firmware", action="store_true", dest="list_firmware", help="list the firmware of all devices")
    parser.add_option_group(group)

    parser.add_option("", "--list-security-journal", action="store_true", dest="list_security_journal", help="display the security journal")
    group.add_option("-d", "--device", dest="device", help="the device you want to modify (see \"Device Settings\")")

    group = OptionGroup(parser,"Device Settings")
    group.add_option("", "--turn_on", action="store_true", dest="device_switch_state", help="turn the switch on")
    group.add_option("", "--turn_off", action="store_false", dest="device_switch_state", help="turn the switch off")
    group.add_option("", "--set-label", dest="device_new_label", help="set a new label")
    group.add_option("", "--set-display", dest="device_display", type="choice", action="store", help="set the display mode", choices=["actual","setpoint", "actual_humidity"])
    parser.add_option_group(group)   

    if len(sys.argv) == 1:
        parser.print_help()
        return

    (options, args) = parser.parse_args()

    logger.setLevel(options.debug_level)

    homematicip.init(config.ACCESS_POINT)
    homematicip.set_auth_token(config.AUTH_TOKEN)

    home = homematicip.Home()
    home.get_current_state()


    if options.list_devices:
        sortedDevices = sorted(home.devices, key=attrgetter('deviceType', 'label'))
        for d in sortedDevices:
            print d.id, unicode(d)

    elif options.list_groups:
        sortedGroups = sorted(home.groups, key=attrgetter('groupType', 'label'))
        for g in sortedGroups:
            print unicode(g)
       
    elif options.list_firmware:
        sortedDevices = sorted(home.devices, key=attrgetter('deviceType', 'label'))
        for d in sortedDevices:
            print unicode(u"{:45s} - Firmware: {:6s} - Available Firmware: {} UpdateState: {}".format(d.label, d.firmwareVersion,
                                                                                      d.availableFirmwareVersion, d.updateState))
    elif options.list_security_journal:
        journal = home.get_security_journal()
        for entry in journal:
            print unicode(entry)
    elif options.device:
        device = None
        for d in home.devices:
            if d.id == options.device:
                device = d
                break
        if device == None:
            logger.error("Could not find device {}".format(options.device))
            return

        if options.device_new_label:
            device.set_label(options.device_new_label)
        if options.device_switch_state != None:
            if isinstance(device, homematicip.PlugableSwitch):
                device.set_switch_state(options.device_switch_state)
            else:
                logger.error("can't turn on/off device {} of type {}".format(device.id,device.deviceType))

        if options.device_display != None:
            if isinstance(device, homematicip.TemperatureHumiditySensorDisplay):
                device.set_display(options.device_display.upper())
            else:
                logger.error("can't set display of device {} of type {}".format(device.id,device.deviceType))

        else:
            parser.print_help()
    else:
        parser.print_help()



if __name__ == "__main__":
    main()