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


def channel_only(func):
    @functools.wraps(func)
    def wrapper(bot, listener, target, author, message, private):
        if not private:
            return func(bot, listener, target, author, message, private)
        raise BotError('This command can only be run in a channel.')

    return wrapper


def private_message_only(func):
    @functools.wraps(func)
    def wrapper(bot, listener, target, author, message, private):
        if private:
            return func(bot, listener, target, author, message, private)
        raise BotError('This command can only be run in a private message.')

    return wrapper


def allowed_listeners(listeners):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(bot, listener, target, author, message, private):
            if not listeners:
                return func(bot, listener, target, author, message, private)
            for l in listeners:
                if isinstance(listener, l.value):
                    return func(
                        bot, listener, target, author, message, private
                    )
            raise BotError('This command cannot be run on this listener.')

        return wrapper

    return decorator
