from gevent import monkey  # isort:skip

monkey.patch_all()  # noqa

import logging
import sys
from enum import Enum
from pathlib import Path

import click
from appdirs import user_data_dir

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s:%(name)s - %(message)s'
)
handler.setFormatter(formatter)

logger.addHandler(handler)


DATA_DIR = Path(user_data_dir('snowball', 'dazzler'))
DATABASE_PATH = DATA_DIR / 'db.sqlite3'
CONFIG_PATH = DATA_DIR / 'config.json'


if not DATA_DIR.is_dir():
    try:
        DATA_DIR.mkdir(mode=0o700)
    except OSError:
        logger.critical(f'Could not create data directory ({DATA_DIR}).')
        sys.exit(1)


class BotError(Exception):
    pass


class Listeners(Enum):
    IRC = 'IRC'
    Discord = 'Discord'


@click.group()
def cmdgroup():
    pass
