homematicip-rest-api
====================

A **Python 3** wrapper for the homematicIP REST API (Access Point Based)
Since there is no official documentation about this API everything was
done via reverse engineering Use at your own risk.

|CircleCI| |PyPi| |codecov| |Average time to resolve an issue| |commits-since-latest-release|

Installation
============

Just run **pip3 install homematicip** to get the package

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

   -  %APPDATA%:raw-latex:`\homematicip`-rest-api
   -  %PROGRAMDATA%:raw-latex:`\homematicip`-rest-api

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

-  [X] HMIP-eTRV (Heating-thermostat)
-  [X] HMIP-WTH, HMIP-WTH-2 (Wall Mounted Thermostat Pro)
-  [X] HMIP-BWTH (Brand Wall Mounted Thermostat Pro)
-  [X] HMIP-SWDO (Shutter Contact)
-  [X] HMIP-SWDO-I (Shutter Contact Invisible)
-  [X] HMIP-SWSD (Smoke Detector)
-  [X] HMIP-FAL230-C6 (Floor Terminal Block)
-  [X] HMIP-PS (Plugable Switch)
-  [X] HMIP-PSM (Plugable Switch Measuring)
-  [X] HMIP-STHD (Temperature and Humidity Sensor with display - indoor)
-  [X] HMIP-STH (Temperature and Humidity Sensor without display -
   indoor)
-  [X] HMIP-WRC2 (Wall-mount Remote Control - 2-button)
-  [X] HMIP-ASIR (Alarm Siren)
-  [X] HMIP-KRCA (Key Ring Remote Control & alarm)
-  [X] HMIP-SMI (Motion Detector with Brightness Sensor - indoor)
-  [X] HMIP-FROLL (Shutter Actuator - flush-mount)
-  [X] HMIP-BROLL (Shutter Actuator - brand-mount)
-  [X] HMIP-SPI (Precence Sensor - indoor)
-  [X] HmIP-PDT (Pluggable Dimmer)
-  [X] HMIP-BSM (Brand Switch and Meter)
-  [X] HmIP-PCBS-BAT (Printed Curcuit Board Switch Battery)
-  [X] HmIP-STHO (Temperature and Humidity Sensor outdoor)
-  [X] HmIP-SWO-PR (Weather Sensor – pro)
-  [X] HmIP-SWO-B (Weather Sensor)
-  [X] HmIP-SRH (Rotary Handle Sensor )

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
