# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- API
  - DeviceUpdateState enum 
  - functionalChannel
    - DevicePermanentFullRxChannel
  - Device
    - MotionDetectorPushButton
      - added permanentFullRx property
### Changes
- API
  - moved functionalChannels to homematicip.base 

## [0.10.3] - 2019-01-06
### Added
- Devices
  - HmIP-SWO-PL

## [0.10.2] - 2019-01-06
### Added
- Devices
  - HmIP-SMO-A
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
    - HmIP-FAL230-C6 
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
  - HmIP-SWD
  - HmIP-SMI55
  
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

[Unreleased]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.10.3...HEAD
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