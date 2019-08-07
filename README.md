# chitanda

An extensible IRC & Discord bot. Requires Python 3.7.

Refer to the [GitHub wiki](https://github.com/dazuling/chitanda/wiki) for
documentation.

## Installation

### From PyPI with pipx

```bash
$ pipx install chitanda
$ chitanda migrate  # Upgrade database to latest version.
$ chitanda config  # See wiki for configuration instructions.
```

Run chitanda with

```bash
$ chitanda run
```

### From source

```bash
$ git clone git@github.com:dazuling/chitanda.git
$ cd chitanda
$ python3 -m virtualenv .venv
$ source .venv/bin/activate
$ pip install -e .
$ chitanda migrate  # Upgrade database to latest version.
$ chitanda config  # See wiki for configuration instructions.
```

Run chitanda with the following commands

```bash
$ cd chitanda  # Change to project directory.
$ source .venv/bin/activate
$ chitanda run
```
