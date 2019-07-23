import logging

from snowball.commands import load_commands
from snowball.config import config
from snowball.util import admin_only, args, register

logger = logging.getLogger(__name__)


@register('reload')
@admin_only
@args(r'$')
async def call(bot, listener, target, author, args, private):
    """Hot reload the bot's config and modules."""
    try:
        config.reload()
    except Exception as e:  # noqa: E203
        logger.error(f'Error reloading config: {e}')
        return 'Error reloading config.'

    try:
        load_commands(bot, run_setup=False)
    except Exception as e:  # noqa: E203
        logger.error(f'Error reloading commands: {e}')
        return 'Error reloading commands.'

    return 'Commands reloaded.'
