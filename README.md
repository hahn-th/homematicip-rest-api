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
* list_devices.py - this file will list all (yet implemented) devices from your AP and will print some informations about them
* list_groups.py this file will list all groups from your AP and will print some informations about them
* list_securityJournal.py this file will list all events from the security journal
* show_firmware.py - this file shows current and available firmware versions of all devices

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
- [X] HMIP-SWDO (Shutter Contact)
- [X] HMIP-SWSD (Smoke Detector)
- [X] HMIP-FAL230-C6 (Floor Terminal Block)
- [X] HMIP-PSM (Plugable Switch Measuring)
- [X] HMIP-STHD (Temperature and Humidity Sensor with display - indoor)
- [X] HMIP-WRC2 (Wall-mount Remote Control - 2-button)
- [X] HMIP-ASIR (Alarm Siren)
- [X] HMIP-KRCA (Key Ring Remote Control – alarm)
- [X] HMIP-SMI (Motion Detector with Brightness Sensor - indoor)

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


## Implemented Functions: ##
### General ###
- [X] getCurrentState (this reads the base configuration for the whole AP)
- [X] setZonesActivation (activates the alarm zones (internal and/or external))
- [X] everything needed for a successfull registration/authentication
- [X] setLocation
- [X] setPin

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

### Alarm ###
- [X] testSignalOptical
- [X] setSignalOptical
