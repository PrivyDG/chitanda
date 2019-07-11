import asyncio

from snowball.listeners import Listeners
from snowball.util import admin_only, allowed_listeners, args, register


@register('join')
@allowed_listeners(Listeners.IRC)
@admin_only
@args(r'([#&][^\x07\x2C\s]{,199})')
def call(bot, listener, target, author, args, private):
    """Join a channel."""
    channel = args[0]
    asyncio.ensure_future(listener.join(channel))
    return f'Attempted to join {channel}.'
