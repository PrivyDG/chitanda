import logging
import re
from collections import defaultdict, deque
from functools import partial

from chitanda import BotError
from chitanda.listeners import DiscordListener, IRCListener
from chitanda.util import args, channel_only, irc_unstyle, register

logger = logging.getLogger(__name__)

REGEX = re.compile(r'\.?s/(.*?)(?<!\\)/(.*?)(?:(?<!\\)/([gi]{,2})?)?$')


def setup(bot):
    bot.message_handlers.append(on_message)
    bot.response_handlers.append(on_response)


async def on_message(listener, target, author, message, private):
    if private:
        return

    _attach_message_log(listener)

    match = REGEX.match(message)
    message_log = listener.message_log[target]
    if match:
        return _substitute(match, message_log)
    else:
        message_log.appendleft(_format_message(message, author, listener))


def on_response(listener, target, response):
    _attach_message_log(listener)
    listener.message_log[target].appendleft(
        _format_message(response, _get_author(listener), listener)
    )


def _attach_message_log(listener):
    if not hasattr(listener, 'message_log'):
        listener.message_log = defaultdict(partial(deque, maxlen=1024))


def _get_author(listener):
    if isinstance(listener, DiscordListener):
        return f'<@listener.user.id>'
    elif isinstance(listener, IRCListener):
        return listener.nickname


@register('sed')
@channel_only
@args(REGEX)
def call(*, bot, listener, target, author, args, private):
    """Find and replace a message in the message history."""
    return _substitute(args, listener.message_log[target])


def _substitute(match, message_log):
    flags = _parse_flags(match[3])
    regex = _compile_regex(match[1], flags)

    for message in message_log:
        if regex.search(message):
            return regex.sub(
                match[2], message, count=0 if flags['global'] else 1
            )

    return 'No matching message found.'


def _parse_flags(flags):
    return {
        'global': 'g' in flags if flags else False,
        'nocase': 'i' in flags if flags else False,
    }


def _compile_regex(regex, flags):
    try:
        if flags['nocase']:
            return re.compile(regex, flags=re.IGNORECASE)
        return re.compile(regex)
    except Exception as e:  # noqa E722
        raise BotError(f'{regex} is not a valid regex.') from e


def _format_message(message, author, listener):
    if isinstance(listener, DiscordListener):
        author = f'<@{author}>'
    if isinstance(listener, IRCListener):
        message = irc_unstyle(message)
    return f'<{author}> {message}'
