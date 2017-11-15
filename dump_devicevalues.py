# coding=utf-8
import os.path

import config
import homematicip
from homematicip.home import Home

home = Home()
home.init(config.ACCESS_POINT)
home.set_auth_token(config.AUTH_TOKEN)

home.get_current_state()


def write_shutter(device):
    if not os.path.isfile("shutter.csv"):
        with open("shutter.csv", "w") as csv:
            csv.write("name;timestamp;open/close\n")
    with open("shutter.csv", "a") as csv:
        csv.write("{};{};{}\n".format(device.id, str(device.lastStatusUpdate), d.windowState))


def write_heatingthermostat(device):
    if not os.path.isfile("heatingthermostat.csv"):
        with open("heatingthermostat.csv", "w") as csv:
            csv.write("name;timestamp;valveposition\n")
    with open("heatingthermostat.csv", "a") as csv:
        csv.write("{};{};{}\n".format(device.id, str(device.lastStatusUpdate), d.valvePosition))


def write_plugableswitchmeasuring(device):
    if not os.path.isfile("plugableswitchmeasuring.csv"):
        with open("plugableswitchmeasuring.csv", "w") as csv:
            csv.write("name;timestamp;on;currentPowerConsumption;energyCounter\n")
    with open("plugableswitchmeasuring.csv", "a") as csv:
        csv.write(
            "{};{};{};{};{}\n".format(device.id, str(device.lastStatusUpdate), d.on, d.currentPowerConsumption,
                                      d.energyCounter))


def write_wallmountedthermostatpro(device):
    if not os.path.isfile("wallmountedthermostatpro.csv"):
        with open("wallmountedthermostatpro.csv", "w") as csv:
            csv.write("name;timestamp;humidity;actualTemperature\n")
    with open("wallmountedthermostatpro.csv", "a") as csv:
        csv.write(
            "{};{};{}%;{}°C\n".format(device.id, str(device.lastStatusUpdate), d.humidity, d.actualTemperature))


for d in home.devices:
    if isinstance(d, homematicip.device.ShutterContact):
        write_shutter(d)
    elif isinstance(d, homematicip.device.HeatingThermostat):
        write_heatingthermostat(d)
    elif isinstance(d, homematicip.device.PlugableSwitchMeasuring):
        write_plugableswitchmeasuring(d)
    elif isinstance(d, homematicip.device.WallMountedThermostatPro) or isinstance(d, homematicip.device.TemperatureHumiditySensorDisplay):
        write_wallmountedthermostatpro(d)
