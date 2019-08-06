from gevent import monkey  # isort:skip

monkey.patch_all()  # noqa

import logging
import sys
from pathlib import Path

import click
from appdirs import user_config_dir, user_data_dir
from huey.contrib.minimal import MiniHuey

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

CONFIG_DIR = Path(user_config_dir('snowball', 'dazzler'))
DATA_DIR = Path(user_data_dir('snowball', 'dazzler'))

huey = MiniHuey()


class BotError(Exception):
    pass


@click.group()
def cmdgroup():
    pass


def create_app_dirs():
    try:
        CONFIG_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
        DATA_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    except OSError:
        logger.critical(f'Could not create data directory ({DATA_DIR}).')
        sys.exit(1)
