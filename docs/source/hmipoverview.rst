Homematic IP Overview
*********************

General
=======

The library structure is similar to the REST API or HomematicIP Android/IOS App.
The library has two ways of communicating with the REST API. Either via requests (homematicip package) or via async calls (homematicip.aio package).

Important terms
===============
- Home: is the most important object as it has the "overview" of the installation
- Device: a hardware device e.g. shutter contact, heating thermostat, alarm siren, ...
- Group: a group of devices for a specific need. E.g. Heating group, security group, ...
- MetaGroup: a collection of groups. In the HomematicIP App this is called a "Room"
