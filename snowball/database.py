import sqlite3

DB_PATH = pathlib.Path(__file__).parent.parent / 'db.sqlite3'


@contextmanager
def database():
    with sqlite3.connect(str(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        yield conn, cursor
        cursor.close()
