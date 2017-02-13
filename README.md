# homematicip-rest-api #
A python wrapper for the homematicIP REST API (Access Point Based)
Since there is no official documentation about this API everything was done via reverse engineering
Use at your own risk.

# Usage #
first run generate_auth_token.py to get an auth token for your access point.
copy the generated auth token from the window config.py and add also the Access Point ID

# Examples #
* list_devices.py - this file will list all (yet implemented) devices from your AP and will print some informations about them

# Implemented Stuff #
- [X] generate authentication token
- [X] Read current state of the Environment
- [X] Weather
- [X] Location
- [X] Basic Informations( apversion, pinAssigned, timeZone, ... )
- [X] Devices (partly)
- [X] Client
- [ ] Groups

## Devices: ##
- [X] HMIP-eTRV (Heating-thermostat)
- [X] HmIP-WTH-2 (Wall Mounted Thermostat Pro)
- [X] HMIP-SWDO (Shutter Contact)
- [X] HmIP-SWSD (Smoke Detector)

## Implemented Functions: ##
### General ###
- [X] getCurrentState (this reads the base configuration for the whole AP)
- [X] setZonesActivation (activates the alarm zones (internal and/or external))
- [X] everything needed for a successfull registration/authentication
- [X] setLocation

### Heating ###
- [ ] setBoost
- [ ] getProfile
- [ ] updateProfile
- [X] activateAbsenceWithDuration
- [X] activateAbsenceWithPeriod
- [X] activateVacation
- [X] deactivateVacation
- [X] deactivateAbsence

### Security ###
- [ ] getSecurityJournal
- [X] setIntrusionAlertThroughSmokeDetectors

### Device ###
- [X] setClimateControlDisplay

### Alarm ###
- [ ] testSignalOptical
- [ ] setSignalOptical
