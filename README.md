# homematicip-samples
A collection of samples and simple scripts for the homematicip rest api wrapper.
Each sample requires at least the homematicip package
```pip3 install homematicip```

## PULL Requests
Use the SampleTemplate folder as a base for your requests. 
The script must work.
Also modify this Readme.md to add a short summary of your Project.

If you aren't using Visual Studio you can skip the *.pyproj file. I will add it in an additional commit.

### SampleTemplate
This sample will just display the current AP Version.
The usage for this folder is intended as a template for other examples

### CheckPresenceOnPing
This script will ping (ICMP) all configured IP addresses (e.g. mobile phones which are connected over WiFi). If no device answers the ping, it will activate the security zones

### GetDevicesAndValues
Get´s (all) devices and values.

### ControlDevices
Example of turning a switch on and off

### QRCodeGenerator
This script will create QRCodes for all configured devices and a webpage for easier browsing

### TelegramNotificationBot
This is a bot for the "Telegram" Messenger. It will send a message to all contacts listed in the config file To get the ID's of the user just initiate /start via Telegram on your bot. The Bot will send your userid back.
