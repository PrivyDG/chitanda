import asyncio
import logging

import requests

from snowball import USER_AGENT, BotError
from snowball.config import config
from snowball.util import args, register

logger = logging.getLogger(__name__)


@register('wolframalpha')
@args(r'(.+)')
async def call(bot, listener, target, author, args, private):
    """Queries the Wolfram|Alpha API and relays the response."""
    future = asyncio.get_event_loop().run_in_executor(
        None, lambda: requests.get(
            'https://api.wolframalpha.com/v1/result',
            headers={'User-Agent': USER_AGENT},
            params={
                'appid': config['wolframalpha']['appid'],
                'i': args[0],
            },
            timeout=15,
        )
    )

    try:
        response = (await future).text
    except requests.RequestException as e:
        logger.error(f'Failed to query Wolfram|Alpha: {e}')
        raise BotError('Failed to query Wolfram|Alpha.')

    return f'{response[:497]}...' if len(response) >= 500 else response
