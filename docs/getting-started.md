# Getting Started

## Installation

Just run `pip3 install -U homematicip` in the command line to get the package.
This will install (and update) the library and all required packages.

## Getting the AUTH-TOKEN

Before you can start using the library you will need an auth-token. Otherwise the HMIP Cloud will not trust you.

You will need:

- Access to an active Access Point (it must glow blue)
- the SGTIN of the Access Point
- [optional] the PIN

If you are about to connect to a **HomematicIP HCU1** you have to press the button on top of the device, before running the script. From now, you have 5 Minutes to complete the registration process.

To get an auth-token you have to run the script `hmip_generate_auth_token` which is installed with the library.

```sh
hmip_generate_auth_token
```

It will generate a **config.ini** in your current working directory. The scripts which are using this library are looking

