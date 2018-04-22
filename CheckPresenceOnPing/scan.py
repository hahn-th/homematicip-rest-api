#!/usr/bin/env python3
import homematicip
from homematicip.home import Home
import ping3
from socket import gaierror

config = homematicip.find_and_load_config_file()

SCANABLE_DEVICES = ['<PHONE_IP_1>', '<PHONE_IP_2>', '<PHONE_IP_3>']
ACTIVATE_EXTERNAL_ZONE = True
ACTIVATE_INTERNAL_ZONE = True


DEACTIVATE_ON_PRESENCE = True

def main():
    if config is None:
        print("COULD NOT DETECT CONFIG FILE")
        return
    

    home = Home()
    home.set_auth_token(config.auth_token)
    home.init(config.access_point)

    if not home.get_current_state():
        return
    for ip in SCANABLE_DEVICES:
        try:
            res = ping3.ping(ip)
            if res != None:
                if DEACTIVATE_ON_PRESENCE:
                    for g in home.groups:
                        if isinstance(g, homematicip.group.SecurityZoneGroup) and g.active:
                            print("someone is at home. Deactivating security zones")
                            home.set_security_zones_activation(False,False)
                            return
                    print("someone is at home and security zones are deactivated -> do nothing")
                else:
                    print("someone is at home -> do nothing")
                return
        except gaierror:
            print("could not resolve {}. Marking it as \"not at home\"".format(ip))

    print("Noone is home -> activating security zones")
    home.set_security_zones_activation(ACTIVATE_INTERNAL_ZONE,ACTIVATE_EXTERNAL_ZONE)

if __name__ == "__main__":
    main()