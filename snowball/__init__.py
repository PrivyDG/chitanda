from gevent import monkey  # isort:skip

monkey.patch_all()  # noqa

import logging
import sys

import click

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s:%(name)s - %(message)s'
)
handler.setFormatter(formatter)

logger.addHandler(handler)


class BotError(Exception):
    pass


@click.group()
def cmdgroup():
    pass
