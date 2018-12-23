# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
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
  - [Async]Switch
    - Added channelIndex Parameter to set_switch_state, turn_on, turn_off
  - [Async]PlugableSwitchMeasuring
    - Added reset_energy_counter
  - Group
    - added delete method
  - Home
    - added clearConfig Parameter to get a "fresh" configuration
  
### Removed
- hmip_cli.py
  - converting config.py to config.ini

### Deprecated
- homematicip/base/constants.py -> use homematicip/base/enums.py

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

[Unreleased]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.9.8...HEAD
[0.9.8]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.9.7...0.9.8
[0.9.7]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.9.6...0.9.7
[0.9.6]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.9.5...0.9.6
[0.9.5]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.9.4...0.9.5
[0.9.4]: https://github.com/coreGreenberet/homematicip-rest-api/compare/0.9.3.3...0.9.4