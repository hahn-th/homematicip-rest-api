from operator import attrgetter

import config

import homematicip

homematicip.init(config.ACCESS_POINT, False)
homematicip.set_auth_token(config.AUTH_TOKEN)

home = homematicip.Home()
home.get_current_state()
sortedDevices = sorted(home.devices, key=attrgetter('deviceType', 'label'))

for d in sortedDevices:
    print unicode(u"{:45s} - Firmware: {:6s} - Available Firmware: {}".format(d.label, d.firmwareVersion,
                                                                              d.availableFirmwareVersion))
