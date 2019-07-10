import functools
import sys

from snowball import BotError
from snowball.config import config


def register(trigger):
    def wrapper(func):
        from snowball.bot import Snowball
        Snowball.commands[trigger] = sys.modules[func.__module__]
        return func
    return wrapper


def admin_only(func):
    @functools.wraps(func)
    def wrapper(bot, listener, target, author, message, private):
        if str(author) in config['admins'].get(str(listener), []):
            return func(bot, listener, target, author, message, private)
        raise BotError('Unauthorized.')

    return wrapper
