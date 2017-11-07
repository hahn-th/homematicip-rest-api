# homematicip-rest-api #
A python wrapper for the homematicIP REST API (Access Point Based)
Since there is no official documentation about this API everything was done via reverse engineering
Use at your own risk.

#Installation
Just run **pip install homematicip** to get the package

# Usage #
first download and run generate_auth_token.py to get an auth token for your access point.
copy the generated auth token from the window config.py and add also the Access Point ID

# Examples #
* homematicip_cli.py list devices,groups,securityJournal; set label, turn switches on/off

# Implemented Stuff #
- [X] generate authentication token
- [X] Read current state of the Environment
- [X] Weather
- [X] Location
- [X] Basic Informations( apversion, pinAssigned, timeZone, ... )
- [X] Devices (partly)
- [X] Client
- [X] Groups

## Devices: ##
- [X] HMIP-eTRV (Heating-thermostat)
- [X] HMIP-WTH, HMIP-WTH-2 (Wall Mounted Thermostat Pro)
- [X] HMIP-BWTH (Brand Wall Mounted Thermostat Pro)
- [X] HMIP-SWDO (Shutter Contact)
- [X] HMIP-SWDO-I (Shutter Contact Invisible)
- [X] HMIP-SWSD (Smoke Detector)
- [X] HMIP-FAL230-C6 (Floor Terminal Block)
- [X] HMIP-PS (Plugable Switch)
- [X] HMIP-PSM (Plugable Switch Measuring)
- [X] HMIP-STHD (Temperature and Humidity Sensor with display - indoor)
- [X] HMIP-WRC2 (Wall-mount Remote Control - 2-button)
- [X] HMIP-ASIR (Alarm Siren)
- [X] HMIP-KRCA (Key Ring Remote Control & alarm)
- [X] HMIP-SMI (Motion Detector with Brightness Sensor - indoor)
- [X] HMIP-FROLL (Shutter Actuator - flush-mount)
- [X] HMIP-BROLL (Shutter Actuator - brand-mount)

## Groups ##
- [X] Meta (Rooms)
- [X] Heating
- [X] Security
- [X] Switching
- [X] Switch Groups
- [X] INBOX
- [X] HEATING_TEMPERATURE_LIMITER
- [X] HEATING_HUMIDITY_LIMITER
- [X] SECURITY_ZONE
- [X] ALARM_SWITCHING
- [X] HEATING_CHANGEOVER
- [X] LINKED_SWITCHING
- [X] HEATING_COOLING_DEMAND
- [X] HEATING_DEHUMIDIFIER
- [X] HEATING_EXTERNAL_CLOCK
- [X] HEATING_COOLING_DEMAND_BOILER 
- [X] HEATING_COOLING_DEMAND_PUMP
- [X] OVER_HEAT_PROTECTION_RULE
- [X] SMOKE_ALARM_DETECTION_RULE
- [X] LOCK_OUT_PROTECTION_RULE
- [X] SHUTTER_WIND_PROTECTION_RULE

## Events ##
It's also possible to use push notifications based on a websocket connection
```python
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
        print u"EventType: {} Data: {}".format(event["eventType"], event["data"])

#if needed you can close the websocket connection with
home.disable_events()




```

## Implemented Functions: ##
### General ###
- [X] getCurrentState (this reads the base configuration for the whole AP)
- [X] setZonesActivation (activates the alarm zones (internal and/or external))
- [X] everything needed for a successfull registration/authentication
- [X] setLocation
- [X] setPin
- [X] deleteGroup
- [X] getOAuthOTK (Get Token for Alexa)
- [X] setTimeZone
- [X] setPowerMeterUnitPrice

### Heating ###
- [X] setBoost
- [X] setSetPointTemperature
- [X] getProfile
- [X] updateProfile
- [X] activateAbsenceWithDuration
- [X] activateAbsenceWithPeriod
- [X] activateVacation
- [X] deactivateVacation
- [X] deactivateAbsence

### Security ###
- [X] getSecurityJournal
- [X] setIntrusionAlertThroughSmokeDetectors

### Device ###
- [X] setClimateControlDisplay
- [X] setDeviceLabel
- [X] setSwitchState (turn on/off)
- [X] setShutterLevel
- [X] setShutterStop

### Alarm ###
- [X] testSignalOptical
- [X] setSignalOptical
