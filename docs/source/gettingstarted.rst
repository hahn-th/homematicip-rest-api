Getting Started
***************

Installation
============

Just run **pip3 install -U homematicip** in the command line to get the package.
This will install (and update) the library and all required packages

Getting the AUTH-TOKEN
======================
Before you can start using the library you will need an auth-token. Otherwise the HMIP Cloud will not trust you.

You will need:

-  Access to an active Access Point (it must glow blue)
-  the SGTIN of the Access Point
-  [optional] the PIN


If you are about to connect to a **HomematicIP HCU1** you have to press the button on top of the device, before running the script. From now, you have 5 Minutes to complete the registration process.

To get an auth-token you have to run the script `hmip_generate_auth_token` which is installed with the library.

```sh
hmip_generate_auth_token
```

It will generate a **config.ini** in your current working directory. The scripts which are using this library are looking
for this file to load the auth-token and SGTIN of the Access Point. You can either place it in the working directory when you are 
running the scripts or depending on your OS in different "global" folders:

-  General

   -  current working directory

-  Windows

   -  %APPDATA%\\homematicip-rest-api\
   -  %PROGRAMDATA%\\homematicip-rest-api\

-  Linux

   -  ~/.homematicip-rest-api/
   -  /etc/homematicip-rest-api/

-  MAC OS

   -  ~/Library/Preferences/homematicip-rest-api/
   -  /Library/Application Support/homematicip-rest-api/

Using the CLI
=============

You can send commands to homematicIP using the `hmip_cli` script. To get an overview, use -h or --help param. To address devices, use the argument -d in combination with the 24-digit ID (301400000000000000000000) from --list-devices.

Get Information about devices and groups
----------------------------------------

Commands are bound to the channel type. To get a list of all allowed actions for a device you can write `hmip_cli -d {deviceid} --print-allowed-commands` or `hmip_cli -d {deviceid} -ac`.

To get infos for a device and its channels use the `--print-infos` argument in combination with -d for a device or -g for a group.

Examples
--------

A few examples:

- `hmip_cli --help` to get help
- `hmip_cli --list-devices` to get a list of your devices.
- `hmip_cli -d <id-from-device-list> --toggle-garage-door` to toogle the garage door with HmIP-WGC.
- `hmip_cli --list-events` to listen to events and changes in your homematicIP system
- `hmip_cli -d <id> --set-lock-state LOCKED --pin 1234` to lock a door with HmIP-DLD
- `hmip_cli --dump-configuration --anonymize` to dump the current config and anonymize it.

Batch Testing of applicable commands
====================================

HomematicIP devices can have different channels and each channel can have different commands. To test which commands are applicable for a channel, you can use the `hmip_batch` script.

This script will try to execute commands for a device and print the result. It will also print the commands which are not applicable for the device.

The script takes the device ID and the channel index as arguments. Required is the json-batch file which contains the commands.


> Please pay close attention to the parameters used for each command. Incorrect or inappropriate parameters may lead to unexpected behavior or even malfunction of your HomematicIP devices. Executing commands is at your own risk. Always double-check the documentation and ensure you understand the effects of each command before using it in your environment.

Following steps are required:
- Install this library with pip `pip install -U homematicip`
- Get an access token as described above
- Get your device ID and channel index from the device list using `hmip_cli --list-devices` or `hmip_cli --dump-configuration`
- Download JSON Batch File from https://github.com/hahn-th/homematicip-rest-api/blob/master/homematicip_demo/hmip_batch.json
- Edit the JSON Batch File to choose which commands you want to test. You can enable or disable commands by setting the "active" flag to true or false.



With the "active" flag you can enable or disable commands.

```
    {
      "function": "set_shutter_level_async",
      "active": false,
      "params": {
        "shutter_level": 0.7
      }
    },
```

To run the batch test, use the following command:
```sh
hmip_batch -d <device-id> -i <channel-index> <path-to-json-batch-file>
```
