import asyncio
import logging

import pydle

from snowball.config import config

logger = logging.getLogger(__name__)


class IRCListener(
    pydle.Client,
    pydle.features.AccountSupport,
    pydle.features.TLSSupport,
    pydle.features.RFC1459Support,
):

    message_handlers = {
        'channel': [],
        'pm': [],
    }

    def __init__(self, bot, nickname, hostname):
        self.bot = bot
        self.hostname = hostname
        self.performed = False  # Whether or not performs have been sent.
        super().__init__(nickname, username=nickname, realname=nickname)

    def __repr__(self):
        return f'IRCListener@{self.hostname}'

    async def on_connect(self):
        await self.set_mode(self.nickname, 'BI')
        await self._perform()
        await self._loop_interrupter()

    async def _perform(self):
        logger.info(f'Running IRC perform commands on {self.hostname}.')
        for cmd in config['irc_servers'][self.hostname]['perform']:
            await self.raw(f'{cmd}\r\n')
        self.performed = True

    async def _loop_interrupter(self):
        """
        Pydle's event loop blocks other coroutines from running.
        So there now is this.
        """
        while True:
            await asyncio.sleep(0.01)

    async def on_disconnect(self, expected):
        if not expected:
            # TODO: Reconnect
            pass

    async def message(self, target, message, **_):
        logger.info(
            f'Sending "{message}" on IRC ({self.hostname}) to {target}.'
        )
        await super().message(target, message)

    async def on_channel_message(self, target, by, message):
        if by != self.nickname:
            args = {
                'listener': self,
                'target': target,
                'author': by,
                'message': message,
                'private': False,
            }
            await self.bot.handle_message(**args)

    async def on_private_message(self, target, by, message):
        if by != self.nickname:
            args = {
                'listener': self,
                'target': by,
                'author': by,
                'message': message,
                'private': True,
            }
            await self.bot.handle_message(**args)

    async def on_raw(self, message):
        logger.debug(f'Received raw IRC message: {message}'.rstrip())
        await super().on_raw(message)

    async def is_admin(self, user):
        info = await self.whois(user)
        return (
            info['identified'] and
            info['account'] in config['admins'].get(str(self), [])
        )

    async def is_authed(self, user):
        info = await self.whois(user)
        return info['identified'] and info['account']
