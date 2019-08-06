from discord import Embed

from chitanda.config import config
from chitanda.listeners import DiscordListener
from chitanda.util import args, register


@register('aliases')
@args(r'$')
async def call(*, bot, listener, target, author, args, private):
    """Sends a private message detailing the command aliases."""
    if isinstance(listener, DiscordListener):
        embed = Embed(title='Aliases')
        for alias, command in sorted(config['aliases'].items()):
            embed.add_field(
                name=f'{config["trigger_character"]}{alias}',
                value=f'{config["trigger_character"]}{command}',
                inline=False,
            )

        yield {
            'target': author,
            'message': embed,
            'private': True,
            'embed': True,
        }
    else:
        yield {
            'target': author,
            'message': 'Aliases:',
        }
        for alias, command in sorted(config['aliases'].items()):
            yield {
                'target': author,
                'message': (
                    f'{config["trigger_character"]}{alias} --> '
                    f'{config["trigger_character"]}{command}'
                ),
            }
