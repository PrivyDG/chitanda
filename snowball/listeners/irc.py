import asyncio
import logging

import pydle

from snowball.config import config

logger = logging.getLogger(__name__)


class IRCListener(
    pydle.Client,
    pydle.features.TLSSupport,
    pydle.features.RFC1459Support,
):

    def __init__(self, bot, nickname, hostname):
        self.bot = bot
        self.hostname = hostname
        super().__init__(nickname, username=nickname, realname=nickname)

    def __repr__(self):
        return f'IRCListener@{self.hostname}'

    async def on_connect(self):
        await self.set_mode(self.nickname, 'BI')
        await self._perform()
        await self._join_channels()
        await self._loop_interrupter()

    async def _perform(self):
        logger.info(f'Running IRC perform commands on {self.hostname}.')
        for cmd in config['irc_servers'][self.hostname]['perform']:
            await self.raw(f'{cmd}\r\n')

    async def _join_channels(self):
        # await self.join(channel)
        pass

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
            await self.bot.dispatch_command(
                self,
                target,
                by,
                message,
                private=False,
            )

    async def on_private_message(self, target, by, message):
        if by != self.nickname:
            await self.bot.dispatch_command(
                self,
                by,
                by,
                message,
                private=True,
            )

    async def on_raw(self, message):
        logger.debug(f'Received raw IRC message: {message}')
        await super().on_raw(message)
