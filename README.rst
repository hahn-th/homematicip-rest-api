homematicip-rest-api
====================

A **Python 3** wrapper for the homematicIP REST API (Access Point Based)
Since there is no official documentation about this API everything was
done via reverse engineering. Use at your own risk.

|discord| |CircleCI| |Docs| |PyPi| |codecov| |Average time to resolve an issue| |commits-since-latest-release| |donate-paypal|

Documentation
=============
Documentation can be found under https://homematicip-rest-api.readthedocs.io

Installation
============

Just run **pip3 install -U homematicip** to get the package

Usage
=====

first run hmip_generate_auth_token.py (from the command line) to get an
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

-  [X] generate authentication token
-  [X] Read current state of the Environment
-  [X] Weather
-  [X] Location
-  [X] Basic Informations( apversion, pinAssigned, timeZone, … )
-  [X] Devices (partly)
-  [X] Client
-  [X] Groups

Devices:
--------

-  [X] HMIP-ASIR, HMIP-ASIR-B1 (Alarm Siren)
-  [ ] HMIP-ASIR-O
-  [ ] HMIP-BBL
-  [X] HMIP-BDT (Dimming Actuator for brand switches)
-  [ ] HMIP-BRC2
-  [X] HMIP-BROLL (Shutter Actuator - brand-mount)
-  [ ] HMIP-BSL
-  [X] HMIP-BSM (Brand Switch and Meter)
-  [X] HMIP-BWTH (Brand Wall Mounted Thermostat Pro)
-  [ ] HMIP-BWTH24
-  [ ] HMIP-DBB
-  [X] HMIP-eTRV, HMIP-eTRV2, HMIP-eTRV-B1 (Heating-thermostat)
-  [ ] HMIP-eTRV-2-UK  (not tested, but it should work)
-  [ ] HMIP-eTRV-B     (not tested, but it should work)
-  [ ] HMIP-eTRV-C     (not tested, but it should work)
-  [X] HMIP-FAL230-C6 (Floor Terminal Block)
-  [ ] HMIP-FAL230-C10
-  [ ] HMIP-FAL24-C6
-  [ ] HMIP-FAL24-C10
-  [X] HMIP-FCI1 (Contact Interface flush-mount – 1 channel)
-  [ ] HMIP-FCI6
-  [X] HMIP-FDT (Dimming Actuator flush-mount)
-  [X] HMIP-FROLL (Shutter Actuator - flush-mount)
-  [X] HHMIP-FSM
-  [ ] HMIP-FSM16 (not tested, but it should work)
-  [X] HMIP-KRCA (Key Ring Remote Control & alarm)
-  [ ] HMIP-KRC4
-  [ ] HMIP-MIOB
-  [X] HMIP-MOD-OC8 ( Open Collector Module )
-  [ ] HMIP-MP3P
-  [ ] HMIP-PCBS 
-  [ ] HMIP-PCBS2
-  [X] HMIP-PCBS-BAT (Printed Curcuit Board Switch Battery)
-  [X] HMIP-PDT (Pluggable Dimmer)
-  [ ] HMIP-PDT-UK      (not tested, but it should work)
-  [ ] HMIP-PMFS
-  [X] HMIP-PS (Plugable Switch)
-  [X] HMIP-PSM (Plugable Switch Measuring)
-  [ ] HMIP-PSM-CH      (not tested, but it should work)
-  [ ] HMIP-PSM-IT      (not tested, but it should work)
-  [ ] HMIP-PSM-PE      (not tested, but it should work)
-  [ ] HMIP-PSM-UK      (not tested, but it should work)
-  [X] HMIP-RC8 (Remote Control - 8 buttons)
-  [ ] HMIP-RCB1
-  [ ] HMIP-SAM
-  [ ] HMIP-SLO
-  [X] HMIP-SMI (Motion Detector with Brightness Sensor - indoor)
-  [X] HMIP-SMI55 (Motion Detector with Brightness Sensor and Remote Control - 2-button)
-  [X] HMIP-SMO, HMIP-SMO-A (Motion Detector with Brightness Sensor - outdoor)
-  [X] HMIP-SPI (Precence Sensor - indoor)
-  [X] HMIP-SRH (Rotary Handle Sensor)
-  [X] HMIP-STH (Temperature and Humidity Sensor without display - indoor)
-  [X] HMIP-STHD (Temperature and Humidity Sensor with display - indoor)
-  [X] HMIP-STHO (Temperature and Humidity Sensor outdoor)
HMIP-STHO-A
-  [X] HMIP-SWD (Water Sensor)
-  [X] HMIP-SWDO (Shutter Contact)
-  [X] HMIP-SWDO-I (Shutter Contact Invisible)
-  [X] HMIP-SWDM (Door / Window Contact - magnetic )
-  [X] HMIP-SWDM-B2  (Door / Window Contact - magnetic )
-  [X] HMIP-SWO-B (Weather Sensor)
-  [X] HMIP-SWO-PL (Weather Sensor – plus)
-  [X] HMIP-SWO-PR (Weather Sensor – pro)
-  [X] HMIP-SWSD (Smoke Detector)
HMIP-WGC
HMIP-WHS2
-  [X] HMIP-WRC2 (Wall-mount Remote Control - 2-button)
-  [X] HMIP-WRC6 (Wall-mount Remote Control - 6-button)
-  [X] HMIP-WTH, HMIP-WTH-2 (Wall Mounted Thermostat Pro)


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
   :target: https://discord.gg/mZG2myJ.. |Docs| image:: https://readthedocs.org/projects/homematicip-rest-api/badge/?version=documentation
   :target: https://homematicip-rest-api.readthedocs.io