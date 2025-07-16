# HomematicIP Rest API Documentation

## Welcome to Homematic IP Rest API's documentation!

This documentation is for a **Python 3** wrapper for the homematicIP REST API (Access Point Based).
Since there is no official documentation about this API everything was
done via reverse engineering. Use at your own risk.

# Getting Started

## Installation

Install the library using pip:

```sh
pip install -U homematicip
```

## Getting the AUTH-TOKEN

Before you can use the library, you need an auth-token. Otherwise, the HomematicIP Cloud will not trust your requests.

You will need:
- Access to an active Access Point (it must glow blue)
- The SGTIN of the Access Point
- [Optional] The PIN

If you are connecting to a **HomematicIP HCU1**, press the button on top of the device before running the script. You then have 5 minutes to complete the registration process.

To get an auth-token, run the following script (installed with the library):

```sh
hmip_generate_auth_token
```

This will generate a **config.ini** in your current working directory. Scripts using this library will look for this file to load the auth-token and SGTIN of the Access Point. You can place it in the working directory or in one of the following global folders, depending on your OS:

- **General**
  - Current working directory
- **Windows**
  - %APPDATA%\homematicip-rest-api\
  - %PROGRAMDATA%\homematicip-rest-api\
- **Linux**
  - ~/.homematicip-rest-api/
  - /etc/homematicip-rest-api/
- **macOS**
  - ~/Library/Preferences/homematicip-rest-api/
  - /Library/Application Support/homematicip-rest-api/

## Using the CLI

You can send commands to HomematicIP using the `hmip_cli` script. For an overview, use the `-h` or `--help` parameter. To address devices, use the `-d` argument with the 24-digit ID (e.g., 301400000000000000000000) from `--list-devices`.

### Get Information about Devices and Groups

Commands are bound to the channel type. To get a list of all allowed actions for a device, use:

```sh
hmip_cli -d {deviceid} --print-allowed-commands
# or
hmip_cli -d {deviceid} -ac
```

To get information for a device and its channels, use the `--print-infos` argument with `-d` for a device or `-g` for a group.

### Examples

- `hmip_cli --help` — Show help
- `hmip_cli --list-devices` — List your devices
- `hmip_cli -d <id-from-device-list> --toggle-garage-door` — Toggle the garage door with HmIP-WGC
- `hmip_cli --list-events` — Listen to events and changes in your HomematicIP system
- `hmip_cli -d <id> --set-lock-state LOCKED --pin 1234` — Lock a door with HmIP-DLD
- `hmip_cli --dump-configuration --anonymize` — Dump the current config and anonymize it
