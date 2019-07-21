from snowball.util import register, args


@register('say')
@args(r'(.+)')
async def call(bot, listener, target, author, args, private):
    """Repeats whatever the command was followed by."""
    return args[0]
