import homematicip
from homematicip.home import Home
from homematicip.device import ShutterContact,HeatingThermostat,PlugableSwitchMeasuring,WallMountedThermostatPro

config = homematicip.find_and_load_config_file()

home = Home()
home.set_auth_token(config.auth_token)
home.init(config.access_point)

def write_shutter(room,device):
	print(room, " ", device.label, " ", device.lastStatusUpdate, " ", device.windowState)
	#print(device)

def write_plugableswitchmeasuring(room,device):
	print(room, " ", device.label, " ", device.lastStatusUpdate, " ", device.currentPowerConsumption, " ", device.energyCounter)

def write_heatingthermostat(room,device):
	print(room, " ", device.label, " ", device.lastStatusUpdate)

def write_wallmountedthermostatpro(room,device):
    print(room, " ", device.label, " ", device.lastStatusUpdate, " ", device.actualTemperature, " ", device.setPointTemperature, " ", device.humidity)

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

if __name__ == "__main__":
    main()
