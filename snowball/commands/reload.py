from snowball.commands import reload_commands
from snowball.util import register


@register('!reload')
def call(bot, author, message):
    try:
        reload_commands()
    except:  # noqa: E203
        return 'Error reloading commands.'
    return 'Commands reloaded.'
