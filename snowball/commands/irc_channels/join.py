import asyncio

from snowball.listeners import Listeners
from snowball.util import allowed_listeners, args, register


@register('join')
@allowed_listeners(Listeners.IRC)
@args(r'(#[^ ]+)$')
def call(bot, listener, target, author, args, private):
    """Join a channel (admin only) (IRC only)."""
    channel = args[0]
    asyncio.ensure_future(listener.raw(f'JOIN {channel}\r\n'))
    return f'Attempted to join {channel}.'
