from snowball.util import register


@register('say')
async def call(bot, listener, target, author, message, private):
    """Repeats whatever the command was followed by."""
    return message
