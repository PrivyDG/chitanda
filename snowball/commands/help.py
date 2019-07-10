import inspect

from discord import Embed

from snowball.config import config
from snowball.listeners import DiscordListener
from snowball.util import register


@register('help')
def call(bot, listener, target, author, message, private):
    """Sends a private message detailing the available commands."""
    if isinstance(listener, DiscordListener):
        embed = Embed(title='Help!')
        for trigger, command in sorted(bot.commands.items()):
            if _applicable_listener(listener, command.call):
                embed.add_field(
                    name=f'{config["trigger_character"]}{trigger}',
                    value=_generate_help_text(command.call),
                    inline=False,
                )

        return {
            'target': author,
            'message': embed,
            'private': True,
            'embed': True,
        }
    return _generate_help_lines(bot, author, listener)


def _generate_help_lines(bot, author, listener):
    longest = max(len(t) for t in bot.commands)
    for trigger, command in sorted(bot.commands.items()):
        if _applicable_listener(listener, command.call):
            yield {
                'target': author,
                'message': (
                    f'{config["trigger_character"]}'
                    f'{trigger.ljust(longest)} | '
                    f'{_generate_help_text(command.call)}'
                ),
            }


def _applicable_listener(listener, call):
    return (
        not hasattr(call, 'listeners') or
        type(listener) in call.listeners
    )


def _generate_help_text(call):
    doc = inspect.getdoc(call)
    if hasattr(call, 'admin_only'):
        doc = f'{doc} (admin only)'
    if hasattr(call, 'channel_only'):
        doc = f'{doc} (channel only)'
    if hasattr(call, 'private_message_only'):
        doc = f'{doc} (PM only)'
    return doc
