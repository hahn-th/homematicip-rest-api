import config
import logging
from operator import attrgetter


import homematicip

def create_logger():
  logger = logging.getLogger()
  logger.setLevel(config.LOGGING_LEVEL)
  handler = logging.handlers.TimedRotatingFileHandler(config.LOGGING_FILENAME, when='midnight', backupCount=5) if config.LOGGING_FILENAME else logging.StreamHandler()
  handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
  logger.addHandler(handler)
  return logger

logger = create_logger();

homematicip.init(config.ACCESS_POINT)
homematicip.set_auth_token(config.AUTH_TOKEN)

home = homematicip.Home()
journal = home.get_security_journal()
#sort = sorted(home.groups, key=attrgetter('groupType', 'label'))
for g in journal:
    print unicode(g)
