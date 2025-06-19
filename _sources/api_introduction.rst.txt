API Introduction
****************

There are a few key classes for communication with the Rest API of HomematicIP.

| **Home:** is the most important object as it has the "overview" of the installation
| **Group:** a group of devices for a specific need. E.g. Heating group, security group, ...
| **MetaGroup:** a collection of groups. In the HomematicIP App this is called a "Room"
| **Device:** a hardware device e.g. shutter contact, heating thermostat, alarm siren, ...
| **FunctionChannel:** a channel of a device. For example DoorLockChannel for DoorLockDrive or **DimmerChannel**. A device has multiple channels - depending on its functions.

| For example:
| The device HmIP-DLD is represented by the class **DoorLockDrive** (or AsyncDoorLockDrive). The device has multiple channels. 
| The base channel holds informations about the device and has the index 0.
| The device has also a channel called **DoorLockChannel** which contains the functions "set_lock_state" and "async_set_lock_state". These are functions to set the lock state of that device.

If you have dimmer with multiple I/Os, there are multiple channels. For each I/O a unique channel. 