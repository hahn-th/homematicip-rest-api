# API introduction

The library talks to the Homematic IP cloud the way the app does: REST calls for commands and
for the full state, a websocket for pushed changes. There is no official documentation, so
everything here was reverse engineered and can change with a firmware or cloud update.

## Key classes

- **AsyncHome** is the entry point. `init_async(access_point_id, auth_token)` resolves the cloud
  hosts for the access point, `get_current_state_async()` downloads the whole installation and
  builds the objects below. `Home` in `homematicip.home` wraps it for synchronous code; every
  method there has an `_async` counterpart on `AsyncHome`.
- **Device** is a piece of hardware. Devices are containers: the readings and the commands live
  on their channels, and the device class mostly decides which channel classes get loaded.
- **FunctionalChannel** is one channel of a device, typed by `functionalChannelType`. Channel 0
  is the `DEVICE_BASE` channel with the device-wide values such as `rssiDeviceValue`,
  `lowBat` and `unreach`. Which further channels a device has depends on the model;
  `hmip_cli -d <id> --print-infos` shows them.
- **Group** collects devices for a purpose: a heating group, a security zone, a switching
  group. **MetaGroup** is what the app calls a room.
- **FunctionalHome** holds the home-wide features: `IndoorClimateHome`, `SecurityAndAlarmHome`,
  `LightAndShadowHome`, `AccessControlHome`, `EnergyHome` and `WeatherAndEnvironmentHome`.

A device type the library knows but has no class for loads as `BaseDevice` and keeps all its
channels, a channel type without a class loads as a plain `FunctionalChannel`. Both carry the
raw JSON in `_rawJSONData`, so a missing class rarely means missing data, only missing commands.

## Reading values

```python
device = home.search_device_by_id("3014F711A000000000000001")

for channel in device.functionalChannels:
    print(channel.index, channel.functionalChannelType)

# on a wall thermostat, channel 1 is the WALL_MOUNTED_THERMOSTAT_PRO_CHANNEL
print(device.functionalChannels[1].actualTemperature)
```

## Sending commands

Write methods live where the function lives: switching on the device or its channel, the set
point temperature on the heating group that owns the thermostat:

```python
await device.turn_on_async()
await heating_group.set_point_temperature_async(21.0)
```

A command is one REST call. The cloud answers with the new state only through the websocket,
so read the value again after the next event rather than right after the call.

## Events

`enable_events()` opens the websocket and keeps it open with its own reconnect loop. Every
pushed change updates the objects and calls the handlers registered on `home.onEvent`:

```python
def print_events(event_list):
    for event in event_list:
        print(event["eventType"], event["data"])

home.onEvent += print_events
await home.enable_events()
```

`set_on_connected_handler`, `set_on_disconnected_handler` and `set_on_reconnect_handler`
tell a long-running client what the connection does. After a reconnect the cloud does not
replay missed events, so call `refresh_state_after_reconnect_async()`: it waits for the
websocket, then downloads the state again with an exponential backoff on errors.

## Errors and throttling

All connection problems raise `HmipConnectionError` or a subclass. `HmipAuthenticationError`
means the cloud answered 403, usually because the auth token is no longer valid, and
`HmipThrottlingError` means it answered 429.

The cloud throttles by public IP: too many requests in a short time, typically a client that
reconnects and downloads the whole state in a loop, block every client behind that IP for a
while, from 15 minutes to hours. The library remembers a 429 for the whole process in
`homematicip.connection.throttling`; `throttle_cooldown_remaining()` returns how long to leave
the cloud alone, and the websocket reconnect and the state refresh wait that out themselves.
A client that builds new `AsyncHome` instances, as Home Assistant does on every reload, should
check it before the first call.
