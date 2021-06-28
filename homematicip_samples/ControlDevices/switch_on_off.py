import time
import homematicip
from homematicip.home import Home
from homematicip.device import Switch

config = homematicip.find_and_load_config_file()

home = Home()
home.set_auth_token(config.auth_token)
home.init(config.access_point)

def main():
    global home
    home.get_current_state()
    for device in home.devices:
        if isinstance(device, Switch):
            device.turn_on()
            time.sleep(2)
            device.turn_off()
            return

if __name__ == "__main__":
    main()
