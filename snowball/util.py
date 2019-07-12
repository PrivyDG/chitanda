import functools
import re
import sys

from snowball import BotError
from snowball.config import config


def register(trigger):
    def decorator(func):
        from snowball.bot import Snowball
        Snowball.commands[trigger] = sys.modules[func.__module__]
        return functools.wraps(func)(func)

    return decorator


def args(*regexes):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(bot, listener, target, author, message, private):
            for regex in regexes:
                match = re.match(regex, msg_content)
                if match:
                    return func(
                        bot, listener, target, author, match.groups(), private
                    )
            raise BotError('Invalid arguments.')

        return wrapper

    return decorator


def admin_only(func):
    setattr(func, 'admin_only', True)

    @functools.wraps(func)
    def wrapper(bot, listener, target, author, message, private):
        if str(author) in config['admins'].get(str(listener), []):
            return func(bot, listener, target, author, message, private)
        raise BotError('Unauthorized.')

    return wrapper


def channel_only(func):
    setattr(func, 'channel_only', True)

    @functools.wraps(func)
    def wrapper(bot, listener, target, author, message, private):
        if not private:
            return func(bot, listener, target, author, message, private)
        raise BotError('This command can only be run in a channel.')

    return wrapper


def private_message_only(func):
    setattr(func, 'private_message_only', True)

    @functools.wraps(func)
    def wrapper(bot, listener, target, author, message, private):
        if private:
            return func(bot, listener, target, author, message, private)
        raise BotError('This command can only be run in a private message.')

    return wrapper


def allowed_listeners(*listeners):
    def decorator(func):
        setattr(func, 'listeners', {l.value for l in listeners})

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
