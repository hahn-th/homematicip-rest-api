import homematicip
from homematicip.device import *
import config

homematicip.init(config.ACCESS_POINT,False)
homematicip.set_auth_token(config.AUTH_TOKEN)

home=homematicip.Home()
home.get_current_state()
for d in home.devices:
  print unicode(d)

