# CheckPresenceOnPing #
This script will ping (ICMP) all configured IP addresses (e.g. mobile phones which are connected over WiFi). If no device answers the ping, it will activate the security zones.

## Requirements ##
* This script must run as root/Administrator
* The mobile phones should get a static ip address or a reserved IP over DHCP
* The phones should not have "energy saving" enabled
* The script should be run via crontab or windows task planer (or something similiar) each X Minutes

## Python Requirements ##
see requirements.txt