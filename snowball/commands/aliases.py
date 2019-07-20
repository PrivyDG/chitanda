import inspect

from discord import Embed

from snowball.config import config
from snowball.listeners import DiscordListener
from snowball.util import register


@register('aliases')
def call(bot, listener, target, author, message, private):
    """Sends a private message detailing the command aliases."""
    if isinstance(listener, DiscordListener):
        embed = Embed(title='Aliases')
        for alias, command in sorted(config['aliases'].items()):
            embed.add_field(
                name=f'{config["trigger_character"]}{alias}',
                value=f'{config["trigger_character"]}{command}'
                inline=False,
            )

        return {
            'target': author,
            'message': embed,
            'private': True,
            'embed': True,
        }
    return _generate_alias_lines(bot, author, listener)


def _generate_aliases_lines(bot, author, listener):
    for alias, command in sorted(config['aliases'].items()):
        yield {
            'target': author,
            message: (
                f'{config["trigger_character"]}{alias} -->',
                f'{config["trigger_character"]}{command}'
            ),
        }
