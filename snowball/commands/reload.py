from snowball.commands import reload_commands
from snowball.config import config
from snowball.util import admin_only, register


@register('reload')
@admin_only
def call(bot, listener, target, author, message, private):
    """Hot reload the bot's config and modules."""
    try:
        config.reload()
    except:  # noqa: E203
        return 'Error reloading config.'

    try:
        reload_commands()
    except:  # noqa: E203
        return 'Error reloading config.'

    return 'Commands reloaded.'
