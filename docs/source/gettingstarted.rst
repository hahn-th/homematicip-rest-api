Getting Started
***************

Installation
============

Just run **pip3 install -U homematicip** in the command line to get the package.
This will install (and update) the library and all required packages

Getting the AUTH-TOKEN
======================
Before you can start using the library you will need an auth-token. Otherwise the HMIP Cloud will not trust you.

You will need:

-  Access to an active Access Point (it must glow blue)
-  the SGTIN of the Access Point
-  [optional] the PIN

Now you have to run **hmip_generate_auth_token.py** and follow it's instructions.
It will generate a **config.ini** in your current working directory. The scripts which are using this library are looking
for this file to load the auth-token and SGTIN of the Access Point. You can either place it in the working directory when you are 
running the scripts or depending on your OS in different "global" folders:

-  General

   -  current working directory

-  Windows

   -  %APPDATA%\\homematicip-rest-api\
   -  %PROGRAMDATA%\\homematicip-rest-api\

-  Linux

   -  ~/.homematicip-rest-api/
   -  /etc/homematicip-rest-api/

-  MAC OS

   -  ~/Library/Preferences/homematicip-rest-api/
   -  /Library/Application Support/homematicip-rest-api/

