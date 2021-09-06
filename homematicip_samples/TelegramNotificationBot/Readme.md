# TelegramNotificationBot #
This is a bot for the "Telegram" Messenger. It will send a message to all contacts listed in the config file
To get the ID's of the user just initiate /start via Telegram on your bot. The Bot will send your userid back.

The configuration file is the same as for the homematicip. Just add a new section

[TELEGRAM]
apitoken = THE APIT TOKEN OF YOUR BOT (WITHOUT QUOTES)
contact_users = a semicolon seperated List of Telegram UserID's which should receive messages

## Requirements ##
a Bot Access Token

To generate an Access Token, you have to talk to [BotFather](https://telegram.me/botfather) and follow a few simple steps (described [here](https://core.telegram.org/bots#6-botfather)).

For full details see the official Telegram documentation at [Bots: An introduction for developers](https://core.telegram.org/bots).

## Python Requirements ##
see requirements.txt