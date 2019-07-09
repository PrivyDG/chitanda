from snowball.commands import reload_commands
from snowball.util import register


@register('reload')
def call(bot, listener, author, message):
    """Hot reload the bot's config and modules."""
    try:
        bot.config.reload()
    except:  # noqa: E203
        return 'Error reloading config.'

    try:
        reload_commands()
    except:  # noqa: E203
        return 'Error reloading commands.'

    return 'Commands reloaded.'
