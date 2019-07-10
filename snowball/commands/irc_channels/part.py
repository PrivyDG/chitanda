import asyncio

from snowball import BotError
from snowball.listeners import Listeners
from snowball.util import admin_only, allowed_listeners, args, register


@register('part')
@allowed_listeners(Listeners.IRC)
@admin_only
@args(r'$', r'([#&][^\x07\x2C\s]{,199})')
def call(bot, listener, target, author, args, private):
    """Part a channel."""
    if args:
        channel = args[0]
        asyncio.ensure_future(listener.raw(f'PART {channel}\r\n'))
        return f'Attempted to part {channel}.'
    elif target != author:
        channel = target
        asyncio.ensure_future(listener.raw(f'PART {channel}\r\n'))
    else:
        raise BotError('This command must be ran in a channel.')
