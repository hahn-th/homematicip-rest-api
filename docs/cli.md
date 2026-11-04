# Command line tools

The package installs three scripts: `hmip_generate_auth_token` registers a client with your
access point, `hmip_cli` reads and controls the installation, and `hmip_batch` tries commands
against a channel, see [Batch testing](batch-testing.md).

## Getting an auth token

You need an access point that is online (its LED glows blue), its SGTIN, and the PIN if one is
set. With a **HomematicIP HCU1**, press the button on top of the device first; the registration
then has to complete within five minutes.

```sh
hmip_generate_auth_token
```

The script writes a `config.ini` with the access point ID and the auth token into the current
directory. Every script and every example in this documentation loads it from the current
directory or from one of these places:

- Windows: `%APPDATA%\homematicip-rest-api\` or `%PROGRAMDATA%\homematicip-rest-api\`
- Linux: `~/.homematicip-rest-api/` or `/etc/homematicip-rest-api/`
- macOS: `~/Library/Preferences/homematicip-rest-api/` or
  `/Library/Application Support/homematicip-rest-api/`

## Using hmip_cli

`hmip_cli --help` lists every option. Devices are addressed with `-d` and the 24-digit ID from
`--list-devices`, groups with `-g` and the ID from `--list-groups`.

Commands are bound to the channel type, so the first step with an unknown device is to see
what it offers:

```sh
hmip_cli -d <device id> --print-infos             # the device and its channels
hmip_cli -d <device id> --print-allowed-commands  # what each channel accepts
```

A few examples:

- `hmip_cli --list-devices` lists your devices.
- `hmip_cli -d <id> --toggle-garage-door` toggles the garage door of an HmIP-WGC.
- `hmip_cli -d <id> --set-lock-state LOCKED --pin 1234` locks a door with an HmIP-DLD.
- `hmip_cli --list-events` prints the events the cloud pushes, until you stop it.
- `hmip_cli --dump-configuration --anonymize` dumps the installation for a bug report, see
  [New devices and config dump](index.md#new-devices-and-config-dump).
