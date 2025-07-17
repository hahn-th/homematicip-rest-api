# HomematicIP REST API

A **Python 3** wrapper for the homematicIP REST API (Access Point Based)
Since there is no official documentation about this API everything was
done via reverse engineering. Use at your own risk.

Any help from the community through e.g. pull requests would be highly appreciated.

[![PyPI download month](https://img.shields.io/pypi/dm/homematicip.svg)](https://pypi.python.org/pypi/homematicip/) [![PyPI version fury.io](https://badge.fury.io/py/homematicip.svg)](https://pypi.python.org/pypi/homematicip/) [![Discord](https://img.shields.io/discord/537253254074073088.svg?logo=discord&style=plastic)](https://discord.gg/mZG2myJ) [![CircleCI](https://circleci.com/gh/hahn-th/homematicip-rest-api.svg?style=shield)](https://circleci.com/gh/hahn-th/homematicip-rest-api) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/homematicip)

## Get Help / Discord

If you want to get in contact with me or need help with the library, you can get in touch with me via discord. There is a **[discord server](https://discord.gg/mZG2myJ)** and my discord tag is **agonist#6159**

## Support me

:heart: If you want to say thank you or want to support me, you can do that via PayPal.
[https://paypal.me/thomas08154711](https://paypal.me/thomas08154711?country.x=DE&locale.x=de_DE)

## Thanks

Kudos and a big thank you to @coreGreenberet, who created this library.

## Installation

To install the package, run:
```sh
pip install -U homematicip
```

## New devices and config dump

If you missing a device which is not implemented yet, open an issue and append a dump of your configuration to it using https://gist.github.com. 
To create a dump use the CLI:
```sh
hmip_cli --dump-configuration --anonymize
```