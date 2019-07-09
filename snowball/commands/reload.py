from snowball.commands import reload_commands
from snowball.util import register


@register('reload')
def call(bot, listener, author, message):
    """Hot reloads the bot's modules."""
    try:
        reload_commands()
    except:  # noqa: E203
        return 'Error reloading commands.'
    return 'Commands reloaded.'
