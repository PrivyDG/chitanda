import asyncio
import functools
import re
import sys
from types import AsyncGeneratorType

from snowball import BotError

EVENT_LOOP = asyncio.get_event_loop()


def trim_message(message, length=240):
    if len(message) > len:
        return f'{message[:length - 3]}...'
    return message


def register(trigger):
    def decorator(func):
        from snowball.bot import Snowball
        Snowball.commands[trigger] = sys.modules[func.__module__]
        return functools.wraps(func)(func)

    return decorator


def args(*regexes):
    regexes = [
        re.compile(r) if not isinstance(r, re.Pattern) else r for r in regexes
    ]

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*, message, **kwargs):
            for regex in regexes:
                match = regex.match(message)
                if match:
                    response = func(args=match.groups(), **kwargs)
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
    async def wrapper(*, listener, author, **kwargs):
        if not await listener.is_admin(author):
            raise BotError('Unauthorized.')

        response = func(listener=listener, author=author, **kwargs)
        if isinstance(response, AsyncGeneratorType):
            async for r in response:
                yield r
        else:
            yield await response

    return wrapper


def auth_only(func):
    setattr(func, 'auth_only', True)

    @functools.wraps(func)
    async def wrapper(*, listener, author, **kwargs):
        username = await listener.is_authed(author)
        if not username:
            raise BotError('Identify with NickServ to use this command.')

        response = func(listener=listener, author=author, **kwargs)
        if isinstance(response, AsyncGeneratorType):
            async for r in response:
                yield r
        else:
            yield await response

    return wrapper


def channel_only(func):
    setattr(func, 'channel_only', True)

    @functools.wraps(func)
    async def wrapper(*, private, **kwargs):
        if private:
            raise BotError('This command can only be run in a channel.')

        response = func(private=private, **kwargs)
        if isinstance(response, AsyncGeneratorType):
            async for r in response:
                yield r
        else:
            yield await response

    return wrapper


def private_message_only(func):
    setattr(func, 'private_message_only', True)

    @functools.wraps(func)
    async def wrapper(*, private, **kwargs):
        if not private:
            raise BotError(
                'This command can only be run in a private message.'
            )

        response = func(private=private, **kwargs)
        if isinstance(response, AsyncGeneratorType):
            async for r in response:
                yield r
        else:
            yield await response

    return wrapper


def allowed_listeners(*listeners):
    def decorator(func):
        setattr(func, 'listeners', listeners)

        @functools.wraps(func)
        async def wrapper(*, listener, **kwargs):
            if not listeners:
                response = func(listener=listener, **kwargs)
                if isinstance(response, AsyncGeneratorType):
                    async for r in response:
                        yield r
                else:
                    yield await response
                return

            if any(isinstance(listener, l) for l in listeners):
                response = func(listener=listener, **kwargs)
                if isinstance(response, AsyncGeneratorType):
                    async for r in response:
                        yield r
                else:
                    yield await response
            else:
                raise BotError('This command cannot be run on this listener.')

        return wrapper

    return decorator
