import inspect

from snowball.util import register


@register('help')
def call(bot, listener, author, message):
    """Sends a private message detailing the available commands."""
    longest = max(len(t) for t in bot.commands)
    for trigger, command in sorted(bot.commands.items()):
        doc = inspect.getdoc(command.call)
        yield f'{trigger.ljust(longest)} - {doc}'
