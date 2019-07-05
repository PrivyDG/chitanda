import asyncio
from types import GeneratorType

import pydle

import config
from snowball.commands import load_commands


class Snowball(
    pydle.Client,
    pydle.features.TLSSupport,
    pydle.features.RFC1459Support,
):

    commands = {}

    def __init__(self, *args, **kwargs):
        load_commands()
        super().__init__(*args, **kwargs)

    async def on_connect(self):
        if config.NICKSERV_PASS:
            await self.raw(f'NICKSERV IDENTIFY {config.NICKSERV_PASS}\r\n')
        await self.set_mode(self.nickname, 'BI')
        await self.join(config.CHANNEL)
        await self.loop_interrupter()

    async def loop_interrupter(self):
        """
        Pydle's event loop is blocking outside coroutines from running.
        This is a problem. So I am doing this.
        """
        while True:
            await asyncio.sleep(0.01)

    async def message(self, message):
        return await super().message(config.CHANNEL, message)

    async def on_channel_message(self, target, author, message):
        if target != config.CHANNEL:
            return
        try:
            command = message.split(' ', 1)[0].lower()
            resp = self.commands[command].call(self, author, message)
            if isinstance(resp, str):
                await self.message(resp)
            elif isinstance(resp, GeneratorType):
                for msg in resp:
                    await self.message(msg)
        except (IndexError, KeyError):
            pass
