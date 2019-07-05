from gevent import monkey  # isort:skip

monkey.patch_all()  # noqa

import pathlib

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

DB_PATH = pathlib.Path(__file__).parent.parent / 'countdown.db'


class BotError(Exception):
    pass
