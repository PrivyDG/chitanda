# chitanda

An extensible IRC & Discord bot. Requires Python 3.7.

## Setup

```bash
$ git clone git@github.com:dazuling/chitanda.git
$ cd chitanda
$ python3 -m virtualenv .venv
$ source .venv/bin/activate
$ pip install -e .
$ chitanda migrate  # Upgrade database to latest version.
$ chitanda config  # See wiki for configuration instructions.
```

## Running

```bash
$ cd chitanda
$ source .venv/bin/activate
$ chitanda run
```

Refer to the [wiki](https://github.com/dazuling/chitanda/wiki) for more
information about this bot, including a list of modules and their descriptions.
