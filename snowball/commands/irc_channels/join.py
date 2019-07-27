import asyncio

from snowball.listeners import IRCListener
from snowball.util import admin_only, allowed_listeners, args, register


@register('join')
@allowed_listeners(IRCListener)
@admin_only
@args(r'([#&][^\x07\x2C\s]{,199})$')
async def call(bot, listener, target, author, args, private):
    """Join a channel."""
    channel = args[0]
    asyncio.ensure_future(listener.join(channel))
    return f'Attempted to join {channel}.'
