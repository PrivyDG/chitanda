import sys
from contextlib import contextmanager


def register(trigger):
    def wrapper(func):
        from snowball.bot import Snowball
        Snowball.commands[trigger] = sys.modules[func.__module__]
        return func
    return wrapper
