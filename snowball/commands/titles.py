import asyncio
import html
import logging
import re

import requests

from snowball.config import config
from snowball.listeners import IRCListener

logger = logging.getLogger(__name__)

URL_REGEX = re.compile(r'.*(https?:\/\/[^ \.]+\.[^ ]+)+.*')
TITLE_REGEX = re.compile(r'<title>(.*?)</title>')


def setup(bot):
    async def title_handler(listener, target, author, message, private):
        if isinstance(listener, IRCListener) and not private:
            matches = URL_REGEX.search(message)
            if matches:
                for match in matches.groups():
                    try:
                        title = await _get_title(match)
                    except (requests.RequestException, UnicodeDecodeError):
                        continue

                    if title:
                        logger.info(
                            f'Title found from {match} in {target} '
                            f'from {listener}'
                        )
                        await listener.message(target, title)

    bot.message_handlers.append(title_handler)


async def _get_title(url):
    response = await asyncio.get_event_loop().run_in_executor(
        None, lambda: requests.get(
            url,
            headers={'User-Agent': config['user_agent']},
            stream=True,
            timeout=5,
        )
    )

    data = response.raw.read(512000, decode_content=True).decode('utf-8')
    text = ' '.join(re.split(r'\r|\n|\r\n', html.unescape(data.strip())))
    match = TITLE_REGEX.search(text)
    if match:
        return f'Title: {match[1]}'
