# chitanda

[![Build Status](https://travis-ci.org/dazuling/chitanda.svg?branch=master)](https://travis-ci.org/dazuling/chitanda)
[![Coverage Status](https://coveralls.io/repos/github/dazuling/chitanda/badge.svg?branch=master)](https://coveralls.io/github/dazuling/chitanda?branch=master)
[![Pypi](https://img.shields.io/pypi/v/chitanda.svg)](https://pypi.python.org/pypi/chitanda)
[![Pyversions](https://img.shields.io/pypi/pyversions/chitanda.svg)](https://pypi.python.org/pypi/chitanda)

An extensible IRC & Discord bot. Requires Python 3.7.

Refer to the [GitHub wiki](https://github.com/dazuling/chitanda/wiki) for
documentation on using the bot and (TODO) extending it.

## Setup

### From PyPI with pipx

```bash
$ pipx install chitanda
$ chitanda migrate  # Upgrade database to latest version.
$ chitanda config  # See wiki for configuration instructions.
```

Run chitanda with the following command:

```bash
$ chitanda run
```

### From source with poetry

```bash
$ git clone git@github.com:dazuling/chitanda.git
$ cd chitanda
$ poetry install
$ poetry shell
$ chitanda migrate  # Upgrade database to latest version.
$ chitanda config  # See wiki for configuration instructions.
```

Run chitanda with the following commands:

```bash
$ cd chitanda  # Change to project directory.
$ poetry run chitanda run
```

### From source with pip

```bash
$ git clone git@github.com:dazuling/chitanda.git
$ cd chitanda
$ python3 -m virtualenv .venv
$ source .venv/bin/activate
$ pip install -e .
$ chitanda migrate  # Upgrade database to latest version.
$ chitanda config  # See wiki for configuration instructions.
```

Run chitanda with the following commands:

```bash
$ cd chitanda  # Change to project directory.
$ source .venv/bin/activate
$ chitanda run
```
