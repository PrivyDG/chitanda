from snowball.util import args, register


@register('say')
@args(r'(.+)')
async def call(*, bot, listener, target, author, args, private):
    """Repeats whatever the command was followed by."""
    return args[0]
