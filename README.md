# snowball

An extensible IRC & Discord bot. Requires Python 3.7.

## Setup

```bash
$ git clone git@github.com:dazuling/snowball.git
$ cd snowball
$ python3 -m virtualenv .venv
$ source .venv/bin/activate
$ pip install -e .
$ snowball migrate  # Upgrade database to latest version.
$ snowball config  # See wiki for configuration instructions.
```

## Running

```bash
$ cd snowball
$ source .venv/bin/activate
$ snowball run
```

Refer to the [wiki](https://github.com/dazuling/snowball/wiki) for more
information about this bot, including a list of modules and their descriptions.
