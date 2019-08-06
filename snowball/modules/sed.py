import logging
import re
from collections import defaultdict, deque
from functools import partial

from ircmessage import unstyle

from snowball import BotError
from snowball.listeners import DiscordListener, IRCListener
from snowball.util import args, channel_only, register

logger = logging.getLogger(__name__)

REGEX = re.compile(r'\.?s/(.*?)(?<!\\)/(.*?)(?:(?<!\\)/([gi]{,2})?)?$')


def setup(bot):
    bot.message_handlers.append(on_message)


async def on_message(listener, target, author, message, private):
    if private:
        return

    if not hasattr(listener, 'message_log'):
        listener.message_log = defaultdict(partial(deque, maxlen=1024))

    match = REGEX.match(message)
    message_log = listener.message_log[target]
    if match:
        return _substitute(match, message_log)
    else:
        message_log.appendleft(_format_message(message, author, listener))


@register('sed')
@channel_only
@args(REGEX)
def call(*, bot, listener, target, author, args, private):
    return _substitute(args, listener.message_log[target])


def _substitute(match, message_log):
    flags = _parse_flags(match[3])
    regex = _compile_regex(match, flags)

    for message in message_log:
        if regex.search(message):
            return regex.sub(
                match[2],
                message,
                count=0 if flags['global'] else 1,
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
        message = unstyle(message)
    return f'<{author}> {message}'
