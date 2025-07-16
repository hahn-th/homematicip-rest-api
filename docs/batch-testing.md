# Batch Testing of Applicable Commands

HomematicIP devices can have different channels, and each channel can have different commands. To test which commands are applicable for a channel, use the `hmip_batch` script. This script will try to execute commands for a device and print the result. It will also print the commands that are not applicable for the device.

The script takes the device ID and the channel index as arguments. You also need a JSON batch file containing the commands.

> **Warning**
> Please pay close attention to the parameters used for each command. Incorrect or inappropriate parameters may lead to unexpected behavior or even malfunction of your HomematicIP devices. Executing commands is at your own risk. Always double-check the documentation and ensure you understand the effects of each command before using it in your environment.

### Steps to Run a Batch Test

1. Install this library with pip: `pip install -U homematicip`
2. Get an access token as described above.
3. Get your device ID and channel index from the device list using:  
`hmip_cli --list-devices`  
or dump the configuration with:  
`hmip_cli --dump-configuration`
4. Download the JSON batch file from [GitHub](https://github.com/hahn-th/homematicip-rest-api/blob/master/homematicip_demo/hmip_batch.json).
5. Edit the JSON batch file to choose which commands you want to test. You can enable or disable commands by setting the `active` flag to `true` or `false`.

With the `active` flag you can enable or disable commands:

```json
{
  "function": "set_shutter_level_async",
  "active": false,
  "params": {
    "shutter_level": 0.7
  }
},
```

To run the batch test, use the following command:

```sh
hmip_batch -d <device-id> -i <channel-index> <path-to-json-batch-file>
```
