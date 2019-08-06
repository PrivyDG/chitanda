import asyncio
import html
import logging
import re

import requests

from snowball.config import config
from snowball.listeners import IRCListener
from snowball.util import trim_message

logger = logging.getLogger(__name__)

URL_REGEX = re.compile(r'.*(https?:\/\/[^ \.]+\.[^ ]+)+.*')
TITLE_REGEX = re.compile(r'<title>(.*?)</title>')


def setup(bot):
    bot.message_handlers.append(title_handler)


async def title_handler(listener, target, author, message, private):
    if isinstance(listener, IRCListener) and not private:
        matches = URL_REGEX.search(message)
        if not matches:
            return

        for match in matches.groups():
            title = await _get_title(match)
            if title:
                yield title
                logger.info(
                    f'Title relayed from {match} in {target} from {listener}'
                )


async def _get_title(url):
    try:
        response = await asyncio.get_event_loop().run_in_executor(
            None, lambda: requests.get(
                url,
                headers={'User-Agent': config['user_agent']},
                stream=True,
                timeout=5,
            )
        )
        data = response.raw.read(512000, decode_content=True).decode('utf-8')
    except (requests.RequestException, UnicodeDecodeError):
        return

    match = TITLE_REGEX.search(
        ' '.join(re.split(r'\r|\n|\r\n', html.unescape(data))).strip()
    )
    if match:
        return f'Title: {trim_message(match[1], length=400)}'
