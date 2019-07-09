import sqlite3
from contextlib import contextmanager

from snowball.constants import DATABASE_PATH


@contextmanager
def database():
    with sqlite3.connect(str(DATABASE_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        yield conn, cursor
        cursor.close()
