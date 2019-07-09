import asyncio

import pydle


class IRCListener(
    pydle.Client,
    pydle.features.TLSSupport,
    pydle.features.RFC1459Support,
):

    def __init__(self, bot, host, port, tls, tls_verify):
        self.bot = bot
        self.host = host
        self.port = port
        self.tls = tls
        self.tls_verify = self.tls_verify
        super().__init__(host, port, tls=tls, tls_verify=tls_verify)

    async def on_connect(self):
        await self.set_mode(self.nickname, 'BI')
        await self._auth_nickserv()
        await self._join_channels()
        await self._loop_interrupter()

    async def _auth_nickserv(self):
        # check against list of nickserv passwords
        pass

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

    async def on_channel_message(self, target, author, message):
        self.bot.dispatch_command(self, target, author, message)
