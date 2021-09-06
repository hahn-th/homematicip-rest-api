
import sys
import homematicip
from homematicip.home import Home
from homematicip.device import ShutterContact,HeatingThermostat,PlugableSwitchMeasuring,WallMountedThermostatPro
from homematicip.device import WaterSensor,TemperatureHumiditySensorDisplay

config = homematicip.find_and_load_config_file()
if config == None:
    print("Cannot find config.ini!")
    sys.exit()
    
home = Home()
home.set_auth_token(config.auth_token)
home.init(config.access_point)

def write_shutter(room,device):
	print(room, " ", device.label, " ", device.lastStatusUpdate, " ", device.rssiDeviceValue, " ", device.windowState)

def write_plugableswitchmeasuring(room,device):
	print(room, " ", device.label, " ", device.lastStatusUpdate, " ", device.rssiDeviceValue, " ", device.currentPowerConsumption, " ", device.energyCounter)

def write_heatingthermostat(room,device):
	print(room, " ", device.label, " ", device.lastStatusUpdate, " ", device.rssiDeviceValue)

def write_wallmountedthermostatpro(room,device):
    print(room, " ", device.label, " ", device.lastStatusUpdate, " ", device.rssiDeviceValue, " ", device.actualTemperature, " ", device.setPointTemperature, " ", device.humidity)

def write_watersensor(room,device):
    print(room, " ", device.label, " ", device.lastStatusUpdate, " ", device.rssiDeviceValue, " ", device.moistureDetected, " ", device.waterlevelDetected, " ", device.incorrectPositioned)

def write_temperaturehumiditysensordisplay(room,device):
    print(room, " ", device.label, " ", device.lastStatusUpdate, " ", device.rssiDeviceValue, " ", device.actualTemperature, " ", device.humidity)
    
def main():
    global home
    home.get_current_state()
    for g in home.groups:
        if g.groupType=="META":
            for d in g.devices:
                if isinstance(d,ShutterContact):
                    write_shutter(g.label,d)
                elif isinstance(d,HeatingThermostat):
                    write_heatingthermostat(g.label,d)
                elif isinstance(d,PlugableSwitchMeasuring):
                    write_plugableswitchmeasuring(g.label,d)
                elif isinstance(d,WallMountedThermostatPro):
                    write_wallmountedthermostatpro(g.label,d)
                elif isinstance(d,WaterSensor):
                    write_watersensor(g.label,d)
                elif isinstance(d,TemperatureHumiditySensorDisplay):
                    write_temperaturehumiditysensordisplay(g.label,d)
                else:
                    print(g.label, " ", d.deviceType, " ", d.label, " ", d.lastStatusUpdate, " ", d.rssiDeviceValue)

if __name__ == "__main__":
    main()
