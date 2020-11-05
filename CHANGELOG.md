# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### ADDED
- API
    - Devices
      - [HMIP-HDM1] (Hunter Douglas & erfal window blinds)
      - [HMIP-HAP] (HomematicIP Access Point)


### CHANGED

- [BUG: 342] NameError: name 'xrange' is not defined on Python 3.8.1

## [0.11.0] 2020-08-31

### ADDED
- API
    - Devices
      - HMIPW-DRD3 (Homematic IP Wired Dimming Actuator – 3x channels)
      - HMIPW-DRS8 (Homematic IP Wired Switch Actuator – 8x channels)
      - HMIPW-DRI32 (Homematic IP Wired Inbound module – 32x channels)
      - HMIP-STV (Inclination and vibration Sensor)
      - Fields
        - connectionType
        - new OptionalFeatures
    - Home
      - accessPointUpdateStates
	  
### CHANGED

- [BUG: 325] Requirements are now using a min version instead of a pinned version. requirements_dev.txt will still use the pinned versions to make sure that the latest version is compatible with the library.

## [0.10.19] 2020-07-08

### FIXED
- [PR: 320] Fix FSI-16

## [0.10.18] 2020-06-07

### Added
- Devices
  - [HMIP-MOD-HO] (Module for Hörmann drives)
  - [HMIP-FSI16] (Switch Actuator with Push-button Input 230V, 16A)
  - [HMIP-SWDO-PL] (Shutter Contact Plus)
- CLI
  - --channel parameter for turning on/off different channels and not just the first one

## [0.10.17] 2020-02-16

### FIXED
- [PR: 300] Fix AsyncMotionDetectorPushButton

## [0.10.16] 2020-02-16

### Added
- Devices
  - [HMIP-WTH-B] (Wall Thermostat Basic)
  - [ALPHA-IP-RBG]  (Alpha IP Wall Thermostat Display)
  - [ALPHA-IP-RBGa] (ALpha IP Wall Thermostat Display analog)
### FIXED
- [BUG: 294]: hmip_cli.py --anonymize will wrongly anonymize other fields

## [0.10.15] 2019-12-30
### Added
- API
  - Groups
    - Created new Async/SwitchBaseGroup class for groups which are using on, dimLevel, lowbat and dutycycle
    - ShutterProfile
- Devices
  - [HMIP-FALMOT-C12] (Floor Heating Actuator – 12x channels, motorised)
  - [HMIP-WHS2]       (Switch Actuator for heating systems – 2x channels)
  - [HMIP-PMFS]       (Pluggable Power Supply Monitoring)

## [0.10.14] - 2019-12-22
### Added
- API
  - FunctionalChannels:
    - DOOR_CHANNEL
    - DEVICE_RECHARGEABLE_WITH_SABOTAGE
  - ExtendedLinkedShutterGroup.set_slats_level 
    - added missing attributes
- Devices
  - HMIP-MOD-TM (Garage Door Module for Novoferm and Tormatic door operators)
  - HMIP-ASIR-O (Alarm Siren - outdoor)

- Groups
  - HOT_WATER
- Python 3.8 support

### Changed
- General
  - removed homematicip-testing package. Pip will automatically install the latest tagged release. For a "nightly" build you just have to run it with the "--pre" argument.
### FIXED
- [BUG: 266]: Anonymize won't work on the Silvercrest models

## [0.10.13] - 2019-10-19
### Changed
- API
  - converted FakeCloudServer to an async implementation
  - the Home websocket can now automatically reopen a lost connection (default)
## [0.10.12] - 2019-09-27
### Added
- API
  - Added event handlers for adding/updating/removing devices and groups
  - fixed cloud bug: DEVICE/GROUP_ADDED will now be generated instead of DEVICE/GROUP_CHANGED on an added device
  
## [0.10.11] - 2019-09-23
### Added
- Devices
  - HMIP-MOD-RC8 (Open Collector Module Sender - 8x)
  - HMIP-SAM     (Acceleration Sensor)

### Deprecated
- API
  - moved homematicip.HomematicIPBaseObject to homematicip.base.HomematicIPBaseObject package 
## [0.10.10] - 2019-08-01
### Added
- Devices
  - HMIP-SCI (Contact Interface Sensor) 
- API
  - add supported optional features
  
### Fixes
- [BUG: 223] activateVacation does not work 


## [0.10.9] - 2019-07-06
### Added
- API
  - homematicip_demo package for testing against a test server
  - a warning on parsing an enum value from string which isn't currently existing in the API
 
### Fixes
- [BUG: 220] Support controlMode ECO 

## [0.10.8] - 2019-05-23
### Added
- Devices
  - HMIP-PCBS2 (Switch Circuit Board - 2x channels) 
  - HMIP-BBL (Blind Actuator for brand switches)
  - HMIP-FAL230-C10 (Floor Heating Actuator – 10x channels, 230V)
  - HMIP-FAL24-C6   (Floor Heating Actuator – 6x channels, 24V)
  - HMIP-FAL24-C10  (Floor Heating Actuator – 10x channels, 24V)
  - Async implementation of HMIP-PCBS-BAT (Printed Circuit Board Switch Battery)
 
## [0.10.7] - 2019-04-09
### Added
- Devices
  - HMIP-MIOB (Multi IO Box for floor heating & cooling)
- API
  - FunctionalChannels: ANALOG_OUTPUT_CHANNEL, GENERIC_INPUT_CHANNEL
  - WeatherCondition.STRONG_WIND
  - vaporAmount property to WeatherSensorPro, WeatherSensorPlus, WeatherSensor, TemperatureHumiditySensorOutdoor, TemperatureHumiditySensorWithoutDisplay, TemperatureHumiditySensorDisplay, WeatherSensorChannel and Weather
  
### FIXED
- [BUG: 188] STRONG_WIND Weather condition  

## [0.10.6] - 2019-03-02
### Added
- Devices
  - HMIP-FBL (Blind Actuator - flush-mount)
  - HMIP-BRC2 (Remote Control for brand switches – 2 channels)
  - HMIP-eTRV-C (Heating-thermostat compact without display)

- API
  - AutoNameEnum.from_str does now take a default parameter_ 
  - HeatingThermostat.**valveActualTemperature** = we are now able to read the measured temperature on the VALVE!
  - Async/HeatingFailureAlertRuleGroup

## [0.10.5] - 2019-01-26
### Added
- started with documentation
- Devices
  - HMIP-BSL (Switch Actuator for brand switches – with signal lamp)
  - HMIP-KRC4 (Key Ring Remote Control - 4 buttons)
  - HMIP-SLO (Light Sensor outdoor)
- API
  - Groups
    - Async/AlarmSwitchingGroup
      - added test/set_signal_acoustic methods
    - HeatingGroup
      - added heatingFailureSupported, valveSilentModeEnabled, valveSilentModeSupported properties
    - Async/HeatingFailureAlertRuleGroup

## [0.10.4] - 2019-01-20
### Added
- Devices
  - HMIP-SPDR 
  - HMIP-FCI1
- API
  - DeviceUpdateState enum 
  - functionalChannel
    - DevicePermanentFullRxChannel
    - PassageDetectorChannel
    - InternalSwitchChannel
    - MultiModeInputChannel
  - Device
    - MotionDetectorPushButton
      - added permanentFullRx property
  - Enums
    - MultiModeInputMode
    - BinaryBehaviorType
  - Group
    - HeatingGroup
      - added set_control_mode method  
- CLI
  - added --server-config parameter. Instead of downloading the configuration from the cloud it will load a file.

### Changes
- API
  - moved functionalChannels to homematicip.base 

## [0.10.3] - 2019-01-06
### Added
- Devices
  - HMIP-SWO-PL

## [0.10.2] - 2019-01-06
### Added
- Devices
  - HMIP-SMO-A
### Changes
- API
  - Small Bugfix in the aio library

## [0.10.1] - 2018-12-28
### Added
- API
  - FunctionalChannels
    - AlarmSirenChannel
    - FloorTerminalBlockChannel
    - FloorTerminalBlockLocalPumpChannel
    - HeatDemandChannel
    - DehumidifierDemandChannel
  - Enums
    - HeatingLoadType
  - Devices
    - HMIP-FAL230-C6 
      - added missing properties
      
### Changes
- Stability improvements

## [0.10.0] - 2018-12-23
### Added
- Devices
  - HMIP-FDT
  - HMIP-MOD-OC8
  - HMIP-RC8
  - HMIP-SWDM
  - HMIP-SWDM-2
  - HMIP-WRC6

- hmip_cli.py
  - Parameter added: --set-dim-level
  - Parameter added: --reset-energy-counter
  - Parameter added: --set-boost-duration

- API
  - FunctionalChannels
  - [Async]Home
    - get_OAuth_OTK
  - AsyncHome
    - delete_group
    - get_security_journal
    - set_powermeter_unit_price
    - set_timezone
    - set_pin
    - set_zone_activation_delay
  - Home
    - added clearConfig Parameter to get a "fresh" configuration
  - [Async]Switch
    - Added channelIndex Parameter to set_switch_state, turn_on, turn_off
  - [Async]PlugableSwitchMeasuring
    - Added reset_energy_counter
  - [Async]Group
    - added delete method
  - AsyncGroup
    - set_label
  - AsyncHeatingGroup
    - set_boost_duration
  - [Async]SecurityEvents
    - SensorEvent
    - SabotageEvent
    - MoistureDetectionEvent
    - SmokeAlarmEvent
    - ExternalTriggeredEvent
    - OfflineAlarmEvent
    - WaterDetectionEvent
    - MainsFailureEvent
    - OfflineWaterDetectionEvent
  
### Removed
- hmip_cli.py
  - converting config.py to config.ini

### Deprecated
- homematicip/base/constants.py -> use homematicip/base/enums.py
### FIXED
- [BUG: 141] AsyncSwitchingGroup.turn_off will turn the group on

## [0.9.8] - 2018-07-14
### Added
- API
  - enum backward compatibility for python 3.5
  - FunctionalHomes
  
## [0.9.7] - 2018-07-06
### Added
- Devices
  - HMIP-SWD
  - HMIP-SMI55
  
## [0.9.6] - 2018-06-12
### Changed
- API
-- async packaged got renamed to aio

## [0.9.5] - 2018-06-09
### Added
- API
-- async auth module

## [0.9.4] - 2018-05-23
### Changed
- API
-- Support for the new HMIP Cloud Update

[Unreleased]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.11.0...HEAD
[0.11.0]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.19...0.11.0
[0.10.19]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.18...0.10.19
[0.10.18]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.17...0.10.18
[0.10.17]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.16...0.10.17
[0.10.16]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.15...0.10.16
[0.10.15]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.14...0.10.15
[0.10.14]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.13...0.10.14
[0.10.13]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.12...0.10.13
[0.10.12]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.11...0.10.12
[0.10.11]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.10...0.10.11
[0.10.10]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.9...0.10.10
[0.10.9]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.8...0.10.9
[0.10.8]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.7...0.10.8
[0.10.7]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.6...0.10.7
[0.10.6]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.5...0.10.6
[0.10.5]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.4...0.10.5
[0.10.4]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.3...0.10.4
[0.10.3]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.2...0.10.3
[0.10.2]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.1...0.10.2
[0.10.1]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.0...0.10.1
[0.10.0]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.9.8...0.10.0
[0.9.8]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.9.7...0.9.8
[0.9.7]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.9.6...0.9.7
[0.9.6]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.9.5...0.9.6
[0.9.5]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.9.4...0.9.5
[0.9.4]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.9.3.3...0.9.4

[BUG: 141]: https://github.com/coreGreenberet/homematicip-rest-api/issues/141
[BUG: 188]: https://github.com/coreGreenberet/homematicip-rest-api/issues/188
[BUG: 220]: https://github.com/coreGreenberet/homematicip-rest-api/issues/220
[BUG: 223]: https://github.com/coreGreenberet/homematicip-rest-api/issues/223
[BUG: 266]: https://github.com/coreGreenberet/homematicip-rest-api/issues/266
[BUG: 294]: https://github.com/coreGreenberet/homematicip-rest-api/issues/294
[PR: 300]: https://github.com/coreGreenberet/homematicip-rest-api/pull/300
[PR: 320]: https://github.com/coreGreenberet/homematicip-rest-api/pull/320
[BUG: 325]: https://github.com/coreGreenberet/homematicip-rest-api/issues/325
[BUG: 342]: https://github.com/coreGreenberet/homematicip-rest-api/issues/342

[HMIP-FALMOT-C12]: https://github.com/coreGreenberet/homematicip-rest-api/issues/281
[HMIP-WHS2]: https://github.com/coreGreenberet/homematicip-rest-api/issues/280
[HMIP-PMFS]: https://github.com/coreGreenberet/homematicip-rest-api/issues/282 
[HMIP-WTH-B]: https://github.com/coreGreenberet/homematicip-rest-api/issues/286
[ALPHA-IP-RBG]: https://github.com/coreGreenberet/homematicip-rest-api/issues/290
[ALPHA-IP-RBGa]: https://github.com/coreGreenberet/homematicip-rest-api/issues/290
[HMIP-MOD-HO]: https://github.com/coreGreenberet/homematicip-rest-api/issues/304
[HMIP-FSI16]: https://github.com/coreGreenberet/homematicip-rest-api/issues/310
[HMIP-SWDO-PL]: https://github.com/coreGreenberet/homematicip-rest-api/issues/315
[HMIP-HDM1]: https://github.com/coreGreenberet/homematicip-rest-api/issues/332
[HMIP-HAP]: https://github.com/coreGreenberet/homematicip-rest-api/issues/335