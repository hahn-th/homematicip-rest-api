# HomematicIP REST API

A **Python 3** wrapper for the homematicIP REST API (Access Point Based)
Since there is no official documentation about this API everything was
done via reverse engineering. Use at your own risk.

Any help from the community through e.g. pull requests would be highly appreciated.

[![PyPI download month](https://img.shields.io/pypi/dm/homematicip.svg)](https://pypi.python.org/pypi/homematicip/) [![PyPI version fury.io](https://badge.fury.io/py/homematicip.svg)](https://pypi.python.org/pypi/homematicip/) [![Discord](https://img.shields.io/discord/537253254074073088.svg?logo=discord&style=plastic)](https://discord.gg/mZG2myJ) [![Tests](https://github.com/hahn-th/homematicip-rest-api/actions/workflows/test-on-push.yml/badge.svg)](https://github.com/hahn-th/homematicip-rest-api/actions/workflows/test-on-push.yml) [![Coverage](https://codecov.io/gh/hahn-th/homematicip-rest-api/branch/master/graph/badge.svg)](https://codecov.io/gh/hahn-th/homematicip-rest-api) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/homematicip) [![License](https://img.shields.io/pypi/l/homematicip.svg)](LICENSE.txt)

## Using Home Assistant?

Home Assistant's [Homematic IP Cloud](https://www.home-assistant.io/integrations/homematicip_cloud/)
integration is built on this library. If your question is about entities, devices or automations
inside Home Assistant, start with the integration documentation. This README is about the library
itself and its command line tools.

A device has to be supported here before Home Assistant can expose it, so if your device is missing
entirely, see [New devices and config dump](#new-devices-and-config-dump).

## Get Help / Discord

If you want to get in contact with me or need help with the library, you can get in touch with me via discord. There is a **[discord server](https://discord.gg/mZG2myJ)** and my discord tag is **agonist#6159**

## :book: Documentation

The documentation is at https://hahn-th.github.io/homematicip-rest-api and is generated from the
`docs/` folder of this repository. It covers getting started, the API reference and the changelog.

## Support me

:heart: If you want to say thank you or want to support me, you can do that via PayPal.
[https://paypal.me/thomas08154711](https://paypal.me/thomas08154711?country.x=DE&locale.x=de_DE)

## Thanks

Kudos and a big thank you to @coreGreenberet, who created this library.

## Installation

To install the package, run:
```sh
pip install -U homematicip
```

## Usage

### Generate a token

If you are about to connect to a **HomematicIP HCU1** you have to press the button on top of the device, before running the script. From now, you have 5 Minutes to complete the registration process.

After that, run `hmip_generate_auth_token` (from the command line) to get an auth token for your access point. It will generate a `config.ini` in your current directory.

### Use the CLI

You can send commands to homematicIP using the `hmip_cli` script. To get an overview, use -h or --help param. To address devices, use the argument -d in combination with the 24-digit ID (301400000000000000000000) from --list-devices.

A few examples:

- `hmip_cli --help` to get help
- `hmip_cli --list-devices` to get a list of your devices.
- `hmip_cli -d <id-from-device-list> --toggle-garage-door` to toggle the garage door with HmIP-WGC.
- `hmip_cli --list-events` to listen to events and changes in your homematicIP system
- `hmip_cli -d <id> --set-lock-state LOCKED --pin 1234` to lock a door with HmIP-DLD
- `hmip_cli --dump-configuration --anonymize` to dump the current config and anonymize it.

### Examples

All examples assume a `config.ini` created by `hmip_generate_auth_token`, see
[Paths for config.ini](#paths-for-configini) for where it is looked up.

Connect and list your devices:

```python
import homematicip
from homematicip.home import Home

config = homematicip.find_and_load_config_file()

home = Home()
home.init(config.access_point, config.auth_token)
home.get_current_state()

for device in home.devices:
    print(f"{device.id}  {device.label}  ({device.modelType})")
```

Read a value. Devices are containers; the readings live on their functional channels, and which
channel carries what depends on the device:

```python
device = home.search_device_by_id("3014F711A000000000000001")

for channel in device.functionalChannels:
    print(channel.index, channel.functionalChannelType)

# on a wall thermostat, channel 1 is the WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL
print(device.functionalChannels[1].actualTemperature)
```

Switch something on. The write methods live on the device and on the channel:

```python
device = home.search_device_by_id("3014F711A000000000000001")
device.turn_on()
```

The library is async underneath. Every method has an `_async` counterpart, and `Home` wraps those
for synchronous use. In an async application use `AsyncHome` directly:

```python
import asyncio

import homematicip
from homematicip.async_home import AsyncHome


async def main():
    config = homematicip.find_and_load_config_file()

    home = AsyncHome()
    await home.init_async(config.access_point, config.auth_token)
    await home.get_current_state_async()

    for device in home.devices:
        print(device.label)


asyncio.run(main())
```

## Events

It is also possible to receive push notifications over a websocket connection. Events are only
delivered while the connection is open, so this has to run inside an event loop:

```python
import asyncio

import homematicip
from homematicip.async_home import AsyncHome


def print_events(event_list):
    for event in event_list:
        print(f"EventType: {event['eventType']} Data: {event['data']}")


async def main():
    config = homematicip.find_and_load_config_file()

    home = AsyncHome()
    await home.init_async(config.access_point, config.auth_token)
    await home.get_current_state_async()

    home.onEvent += print_events
    await home.enable_events()

    try:
        while True:
            await asyncio.sleep(1)
    finally:
        await home.disable_events_async()


asyncio.run(main())
```

## Paths for config.ini

The scripts will look for a config.ini in 3
different locations depending on your OS. Copy the file to one of these
locations so that it will be accessible for the scripts.

- General
  - current working directory
- Windows
  - %APPDATA%\\homematicip-rest-api
  - %PROGRAMDATA%\\homematicip-rest-api
- Linux
  - ~/.homematicip-rest-api/
  - /etc/homematicip-rest-api/
- MAC OS
  - ~/Library/Preferences/homematicip-rest-api/
  - /Library/Application Support/homematicip-rest-api/

## New devices and config dump

If your device is missing from the list below, or is listed but does not do what you need, open an
issue with a configuration dump attached. A dump is what makes a device implementable without owning
the hardware.

**From Home Assistant**, which is the shortest path if you use it: open Settings > Devices &
services > Homematic IP Cloud, use the three-dot menu next to your access point and choose *Download
diagnostics*. The result is already redacted and contains everything needed.

**From this library**, if you have it set up:

```sh
hmip_cli --dump-configuration --anonymize
```

`--anonymize` replaces the identifying values with placeholders: every GUID, every SGTIN serial
number, the refresh token, and your city and coordinates. It does **not** touch the names you gave
your devices and groups, so check the output before posting it publicly.

Please include:

- the model number as printed on the device, for example `HmIP-WGRC`
- what the device should do that the library cannot do yet
- the dump itself, as a [gist](https://gist.github.com) if it is long

## Device support

A checked box means the model is mapped to a device class here, so its readings and commands are
available. An unchecked box means the model is known but not implemented, usually because nobody has
sent a dump for it yet, see [New devices and config dump](#new-devices-and-config-dump).

Radio and wired devices are in one list; wired models carry the `HMIPW` prefix. Entries marked
`*powered by HmIP` are third-party devices speaking the Homematic IP protocol.

- [x] ALPHA-IP-RBG (Alpha IP Wall Thermostat Display)
- [x] ALPHA-IP-RBGa (Alpha IP Wall Thermostat Display analog)
- [ ] ELV-SH-AI8 (Alarmline Interface 8x Inputs) \*powered by HmIP
- [x] ELV-SH-BS2 (Switch Actuator for brand switches 2x channels) \*powered by HmIP
- [x] ELV-SH-CRC (Remote Control Compact) \*powered by HmIP
- [x] ELV-SH-CTH (Temperature and Humidity Sensor Compact) \*powered by HmIP
- [x] ELV-SH-CTV Tilt Vibration Sensor Compact
- [x] ELV-SH-DUSI (Ultrasonic Distance Sensor Interface) \*powered by HmIP
- [ ] ELV-SH-GVI (Garden valve interface) \*powered by HmIP
- [ ] ELV-SH-IRS8 (Infrared Remote control - 8x channels) \*powered by HmIP
- [x] ELV-SH-PSMCI (Switch Measuring Cable Indoor) \*powered by HmIP
- [x] ELV-SH-PTI2 (Temperature Difference Sensor 2 - Platin) \*powered by HmIP
- [x] ELV-SH-SB8 (Status Board) \*powered by HmIP
- [x] ELV-SH-SMSI (Soil Moisture Sensor Interface) \*powered by HmIP
- [x] ELV-SH-SPS25 (Switchable Power Supply) \*powered by HmIP
- [ ] ELV-SH-SW1-BAT (2x Actuator Switch for 30V/1A with 2xAA Batteries) \*powered by HmIP
- [x] ELV-SH-TACO (Temperature, Tilt and Vibration Sensor) \*powered by HmIP
- [ ] ELV-SH-WSC (2x Servo Controls, 5v - 12V) \*powered by HmIP
- [x] ELV-SH-WSM (Watering Actuator) \*powered by HmIP
- [ ] ELV-SH-WUA (Dimming Actuator, 0-10/1-10-V-Control inputs, 8A 230V) \*powered by HmIP
- [x] HMIP-ASIR (Alarm Siren - indoor)
- [x] HMIP-ASIR-2 (Alarm Siren - indoor) New Version
- [x] HMIP-ASIR-B1 (Alarm Siren - indoor) _Silvercrest Edition_
- [x] HMIP-ASIR-O (Alarm Siren - outdoor)
- [x] HMIP-BBL (Blind Actuator for brand switches)
- [ ] HMIP-BBL-2 (Blind Actuator for brand switches) New Version
- [x] HMIP-BDT (Dimming Actuator for brand switches)
- [x] HMIP-BRC2 (Remote Control for brand switches – 2x channels)
- [x] HMIP-BROLL (Shutter Actuator - brand-mount)
- [ ] HMIP-BROLL-2 (Shutter Actuator - brand-mount) New Version
- [x] HMIP-BSL (Switch Actuator for brand switches – with signal lamp)
- [x] HMIP-BSM (Brand Switch and Meter Actuator)
- [ ] HMIP-BSM-I (Brand Switch and Meter Actuator, International)
- [x] HMIP-BWTH (Wall Thermostat Display with switching output – for brand switches, 230V)
- [ ] HMIP-BWTH24 (Wall Thermostat Display with switching output – for brand switches, 24V)
- [x] HMIP-DBB (Doorbell Push-Button)
- [x] HMIP-DLD (Door Lock Drive)
- [x] HMIP-DLP (Door Lock Drive Pro)
- [x] HMIP-DLS (Door Lock Sensor)
- [x] HMIP-DRBLI4 (Blind Actuator for DIN rail mount – 4 channels)
- [x] HMIP-DRDI3 (Dimming Actuator Inbound 230V – 3x channels, 200W per channel) electrical DIN rail
- [x] HmIP-DRG-DALI (Dali Gateway - readonly at the moment)
- [x] HMIP-DRSI1 (Switch Actuator for DIN rail mount – 1x channel)
- [x] HMIP-DRSI4 (Switch Actuator for DIN rail mount – 4x channels)
- [x] HMIP-DSD-PCB (Door Signal Detector PCB)
- [x] HMIP-ESI (Energy Sensors Interface)
- [x] HMIP-eTRV (Heating-Thermostat with Display)
- [x] HMIP-eTRV-2 (Heating-Thermostat with Display) New Version
- [x] HMIP-eTRV-2 I9F (Heating-Thermostat with Display) New Version
- [ ] HMIP-eTRV-2-UK (UK Version not tested, but it should work)
- [x] HMIP-eTRV-3 (Heating-Thermostat pure, white)
- [x] HMIP-eTRV-B (Heating-Thermostat basic with Display)
- [ ] HMIP-eTRV-B-2 (Heating-Thermostat basic with Display) New Version
- [ ] HMIP-eTRV-B-2 R4M (Heating-Thermostat basic with Display) New Version
- [ ] HMIP-eTRV-B-UK (UK Version not tested, but it should work)
- [x] HMIP-eTRV-B1 (Heating-Thermostat basic with Display) _Silvercrest Edition_
- [x] HMIP-eTRV-C (Heating-Thermostat compact without display)
- [x] HMIP-eTRV-C-2 (Heating-Thermostat compact without display) New Version
- [x] HmIP-eTRV-CL (Heating-thermostat compact with display)
- [x] HMIP-eTRV-E (Heating-Thermostat Design Evo _New Generation_, white)
- [ ] HMIP-eTRV-E-A (Heating-Thermostat Design Evo _New Generation_, anthracite)
- [ ] HMIP-eTRV-E-S (Heating-Thermostat Design Evo _New Generation_, silver)
- [x] HMIP-eTRV-F (Heating-Thermostat flex, white)
- [x] HMIP-FAL230-C10 (Floor Heating Actuator – 10x channels, 230V)
- [x] HMIP-FAL230-C6 (Floor Heating Actuator – 6x channels, 230V)
- [x] HMIP-FAL24-C10 (Floor Heating Actuator – 10x channels, 24V)
- [x] HMIP-FAL24-C6 (Floor Heating Actuator – 6x channels, 24V)
- [x] HMIP-FALMOT-C12 (Floor Heating Actuator – 12x channels, motorised)
- [x] HMIP-FALMOT-C8 (Floor Heating Actuator – 8x channels, motorised)
- [x] HMIP-FBL (Blind Actuator - flush-mount)
- [x] HMIP-FCI1 (Contact Interface flush-mount – 1x channel)
- [x] HMIP-FCI6 (Contact Interface flush-mount – 6x channels)
- [x] HMIP-FDC (Full Flush Door Controller / Türöffner-Aktor)
- [x] HMIP-FDT (Dimming Actuator - flush-mount)
- [x] HMIP-FLC (Full Flush Lock Controller)
- [x] HMIP-FROLL (Shutter Actuator - flush-mount)
- [x] HMIP-FSI16 (Switch Actuator with Push-button Input 230V, 16A)
- [x] HMIP-FSI6 (Full Flush Input Switch Compact)
- [x] HMIP-FSM (Switch Actuator and Meter 5A – flush-mount)
- [x] HMIP-FSM16 (Switch Actuator and Meter 16A – flush-mount)
- [x] HMIP-FWI (Wiegand Interface)
- [x] HMIP-HAP (Cloud Access Point)
- [x] HMIP-HAP-B1 (Cloud Access Point) _Silvercrest Edition_
- [x] HMIP-HAP2 (Access Point 2)
- [x] HMIP-HCU (Home Control Unit)
- [x] HMIP-HDM1 (Hunter Douglas & erfal window blinds)
- [ ] HMIP-HDRC (Hunter Douglas & erfal window blinds remote control)
- [ ] HMIP-K-DRBLI4 (Blinds Actuator – 4x channels, 230V, 2,2A / 500W per channel) electrical DIN rail
- [ ] HMIP-K-DRDI3 (Dimming Actuator Inbound 230V – 3x channels, 200W per channel) electrical DIN rail
- [ ] HMIP-K-DRSI1 (Actuator Inbound 230V – 1x channel) electrical DIN rail
- [ ] HMIP-K-DRSI4 (Switch Actuator – 4x channels, 16A per channel) electrical DIN rail
- [x] HmIP-KRC-K (Key Ring Remote Control for KeyMatic - 4x buttons)
- [x] HMIP-KRC4 (Key Ring Remote Control - 4x buttons)
- [x] HMIP-KRCA (Key Ring Remote Control & Alarm)
- [x] HMIP-LSC (Light Strip Controller)
- [ ] HMIP-MIO16-PCB (Multi Analog/Digital Interface - Switch Circuit Board)
- [x] HMIP-MIOB (Multi IO Box for floor heating & cooling)
- [x] HMIP-MOD-HO (Garage Door Module for Hörmann)
- [x] HMIP-MOD-OC8 (Open Collector Module Receiver - 8x)
- [x] HMIP-MOD-RC8 (Open Collector Module Sender - 8x)
- [x] HMIP-MOD-TM (Garage Door Module for Novoferm and Tormatic door operators)
- [x] HMIP-MP3P (Combination Signalling Device MP3)
- [ ] HMIP-P-DRG-DALI (DALI Lights Gateway)
- [x] HMIP-PCBS (Switch Circuit Board - 1x channel)
- [x] HMIP-PCBS-BAT (Switch Circuit Board with Battery - 1x channel)
- [x] HMIP-PCBS2 (Switch Circuit Board - 2x channels)
- [x] HMIP-PDT (Plugable Dimmer)
- [ ] HMIP-PDT-UK (UK Version not tested, but it should work)
- [x] HMIP-PMFS (Plugable Power Supply Monitoring)
- [x] HMIP-PS (Plugable Switch)
- [ ] HMIP-PS-2 (Plugable Switch) New Version
- [x] HMIP-PSM (Plugable Switch Measuring, Type F - Standard for Homematic)
- [ ] HMIP-PSM-2 (Plugable Switch Measuring, Type F - Standard for Homematic) New Version
- [x] HMIP-PSM-CH (Plugable Switch Measuring, Type J)
- [ ] HMIP-PSM-IT (Type L not tested, but it should work)
- [ ] HMIP-PSM-PE (Type E not tested, but it should work)
- [ ] HMIP-PSM-UK (Type G not tested, but it should work)
- [x] HMIP-PSMCO (Schalt-Mess-Kabel – außen)
- [x] HMIP-RC8 (Remote Control - 8x buttons)
- [ ] HMIP-RCB1 (Remote Control - 1x button)
- [x] HMIP-RGBW (RGB Led Controller - Readonly at the moment)
- [x] HMIP-SAM (Acceleration Sensor)
- [x] HMIP-SCI (Contact Interface Sensor)
- [x] HMIP-SCTH230 (CO2, Temperature and Humidity Sensor 230V)
- [x] HMIP-SFD (Fine Dust Sensor)
- [x] HMIP-SLO (Light Sensor - outdoor)
- [x] HMIP-SMI (Motion Detector with Brightness Sensor - indoor)
- [x] HMIP-SMI55 (Motion Detector with Brightness Sensor and Remote Control - 2x buttons)
- [ ] HMIP-SMI55-2 (Motion Detector with Brightness Sensor and Remote Control - 2x buttons) New Version
- [x] HMIP-SMO (Motion Detector with Brightness Sensor - outdoor)
- [ ] HMIP-SMO-2 (Motion Detector with Brightness Sensor - outdoor) New Version
- [x] HMIP-SMO-A (Motion Detector with Brightness Sensor - outdoor, anthracite)
- [ ] HMIP-SMO-A-2 (Motion Detector with Brightness Sensor - outdoor, anthracite) New Version
- [x] HmIP-SMO230-A
- [x] HMIP-SPDR (Passage Sensor with Direction Recognition)
- [x] HMIP-SPI (Presence Sensor - indoor)
- [x] HMIP-SRD (Rain Sensor)
- [x] HMIP-SRH (Window Rotary Handle Sensor)
- [x] HMIP-STE2-PCB (Temperature Difference Sensors - 2x sensors)
- [x] HMIP-STH (Temperature and Humidity Sensor without display - indoor)
- [x] HMIP-STHD (Temperature and Humidity Sensor with display - indoor)
- [x] HMIP-STHO (Temperature and Humidity Sensor - outdoor)
- [x] HMIP-STHO-A (Temperature and Humidity Sensor – outdoor, anthracite)
- [x] HMIP-STV (Inclination and vibration Sensor)
- [x] HMIP-SWD (Water Sensor)
- [x] HMIP-SWDM (Door / Window Contact - magnetic)
- [ ] HMIP-SWDM-2 (Door / Window Contact - magnetic) New Version
- [x] HMIP-SWDM-B2 (Door / Window Contact - magnetic) _Silvercrest Edition_
- [x] HMIP-SWDO (Shutter Contact Optical)
- [ ] HMIP-SWDO-2 (Shutter Contact Optical) New Version
- [x] HMIP-SWDO-I (Shutter Contact Optical Invisible)
- [x] HMIP-SWDO-PL (Shutter Contact Optical Plus)
- [ ] HMIP-SWDO-PL-2 (Shutter Contact Optical Plus) New Version
- [x] HMIP-SWO-B (Weather Sensor - Basic)
- [x] HMIP-SWO-PL (Weather Sensor – Plus)
- [x] HMIP-SWO-PR (Weather Sensor – Pro)
- [x] HMIP-SWSD (Smoke Detector)
- [x] HMIP-SWSD-2 (Smoke Detector with Siren)
- [x] HMIP-USBSM (USB Switching Measurement Actuator)
- [x] HMIP-WGC (Garage Door Button)
- [x] HmIP-WGS (Wall Mounted Glass Switch)
- [x] HMIP-WGT (Wall Thermostat with Glass Display)
- [x] HMIP-WGTC (Wall Mounted Glass Thermostat with Carbon Dioxide Sensor)
- [x] HMIP-WHS2 (Switch Actuator for heating systems – 2x channels)
- [x] HMIP-WKP (Keypad)
- [x] HMIP-WLAN-HAP (WLAN Access Point)
- [x] HmIP-WLAN-HAP-B
- [x] HMIP-WRC2 (Wall-mount Remote Control - 2x buttons)
- [x] HMIP-WRC6 (Wall-mount Remote Control - 6x buttons)
- [x] HmIP-WRC6-230 (Wall-mount Remote Control - 6x buttons, 230V, with LED)
- [x] HMIP-WRCC2 (Wall-mount Remote Control – flat)
- [ ] HMIP-WRCD (Wall-mount Remote Control - E-Paper-Status display)
- [x] HMIP-WRCR (Wall-mount Remote Control - Rotary)
- [ ] HMIP-WT (Wall Mounted Thermostat without adjusting wheel) #probably only prototype for WTH-B and was not released
- [x] HMIP-WTH (Wall Mounted Thermostat Pro with Display)
- [x] HMIP-WTH-1 (Wall Mounted Thermostat Pro with Display _Newest Version_ - successor of WTH-2 - really)
- [x] HMIP-WTH-2 (Wall Mounted Thermostat Pro with Display)
- [x] HMIP-WTH-B (Wall Mounted Thermostat basic without adjusting wheel)
- [ ] HMIP-WTH-B-2 (Wall Mounted Thermostat basic without adjusting wheel) New Version
- [x] HMIP-WUA (Dimming Actuator, 0-10/1-10-V-Control inputs, 8A 230V)
- [ ] HMIPW-BRC2 (Homematic IP Wired Remote Control for brand switches – 2x channels)
- [x] HMIPW-DRAP (Homematic IP Wired Access Point)
- [x] HMIPW-DRBL4 (Homematic IP Wired Blinds Actuator – 4x channels)
- [x] HMIPW-DRD3 (Homematic IP Wired Dimming Actuator – 3x channels)
- [x] HMIPW-DRI16 (Homematic IP Wired Inbound module – 16x channels)
- [x] HMIPW-DRI32 (Homematic IP Wired Inbound module – 32x channels)
- [x] HMIPW-DRS4 (Homematic IP Wired Switch Actuator – 4x channels)
- [x] HMIPW-DRS8 (Homematic IP Wired Switch Actuator – 8x channels)
- [ ] HMIPW-FAL230-C10 (Homematic IP Wired Floor Heating Actuator – 10x channels, 230V)
- [ ] HMIPW-FAL230-C6 (Homematic IP Wired Floor Heating Actuator – 6x channels, 230V)
- [ ] HMIPW-FAL24-C10 (Homematic IP Wired Floor Heating Actuator – 10x channels, 24V)
- [ ] HMIPW-FAL24-C6 (Homematic IP Wired Floor Heating Actuator – 6x channels, 24V)
- [x] HMIPW-FALMOT-C12 (Homematic IP Wired Floor Heating Actuator – 12x channels, motorised)
- [x] HMIPW-FIO6 (Homematic IP Wired IO Module flush-mount – 6x channels)
- [x] HMIPW-SCTHD (Homematic IP Wired CO2, Temperature and Humidity Sensor with Display)
- [x] HMIPW-SMI55 (Homematic IP Wired Motion Detector with Brightness Sensor and Remote Control - 2x buttons)
- [x] HMIPW-SPI (Homematic IP Wired Presence Sensor - indoor)
- [ ] HMIPW-STH (Homematic IP Wired Temperature and Humidity Sensor without display - indoor)
- [ ] HMIPW-STHD (Homematic IP Wired Temperature and Humidity Sensor with display - indoor)
- [ ] HMIPW-WGD (Homematic IP Wired Wall-mount Glas Display - black edition)
- [ ] HMIPW-WGD-PL (Homematic IP Wired Wall-mount Glas Display Play - black edition)
- [x] HMIPW-WRC2 (Homematic IP Wired Wall-mount Remote Control - 2x channels)
- [x] HMIPW-WRC6 (Homematic IP Wired Wall-mount Remote Control - 6x channels)
- [x] HMIPW-WTH (Homematic IP Wired Wall Mounted Thermostat Pro with Display)
