import asyncio

import requests

from snowball import BotError
from snowball.config import config
from snowball.util import args, register


@register('wolframalpha')
@args(r'(.+)')
async def call(bot, listener, target, author, args, private):
    """Queries the Wolfram|Alpha API and relays the response."""
    future = asyncio.get_event_loop().run_in_executor(
        None, lambda: requests.get(
            'https://api.wolframalpha.com/v1/result',
            headers={'User-Agent': 'snowball irc and discord bot'},
            params={
                'appid': config['wolframalpha']['appid'],
                'i': args[0],
            },
            timeout=5,
        )
    )

    try:
        response = (await future).text
    except requests.RequestException:
        raise BotError('Failed to query Wolfram|Alpha.')

    return f'{response[:497]}...' if len(response) >= 500 else response
