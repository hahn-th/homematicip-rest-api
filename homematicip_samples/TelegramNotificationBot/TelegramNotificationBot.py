#!/usr/bin/env python3
import logging

import homematicip
from homematicip.home import Home
config = homematicip.find_and_load_config_file()

from telegram.ext import Updater, CommandHandler
from telegram import Bot, ParseMode

TG_TOKEN = None
TG_BOT = None
TG_USERS = []
logger = None

HMIP_Home = Home()

def create_logger(level, file_name):
    logger = logging.getLogger()
    logger.setLevel(level)
    handler = TimedRotatingFileHandler(file_name, when='midnight', backupCount=5) if file_name else logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger

### TELEGRAM COMMAND HANDLERS ###

def tg_start_handler(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text="Your UserID is {}".format(update.message.chat_id))

def tg_send_notifications(msg):
    global TG_USERS
    global TG_BOT
    for user in TG_USERS:
        TG_BOT.send_message(user,msg,parse_mode=ParseMode.MARKDOWN)

### HMIP Event Handlers ###
def hmip_events(eventList):
    for event in eventList:
        print("EventType: {} Data: {}".format(event["eventType"], event["data"]))
        eventType = event["eventType"]
        if eventType == 'GROUP_CHANGED':
            group = event["data"]
            if isinstance(group, homematicip.group.SecurityGroup):
                send = False
                forceSend = False
                msg = "Security Breach:\nRoom {}\n".format(group.label)
                if group.windowState == 'OPEN':
                    msg += "Windows are OPEN\n"
                    send = True
                if group.sabotage:
                    msg += "Sabotage on one of the devices\n"
                    send = True
                if group.motionDetected:
                    msg += "Motion Detected: {}\n".format(group.motionDetected)
                    send = True
                if group.smokeDetectorAlarmType and group.smokeDetectorAlarmType != 'IDLE_OFF':
                    msg += "SMOKE ALARM: {}\n".format(group.smokeDetectorAlarmType)
                    forceSend = True

                if forceSend or (send and True in HMIP_Home.get_security_zones_activation()):
                    tg_send_notifications(msg)

### MAIN ###

def main():
    if config is None:
        print("COULD NOT DETECT CONFIG FILE")
        return

    global logger
    logger = create_logger(config.log_level, config.log_file)

    global HMIP_Home

    HMIP_Home.set_auth_token(config.auth_token)
    HMIP_Home.init(config.access_point)

    HMIP_Home.get_current_state()
    HMIP_Home.onEvent += hmip_events

    global TG_TOKEN
    if TG_TOKEN is None:
        TG_TOKEN = config.raw_config['TELEGRAM']['apitoken']

    global TG_BOT
    TG_BOT = Bot(token = TG_TOKEN)
    global TG_USERS
    TG_USERS = str(config.raw_config['TELEGRAM']['contact_users']).split(';')

    tg_updater = Updater(token=TG_TOKEN)
    dispatcher = tg_updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', tg_start_handler))

    tg_updater.start_polling()
    HMIP_Home.enable_events()
    tg_updater.idle()
    HMIP_Home.disable_events()

if __name__ == "__main__":
    main()