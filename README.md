# snowball

An IRC & Discord bot framework. Requires Python 3.7.

## Setup

```bash
$ git clone git@github.com:dzlr/snowball.git
$ cd snowball
$ python3 -m virtualenv .venv
$ source .venv/bin/activate
$ pip install -e .
$ snowball config  # See next section in README.
$ snowball migrate  # Upgrade database to latest version.
```

## Configuration

The fields in the config file are as follows:

- `trigger_character` - The character that precedes all commands.
- `irc_servers` - A dictionary of IRC servers to connect to, mapping the
  hostname to another dictionary containing information about the server. The
  specific keys available can be found in the example configuration below. The
  `perform` key defines commands that are run upon an established connection
  to the IRC server.
- `discord_token` - The token of a discord bot. This can be generated in the
  discord developer portal.
- `modules_enabled` - Modules to enable. Leave blank to enable all.
- `admins` - A list of bot admins. The admins have access to commands that
  others don't have access to. It is configured as a dictionary mapping an
  identifier of the service ("DiscordListener" for Discord and
  "IRCListener@{hostname}" for IRC) to a list of administrator names. For
  Discord, the unique account identifier is used, which can be copied
  after enabling Developer mode in the Discord client. For IRC, the nickname is
  used.

Example configuration:

```json
{
    "trigger_character": "!",
    "irc_servers": {
        "irc.freenode.net": {
            "port": "6697",
            "tls": true,
            "tls_verify": false,
            "nickname": "snowball",
            "perform": [
                "NICKSERV IDENTIFY i_throw_snowballs"
            ]
        }
    },
    "discord_token": "sample",
    "modules_enabled": [],
    "admins": {
        "DiscordListener": [
            "111111111111111111"
        ],
        "IRCListener@irc.freenode.net": [
            "ballsnow"
        ]
    }
}
```

## Running

```bash
$ cd snowball
$ source .venv/bin/activate
$ snowball
```

## Modules

### GitHub Relay (`github_relay`)

This module allows the bot to receive GitHub webhooks and report push, issue,
and pull request events to a specified channel. If this module is enabled, a
key/value pair similar to the following should be added to the configuration
file.

- `port` - The port for the webserver to listen on.
- `secret` - A secret key used to verify signed payloads from GitHub.
- `relays` - A dictionary mapping repository IDs to lists of channels to relay
  webhook events to.
- `relays[][[listener]]` - Corresponds to the channel to relay to. Either
  `IRC@{hostname}` or `Discord`).
- `relays[][[channel]]` - The channel to relay to. `#channel` for IRC and the
  channel ID for Discord.
- `relays[][[branches]]` - If empty, commits to all branches will be reported.
  Otherwise, only commits to the listed branches will be reported.

```json
"github_relay": {
    "port": 38428,
    "secret": null,
    "relays": {
        1: [
            {
                "listener": "Discord",
                "channel": "12345",
                "branches": [
                    "master"
                ]
            }
        ]
    }
}
```

No commands

### Help (`help`)

Send a private message with all bot commands to any user who types !help.

Commands:
```
help  // triggers the private message
```

### IRC Channels (`irc_channels`)

An IRC only module that handles channel joins and parts. It keeps track of
which channels the bot was in prior to quitting, handling channel rejoins after
the bot reconnects. Admin only.

Commands:
```
join #channel
part  // parts current channel
part #channel
```

### Reload (`reload`)

Hot reloads the bot's config and modules. Will handle changes in the bot's
configuration of enabled modules. Admin only.

Commands:
```
reload  // triggers the reload
```
