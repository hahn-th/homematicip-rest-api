import requests
import homematicip
from homematicip.home import Home
from homematicip.device import ShutterContact,HeatingThermostat,PlugableSwitchMeasuring,WallMountedThermostatPro

config = homematicip.find_and_load_config_file()

home = Home()
home.set_auth_token(config.auth_token)
home.init(config.access_point)

def write_plugableswitchmeasuring(room,device):
	print(room, " ", device.label, " ", device.lastStatusUpdate, " ", device.currentPowerConsumption, " ", device.energyCounter)
  payload = {'room': room, 'device': device.label, 'lastStatusUpdate': device.lastStatusUpdate, 'currentPowerConsumption': device.currentPowerConsumption, 'energyCounter': device.energyCounter}
  send_request(payload)
    
def write_heatingthermostat(room,device):
	print(room, " ", device.label, " ", device.lastStatusUpdate)
  payload = {'room': room, 'device': device.label, 'lastStatusUpdate': device.lastStatusUpdate}
  send_request(payload)

def write_shutter(room,device):
	print(room, " ", device.label, " ", device.lastStatusUpdate, " ", device.windowState)
	payload = {'room': room, 'device': device.label, 'type': 'windowState', 'value': device.windowState}
	send_request(payload)
	
def write_wallmountedthermostatpro(room,device):
  print(room, " ", device.label, " ", device.lastStatusUpdate, " ", device.actualTemperature, " ", device.setPointTemperature, " ", device.humidity)
  payload = {'room': room, 'device': device.label, 'type': 'actualTemperature', 'value': device.actualTemperature}
  send_request(payload)
  payload = {'room': room, 'device': device.label, 'type': 'setPointTemperature', 'value': device.setPointTemperature}
  send_request(payload)
  payload = {'room': room, 'device': device.label, 'type': 'humidity', 'value': device.humidity}
  send_request(payload)  
    
def send_request(payload):
	r = requests.post('YOUR_ENDPOINT_URL', data=payload, auth=('<user>', '<pass>'))
	print(r.status_code)
	print(r.text)
  
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
