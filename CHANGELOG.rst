Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a
Changelog <https://keepachangelog.com/en/1.0.0/>`__, and this project
adheres to `Semantic
Versioning <https://semver.org/spec/v2.0.0.html>`__.

`UNRELEASED <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.16...master>`__
----------------------------------------------------------------------------------------

[1.1] 2024-01-06
----------------

ADDED
~~~~~

-  Add support for python 3.12
-  Add support for optional feature IFeatureDeviceSensorError
-  Add support for optional feature
   IFeatureDeviceSensorCommunicationError
-  Add support for optional feature
   IOptionalFeatureDeviceErrorLockJammed
-  Add support for device HmIP-ESI
-  Add support for function channel DeviceOperationLockWithSabotage

CHANGED
~~~~~~~

-  Changed from flat project layout to src based layout. The sourcecode
   is not placed into ./src folder. The scripts are in folder ./bin
-  Replaced versioneer with setuptools-scm to build version infos based
   on git tags and the building process.

REMOVED
~~~~~~~

-  Dropped support for python < 3.9

.. _section-1:

`1.0.16 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.15...1.1.16>`__ 2023-10-25
-----------------------------------------------------------------------------------------------

.. _added-1:

ADDED
~~~~~

-  CLI: Add argument –set-group-slats-level to set slatsLevel of Groups
-  CLI: Add argument –set-slats-level to set slatsLevel of devices.
-  CLI: Add argument –print-allowed-commands (-ac) to print allowed
   commands of device channels
-  Add support for ENERGY FunctionalHomes
-  Add support for IOptionalFeatureFilteredMulticastRouter

FIXED
~~~~~

-  Set shutterLevel to currentValue if shutterLevel is None in function
   set_slats_level of FunctionalChannel BlindChannel

.. _section-2:

`1.0.15 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.14...1.1.15>`__ 2023-08-26
-----------------------------------------------------------------------------------------------

.. _added-2:

ADDED
~~~~~

-  :warning: Functions for interacting with the device
   (set-shutter-level i.E.) are added to functionalChannel classes. This
   is because actions are bound to channels, not the devices. This is
   the foundation for more changes in the future. These functions in
   device classes are deprecated soon.
-  Add field channelRole to MultiModeInputChannel
-  Default Channel for device HmIP-DLD is set to 1
-  HmIP-DLD is a OperationLockableDevice
-  Add support for IOptionalFeatureMountingOrientation
-  Add support for IOptionalFeatureControlsMountingOrientation
-  Add support for HmIP-eTRV-CL

.. _fixed-1:

FIXED
~~~~~

-  hmip_cli: Set basic logger level in hmip_cli based on –debug-level
   argument
-  hmip_cli: Use functions from functionalChannels to execute
   set_shutter_level
-  Fix several deprecation warnings

.. _changed-1:

CHANGED
~~~~~~~

-  Bump request from 2.28.1 to 2.31.0
-  Bump aiohttp from 3.8.1 to 3.8.5
-  Drop support for Python 3.8
-  Support for Python 3.11 is added

.. _section-3:

`1.0.14 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.13...1.0.14>`__ 2023-03-04
-----------------------------------------------------------------------------------------------

.. _added-3:

ADDED
~~~~~

-  Throw HmipThrottlingError, when REST API returns 429
-  Add device HmIPW-DRS4
-  Add output for InteralSwitchChannel
-  Add HmIPW-FALMOT-12
-  Add HmIPW-WTH
-  Add HmIPW-FIO6
-  Add HmIPW-DRBL4
-  Add HmIPW-WRC6
-  Add HmIPW-WRC2
-  Add OpticalSignalChannel
-  Add OpticalSignalGroupChannel
-  Add HmIPW-SMI55
-  Add HmIPW-SPI
-  Add HmIPW-DRAP
-  Add HmIP-DSD-PCB
-  Add HmIP-DBB
-  Add HmIP-SCTH230

.. _section-4:

`1.0.13 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.12...1.0.13>`__ 2022-12-05
-----------------------------------------------------------------------------------------------

.. _fixed-2:

FIXED
~~~~~

-  Fixed device HmIP-DRDI3. Changed parent class from AsyncSwitch to
   AsyncDimmer

.. _section-5:

`1.0.12 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.11...1.0.12>`__ 2022-11-30
-----------------------------------------------------------------------------------------------

.. _added-4:

ADDED
~~~~~

-  Add Async device for HmIP-DRDI3

.. _section-6:

`1.0.11 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.10...1.0.11>`__ 2022-11-27
-----------------------------------------------------------------------------------------------

.. _added-5:

ADDED
~~~~~

-  Support for Hue devices

   -  Unknown devices are now represented by class BaseDevice
   -  Add device type ExternalDevice (which represents external devices
      (Hue))
   -  Add deviceArchetype (which differentiates between HMIP and
      EXTERNAL devices)
   -  Add ExternalBaseChannel
   -  Add ExternalUniversalLightChannel

.. _section-7:

`1.0.10 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.9...1.0.10>`__ 2022-11-26
----------------------------------------------------------------------------------------------

.. _added-6:

ADDED
~~~~~

-  CLI: Print result when using set_switch_state and set_dim_level
-  Add tests for Multi IO Box HmIP-MIOB

.. _fixed-3:

FIXED
~~~~~

-  `issue:
   471 <https://github.com/hahn-th/homematicip-rest-api/issues/471>`__
   Fix AsyncHeatingThermostatEvo

.. _changed-2:

CHANGED
~~~~~~~

-  Changed contact email-address for pypi-Package

.. _section-8:

`1.0.9 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.8...1.0.9>`__ 2022-10-08
--------------------------------------------------------------------------------------------

.. _added-7:

ADDED
~~~~~

-  `issue:
   450 <https://github.com/hahn-th/homematicip-rest-api/issues/450>`__
   Add support for device ELV-SH-BS2
-  `issue:
   464 <https://github.com/hahn-th/homematicip-rest-api/issues/464>`__
   Add support for group INDOOR_CLIMATE
-  `issue:
   465 <https://github.com/hahn-th/homematicip-rest-api/issues/465>`__
   Add argument –print-infos to CLI to print channels of a device or
   devices of a group

.. _section-9:

`1.0.8 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.7...1.0.8>`__ 2022-10-04
--------------------------------------------------------------------------------------------

.. _fixed-4:

FIXED
~~~~~

-  `bug:
   463 <https://github.com/hahn-th/homematicip-rest-api/issues/463>`__
   Add valvePosition for device HmIP-FALMOT-C12
-  Fixed –toggle-garage-door in hmip_cli.py

.. _added-8:

ADDED
~~~~~

-  `PR:
   453 <https://github.com/hahn-th/homematicip-rest-api/pull/453>`__ Add
   support for device HmIP-DLS (Door Lock Sensor)
-  `PR:
   451 <https://github.com/hahn-th/homematicip-rest-api/pull/451>`__ Add
   support for device HmIP-DLD (Door Lock Drive)
-  Add Group AccessAuthorizationProfileGroup
-  Add Group AccessControlGroup
-  Add argument ``--pin 1234`` to hmip_cli.py
-  Add argument ``--set-lock-state OPEN/LOCKED/UNLOCKED`` to hmip_cli.py

.. _changed-3:

CHANGED
~~~~~~~

-  README.md has been created which replaces README.rst
-  Github actions is used for releases and testing

.. _section-10:

`1.0.7 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.5...1.0.7>`__ 2022-07-25
--------------------------------------------------------------------------------------------

.. _added-9:

ADDED
~~~~~

-  `PR:
   449 <https://github.com/hahn-th/homematicip-rest-api/pull/449>`__ Add
   support for Device HmIP-WGC

.. _fixed-5:

FIXED
~~~~~

-  Fixed some typos from Version 1.0.5

.. _section-11:

`1.0.5 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.4...1.0.5>`__ 2022-07-16
--------------------------------------------------------------------------------------------

.. _fixed-6:

FIXED
~~~~~

-  

.. _changed-4:

CHANGED
~~~~~~~

-  

.. _section-12:

`1.0.4 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.3...1.0.4>`__ 2022-07-12
--------------------------------------------------------------------------------------------

.. _fixed-7:

FIXED
~~~~~

-  

.. _section-13:

`1.0.3 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.2...1.0.3>`__ 2022-07-06
--------------------------------------------------------------------------------------------

General
~~~~~~~

-  

.. _section-14:

`1.0.2 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.1...1.0.2>`__ 2022-02-03
--------------------------------------------------------------------------------------------

.. _added-10:

Added
~~~~~

.. _general-1:

General
~~~~~~~

-  

.. _changed-5:

CHANGED
~~~~~~~

-  API

   -  

.. _section-15:

`1.0.1 <https://github.com/hahn-th/homematicip-rest-api/compare/1.0.0...1.0.1>`__ 2021-05-27
--------------------------------------------------------------------------------------------

.. _added-11:

ADDED
~~~~~

-  Devices

   -  `HMIP-DRDI3 <https://github.com/hahn-th/homematicip-rest-api/pull/405>`__
      (Dimming Actuator Inbound 230V – 3x channels, 200W per channel)

-  API

   -  Groups

      -  `PR:
         410 <https://github.com/hahn-th/homematicip-rest-api/pull/413>`__
         Add support for channel parsing in SECURITY_ZONES and
         SECURITY_AND_ALARM

.. _section-16:

`1.0.0 <https://github.com/hahn-th/homematicip-rest-api/compare/0.13.1...1.0.0>`__ 2021-04-05
---------------------------------------------------------------------------------------------

.. _added-12:

ADDED
~~~~~

-  Devices

   -  `HmIP-STE2-PCB <https://github.com/hahn-th/homematicip-rest-api/issues/386>`__
      (Temperature Difference Sensors - 2x sensors)

.. _fixed-8:

FIXED
~~~~~

-  API

   -  `BUG:
      387 <https://github.com/hahn-th/homematicip-rest-api/issues/387>`__
      Groups were missing in the functional channels of devices
   -  `BUG:
      398 <https://github.com/hahn-th/homematicip-rest-api/issues/398>`__
      ‘ACCESS_CONTROL’ isn’t a valid option for class
      ‘FunctionalHomeType’
   -  `BUG:
      391 <https://github.com/hahn-th/homematicip-rest-api/issues/391>`__
      There is no class for device ‘PUSH_BUTTON_FLAT’ yet

.. _section-17:

`0.13.1 <https://github.com/hahn-th/homematicip-rest-api/compare/0.13.0...0.13.1>`__ 2021-01-23
-----------------------------------------------------------------------------------------------

.. _added-13:

ADDED
~~~~~

-  API

   -  Rules

      -  Add async classes and methods for rules

   -  Home

      -  Added
         `activate_absence_permanent <https://github.com/hahn-th/homematicip-rest-api/issues/357>`__
         method

-  Devices

   -  `HMIP-DRSI1 <https://github.com/hahn-th/homematicip-rest-api/issues/373>`__
      (Switch Actuator for DIN rail mount – 1x channel)
   -  `HMIP-SRD <https://github.com/hahn-th/homematicip-rest-api/issues/375>`__
      (Rain Sensor)
   -  `HMIP-WRCC2 <https://github.com/hahn-th/homematicip-rest-api/issues/373>`__
      (Wall-mount Remote Control – flat)

.. _section-18:

`0.13.0 <https://github.com/hahn-th/homematicip-rest-api/compare/0.12.1...0.13.0>`__ 2020-12-03
-----------------------------------------------------------------------------------------------

.. _added-14:

ADDED
~~~~~

-  Devices

   -  [HMIP-DRSI4] (Switch Actuator for DIN rail mount – 4x channels)
   -  [HMIP-DRBLI4] (Blind Actuator for DIN rail mount – 4 channels)
   -  [HMIP-FCI6] (Contact Interface flush-mount – 6x channels)

.. _section-19:

`0.12.1 <https://github.com/hahn-th/homematicip-rest-api/compare/0.12.0...0.12.1>`__ 2020-11-10
-----------------------------------------------------------------------------------------------

.. _added-15:

ADDED
~~~~~

-  Devices

   -  `HMIP-HDM1 <https://github.com/hahn-th/homematicip-rest-api/issues/332>`__
      (Hunter Douglas & erfal window blinds)
   -  stop method

.. _section-20:

`0.12.0 <https://github.com/hahn-th/homematicip-rest-api/compare/0.11.0...0.12.0>`__ 2020-11-09
-----------------------------------------------------------------------------------------------

.. _added-16:

ADDED
~~~~~

-  Devices

   -  `HMIP-HDM1 <https://github.com/hahn-th/homematicip-rest-api/issues/332>`__
      (Hunter Douglas & erfal window blinds)
   -  `HMIP-HAP <https://github.com/hahn-th/homematicip-rest-api/issues/335>`__
      (HomematicIP Access Point)

.. _fixed-9:

FIXED
~~~~~

-  `BUG:
   342 <https://github.com/hahn-th/homematicip-rest-api/issues/342>`__
   NameError: name ‘xrange’ is not defined on Python 3.8.1

.. _section-21:

`0.11.0 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.19...0.11.0>`__ 2020-08-31
------------------------------------------------------------------------------------------------

.. _added-17:

ADDED
~~~~~

-  API

   -  Home

      -  accessPointUpdateStates

-  Devices

   -  HMIPW-DRD3 (Homematic IP Wired Dimming Actuator – 3x channels)
   -  HMIPW-DRS8 (Homematic IP Wired Switch Actuator – 8x channels)
   -  HMIPW-DRI32 (Homematic IP Wired Inbound module – 32x channels)
   -  HMIP-STV (Inclination and vibration Sensor)
   -  Fields
   -  connectionType
   -  new OptionalFeatures

.. _changed-6:

CHANGED
~~~~~~~

-  `BUG:
   325 <https://github.com/hahn-th/homematicip-rest-api/issues/325>`__
   Requirements are now using a min version instead of a pinned version.
   requirements_dev.txt will still use the pinned versions to make sure
   that the latest version is compatible with the library.

.. _section-22:

`0.10.19 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.18...0.10.19>`__ 2020-07-08
--------------------------------------------------------------------------------------------------

.. _fixed-10:

FIXED
~~~~~

-  `PR:
   320 <https://github.com/hahn-th/homematicip-rest-api/pull/320>`__ Fix
   FSI-16

.. _section-23:

`0.10.18 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.17...0.10.18>`__ 2020-06-07
--------------------------------------------------------------------------------------------------

.. _added-18:

Added
~~~~~

-  Devices

   -  `HMIP-MOD-HO <https://github.com/hahn-th/homematicip-rest-api/issues/304>`__
      (Module for Hörmann drives)
   -  `HMIP-FSI16 <https://github.com/hahn-th/homematicip-rest-api/issues/310>`__
      (Switch Actuator with Push-button Input 230V, 16A)
   -  `HMIP-SWDO-PL <https://github.com/hahn-th/homematicip-rest-api/issues/315>`__
      (Shutter Contact Plus)

-  CLI

   -  –channel parameter for turning on/off different channels and not
      just the first one

.. _section-24:

`0.10.17 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.16...0.10.17>`__ 2020-02-16
--------------------------------------------------------------------------------------------------

.. _fixed-11:

FIXED
~~~~~

-  `PR:
   300 <https://github.com/hahn-th/homematicip-rest-api/pull/300>`__ Fix
   AsyncMotionDetectorPushButton

.. _section-25:

`0.10.16 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.15...0.10.16>`__ 2020-02-16
--------------------------------------------------------------------------------------------------

.. _added-19:

Added
~~~~~

-  Devices

   -  `HMIP-WTH-B <https://github.com/hahn-th/homematicip-rest-api/issues/286>`__
      (Wall Thermostat Basic)
   -  `ALPHA-IP-RBG <https://github.com/hahn-th/homematicip-rest-api/issues/290>`__
      (Alpha IP Wall Thermostat Display)
   -  `ALPHA-IP-RBGa <https://github.com/hahn-th/homematicip-rest-api/issues/290>`__
      (ALpha IP Wall Thermostat Display analog)

.. _fixed-12:

FIXED
~~~~~

-  

.. _section-26:

`0.10.15 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.14...0.10.15>`__ 2019-12-30
--------------------------------------------------------------------------------------------------

.. _added-20:

Added
~~~~~

-  API

   -  Groups

      -  Created new Async/SwitchBaseGroup class for groups which are
         using on, dimLevel, lowbat and dutycycle
      -  ShutterProfile

-  Devices

   -  `HMIP-FALMOT-C12 <https://github.com/hahn-th/homematicip-rest-api/issues/281>`__
      (Floor Heating Actuator – 12x channels, motorised)
   -  `HMIP-WHS2 <https://github.com/hahn-th/homematicip-rest-api/issues/280>`__
      (Switch Actuator for heating systems – 2x channels)
   -  `HMIP-PMFS <https://github.com/hahn-th/homematicip-rest-api/issues/282>`__
      (Pluggable Power Supply Monitoring)

.. _section-27:

`0.10.14 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.13...0.10.14>`__ - 2019-12-22
----------------------------------------------------------------------------------------------------

.. _added-21:

Added
~~~~~

-  API

   -  FunctionalChannels:

      -  DOOR_CHANNEL
      -  DEVICE_RECHARGEABLE_WITH_SABOTAGE

   -  ExtendedLinkedShutterGroup.set_slats_level

      -  added missing attributes

-  Devices

   -  HMIP-MOD-TM (Garage Door Module for Novoferm and Tormatic door
      operators)
   -  HMIP-ASIR-O (Alarm Siren - outdoor)

-  Groups

   -  HOT_WATER

-  Python 3.8 support

.. _changed-7:

Changed
~~~~~~~

-  General

   -  removed homematicip-testing package. Pip will automatically
      install the latest tagged release. For a “nightly” build you just
      have to run it with the “–pre” argument.

.. _fixed-13:

FIXED
~~~~~

-  

.. _section-28:

`0.10.13 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.12...0.10.13>`__ - 2019-10-19
----------------------------------------------------------------------------------------------------

.. _changed-8:

Changed
~~~~~~~

-  API

   -  converted FakeCloudServer to an async implementation
   -  the Home websocket can now automatically reopen a lost connection
      (default)

.. _section-29:

`0.10.12 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.11...0.10.12>`__ - 2019-09-27
----------------------------------------------------------------------------------------------------

.. _added-22:

Added
~~~~~

-  API

   -  Added event handlers for adding/updating/removing devices and
      groups
   -  fixed cloud bug: DEVICE/GROUP_ADDED will now be generated instead
      of DEVICE/GROUP_CHANGED on an added device

.. _section-30:

`0.10.11 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.10...0.10.11>`__ - 2019-09-23
----------------------------------------------------------------------------------------------------

.. _added-23:

Added
~~~~~

-  Devices

   -  HMIP-MOD-RC8 (Open Collector Module Sender - 8x)
   -  HMIP-SAM (Acceleration Sensor)

Deprecated
~~~~~~~~~~

-  API

   -  moved homematicip.HomematicIPBaseObject to
      homematicip.base.HomematicIPBaseObject package

.. _section-31:

`0.10.10 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.9...0.10.10>`__ - 2019-08-01
---------------------------------------------------------------------------------------------------

.. _added-24:

Added
~~~~~

-  Devices

   -  HMIP-SCI (Contact Interface Sensor)

-  API

   -  add supported optional features

Fixes
~~~~~

-  `BUG:
   223 <https://github.com/hahn-th/homematicip-rest-api/issues/223>`__
   activateVacation does not work

.. _section-32:

`0.10.9 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.8...0.10.9>`__ - 2019-07-06
-------------------------------------------------------------------------------------------------

.. _added-25:

Added
~~~~~

-  API

   -  homematicip_demo package for testing against a test server
   -  a warning on parsing an enum value from string which isn’t
      currently existing in the API

.. _fixes-1:

Fixes
~~~~~

-  `BUG:
   220 <https://github.com/hahn-th/homematicip-rest-api/issues/220>`__
   Support controlMode ECO

.. _section-33:

`0.10.8 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.7...0.10.8>`__ - 2019-05-23
-------------------------------------------------------------------------------------------------

.. _added-26:

Added
~~~~~

-  Devices

   -  HMIP-PCBS2 (Switch Circuit Board - 2x channels)
   -  HMIP-BBL (Blind Actuator for brand switches)
   -  HMIP-FAL230-C10 (Floor Heating Actuator – 10x channels, 230V)
   -  HMIP-FAL24-C6 (Floor Heating Actuator – 6x channels, 24V)
   -  HMIP-FAL24-C10 (Floor Heating Actuator – 10x channels, 24V)
   -  Async implementation of HMIP-PCBS-BAT (Printed Circuit Board
      Switch Battery)

.. _section-34:

`0.10.7 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.6...0.10.7>`__ - 2019-04-09
-------------------------------------------------------------------------------------------------

.. _added-27:

Added
~~~~~

-  Devices

   -  HMIP-MIOB (Multi IO Box for floor heating & cooling)

-  API

   -  FunctionalChannels: ANALOG_OUTPUT_CHANNEL, GENERIC_INPUT_CHANNEL
   -  WeatherCondition.STRONG_WIND
   -  vaporAmount property to WeatherSensorPro, WeatherSensorPlus,
      WeatherSensor, TemperatureHumiditySensorOutdoor,
      TemperatureHumiditySensorWithoutDisplay,
      TemperatureHumiditySensorDisplay, WeatherSensorChannel and Weather

.. _fixed-14:

FIXED
~~~~~

-  `BUG:
   188 <https://github.com/hahn-th/homematicip-rest-api/issues/188>`__
   STRONG_WIND Weather condition

.. _section-35:

`0.10.6 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.5...0.10.6>`__ - 2019-03-02
-------------------------------------------------------------------------------------------------

.. _added-28:

Added
~~~~~

-  Devices

   -  HMIP-FBL (Blind Actuator - flush-mount)
   -  HMIP-BRC2 (Remote Control for brand switches – 2 channels)
   -  HMIP-eTRV-C (Heating-thermostat compact without display)

-  API

   -  AutoNameEnum.from\ *str does now take a default parameter*
   -  HeatingThermostat.\ **valveActualTemperature** = we are now able
      to read the measured temperature on the VALVE!
   -  Async/HeatingFailureAlertRuleGroup

.. _section-36:

`0.10.5 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.4...0.10.5>`__ - 2019-01-26
-------------------------------------------------------------------------------------------------

.. _added-29:

Added
~~~~~

-  started with documentation
-  Devices

   -  HMIP-BSL (Switch Actuator for brand switches – with signal lamp)
   -  HMIP-KRC4 (Key Ring Remote Control - 4 buttons)
   -  HMIP-SLO (Light Sensor outdoor)

-  API

   -  Groups

      -  Async/AlarmSwitchingGroup

         -  added test/set_signal_acoustic methods

      -  HeatingGroup

         -  added heatingFailureSupported, valveSilentModeEnabled,
            valveSilentModeSupported properties

      -  Async/HeatingFailureAlertRuleGroup

.. _section-37:

`0.10.4 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.3...0.10.4>`__ - 2019-01-20
-------------------------------------------------------------------------------------------------

.. _added-30:

Added
~~~~~

-  Devices

   -  HMIP-SPDR
   -  HMIP-FCI1

-  API

   -  DeviceUpdateState enum
   -  functionalChannel

      -  DevicePermanentFullRxChannel
      -  PassageDetectorChannel
      -  InternalSwitchChannel
      -  MultiModeInputChannel

   -  Device

      -  MotionDetectorPushButton

         -  added permanentFullRx property

   -  Enums

      -  MultiModeInputMode
      -  BinaryBehaviorType

   -  Group

      -  HeatingGroup

         -  added set_control_mode method

-  CLI

   -  added –server-config parameter. Instead of downloading the
      configuration from the cloud it will load a file.

Changes
~~~~~~~

-  API

   -  moved functionalChannels to homematicip.base

.. _section-38:

`0.10.3 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.2...0.10.3>`__ - 2019-01-06
-------------------------------------------------------------------------------------------------

.. _added-31:

Added
~~~~~

-  Devices

   -  HMIP-SWO-PL

.. _section-39:

`0.10.2 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.1...0.10.2>`__ - 2019-01-06
-------------------------------------------------------------------------------------------------

.. _added-32:

Added
~~~~~

-  Devices

   -  HMIP-SMO-A

.. _changes-1:

Changes
~~~~~~~

-  API

   -  Small Bugfix in the aio library

.. _section-40:

`0.10.1 <https://github.com/hahn-th/homematicip-rest-api/compare/0.10.0...0.10.1>`__ - 2018-12-28
-------------------------------------------------------------------------------------------------

.. _added-33:

Added
~~~~~

-  API

   -  FunctionalChannels

      -  AlarmSirenChannel
      -  FloorTerminalBlockChannel
      -  FloorTerminalBlockLocalPumpChannel
      -  HeatDemandChannel
      -  DehumidifierDemandChannel

   -  Enums

      -  HeatingLoadType

   -  Devices

      -  HMIP-FAL230-C6

         -  added missing properties

.. _changes-2:

Changes
~~~~~~~

-  Stability improvements

.. _section-41:

`0.10.0 <https://github.com/hahn-th/homematicip-rest-api/compare/0.9.8...0.10.0>`__ - 2018-12-23
------------------------------------------------------------------------------------------------

.. _added-34:

Added
~~~~~

-  Devices

   -  HMIP-FDT
   -  HMIP-MOD-OC8
   -  HMIP-RC8
   -  HMIP-SWDM
   -  HMIP-SWDM-2
   -  HMIP-WRC6

-  hmip_cli.py

   -  Parameter added: –set-dim-level
   -  Parameter added: –reset-energy-counter
   -  Parameter added: –set-boost-duration

-  API

   -  FunctionalChannels
   -  [Async]Home

      -  get_OAuth_OTK

   -  AsyncHome

      -  delete_group
      -  get_security_journal
      -  set_powermeter_unit_price
      -  set_timezone
      -  set_pin
      -  set_zone_activation_delay

   -  Home

      -  added clearConfig Parameter to get a “fresh” configuration

   -  [Async]Switch

      -  Added channelIndex Parameter to set_switch_state, turn_on,
         turn_off

   -  [Async]PlugableSwitchMeasuring

      -  Added reset_energy_counter

   -  [Async]Group

      -  added delete method

   -  AsyncGroup

      -  set_label

   -  AsyncHeatingGroup

      -  set_boost_duration

   -  [Async]SecurityEvents

      -  SensorEvent
      -  SabotageEvent
      -  MoistureDetectionEvent
      -  SmokeAlarmEvent
      -  ExternalTriggeredEvent
      -  OfflineAlarmEvent
      -  WaterDetectionEvent
      -  MainsFailureEvent
      -  OfflineWaterDetectionEvent

.. _removed-1:

Removed
~~~~~~~

-  hmip_cli.py

   -  converting config.py to config.ini

.. _deprecated-1:

Deprecated
~~~~~~~~~~

-  homematicip/base/constants.py -> use homematicip/base/enums.py

.. _fixed-15:

FIXED
~~~~~

-  `BUG:
   141 <https://github.com/hahn-th/homematicip-rest-api/issues/141>`__
   AsyncSwitchingGroup.turn_off will turn the group on

.. _section-42:

`0.9.8 <https://github.com/hahn-th/homematicip-rest-api/compare/0.9.7...0.9.8>`__ - 2018-07-14
----------------------------------------------------------------------------------------------

.. _added-35:

Added
~~~~~

-  API

   -  enum backward compatibility for python 3.5
   -  FunctionalHomes

.. _section-43:

`0.9.7 <https://github.com/hahn-th/homematicip-rest-api/compare/0.9.6...0.9.7>`__ - 2018-07-06
----------------------------------------------------------------------------------------------

.. _added-36:

Added
~~~~~

-  Devices

   -  HMIP-SWD
   -  HMIP-SMI55

.. _section-44:

`0.9.6 <https://github.com/hahn-th/homematicip-rest-api/compare/0.9.5...0.9.6>`__ - 2018-06-12
----------------------------------------------------------------------------------------------

.. _changed-9:

Changed
~~~~~~~

-  API – async packaged got renamed to aio

.. _section-45:

`0.9.5 <https://github.com/hahn-th/homematicip-rest-api/compare/0.9.4...0.9.5>`__ - 2018-06-09
----------------------------------------------------------------------------------------------

.. _added-37:

Added
~~~~~

-  API – async auth module

.. _section-46:

`0.9.4 <https://github.com/hahn-th/homematicip-rest-api/compare/0.9.3.3...0.9.4>`__ - 2018-05-23
------------------------------------------------------------------------------------------------

.. _changed-10:

Changed
~~~~~~~

-  API – Support for the new HMIP Cloud Update
