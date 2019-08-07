import functools
import re
import sys
from inspect import isasyncgenfunction

from chitanda import BotError


def irc_unstyle(text):
    """
    Taken from Makoto Fujimoto's ircmessage library.

    The MIT License (MIT)
    Copyright (c) 2015 Makoto Fujimoto
    """
    for code in ['\x0F', '\x02', '\x1D', '\x1F']:
        text = text.replace(code, '')
    return re.sub(r'\x03(?P<fg>\d{2})(,(?P<bg>\d{2}))?', '', text)


def trim_message(message, length=240):
    if len(message) > length:
        return f'{message[:length - 3]}...'
    return message


def register(trigger):
    def decorator(func):
        from chitanda.bot import Chitanda

        Chitanda.commands[trigger] = sys.modules[func.__module__]
        return functools.wraps(func)(func)

    return decorator


def args(*regexes):
    regexes = [
        re.compile(r) if not isinstance(r, re.Pattern) else r for r in regexes
    ]

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*, message, **kwargs):
            for regex in regexes:
                match = regex.match(message)
                if match:
                    return func(args=match.groups(), **kwargs)
            else:
                raise BotError('Invalid arguments.')

        return wrapper

    return decorator


def admin_only(func):
    setattr(func, 'admin_only', True)

    if isasyncgenfunction(func):

        @functools.wraps(func)
        async def wrapper(*, listener, author, **kwargs):
            if not await listener.is_admin(author):
                raise BotError('Unauthorized.')
            async for r in func(listener=listener, author=author, **kwargs):
                yield r

    else:

        @functools.wraps(func)
        async def wrapper(*, listener, author, **kwargs):
            if not await listener.is_admin(author):
                raise BotError('Unauthorized.')
            return await func(listener=listener, author=author, **kwargs)

    return wrapper


def auth_only(func):
    setattr(func, 'auth_only', True)

    if isasyncgenfunction(func):

        @functools.wraps(func)
        async def wrapper(*, listener, author, **kwargs):
            username = await listener.is_authed(author)
            if not username:
                raise BotError('Identify with NickServ to use this command.')

            async for r in func(
                listener=listener, author=author, username=username, **kwargs
            ):
                yield r

    else:

        @functools.wraps(func)
        async def wrapper(*, listener, author, **kwargs):
            username = await listener.is_authed(author)
            if not username:
                raise BotError('Identify with NickServ to use this command.')
            return await func(
                listener=listener, author=author, username=username, **kwargs
            )

    return wrapper


def channel_only(func):
    setattr(func, 'channel_only', True)

    @functools.wraps(func)
    def wrapper(*, private, **kwargs):
        if not private:
            return func(private=private, **kwargs)
        raise BotError('This command can only be run in a channel.')

    return wrapper


def private_message_only(func):
    setattr(func, 'private_message_only', True)

    @functools.wraps(func)
    def wrapper(*, private, **kwargs):
        if private:
            return func(private=private, **kwargs)
        raise BotError('This command can only be run in a private message.')

    return wrapper


def allowed_listeners(*listeners):
    def decorator(func):
        setattr(func, 'listeners', listeners)

        if listeners:

            @functools.wraps(func)
            def wrapper(*, listener, **kwargs):
                if any(isinstance(listener, l) for l in listeners):
                    return func(listener=listener, **kwargs)
                raise BotError('This command cannot be run on this listener.')

            return wrapper

        return func

    return decorator
