import inspect

from discord import Embed

from snowball.config import config
from snowball.listeners import DiscordListener
from snowball.util import register


@register('help')
def call(bot, listener, target, author, message):
    """Sends a private message detailing the available commands."""
    if isinstance(listener, DiscordListener):
        embed = Embed(title='Help!')
        for trigger, command in sorted(bot.commands.items()):
            print(trigger)
            embed.add_field(
                name=f'{config["trigger_character"]}{trigger}',
                value=inspect.getdoc(command.call),
            )
        return {
            'target': author,
            'message': embed,
            'private': True,
            'embed': True,
        }
    else:
        # Non-Discord requests don't have embed.
        return _generate_help_lines(bot, author)


def _generate_help_lines(bot, author):
    longest = max(len(t) for t in bot.commands)
    for trigger, command in sorted(bot.commands.items()):
        doc = inspect.getdoc(command.call)
        yield {
            'target': author,
            'message': f'{trigger.ljust(longest)} - {doc}',
        }
