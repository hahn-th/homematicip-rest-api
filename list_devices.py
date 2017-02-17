import config
import logging

import homematicip

def create_logger():
  logger = logging.getLogger()
  logger.setLevel(config.LOGGING_LEVEL)
  handler = logging.handlers.TimedRotatingFileHandler(config.LOGGING_FILENAME, when='midnight', backupCount=5) if config.LOGGING_FILENAME else logging.StreamHandler()
  handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
  logger.addHandler(handler)
  return logger

logger = create_logger();

homematicip.init(config.ACCESS_POINT, False)
homematicip.set_auth_token(config.AUTH_TOKEN)

home = homematicip.Home()
home.get_current_state()
for d in home.devices:
    print unicode(d)
