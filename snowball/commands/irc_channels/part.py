import asyncio

from snowball import BotError
from snowball.listeners import Listeners
from snowball.util import allowed_listeners, args, register


@register('part')
@allowed_listeners(Listeners.IRC)
@args(r'$', r'(#[^ ]+)$')
def call(bot, listener, target, author, args, private):
    """Parts a channel (admin only) (IRC only)."""
    if args:
        channel = args[0]
        asyncio.ensure_future(listener.raw(f'PART {channel}\r\n'))
        return f'Attempted to part {channel}.'
    elif target != author:
        channel = target
        asyncio.ensure_future(listener.raw(f'PART {channel}\r\n'))
    else:
        raise BotError('This command must be ran in a channel.')
