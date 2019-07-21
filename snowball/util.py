import asyncio
import functools
import re
import sys
from types import AsyncGeneratorType

from snowball import BotError

EVENT_LOOP = asyncio.get_event_loop()

# Duplication of code due to accomodating async generator.


def register(trigger):
    def decorator(func):
        from snowball.bot import Snowball
        Snowball.commands[trigger] = sys.modules[func.__module__]
        return functools.wraps(func)(func)

    return decorator


def args(*regexes):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(bot, listener, target, author, message, *args):
            for regex in regexes:
                match = re.match(regex, message)
                if match:
                    response = func(
                        bot, listener, target, author, match.groups(), *args
                    )
                    if isinstance(response, AsyncGeneratorType):
                        async for r in response:
                            yield r
                    else:
                        yield await response
                    break
            else:
                raise BotError('Invalid arguments.')

        return wrapper

    return decorator


def admin_only(func):
    setattr(func, 'admin_only', True)

    @functools.wraps(func)
    async def wrapper(bot, listener, target, author, *args):
        if not await listener.is_admin(author):
            raise BotError('Unauthorized.')

        response = func(bot, listener, target, author, *args)
        if isinstance(response, AsyncGeneratorType):
            async for r in response:
                yield r
        else:
            yield await response

    return wrapper


def auth_only(func):
    setattr(func, 'auth_only', True)

    @functools.wraps(func)
    async def wrapper(bot, listener, target, author, message, private):
        username = await listener.is_authed(author)
        if not username:
            raise BotError('Identify with NickServ to use this command.')

        response = func(
            bot, listener, target, author, message, private, username
        )
        if isinstance(response, AsyncGeneratorType):
            async for r in response:
                yield r
        else:
            yield await response

    return wrapper


def channel_only(func):
    setattr(func, 'channel_only', True)

    @functools.wraps(func)
    async def wrapper(bot, listener, target, author, message, private, *args):
        if private:
            raise BotError('This command can only be run in a channel.')

        response = func(bot, listener, target, author, message, private, *args)
        if isinstance(response, AsyncGeneratorType):
            async for r in response:
                yield r
        else:
            yield await response

    return wrapper


def private_message_only(func):
    setattr(func, 'private_message_only', True)

    @functools.wraps(func)
    async def wrapper(bot, listener, target, author, message, private, *args):
        if not private:
            raise BotError(
                'This command can only be run in a private message.'
            )

        response = func(bot, listener, target, author, message, private, *args)
        if isinstance(response, AsyncGeneratorType):
            async for r in response:
                yield r
        else:
            yield await response

    return wrapper


def allowed_listeners(*listeners):
    def decorator(func):
        setattr(func, 'listeners', {l.value for l in listeners})

        @functools.wraps(func)
        async def wrapper(bot, listener, *args):
            if not listeners:
                response = func(bot, listener, *args)
                if isinstance(response, AsyncGeneratorType):
                    async for r in response:
                        yield r
                else:
                    yield await response
                return

            for l in listeners:
                if isinstance(listener, l.value):
                    response = func(bot, listener, *args)
                    if isinstance(response, AsyncGeneratorType):
                        async for r in response:
                            yield r
                    else:
                        yield await response
                    break
            else:
                raise BotError('This command cannot be run on this listener.')

        return wrapper

    return decorator
