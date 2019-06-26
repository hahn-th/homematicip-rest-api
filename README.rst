homematicip-rest-api
====================

A **Python 3** wrapper for the homematicIP REST API (Access Point Based)
Since there is no official documentation about this API everything was
done via reverse engineering. Use at your own risk.

Any help from the community thru e.g. Pull Request would be highly appreciated.

|discord| |CircleCI| |Docs| |PyPi| |codecov| |requirements| |Average time to resolve an issue| |commits-since-latest-release| |donate-paypal|

Documentation
=============
Documentation can be found under https://homematicip-rest-api.readthedocs.io

Installation
============

Just run **pip3 install -U homematicip** to get the package

Usage
=====

First run hmip_generate_auth_token.py (from the command line) to get an
auth token for your access point. it will generate a “config.ini” in
your current directory. The scripts will look for a config.ini in 3
different locations depending on your OS. Copy the file to one of these
locations so that it will be accessable for the scripts.

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

Examples
========

-  hmip_cli.py for list devices,groups,securityJournal; set label, turn
   switches on/off
-  Sample Projects are under
   https://github.com/coreGreenberet/homematicip-samples

Implemented Stuff
=================

-  [X] Generate authentication token
-  [X] Read current state of the Environment
-  [X] Weather
-  [X] Location
-  [X] Basic Informations( apversion, pinAssigned, timeZone, … )
-  [X] Devices (partly)
-  [X] Client
-  [X] Groups

Homematic IP Devices:
---------------------

-  [X] HMIP-ASIR, HMIP-ASIR-B1 (Alarm Siren - indoor)
-  [ ] HMIP-ASIR-2     (Alarm Siren2 - indoor)
-  [ ] HMIP-ASIR-O     (Alarm Siren - outdoor)
-  [X] HMIP-BBL        (Blind Actuator for brand switches)
-  [X] HMIP-BDT        (Dimming Actuator for brand switches)
-  [X] HMIP-BRC2       (Remote Control for brand switches – 2x channels)
-  [X] HMIP-BROLL      (Shutter Actuator - brand-mount)
-  [X] HMIP-BSL        (Switch Actuator for brand switches – with signal lamp)
-  [X] HMIP-BSM        (Brand Switch and Meter Actuator)
-  [X] HMIP-BWTH       (Wall Thermostat Display with switching output – for brand switches, 230V)
-  [ ] HMIP-BWTH24     (Wall Thermostat Display with switching output – for brand switches, 24V)
-  [ ] HMIP-DBB        (Doorbell Push-Button)
-  [X] HMIP-eTRV, HMIP-eTRV2, HMIP-eTRV-B1 (Heating-Thermostat with Display)
-  [ ] HMIP-eTRV-2-UK  (UK Version not tested, but it should work)
-  [ ] HMIP-eTRV-B     (Heating-Thermostat with Display not tested, but it should work)
-  [X] HMIP-eTRV-C     (Heating-thermostat compact without display)
-  [X] HMIP-FAL230-C6  (Floor Heating Actuator – 6x channels, 230V)
-  [X] HMIP-FAL230-C10 (Floor Heating Actuator – 10x channels, 230V)
-  [X] HMIP-FAL24-C6   (Floor Heating Actuator – 6x channels, 24V)
-  [X] HMIP-FAL24-C10  (Floor Heating Actuator – 10x channels, 24V)
-  [ ] HMIP-FALMOT-C12 (Floor Heating Actuator – 12x channels, motorised)
-  [X] HMIP-FBL        (Blind Actuator - flush-mount)
-  [X] HMIP-FCI1       (Contact Interface flush-mount – 1x channel)
-  [ ] HMIP-FCI6       (Contact Interface flush-mount – 6x channels)
-  [X] HMIP-FDT        (Dimming Actuator - flush-mount)
-  [X] HMIP-FROLL      (Shutter Actuator - flush-mount)
-  [X] HMIP-FSM        (Switch Actuator and Meter 5A – flush-mount)
-  [X] HMIP-FSM16      (Switch Actuator and Meter 16A – flush-mount)
-  [X] HMIP-KRCA       (Key Ring Remote Control & Alarm)
-  [X] HMIP-KRC4       (Key Ring Remote Control - 4x buttons)
-  [ ] HMIP-MIO16-PCB  (Multi Analog/Digitial Interface - Switch Circuit Board)
-  [X] HMIP-MIOB       (Multi IO Box for floor heating & cooling)
-  [X] HMIP-MOD-OC8    (Open Collector Module Receiver - 8x)
-  [ ] HMIP-MOD-RC8    (Open Collector Module Sender - 8x)
-  [ ] HMIP-MOD-TM     (Garage Door Module for Novoferm and Tormatic door operators)
-  [ ] HMIP-MP3P       (Combination Signalling Device MP3)
-  [X] HMIP-PCBS       (Switch Circuit Board - 1x channel)
-  [X] HMIP-PCBS2      (Switch Circuit Board - 2x channels)
-  [X] HMIP-PCBS-BAT   (Switch Circuit Board with Battery - 1x channel)
-  [X] HMIP-PDT        (Plugable Dimmer)
-  [ ] HMIP-PDT-UK     (UK Version not tested, but it should work)
-  [ ] HMIP-PMFS       (Plugable Power Supply Monitoring)
-  [X] HMIP-PS         (Plugable Switch)
-  [X] HMIP-PSM        (Plugable Switch Measuring, Type F - Standard for Homematic)
-  [ ] HMIP-PSM-CH     (Type J not tested, but it should work)
-  [ ] HMIP-PSM-IT     (Type L not tested, but it should work)
-  [ ] HMIP-PSM-PE     (Type E not tested, but it should work)
-  [ ] HMIP-PSM-UK     (Type G not tested, but it should work)
-  [X] HMIP-RC8        (Remote Control - 8x buttons)
-  [ ] HMIP-RCB1       (Remote Control - 1x button)
-  [ ] HMIP-SAM        (Acceleration Sensor)
-  [ ] HMIP-SCI        (Contact Interface Sensor)
-  [X] HMIP-SLO        (Light Sensor - outdoor)
-  [X] HMIP-SMI        (Motion Detector with Brightness Sensor - indoor)
-  [X] HMIP-SMI55      (Motion Detector with Brightness Sensor and Remote Control - 2x buttons)
-  [X] HMIP-SMO        (Motion Detector with Brightness Sensor - outdoor)
-  [X] HMIP-SMO-A      (Motion Detector with Brightness Sensor - outdoor, anthracite)
-  [X] HMIP-SPI        (Presence Sensor - indoor)
-  [X] HMIP-SRH        (Window Rotary Handle Sensor)
-  [X] HMIP-STH        (Temperature and Humidity Sensor without display - indoor)
-  [X] HMIP-STHD       (Temperature and Humidity Sensor with display - indoor)
-  [X] HMIP-STHO       (Temperature and Humidity Sensor - outdoor)
-  [X] HMIP-STHO-A     (Temperature and Humidity Sensor – outdoor, anthracite)
-  [X] HMIP-SWD        (Water Sensor)
-  [X] HMIP-SWDO       (Shutter Contact)
-  [X] HMIP-SWDO-I     (Shutter Contact Invisible)
-  [X] HMIP-SWDM       (Door / Window Contact - magnetic)
-  [X] HMIP-SWDM-B2    (Door / Window Contact - magnetic)
-  [X] HMIP-SWO-B      (Weather Sensor - Basic)
-  [X] HMIP-SWO-PL     (Weather Sensor – Plus)
-  [X] HMIP-SWO-PR     (Weather Sensor – Pro)
-  [X] HMIP-SWSD       (Smoke Detector)
-  [ ] HMIP-WGC        (Garage Door Button)
-  [ ] HMIP-WHS2       (Switch Actuator for heating systems – 2x channels)
-  [X] HMIP-WRC2       (Wall-mount Remote Control - 2x buttons)
-  [X] HMIP-WRC6       (Wall-mount Remote Control - 6x buttons)
-  [ ] HMIP-WRCD       (Wall-mount Remote Control - E-Paper-Status display)
-  [ ] HMIP-WT         (Wall Mounted Thermostat without Display)
-  [X] HMIP-WTH, HMIP-WTH-2 (Wall Mounted Thermostat Pro with Display)

Homematic IP Wired Devices:
---------------------------

-  [ ] HMIPW-DRAP       (Homematic IP Wired Access Point)
-  [ ] HMIPW-DRBL4      (Homematic IP Wired Blinds Actuator – 4x channels)
-  [ ] HMIPW-DRD3       (Homematic IP Wired Dimming Actuator – 3x channels)
-  [ ] HMIPW-DRS4       (Homematic IP Wired Swich Actuator – 4x channels)
-  [ ] HMIPW-DRI16      (Homematic IP Wired Inbound module – 16x channels)
-  [ ] HMIPW-DRI32      (Homematic IP Wired Inbound module – 32x channels)
-  [ ] HMIPW-DRS8       (Homematic IP Wired Switch Actuator – 8x channels)
-  [ ] HMIPW-FAL24-C6   (Homematic IP Wired Floor Heating Actuator – 6x channels, 24V)
-  [ ] HMIPW-FAL24-C10  (Homematic IP Wired Floor Heating Actuator – 10x channels, 24V)
-  [ ] HMIPW-FAL230-C6  (Homematic IP Wired Floor Heating Actuator – 6x channels, 230V)
-  [ ] HMIPW-FAL230-C10 (Homematic IP Wired Floor Heating Actuator – 10x channels, 230V)
-  [ ] HMIPW-FIO6       (Homematic IP Wired IO Module flush-mount – 6x channels) 
-  [ ] HMIPW-STH        (Homematic IP Wired Temperature and Humidity Sensor without display - indoor)
-  [ ] HMIPW-STHD       (Homematic IP Wired Temperature and Humidity Sensor with display - indoor)
-  [ ] HMIPW-WTH        (Homematic IP Wired Wall Mounted Thermostat Pro with Display)

Events
------

It’s also possible to use push notifications based on a websocket
connection

.. code:: python

    ##initialize the api
    #...
    #get the home object
    home = homematicip.Home()
    #add a function to handle new events
    home.onEvent += printEvents
    #enable the event connection -> this will also start the websocket connection to the homeMaticIP Cloud
    home.enable_events()


    #example function to display incoming events
    def printEvents(eventList):
        for event in eventList:
            print "EventType: {} Data: {}".format(event["eventType"], event["data"])

    #if needed you can close the websocket connection with
    home.disable_events()

.. |CircleCI| image:: https://circleci.com/gh/coreGreenberet/homematicip-rest-api.svg?style=shield
   :target: https://circleci.com/gh/coreGreenberet/homematicip-rest-api
.. |PyPi| image:: https://badge.fury.io/py/homematicip.svg
   :target: https://badge.fury.io/py//homematicip
.. |codecov| image:: https://codecov.io/gh/coreGreenberet/homematicip-rest-api/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/coreGreenberet/homematicip-rest-api
.. |Average time to resolve an issue| image:: http://isitmaintained.com/badge/resolution/coreGreenberet/homematicip-rest-api.svg
   :target: http://isitmaintained.com/project/coreGreenberet/homematicip-rest-api
.. |commits-since-latest-release| image:: https://img.shields.io/github/commits-since/coreGreenberet/homematicip-rest-api/latest.svg 
.. |donate-paypal| image:: https://img.shields.io/badge/Donate-PayPal-green.svg 
   :target: https://paypal.me/coreGreenberet
.. |discord| image:: https://img.shields.io/discord/537253254074073088.svg?logo=discord&style=plastic
   :target: https://discord.gg/mZG2myJ
.. |Docs| image:: https://readthedocs.org/projects/homematicip-rest-api/badge/?version=latest
   :target: https://homematicip-rest-api.readthedocs.io
.. |requirements| image:: https://requires.io/github/coreGreenberet/homematicip-rest-api/requirements.svg?branch=master
   :target: https://requires.io/github/coreGreenberet/homematicip-rest-api/requirements/?branch=master
