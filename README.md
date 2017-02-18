# homematicip-rest-api #
A python wrapper for the homematicIP REST API (Access Point Based)
Since there is no official documentation about this API everything was done via reverse engineering
Use at your own risk.

# Usage #
first run generate_auth_token.py to get an auth token for your access point.
copy the generated auth token from the window config.py and add also the Access Point ID

# Examples #
* list_devices.py - this file will list all (yet implemented) devices from your AP and will print some informations about them
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
- [X] HmIP-eTRV (Heating-thermostat)
- [X] HmIP-WTH-2 (Wall Mounted Thermostat Pro)
- [X] HmIP-SWDO (Shutter Contact)
- [X] HmIP-SWSD (Smoke Detector)
- [X] HmIP-FAL230-C6 (Floor Terminal Block)
- [X] HMIP-PSM (Plugable Switch Measuring)

## Groups ##
- [X] Meta (Rooms)
- [ ] Heating
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

## Implemented Functions: ##
### General ###
- [X] getCurrentState (this reads the base configuration for the whole AP)
- [X] setZonesActivation (activates the alarm zones (internal and/or external))
- [X] everything needed for a successfull registration/authentication
- [X] setLocation
- [X] setPin

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
- [X] setDeviceLabel
- [X] setSwitchState (turn on/off)

### Alarm ###
- [ ] testSignalOptical
- [ ] setSignalOptical
