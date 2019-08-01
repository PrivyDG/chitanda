# snowball

An extensible IRC & Discord bot. Requires Python 3.7.

## Table of Contents

- [Setup](#setup)
- [Configuration](#configuration)
- [Running](#running)
- [Modules](#modules)

## Setup

```bash
$ git clone git@github.com:dazuling/snowball.git
$ cd snowball
$ python3 -m virtualenv .venv
$ source .venv/bin/activate
$ pip install -e .
$ snowball migrate  # Upgrade database to latest version.
$ snowball config  # See next section in README.
```

## Configuration

The fields in the config file are as follows:

- `trigger_character` - The character that precedes all commands.
- `user_agent` - User Agent to use when making HTTP requests.
- `irc_servers` - A dictionary of IRC servers to connect to, mapping the
  hostname to another dictionary containing information about the server. The
  specific keys available can be found in the example configuration below. The
  `perform` key defines commands that are run upon an established connection
  to the IRC server.
- `discord_token` - The token of a discord bot. This can be generated in the
  discord developer portal.
- `modules_enabled` - Modules to enable. Leave blank to enable all.
- `aliases` - A dictionary of trigger aliases mapping custom triggers to the
  triggers supported by the bot. Do not include the trigger character.
- `admins` - A list of bot admins. The admins have access to commands that
  others don't have access to. It is configured as a dictionary mapping an
  identifier of the service ("DiscordListener" for Discord and
  "IRCListener@{hostname}" for IRC) to a list of administrator names. For
  Discord, the unique account identifier is used, which can be copied
  after enabling Developer mode in the Discord client. For IRC, the NickServ
  account name is used.

Example configuration:

```json
{
  "trigger_character": "!",
  "user_agent": "snowball irc/discord bot",
  "irc_servers": {
    "irc.freenode.net": {
      "port": "6697",
      "tls": true,
      "tls_verify": false,
      "nickname": "snowball",
      "perform": ["NICKSERV IDENTIFY i_throw_snowballs"]
    }
  },
  "discord_token": "sample",
  "modules_enabled": [],
  "aliases": {
    "j": "join"
  },
  "admins": {
    "DiscordListener": ["111111111111111111"],
    "IRCListener@irc.freenode.net": ["ballsnow"]
  }
}
```

## Running

```bash
$ cd snowball
$ source .venv/bin/activate
$ snowball run
```

## Modules

Note: All module-specific configuration sections should be added to the
top-level dictionary of the JSON, on the same level as the `trigger_character`
and `aliases`.

- [Aliases](#aliases-aliases)
- [Choose](#choose-choose)
- [GitHub Relay](#github-relay-github_relay)
- [Help](#help-help)
- [IRC Channels](#irc-channels-irc_channels)
- [Last.FM](#lastfm-lastfm)
- [Quotes](#quotes-quotes)
- [Reload](#reload-reload)
- [Say](#say-say)
- [Tell](#tell-tell)
- [Titles](#titles-titles)
- [UrbanDictionary](#urbandictionary-urbandictionary)
- [WolframAlpha](#wolframalpha-wolframalpha)

### Aliases (`aliases`)

This module allows users to trigger a PM containing the list of aliases
specified in the bot's configuration.

Commands:

```
aliases  // sends the list of aliases to the user via PM
```

### Choose (`choose`)

The bot can make a choice for you!

Commands:

```
choose <#>-<#>  // bot will respond with a number in the given range
choose word1 word2 word3  // bot will respond with one of the words
choose phrase1, phrase2, phrase3  // bot will respond with one of the phrases
```

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
    "1": [
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

### Last.FM (`lastfm`)

Fetches a user's now playing track from Last.FM.

Requires the following addition to the config:

```json
"lastfm": {
  "api_key": "your api key"
}
```

Commands:

```
nowplaying  // fetches and relays your now playing track
setplaying <lastfm username>  // sets the lastfm account to fetch from
unsetplaying  // unsets your lastfm username
```

### Quotes (`quotes`)

Allows users to store and fetch quotes of messages to and from the bot's
database. Quotes are stored separately for each channel. Deletion of quotes is
admin only.

Commands:

```
quote  // fetches a random quote
quote <quote id> <quote id> <quote id>  // fetches quotes by ID (max: 3)
addquote <quote>  // adds a quote
delquote <quote id>  // delets a quote
findquote <string>  // searches for a quote from its contents
```

### Reload (`reload`)

Hot reloads the bot's config and modules. Will handle changes in the bot's
configuration of enabled modules. Admin only.

Commands:

```
reload  // triggers the reload
```

### Say (`say`)

The bot parrots your message back to you.

Commands:

```
say <message>  // bot says the message
```

### Sed (`sed`)

Sed a previous message from the channel. Up to 1024 messages are saved in the
history per-channel. Supports case-insensitive `i` and global `g` flags.

Commands:

```
s/find/replace  // replace 'find' with 'replace'
```

### Tell (`tell`)

Allow for messages to be stored and relayed to users who are not currently
online.

Commands:

```

tell <user> <message> // store a message to be relayed to user

```

### Titles (`titles`)

The bot will print the <title> tag of URLs messaged to the channel. This
module listens only on IRC.

No commands.

### UrbanDictionary (`urbandictionary`)

Allows queries to the UrbanDictionary API and relaying of definitions.

Commands:

```

urbandictionary <string> // fetches top definition for string
urbandictionary <number> <string> // fetches <number> ranked definition

```

### WolframAlpha (`wolframalpha`)

Allows basic queries and answer fetching to the WolframAlpha API. Useful for
math and weather, among other things.

To enable this command, a configuration section must be added to the config,
per the following:

```json
"wolframalpha": {
  "appid": "your api key goes here"
}
```

Commands:

```
wolframalpha <query>  // fetches wolframalpha's response to the query
```
