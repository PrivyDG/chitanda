# snowball

An IRC & Discord bot framework. Requires Python 3.7.

## Setup

```bash
$ git clone git@github.com:dzlr/snowball.git
$ cd snowball
$ python3 -m virtualenv .venv
$ source .venv/bin/activate
$ pip install -e .
$ snowball config  # See next section in README
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
