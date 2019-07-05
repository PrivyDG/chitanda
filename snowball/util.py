import sqlite3
import sys
from contextlib import contextmanager

from snowball import DB_PATH


def register(trigger):
    def wrapper(func):
        from snowball.bot import Snowball
        Snowball.commands[trigger] = sys.modules[func.__module__]
        return func
    return wrapper


@contextmanager
def database():
    with sqlite3.connect(str(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        yield conn, cursor
        cursor.close()
