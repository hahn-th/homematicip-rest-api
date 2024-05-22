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

Now you have to run **hmip_generate_auth_token.py** and follow it's instructions.
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

You can send commands to homematicIP using the `hmip_cli.py` script. To get an overview, use -h or --help param. To address devices, use the argument -d in combination with the 24-digit ID (301400000000000000000000) from --list-devices.

Get Information about devices and groups
----------------------------------------

Commands are bound to the channel type. To get a list of all allowed actions for a device you can write `hmip_cli -d {deviceid} --print-allowed-commands` or `hmip_cli -d {deviceid} -ac`.

To get infos for a device and its channels use the `--print-infos` argument in combination with -d for a device or -g for a group.

Examples
--------

A few examples:

- `python hmip_cli.py --help` to get help
- `python hmip_cli.py --list-devices` to get a list of your devices.
- `python hmip_cli.py -d <id-from-device-list> --toggle-garage-door` to toogle the garage door with HmIP-WGC.
- `python hmip_cli.py --list-events` to listen to events and changes in your homematicIP system
- `python hmip_cli.py -d <id> --set-lock-state LOCKED --pin 1234` to lock a door with HmIP-DLD
- `python hmip_cli.py --dump-configuration --anonymize` to dump the current config and anonymize it.
