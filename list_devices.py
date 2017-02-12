import homematicip
from homematicip.device import *
import config

homematicip.init(config.ACCESS_POINT)
homematicip.set_auth_token(config.AUTH_TOKEN)

home=homematicip.Home()
home.get_current_state()
for d in home.devices:
  if type(d) is HeatingThermostat:
    print d.label, "valvestate=", d.valvePosition
  if type(d) is ShutterContact:
    print d.label, "open=", d.open
  if type(d) is WallMountedThermostatPro:
    print d.label, "actualtemperature=", d.actualTemperature

