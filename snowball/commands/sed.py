import logging
import re
from collections import defaultdict, deque
from functools import partial

from ircmessage import unstyle

from snowball import BotError
from snowball.listeners import DiscordListener, IRCListener

logger = logging.getLogger(__name__)

REGEX = re.compile(r'\.?s/(.*?)(?<!\\)/(.*?)(?:(?<!\\)/([gi]{,2})?)?$')


def setup(bot):

    async def handler(listener, target, author, message, private):
        if private:
            return

        if not hasattr(listener, 'message_log'):
            listener.message_log = defaultdict(partial(deque, maxlen=1024))

        if isinstance(listener, IRCListener):
            message = unstyle(message)

        match = REGEX.match(message)
        if match:
            try:
                new_message = _substitute(match, listener.message_log[target])
            except BotError as e:
                new_message = f'Error: {e}'
            await listener.message(target, new_message)
        else:
            listener.message_log[target].appendleft(
                _format_message(message, author, listener)
            )

    bot.message_handlers.append(handler)


def _substitute(match, message_log):
    flags = _parse_flags(match[3])
    try:
        regex = re.compile(
            match[1], **({'flags': re.IGNORECASE} if flags['nocase'] else {})
        )
    except Exception as e:  # noqa E722
        raise BotError(f'{match[1]} is not a valid regex.')

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


def _format_message(message, author, listener):
    if isinstance(listener, DiscordListener):
        author = f'<@{author}>'

    return f'<{author}> {message}'
