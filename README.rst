HomematicIP REST API
====================

A **Python 3** wrapper for the homematicIP REST API (Access Point Based)
Since there is no official documentation about this API everything was
done via reverse engineering. Use at your own risk.

Any help from the community through e.g. pull requests would be highly
appreciated.

|PyPI download month| |PyPI version fury.io| |Discord| |CircleCI| |PyPI
- Python Version|

Get Help / Discord
------------------

If you want to get in contact with me or need help with the library, you
can get in touch with me via discord. There is a `discord
server <https://discord.gg/mZG2myJ>`__ and my discord tag is
**agonist#6159**

Support me
----------

:heart: If you want to say thank you or want to support me, you can do
that via PayPal.
`https://paypal.me/thomas08154711 <https://paypal.me/thomas08154711?country.x=DE&locale.x=de_DE>`__

Thanks
------

Kudos and a big thank you to @coreGreenberet, who created this library.

Documentation
-------------

**Documentation is currently not updated**

Documentation can be found under
https://homematicip-rest-api.readthedocs.io

Installation
------------

Just run **pip install -U homematicip** to get the package

“Nightly” Builds
~~~~~~~~~~~~~~~~

Each push on the master branch will trigger a build. That way you can
test the latest version of the library with your systems. Just run
``pip install -U homematicip --pre`` to get the package.

New devices and config dump
---------------------------

If you missing a device which is not implemented yet, open an issue and
append a dump of your configuration to it using https://gist.github.com.
To create a dump use the CLI:
``python hmip_cli.py --dump-configuration --anonymize``. See
`Usage <#usage>`__ for more instructions.

Usage
-----

Generate Token
~~~~~~~~~~~~~~

First run ``python hmip_generate_auth_token.py`` (from the command line)
to get an auth token for your access point. it will generate a
“config.ini” in your current directory.

Use the CLI
~~~~~~~~~~~

You can send commands to homematicIP using the ``hmip_cli.py`` script.
To get an overview, use -h or –help param. To address devices, use the
argument -d in combination with the 24-digit ID
(301400000000000000000000) from –list-devices.

A few examples:

-  ``python hmip_cli.py --help`` to get help
-  ``python hmip_cli.py --list-devices`` to get a list of your devices.
-  ``python hmip_cli.py -d <id-from-device-list> --toggle-garage-door``
   to toogle the garage door with HmIP-WGC.
-  ``python hmip_cli.py --list-events`` to listen to events and changes
   in your homematicIP system
-  ``python hmip_cli.py -d <id> --set-lock-state LOCKED --pin 1234`` to
   lock a door with HmIP-DLD
-  ``python hmip_cli.py --dump-configuration --anonymize`` to dump the
   current config and anonymize it.

Examples
--------

-  hmip_cli.py for listing devices, groups, securityJournal; setting
   labels, turning switches on/off
-  Sample Projects are under ./homematicip-samples

Implemented Stuff
-----------------

-  ☒ Generate authentication token
-  ☒ Read current state of the Environment
-  ☒ Weather
-  ☒ Location
-  ☒ Basic Informations( apversion, pinAssigned, timeZone, … )
-  ☒ Devices (partly)
-  ☒ Client
-  ☒ Groups

Homematic IP Devices:
---------------------

-  ☒ ALPHA-IP-RBG (Alpha IP Wall Thermostat Display)
-  ☒ ALPHA-IP-RBGa (ALpha IP Wall Thermostat Display analog)
-  ☐ ELV-SH-AI8 (Alarmline Interface 8x Inputs) \*powered by HmIP
-  ☐ ELV-SH-BS2 (Switch Actuator for brand switches 2x channels)
   \*powered by HmIP
-  ☐ ELV-SH-GVI (Garden valve interface) \*powered by HmIP
-  ☐ ELV-SH-IRS8 (Infared Remote control - 8x channels) \*powered by
   HmIP
-  ☐ ELV-SH-SW1-BAT (2x Actuator Switch for 30V/1A with 2xAA Batteries)
   \*powered by HmIP
-  ☐ ELV-SH-WUA (Dimming Actuator, 0-10/1-10-V-Control inputs, 8A 230V)
   \*powered by HmIP
-  ☐ ELV-SH-WSC (2x Servo Controls, 5v - 12V) \*powered by HmIP
-  ☒ HMIP-ASIR (Alarm Siren - indoor)
-  ☒ HMIP-ASIR-B1 (Alarm Siren - indoor) *Silvercrest Edition*
-  ☒ HMIP-ASIR-2 (Alarm Siren - indoor) New Version
-  ☒ HMIP-ASIR-O (Alarm Siren - outdoor)
-  ☒ HMIP-BBL (Blind Actuator for brand switches)
-  ☐ HMIP-BBL-2 (Blind Actuator for brand switches) New Version
-  ☒ HMIP-BDT (Dimming Actuator for brand switches)
-  ☒ HMIP-BRC2 (Remote Control for brand switches – 2x channels)
-  ☒ HMIP-BROLL (Shutter Actuator - brand-mount)
-  ☐ HMIP-BROLL-2 (Shutter Actuator - brand-mount) New Version
-  ☒ HMIP-BSL (Switch Actuator for brand switches – with signal lamp)
-  ☒ HMIP-BSM (Brand Switch and Meter Actuator)
-  ☐ HMIP-BSM-I (Brand Switch and Meter Actuator, International)
-  ☒ HMIP-BWTH (Wall Thermostat Display with switching output – for
   brand switches, 230V)
-  ☐ HMIP-BWTH24 (Wall Thermostat Display with switching output – for
   brand switches, 24V)
-  ☒ HMIP-DBB (Doorbell Push-Button)
-  ☒ HMIP-DLD (Door Lock Drive)
-  ☒ HMIP-DLS (Door Lock Sensor)
-  ☒ HMIP-DRBLI4 (Blind Actuator for DIN rail mount – 4 channels)
-  ☒ HMIP-DRSI1 (Switch Actuator for DIN rail mount – 1x channel)
-  ☒ HMIP-DRDI3 (Dimming Actuator Inbound 230V – 3x channels, 200W per
   channel) electrical DIN rail
-  ☒ HMIP-DRSI4 (Switch Actuator for DIN rail mount – 4x channels)
-  ☒ HMIP-DSD-PCB (Door Signal Dector PCB)
-  ☒ HMIP-eTRV (Heating-Thermostat with Display)
-  ☒ HMIP-eTRV-2 (Heating-Thermostat with Display) New Version
-  ☐ HMIP-eTRV-2 I9F (Heating-Thermostat with Display) New Version
-  ☐ HMIP-eTRV-2-UK (UK Version not tested, but it should work)
-  ☒ HMIP-eTRV-B (Heating-Thermostat basic with Display)
-  ☐ HMIP-eTRV-B-2 (Heating-Thermostat basic with Display) New Version
-  ☐ HMIP-eTRV-B-2 R4M (Heating-Thermostat basic with Display) New
   Version
-  ☐ HMIP-eTRV-B-UK (UK Version not tested, but it should work)
-  ☒ HMIP-eTRV-B1 (Heating-Thermostat basic with Display) *Silvercrest
   Edition*
-  ☒ HMIP-eTRV-C (Heating-Thermostat compact without display)
-  ☒ HMIP-eTRV-C-2 (Heating-Thermostat compact without display) New
   Version
-  ☐ HmIP-eTRV-CL (Heating-thermostat compact with dispay)
-  ☒ HMIP-eTRV-E (Heating-Thermostat Design Evo *New Generation*, white)
-  ☐ HMIP-eTRV-E-A (Heating-Thermostat Design Evo *New Generation*,
   anthracite)
-  ☐ HMIP-eTRV-E-S (Heating-Thermostat Design Evo *New Generation*,
   silver)
-  ☒ HMIP-FAL230-C6 (Floor Heating Actuator – 6x channels, 230V)
-  ☒ HMIP-FAL230-C10 (Floor Heating Actuator – 10x channels, 230V)
-  ☒ HMIP-FAL24-C6 (Floor Heating Actuator – 6x channels, 24V)
-  ☒ HMIP-FAL24-C10 (Floor Heating Actuator – 10x channels, 24V)
-  ☒ HMIP-FALMOT-C12 (Floor Heating Actuator – 12x channels, motorised)
-  ☒ HMIP-FBL (Blind Actuator - flush-mount)
-  ☒ HMIP-FCI1 (Contact Interface flush-mount – 1x channel)
-  ☒ HMIP-FCI6 (Contact Interface flush-mount – 6x channels)
-  ☒ HMIP-FDT (Dimming Actuator - flush-mount)
-  ☒ HMIP-FROLL (Shutter Actuator - flush-mount)
-  ☒ HMIP-FSI16 (Switch Actuator with Push-button Input 230V, 16A)
-  ☒ HMIP-FSM (Switch Actuator and Meter 5A – flush-mount)
-  ☒ HMIP-FSM16 (Switch Actuator and Meter 16A – flush-mount)
-  ☐ HMIP-FWI (Wiegand Interface)
-  ☒ HMIP-HAP (Cloud Access Point)
-  ☒ HMIP-HAP-B1 (Cloud Access Point) *Silvercrest Edition*
-  ☒ HMIP-HDM1 (Hunter Douglas & erfal window blinds
-  ☐ HMIP-HDRC (Hunter Douglas & erfal window blinds remote control)
-  ☐ HMIP-K-DRBLI4 (Blinds Actuator – 4x channels, 230V, 2,2A / 500W per
   channel) electrical DIN rail
-  ☐ HMIP-K-DRSI1 (Actuator Inbound 230V – 1x channel) electrical DIN
   rail
-  ☐ HMIP-K-DRDI3 (Dimming Actuator Inbound 230V – 3x channels, 200W per
   channel) electrical DIN rail
-  ☐ HMIP-K-DRSI4 (Switch Actuator – 4x channels, 16A per channel)
   electrical DIN rail
-  ☒ HMIP-KRCA (Key Ring Remote Control & Alarm)
-  ☒ HMIP-KRC4 (Key Ring Remote Control - 4x buttons)
-  ☐ HMIP-MIO16-PCB (Multi Analog/Digitial Interface - Switch Circuit
   Board)
-  ☒ HMIP-MIOB (Multi IO Box for floor heating & cooling)
-  ☒ HMIP-MOD-HO (Garage Door Module for Hörmann)
-  ☒ HMIP-MOD-OC8 (Open Collector Module Receiver - 8x)
-  ☒ HMIP-MOD-RC8 (Open Collector Module Sender - 8x)
-  ☒ HMIP-MOD-TM (Garage Door Module for Novoferm and Tormatic door
   operators)
-  ☐ HMIP-MP3P (Combination Signalling Device MP3)
-  ☐ HMIP-P-DRG-DALI (DALI Lights Gateway)
-  ☒ HMIP-PCBS (Switch Circuit Board - 1x channel)
-  ☒ HMIP-PCBS2 (Switch Circuit Board - 2x channels)
-  ☒ HMIP-PCBS-BAT (Switch Circuit Board with Battery - 1x channel)
-  ☒ HMIP-PDT (Plugable Dimmer)
-  ☐ HMIP-PDT-UK (UK Version not tested, but it should work)
-  ☒ HMIP-PMFS (Plugable Power Supply Monitoring)
-  ☒ HMIP-PS (Plugable Switch)
-  ☐ HMIP-PS-2 (Plugable Switch) New Version
-  ☒ HMIP-PSM (Plugable Switch Measuring, Type F - Standard for
   Homematic)
-  ☐ HMIP-PSM-2 (Plugable Switch Measuring, Type F - Standard for
   Homematic) New Version
-  ☒ HMIP-PSM-CH (Plugable Switch Measuring, Type J)
-  ☐ HMIP-PSM-IT (Type L not tested, but it should work)
-  ☐ HMIP-PSM-PE (Type E not tested, but it should work)
-  ☐ HMIP-PSM-UK (Type G not tested, but it should work)
-  ☒ HMIP-RC8 (Remote Control - 8x buttons)
-  ☐ HMIP-RCB1 (Remote Control - 1x button)
-  ☒ HMIP-SAM (Acceleration Sensor)
-  ☒ HMIP-SCI (Contact Interface Sensor)
-  ☒ HMIP-SCTH230 (CO2, Temperature and Humidity Sensor 230V)
-  ☐ HMIP-SFD (Fine Dust Sensor)
-  ☒ HMIP-SLO (Light Sensor - outdoor)
-  ☒ HMIP-SMI (Motion Detector with Brightness Sensor - indoor)
-  ☒ HMIP-SMI55 (Motion Detector with Brightness Sensor and Remote
   Control - 2x buttons)
-  ☐ HMIP-SMI55-2 (Motion Detector with Brightness Sensor and Remote
   Control - 2x buttons) New Version
-  ☒ HMIP-SMO (Motion Detector with Brightness Sensor - outdoor)
-  ☐ HMIP-SMO-2 (Motion Detector with Brightness Sensor - outdoor) New
   Version
-  ☒ HMIP-SMO-A (Motion Detector with Brightness Sensor - outdoor,
   anthracite)
-  ☐ HMIP-SMO-A-2 (Motion Detector with Brightness Sensor - outdoor,
   anthracite) New Version
-  ☒ HMIP-SPDR (Passage Sensor with Direction Recognition)
-  ☒ HMIP-SPI (Presence Sensor - indoor)
-  ☒ HMIP-SRH (Window Rotary Handle Sensor)
-  ☒ HMIP-SRD (Rain Sensor)
-  ☒ HMIP-STE2-PCB (Temperature Difference Sensors - 2x sensors)
-  ☒ HMIP-STH (Temperature and Humidity Sensor without display - indoor)
-  ☒ HMIP-STHD (Temperature and Humidity Sensor with display - indoor)
-  ☒ HMIP-STHO (Temperature and Humidity Sensor - outdoor)
-  ☒ HMIP-STHO-A (Temperature and Humidity Sensor – outdoor, anthracite)
-  ☒ HMIP-STV (Inclination and vibration Sensor)
-  ☒ HMIP-SWD (Water Sensor)
-  ☒ HMIP-SWDM (Door / Window Contact - magnetic)
-  ☐ HMIP-SWDM-2 (Door / Window Contact - magnetic) New Version
-  ☒ HMIP-SWDM-B2 (Door / Window Contact - magnetic) *Silvercrest
   Edition*
-  ☒ HMIP-SWDO (Shutter Contact Optical)
-  ☐ HMIP-SWDO-2 (Shutter Contact Optical) New Version
-  ☒ HMIP-SWDO-I (Shutter Contact Optical Invisible)
-  ☒ HMIP-SWDO-PL (Shutter Contact Optical Plus)
-  ☐ HMIP-SWDO-PL-2 (Shutter Contact Optical Plus) New Version
-  ☒ HMIP-SWO-B (Weather Sensor - Basic)
-  ☒ HMIP-SWO-PL (Weather Sensor – Plus)
-  ☒ HMIP-SWO-PR (Weather Sensor – Pro)
-  ☒ HMIP-SWSD (Smoke Detector)
-  ☐ HMIP-USBSM (USB Switching Measurement Actuator)
-  ☒ HMIP-WGC (Garage Door Button)
-  ☒ HMIP-WHS2 (Switch Actuator for heating systems – 2x channels)
-  ☐ HMIP-WKP (Keypad)
-  ☒ HMIP-WLAN-HAP (WLAN Access Point)
-  ☒ HMIP-WRC2 (Wall-mount Remote Control - 2x buttons)
-  ☒ HMIP-WRC6 (Wall-mount Remote Control - 6x buttons)
-  ☒ HMIP-WRCC2 (Wall-mount Remote Control – flat)
-  ☐ HMIP-WRCD (Wall-mount Remote Control - E-Paper-Status display)
-  ☐ HMIP-WRCR (Wall-mount Remote Control - Rotary)
-  ☐ HMIP-WT (Wall Mounted Thermostat without adjusting wheel) #probably
   only prototype for WTH-B and was not released
-  ☒ HMIP-WTH (Wall Mounted Thermostat Pro with Display)
-  ☐ HMIP-WTH-1 (Wall Mounted Thermostat Pro with Display *Newest
   Version* - successor of WTH-2 - really)
-  ☒ HMIP-WTH-2 (Wall Mounted Thermostat Pro with Display)
-  ☒ HMIP-WTH-B (Wall Mounted Thermostat basic without adjusting wheel)
-  ☐ HMIP-WTH-B-2 (Wall Mounted Thermostat basic without adjusting
   wheel) New Version
-  ☐ HMIP-WUA (Dimming Actuator, 0-10/1-10-V-Control inputs, 8A 230V)

Homematic IP Wired Devices (no radio signal):
---------------------------------------------

-  ☒ HMIPW-DRAP (Homematic IP Wired Access Point)
-  ☐ HMIPW-BRC2 (Homematic IP Wired Remote Control for brand switches –
   2x channels)
-  ☒ HMIPW-DRBL4 (Homematic IP Wired Blinds Actuator – 4x channels)
-  ☒ HMIPW-DRD3 (Homematic IP Wired Dimming Actuator – 3x channels)
-  ☒ HMIPW-DRS4 (Homematic IP Wired Switch Actuator – 4x channels)
-  ☐ HMIPW-DRI16 (Homematic IP Wired Inbound module – 16x channels)
-  ☒ HMIPW-DRI32 (Homematic IP Wired Inbound module – 32x channels)
-  ☒ HMIPW-DRS8 (Homematic IP Wired Switch Actuator – 8x channels)
-  ☐ HMIPW-FAL24-C6 (Homematic IP Wired Floor Heating Actuator – 6x
   channels, 24V)
-  ☐ HMIPW-FAL24-C10 (Homematic IP Wired Floor Heating Actuator – 10x
   channels, 24V)
-  ☐ HMIPW-FAL230-C6 (Homematic IP Wired Floor Heating Actuator – 6x
   channels, 230V)
-  ☐ HMIPW-FAL230-C10 (Homematic IP Wired Floor Heating Actuator – 10x
   channels, 230V)
-  ☒ HMIPW-FALMOT-C12 (Homematic IP Wired Floor Heating Actuator – 12x
   channels, motorised)
-  ☒ HMIPW-FIO6 (Homematic IP Wired IO Module flush-mount – 6x channels)
-  ☐ HMIPW-SCTHD (Homematic IP Wired CO2, Temperature and Humidity
   Sensor with Display)
-  ☒ HMIPW-SMI55 (Homematic IP Wired Motion Detector with Brightness
   Sensor and Remote Control - 2x buttons)
-  ☐ HMIPW-SPI (Homematic IP Wired Presence Sensor - indoor)
-  ☐ HMIPW-STH (Homematic IP Wired Temperature and Humidity Sensor
   without display - indoor)
-  ☐ HMIPW-STHD (Homematic IP Wired Temperature and Humidity Sensor with
   display - indoor)
-  ☐ HMIPW-WGD (Homematic IP Wired Wall-mount Glas Display - black
   edition)
-  ☐ HMIPW-WGD-PL (Homematic IP Wired Wall-mount Glas Display Play -
   black edition)
-  ☒ HMIPW-WRC2 (Homematic IP Wired Wall-mount Remote Control - 2x
   channels)
-  ☒ HMIPW-WRC6 (Homematic IP Wired Wall-mount Remote Control - 6x
   channels)
-  ☐ HMIPW-WTH (Homematic IP Wired Wall Mounted Thermostat Pro with
   Display)

Events
------

It’s also possible to use push notifications based on a websocket
connection:

.. code:: python

       # Example function to display incoming events.
       def print_events(event_list):
           for event in event_list:
               print("EventType: {} Data: {}".format(event["eventType"], event["data"]))


       # Initialise the API.
       config = homematicip.find_and_load_config_file()
       home = Home()
       home.set_auth_token(config.auth_token)
       home.init(config.access_point)

       # Add function to handle events and start the connection.
       home.onEvent += print_events
       home.enable_events()

       try:
           while True:
               time.sleep(1)
       except KeyboardInterrupt:
           print("Interrupt.")

Pathes for config.ini
---------------------

The scripts will look for a config.ini in 3 different locations
depending on your OS. Copy the file to one of these locations so that it
will be accessible for the scripts.

-  General

   -  current working directory

-  Windows

   -  %APPDATA%\\homematicip-rest-api
   -  %PROGRAMDATA%\\homematicip-rest-api

-  Linux

   -  ~/.homematicip-rest-api/
   -  /etc/homematicip-rest-api/

-  MAC OS

   -  ~/Library/Preferences/homematicip-rest-api/
   -  /Library/Application Support/homematicip-rest-api/

.. |PyPI download month| image:: https://img.shields.io/pypi/dm/homematicip.svg
   :target: https://pypi.python.org/pypi/homematicip/
.. |PyPI version fury.io| image:: https://badge.fury.io/py/homematicip.svg
   :target: https://pypi.python.org/pypi/homematicip/
.. |Discord| image:: https://img.shields.io/discord/537253254074073088.svg?logo=discord&style=plastic
   :target: https://discord.gg/mZG2myJ
.. |CircleCI| image:: https://circleci.com/gh/hahn-th/homematicip-rest-api.svg?style=shield
   :target: https://circleci.com/gh/hahn-th/homematicip-rest-api
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/homematicip
