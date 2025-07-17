# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [UNRELEASED](https://github.com/hahn-th/homematicip-rest-api/compare/2.1.0..master)

### Added

- Add IOptionalFeatureOperationDays with attribute operationDays
- Add support for ELV-SH-WSM (Watering Actuator) (#583)

## [2.1.0](https://github.com/hahn-th/homematicip-rest-api/compare/2.0.7..2.1.0) 2025-07-15

### Added

- Add support for HmIPW-DRI16
- Add generic group for OPEN_DOOR_NOTIFICATION_RULE_GROUP

### Changed

- Fix bug in auth CLI

## [2.0.7](https://github.com/hahn-th/homematicip-rest-api/compare/2.0.6..2.0.7) 2025-06-29

### Changed

- Raise HmipConnectionError, if REST-Request in get_state has an error 
- Raise HomeNotInitializedError, if get_state is called before the Home is initialized

## [2.0.6](https://github.com/hahn-th/homematicip-rest-api/compare/2.0.5..2.0.6) 2025-06-19

### Added

- Add module for FunctionalChannel-Commands
- Add hmip_batch commandline tool to execute commands in batch
- Add functions to UNIVERSAL_LIGHT_CHANNEL to control HmIP-RGBW and HmIP-LSC

### Changed

- FunctionalChannels are using the new module for commands
- Improve shutting down of websocket connection

## [2.0.5] 2025-06-12

### Fixed

- Make websocket connection more robust against errors

### Added

- Add support for ELV-SH-WSM (Watering Actuator) (#583)

## [2.0.4] 2025-05-30

### Fixed

- Add attribute "functionalChannelIndex" to ChannelEvent class

## [2.0.3] 2025-05-17

### Added

- Add client type SMART_WATCH
- Add group type AUTO_RELOCK_PROFILE
- Add group type LOCK_PROFILE
- Add device type PLUGIN
- Add device HmIP-WPK
- Add channel CODE_PROTECTED_PRIMARY_ACTION_CHANNEL
- Add channel CODE_PROTECTED_SECONDARY_ACTION_CHANNEL
- Add channel DEVICE_BLOCKING

### Changed

- Replaced websockets lib with aiohttp for websocket connection

## [2.0.2] 2025-05-02

### Added

- Add TILT as option for AccelerationSensorMode

### Removed

- Removed class `SwitchMeasuringCableOutdoor`. The device is represented by `SwitchMeasuring` instead.
- Removed class `PlugableSwitchMeasuring`. The device is represented by `SwitchMeasuring` instead.
- Removed class `BrandSwitchMeasuring`. The device is represented by `SwitchMeasuring` instead.
- Removed class `FullFlushSwitchMeasuring`. The device is represented by `SwitchMeasuring` instead.

## [2.0.1.1] 2025-05-04

### Added

- Add TILT als option for AccelerationSensorMode

### Fixed

- Raise HmipConnectionError, if websocket connection is closed with an error

### Removed

- Removed unused code

## [2.0.1] 2025-04-24

### Added

- Add device HmIP-PMSCO
- Add HmIP-WLAN-HAP-B
- Add HmIP-SMO230
- Add ELV-SH-CTV Tilt Vibration Sensor Compact
- Add ELV-SH-CTH

## [2.0.0] 2025-03-01

:warning: This is a **huge** update with massive api changes!

### Added

- The whole library is Async-first now. All functions are async functions now or calling async functions in the background.
- Completely rewritten RestConnection and WebSocketConnection
- Added RateLimitedRestConnection class to prevent throttling
- Use package `httpx` for rest requests
- Package `aiohttp` is still used for fake server for testing
- Bump `websockets` to websockets>=14.2

### Changed

- Async functions are not at the same classes as sync functions
- Replaced Auth with AsyncAuth. Auth is now async.

### Removed

- Removed all deprecated functions
- Removed all async-dedicated devices and group 

## [1.1.7] 2025-01-28

### Added

- Add support for HmIP-eTRV-3 (thx JoelKle)
- Add support for HmIP-eTRV-F (thx JoelKle)
- Add support for HmIPW-SCTHD

## [1.1.6] 2024-12-15

### Changed

- Removed support for Python lower than 3.12
- [issue: 542] Add support for HmIP-HCU Access Point (#542)
- Make "channelRole" available to FunctionalChannels

## [1.1.5] 2024-12-07

### Added

~~- [issue: 542] Add support for HmIP-HCU Access Point (#542)~~

## [1.1.4] 2024-12-07

### Added

~~- [issue: 542] Add support for HmIP-HCU Access Point (#542)~~

### Changed

- Bump aiohttp from  3.9.4 to 3.10.2
- Bump websockets to websockets 13.1
- Bump requests from 2.31.0 to 2.32.0
- Channel Events are fired by the channel itself.

## [1.1.3] 2024-11-17

### Added

- Add support for channel-events

### Changed

- Use legacy websockets client to avoid issues during connect

## [1.1.2] 2024-07-14

### Added

- Add set_cooling to home to enable/disable cooling

## [1.1.1] 2024-05-08

### Added

- Add support for HmIP-RGBW (readonly)
- Add support for HmIP-DRG-DALI (readonly)
- Add Energy Group
- Add support for Hmip-BSL with Firmware 2.0.2

### Changed

- Bump aiohttp 3.9.0 to aiohttp 3.9.4
- Rename function _restCall to _rest_call
- Rename file HomeMaticIPObject.py to homematicip_object.py

## [1.1.0] 2024-01-06

### Added

- Add support for python 3.12
- Add support for optional feature IFeatureDeviceSensorError
- Add support for optional feature IFeatureDeviceSensorCommunicationError
- Add support for optional feature IOptionalFeatureDeviceErrorLockJammed
- Add support for device HmIP-ESI
- Add support for function channel DeviceOperationLockWithSabotage
- Add new documentation site and workflow

### Changed

- Changed from flat project layout to src based layout. The source code is not placed into ./src folder. The scripts are located in package homematicip.cli
- Replaced versioneer with setuptools-scm to build version infos based on git tags and the building process.

### Fixed

- Fixed an error with --set-lock-state in cli

### Removed

- Dropped support for python < 3.9

## [1.0.16] 2023-10-25

### Added

- CLI: Add argument --set-group-slats-level to set slatsLevel of Groups
- CLI: Add argument --set-slats-level to set slatsLevel of devices.
- CLI: Add argument --print-allowed-commands (-ac) to print allowed commands of device channels
- Add support for ENERGY FunctionalHomes
- Add support for IOptionalFeatureFilteredMulticastRouter

### Fixed

- Set shutterLevel to currentValue if shutterLevel is None in function set_slats_level of FunctionalChannel BlindChannel

## [1.0.15] 2023-08-26

### Added

- :warning: Functions for interacting with the device (set-shutter-level i.E.) are added to functionalChannel classes. This is because actions are bound to channels, not the devices. This is the foundation for more changes in the future. These functions in device classes are deprecated soon.
- Add field channelRole to MultiModeInputChannel
- Default Channel for device HmIP-DLD is set to 1
- HmIP-DLD is a OperationLockableDevice
- Add support for IOptionalFeatureMountingOrientation
- Add support for IOptionalFeatureControlsMountingOrientation
- Add support for HmIP-eTRV-CL

### Fixed

- hmip_cli: Set basic logger level in hmip_cli based on --debug-level argument
- hmip_cli: Use functions from functionalChannels to execute set_shutter_level
- Fix several deprecation warnings

### Changed

- Bump request from 2.28.1 to 2.31.0
- Bump aiohttp from 3.8.1 to 3.8.5
- Drop support for Python 3.8
- Support for Python 3.11 is added

## [1.0.14] 2023-03-04

### Added

- Throw HmipThrottlingError, when REST API returns 429
- Add device HmIPW-DRS4
- Add output for InteralSwitchChannel
- Add HmIPW-FALMOT-12
- Add HmIPW-WTH
- Add HmIPW-FIO6
- Add HmIPW-DRBL4
- Add HmIPW-WRC6
- Add HmIPW-WRC2
- Add OpticalSignalChannel
- Add OpticalSignalGroupChannel
- Add HmIPW-SMI55
- Add HmIPW-SPI
- Add HmIPW-DRAP
- Add HmIP-DSD-PCB
- Add HmIP-DBB
- Add HmIP-SCTH230

## [1.0.13] 2022-12-05

### Fixed

- Fixed device HmIP-DRDI3. Changed parent class from AsyncSwitch to AsyncDimmer

## [1.0.12] 2022-11-30

### Added

- Add Async device for HmIP-DRDI3

## [1.0.11] 2022-11-27

### Added

- Support for Hue devices
  - Unknown devices are now represented by class BaseDevice
  - Add device type ExternalDevice (which represents external devices (Hue))
  - Add deviceArchetype (which differentiates between HMIP and EXTERNAL devices)
  - Add ExternalBaseChannel
  - Add ExternalUniversalLightChannel

## [1.0.10] 2022-11-26

### Added

- CLI: Print result when using set_switch_state and set_dim_level
- Add tests for Multi IO Box HmIP-MIOB

### Fixed

- [issue: 471] Fix AsyncHeatingThermostatEvo

### Changed

- Changed contact email-address for pypi-Package

## [1.0.9] 2022-10-08

### Added

- [issue: 450] Add support for device ELV-SH-BS2
- [issue: 464] Add support for group INDOOR_CLIMATE
- [issue: 465] Add argument --print-infos to CLI to print channels of a device or devices of a group

## [1.0.8] 2022-10-04

### Fixed

- [bug: 463] Add valvePosition for device HmIP-FALMOT-C12
- Fixed --toggle-garage-door in hmip_cli.py

### Added

- [PR: 453] Add support for device HmIP-DLS (Door Lock Sensor)
- [PR: 451] Add support for device HmIP-DLD (Door Lock Drive)
- Add Group AccessAuthorizationProfileGroup
- Add Group AccessControlGroup
- Add argument `--pin 1234` to hmip_cli.py
- Add argument `--set-lock-state OPEN/LOCKED/UNLOCKED` to hmip_cli.py

### Changed

- README.md has been created which replaces README.rst
- Github actions is used for releases and testing

## [1.0.7] 2022-07-25

### Added

- [PR: 449] Add support for Device HmIP-WGC

### Fixed

- Fixed some typos from Version 1.0.5

## [1.0.5] 2022-07-16

### Fixed

- [PR: 447]: Error message when using HmIP-STE2-PCB (There is no class for functionalChannel 'TEMPERATURE_SENSOR_2_EXTERNAL_DELTA_CHANNEL' yet)

### Changed

- [PR: 448]: HomematicIP Rest API should be tested against python versions 3.8, 3.9, 3.10

## [1.0.4] 2022-07-12

### Fixed

- [PR: 444]: the function \_ws_on_message in homematicip/home.py expected two arguments, but just one was provided.

## [1.0.3] 2022-07-06

### General

- [PR: 440]: Do not pass loop for Py3.10 compat

## [1.0.2] 2022-02-03

### Added

### General

- [PR: 413]: added samples

### Changed

- API
  - [PR: 424]: Drop loop kwarg from async_timeout.timeout

## [1.0.1] 2021-05-27

### Added

- Devices
  - [HMIP-DRDI3] (Dimming Actuator Inbound 230V – 3x channels, 200W per channel)
- API
  - Groups
    - [PR: 410] Add support for channel parsing in SECURITY_ZONES and SECURITY_AND_ALARM

## [1.0.0] 2021-04-05

### Added

- Devices
  - [HmIP-STE2-PCB] (Temperature Difference Sensors - 2x sensors)

### Fixed

- API
  - [BUG: 387] Groups were missing in the functional channels of devices
  - [BUG: 398] 'ACCESS_CONTROL' isn't a valid option for class 'FunctionalHomeType'
  - [BUG: 391] There is no class for device 'PUSH_BUTTON_FLAT' yet

## [0.13.1] 2021-01-23

### Added

- API
  - Rules
    - Add async classes and methods for rules
  - Home
    - Added [activate_absence_permanent] method
- Devices
  - [HMIP-DRSI1] (Switch Actuator for DIN rail mount – 1x channel)
  - [HMIP-SRD] (Rain Sensor)
  - [HMIP-WRCC2] (Wall-mount Remote Control – flat)

## [0.13.0] 2020-12-03

### Added

- Devices
  - [HMIP-DRSI4] (Switch Actuator for DIN rail mount – 4x channels)
  - [HMIP-DRBLI4] (Blind Actuator for DIN rail mount – 4 channels)
  - [HMIP-FCI6] (Contact Interface flush-mount – 6x channels)

## [0.12.1] 2020-11-10

### Added

- Devices
  - [HMIP-HDM1] (Hunter Douglas & erfal window blinds)
  - stop method

## [0.12.0] 2020-11-09

### Added

- Devices
  - [HMIP-HDM1] (Hunter Douglas & erfal window blinds)
  - [HMIP-HAP] (HomematicIP Access Point)

### Fixed

- [BUG: 342] NameError: name 'xrange' is not defined on Python 3.8.1

## [0.11.0] 2020-08-31

### Added

- API
  - Home
    - accessPointUpdateStates
- Devices
  - HMIPW-DRD3 (Homematic IP Wired Dimming Actuator – 3x channels)
  - HMIPW-DRS8 (Homematic IP Wired Switch Actuator – 8x channels)
  - HMIPW-DRI32 (Homematic IP Wired Inbound module – 32x channels)
  - HMIP-STV (Inclination and vibration Sensor)
  - Fields
  - connectionType
  - new OptionalFeatures

### Changed

- [BUG: 325] Requirements are now using a min version instead of a pinned version. requirements_dev.txt will still use the pinned versions to make sure that the latest version is compatible with the library.

## [0.10.19] 2020-07-08

### Fixed

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

### Fixed

- [PR: 300] Fix AsyncMotionDetectorPushButton

## [0.10.16] 2020-02-16

### Added

- Devices
  - [HMIP-WTH-B] (Wall Thermostat Basic)
  - [ALPHA-IP-RBG] (Alpha IP Wall Thermostat Display)
  - [ALPHA-IP-RBGa] (ALpha IP Wall Thermostat Display analog)

### Fixed

- [BUG: 294]: hmip_cli.py --anonymize will wrongly anonymize other fields

## [0.10.15] 2019-12-30

### Added

- API
  - Groups
    - Created new Async/SwitchBaseGroup class for groups which are using on, dimLevel, lowbat and dutycycle
    - ShutterProfile
- Devices
  - [HMIP-FALMOT-C12] (Floor Heating Actuator – 12x channels, motorised)
  - [HMIP-WHS2] (Switch Actuator for heating systems – 2x channels)
  - [HMIP-PMFS] (Pluggable Power Supply Monitoring)

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

### Fixed

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
  - HMIP-SAM (Acceleration Sensor)

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
  - HMIP-FAL24-C6 (Floor Heating Actuator – 6x channels, 24V)
  - HMIP-FAL24-C10 (Floor Heating Actuator – 10x channels, 24V)
  - Async implementation of HMIP-PCBS-BAT (Printed Circuit Board Switch Battery)

## [0.10.7] - 2019-04-09

### Added

- Devices
  - HMIP-MIOB (Multi IO Box for floor heating & cooling)
- API
  - FunctionalChannels: ANALOG_OUTPUT_CHANNEL, GENERIC_INPUT_CHANNEL
  - WeatherCondition.STRONG_WIND
  - vaporAmount property to WeatherSensorPro, WeatherSensorPlus, WeatherSensor, TemperatureHumiditySensorOutdoor, TemperatureHumiditySensorWithoutDisplay, TemperatureHumiditySensorDisplay, WeatherSensorChannel and Weather

### Fixed

- [BUG: 188] STRONG_WIND Weather condition

## [0.10.6] - 2019-03-02

### Added

- Devices

  - HMIP-FBL (Blind Actuator - flush-mount)
  - HMIP-BRC2 (Remote Control for brand switches – 2 channels)
  - HMIP-eTRV-C (Heating-thermostat compact without display)

- API
  - AutoNameEnum.from*str does now take a default parameter*
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

### Fixed

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

[2.0.5]: https://github.com/hahn-th/homematicip-rest-api/compare/2.0.4...2.0.5
[2.0.4]: https://github.com/hahn-th/homematicip-rest-api/compare/2.0.3...2.0.4
[2.0.3]: https://github.com/hahn-th/homematicip-rest-api/compare/2.0.2...2.0.3
[2.0.2]: https://github.com/hahn-th/homematicip-rest-api/compare/2.0.1...2.0.2
[2.0.1]: https://github.com/hahn-th/homematicip-rest-api/compare/2.0.0...2.0.1
[2.0.0]: https://github.com/hahn-th/homematicip-rest-api/compare/1.1.7...2.0.0
[1.1.7]: https://github.com/hahn-th/homematicip-rest-api/compare/1.1.6...1.1.7
[1.1.6]: https://github.com/hahn-th/homematicip-rest-api/compare/1.1.5...1.1.6
[1.1.5]: https://github.com/hahn-th/homematicip-rest-api/compare/1.1.4...1.1.5
[1.1.4]: https://github.com/hahn-th/homematicip-rest-api/compare/1.1.3...1.1.4
[1.1.3]: https://github.com/hahn-th/homematicip-rest-api/compare/1.1.2...1.1.3
[1.1.2]: https://github.com/hahn-th/homematicip-rest-api/compare/1.1.1...1.1.2
[1.1.1]: https://github.com/hahn-th/homematicip-rest-api/compare/1.1.0...1.1.1
[1.1.0]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.16...1.1.0
[1.0.16]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.15...1.0.16
[1.0.15]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.14...1.0.15
[1.0.14]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.13...1.0.14
[1.0.13]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.12...1.0.13
[1.0.12]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.11...1.0.12
[1.0.11]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.10...1.0.11
[1.0.10]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.9...1.0.10
[1.0.9]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.8...1.0.9
[1.0.8]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.7...1.0.8
[1.0.7]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.5...1.0.7
[1.0.5]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.4...1.0.5
[1.0.4]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.3...1.0.4
[1.0.3]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/hahn-th/homematicip-rest-api/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/hahn-th/homematicip-rest-api/compare/0.13.1...1.0.0
[0.13.1]: https://github.com/hahn-th/homematicip-rest-api/compare/0.13.0...0.13.1
[0.13.0]: https://github.com/hahn-th/homematicip-rest-api/compare/0.12.1...0.13.0
[0.12.1]: https://github.com/hahn-th/homematicip-rest-api/compare/0.12.0...0.12.1
[0.12.0]: https://github.com/hahn-th/homematicip-rest-api/compare/0.11.0...0.12.0
[0.11.0]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.19...0.11.0
[0.10.19]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.18...0.10.19
[0.10.18]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.17...0.10.18
[0.10.17]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.16...0.10.17
[0.10.16]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.15...0.10.16
[0.10.15]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.14...0.10.15
[0.10.14]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.13...0.10.14
[0.10.13]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.12...0.10.13
[0.10.12]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.11...0.10.12
[0.10.11]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.10...0.10.11
[0.10.10]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.9...0.10.10
[0.10.9]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.8...0.10.9
[0.10.8]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.7...0.10.8
[0.10.7]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.6...0.10.7
[0.10.6]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.5...0.10.6
[0.10.5]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.4...0.10.5
[0.10.4]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.3...0.10.4
[0.10.3]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.2...0.10.3
[0.10.2]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.1...0.10.2
[0.10.1]: https://github.com/hahn-th/homematicip-rest-api/compare/0.10.0...0.10.1
[0.10.0]: https://github.com/hahn-th/homematicip-rest-api/compare/0.9.8...0.10.0
[0.9.8]: https://github.com/hahn-th/homematicip-rest-api/compare/0.9.7...0.9.8
[0.9.7]: https://github.com/hahn-th/homematicip-rest-api/compare/0.9.6...0.9.7
[0.9.6]: https://github.com/hahn-th/homematicip-rest-api/compare/0.9.5...0.9.6
[0.9.5]: https://github.com/hahn-th/homematicip-rest-api/compare/0.9.4...0.9.5
[0.9.4]: https://github.com/hahn-th/homematicip-rest-api/compare/0.9.3.3...0.9.4
[bug: 141]: https://github.com/hahn-th/homematicip-rest-api/issues/141
[bug: 188]: https://github.com/hahn-th/homematicip-rest-api/issues/188
[bug: 220]: https://github.com/hahn-th/homematicip-rest-api/issues/220
[bug: 223]: https://github.com/hahn-th/homematicip-rest-api/issues/223
[bug: 266]: https://github.com/hahn-th/homematicip-rest-api/issues/266
[bug: 294]: https://github.com/hahn-th/homematicip-rest-api/issues/294
[pr: 300]: https://github.com/hahn-th/homematicip-rest-api/pull/300
[pr: 320]: https://github.com/hahn-th/homematicip-rest-api/pull/320
[bug: 325]: https://github.com/hahn-th/homematicip-rest-api/issues/325
[bug: 342]: https://github.com/hahn-th/homematicip-rest-api/issues/342
[bug: 387]: https://github.com/hahn-th/homematicip-rest-api/issues/387
[bug: 391]: https://github.com/hahn-th/homematicip-rest-api/issues/391
[bug: 398]: https://github.com/hahn-th/homematicip-rest-api/issues/398
[pr: 410]: https://github.com/hahn-th/homematicip-rest-api/pull/410
[pr: 410]: https://github.com/hahn-th/homematicip-rest-api/pull/413
[pr: 424]: https://github.com/hahn-th/homematicip-rest-api/pull/424
[pr: 440]: https://github.com/hahn-th/homematicip-rest-api/pull/440
[pr: 440]: https://github.com/hahn-th/homematicip-rest-api/pull/444
[pr: 447]: https://github.com/hahn-th/homematicip-rest-api/pull/447
[pr: 448]: https://github.com/hahn-th/homematicip-rest-api/pull/448
[pr: 449]: https://github.com/hahn-th/homematicip-rest-api/pull/449
[issue: 450]: https://github.com/hahn-th/homematicip-rest-api/issues/450
[pr: 451]: https://github.com/hahn-th/homematicip-rest-api/pull/451
[pr: 453]: https://github.com/hahn-th/homematicip-rest-api/pull/453
[bug: 463]: https://github.com/hahn-th/homematicip-rest-api/issues/463
[issue: 464]: https://github.com/hahn-th/homematicip-rest-api/issues/464
[issue: 465]: https://github.com/hahn-th/homematicip-rest-api/issues/465
[issue: 471]: https://github.com/hahn-th/homematicip-rest-api/issues/471
[issue: 542]: https://github.com/hahn-th/homematicip-rest-api/issues/542
[hmip-falmot-c12]: https://github.com/hahn-th/homematicip-rest-api/issues/281
[hmip-whs2]: https://github.com/hahn-th/homematicip-rest-api/issues/280
[hmip-pmfs]: https://github.com/hahn-th/homematicip-rest-api/issues/282
[hmip-wth-b]: https://github.com/hahn-th/homematicip-rest-api/issues/286
[alpha-ip-rbg]: https://github.com/hahn-th/homematicip-rest-api/issues/290
[alpha-ip-rbga]: https://github.com/hahn-th/homematicip-rest-api/issues/290
[hmip-mod-ho]: https://github.com/hahn-th/homematicip-rest-api/issues/304
[hmip-fsi16]: https://github.com/hahn-th/homematicip-rest-api/issues/310
[hmip-swdo-pl]: https://github.com/hahn-th/homematicip-rest-api/issues/315
[hmip-hdm1]: https://github.com/hahn-th/homematicip-rest-api/issues/332
[hmip-hap]: https://github.com/hahn-th/homematicip-rest-api/issues/335
[hmip-srd]: https://github.com/hahn-th/homematicip-rest-api/issues/375
[hmip-wrcc2]: https://github.com/hahn-th/homematicip-rest-api/issues/373
[hmip-drsi1]: https://github.com/hahn-th/homematicip-rest-api/issues/373
[hmip-ste2-pcb]: https://github.com/hahn-th/homematicip-rest-api/issues/386
[activate_absence_permanent]: https://github.com/hahn-th/homematicip-rest-api/issues/357
[hmip-drdi3]: https://github.com/hahn-th/homematicip-rest-api/pull/405
