import asyncio
import logging
import re
from json import JSONDecodeError

import requests

from chitanda import BotError
from chitanda.config import config
from chitanda.util import args, register

logger = logging.getLogger(__name__)


@register('urbandictionary')
@args(r'(\d+) (.+)', r'(.+)')
async def call(*, bot, listener, target, author, args, private):
    """Queries the UrbanDictionary API and relays the response."""
    entry = int(args[0]) if len(args) == 2 else 1
    search = args[-1]

    future = asyncio.get_event_loop().run_in_executor(
        None,
        lambda: requests.get(
            'https://api.urbandictionary.com/v0/define',
            headers={'User-Agent': config['user_agent']},
            params={'term': search},
            timeout=15,
        ),
    )

    try:
        response = (await future).json()
    except (requests.RequestException, JSONDecodeError) as e:
        logger.error(f'Failed to query UrbanDictionary: {e}')
        raise BotError('Failed to query UrbanDictionary.')

    if not response['list']:
        raise BotError(
            f'Could not find a definition for {search.rstrip(".")}.'
        )

    defi = (
        re.sub(
            r'\[(.*?)\]',
            r'\1',
            sorted(
                response['list'],
                key=lambda x: int(x['thumbs_up']) - int(x['thumbs_down']),
                reverse=True,
            )[entry]['definition'],
        )
        .strip()
        .replace('\n', ' ')
    )

    return f'{defi[:497]}...' if len(defi) >= 500 else defi
