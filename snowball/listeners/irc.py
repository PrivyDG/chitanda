import asyncio

import pydle


class IRCListener(
    pydle.Client,
    pydle.features.TLSSupport,
    pydle.features.RFC1459Support,
):

    def __init__(self, bot, nickname, hostname):
        self.bot = bot
        self.hostname = hostname
        super().__init__(nickname, username=nickname, realname=nickname)

    async def on_connect(self):
        await self.set_mode(self.nickname, 'BI')
        await self._perform()
        await self._join_channels()
        await self._loop_interrupter()

    async def _perform(self):
        for cmd in self.bot.config['irc_servers'][self.hostname]['perform']:
            await self.raw(cmd)

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
        super().message(target, message)

    async def on_channel_message(self, target, author, message):
        await self.bot.dispatch_command(self, target, author, message)
