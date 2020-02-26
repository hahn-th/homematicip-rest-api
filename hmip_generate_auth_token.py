#!/usr/bin/env python3
import configparser
import json
import time
from builtins import input

import homematicip
import homematicip.auth
from homematicip.home import Home


def main():
    while True:
        access_point = (
            input("Please enter the accesspoint id (SGTIN): ").replace("-", "").upper()
        )
        if len(access_point) != 24:
            print("Invalid access_point id")
            continue
        break

    home = Home()
    home.init(access_point)
    auth = homematicip.auth.Auth(home)

    devicename = input(
        "Please enter the client/devicename (leave blank to use default):"
    )

    while True:
        pin = input("Please enter the PIN (leave Blank if there is none): ")

        if pin != "":
            auth.pin = pin
        response = None
        if devicename != "":
            response = auth.connectionRequest(access_point, devicename)
        else:
            response = auth.connectionRequest(access_point)

        if response.status_code == 200:  # ConnectionRequest was fine
            break

        errorCode = json.loads(response.text)["errorCode"]
        if errorCode == "INVALID_PIN":
            print("PIN IS INVALID!")
        else:
            print("Error: {}\nExiting".format(errorCode))
            return

    print("Please press the blue button on the access point")
    while not auth.isRequestAcknowledged():
        print("Please press the blue button on the access point")
        time.sleep(2)

    auth_token = auth.requestAuthToken()
    clientId = auth.confirmAuthToken(auth_token)

    print(
        "-----------------------------------------------------------------------------"
    )
    print("Token successfully registered!")
    print(
        "AUTH_TOKEN:\t{}\nACCESS_POINT:\t{}\nClient ID:\t{}\nsaving configuration to ./config.ini".format(
            auth_token, access_point, clientId
        )
    )

    _config = configparser.ConfigParser()
    _config.add_section("AUTH")
    _config.add_section("LOGGING")
    _config["AUTH"] = {"AuthToken": auth_token, "AccessPoint": access_point}
    _config.set("LOGGING", "Level", "30")
    _config.set("LOGGING", "FileName", "None")
    with open("./config.ini", "w") as configfile:
        _config.write(configfile)


if __name__ == "__main__":
    main()
