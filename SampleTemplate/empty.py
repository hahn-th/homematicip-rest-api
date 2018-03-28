#!/usr/bin/env python3
import homematicip
from homematicip.home import Home
config = homematicip.find_and_load_config_file()


def main():
    if config is None:
        print("COULD NOT DETECT CONFIG FILE")
        return
    

    home = Home()
    home.set_auth_token(config.auth_token)
    home.init(config.access_point)

    home.get_current_state()

    print("current AP Version: {}".format(home.currentAPVersion))

if __name__ == "__main__":
    main()