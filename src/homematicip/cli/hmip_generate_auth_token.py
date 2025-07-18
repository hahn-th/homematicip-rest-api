#!/usr/bin/env python3
import asyncio
import configparser
import json
import time
from builtins import input

import homematicip
import homematicip.auth
from homematicip.connection.connection_context import ConnectionContextBuilder
from homematicip.connection.rest_connection import RestConnection


async def run_auth(access_point: str = None, devicename: str = None, pin: str = None):
    print(
        "If you are about to connect to a HomematicIP HCU1 you have to press the button on top of the device, before you continue.")
    print("From now, you have 5 Minutes to complete the registration process.")
    input("Press Enter to continue...")

    while True:
        access_point = (
            input("Please enter the accesspoint id (SGTIN): ").replace("-", "").upper()
        )
        if len(access_point) != 24:
            print("Invalid access_point id")
            continue
        break

    context = await ConnectionContextBuilder.build_context_async(access_point)
    connection = RestConnection(context, log_status_exceptions=False)

    auth = homematicip.auth.Auth(connection, context.client_auth_token, access_point)

    devicename = input(
        "Please enter the client/devicename (leave blank to use default):"
    )

    while True:
        pin = input("Please enter the PIN (leave Blank if there is none): ")

        if pin != "":
            auth.set_pin(pin)
        response = None
        if devicename == "":
            response = await auth.connection_request(access_point)
        else:
            response = await auth.connection_request(access_point, devicename)

        if response.status == 200:  # ConnectionRequest was fine
            break

        errorCode = json.loads(response.text)["errorCode"]
        if errorCode == "INVALID_PIN":
            print("PIN IS INVALID!")
        elif errorCode == "ASSIGNMENT_LOCKED":
            print("LOCKED ! Press button on HCU to unlock.")
            time.sleep(5)
        else:
            print("Error: {}\nExiting".format(errorCode))
            return

    print("Connection Request successful!")
    print("Please press the blue button on the access point")
    while not await auth.is_request_acknowledged():
        print("Please press the blue button on the access point")
        time.sleep(2)

    auth_token = await auth.request_auth_token()
    clientId = await auth.confirm_auth_token(auth_token)

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


def main():
    asyncio.run(run_auth())


if __name__ == "__main__":
    main()
