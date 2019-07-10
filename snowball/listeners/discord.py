import logging
import re
from collections import defaultdict, deque
from functools import partial

import discord

logger = logging.getLogger(__name__)


class DiscordListener(discord.Client):

    def __init__(self, bot):
        self.bot = bot
        self.message_lock = defaultdict(lambda: False)
        self.message_queue = defaultdict(partial(deque))
        super().__init__()

    def __repr__(self):
        return 'DiscordListener'

    async def message(self, target, message, private=False, embed=False):
        if private:
            target = await self.get_dm_channel_id(target)

        logger.info(
            f'Adding "{message}" to Discord message queue for {target}.'
        )
        self.message_queue[target].append((message, embed))

        if not self.message_lock[target]:
            self.message_lock[target] = True
            try:
                discord_channel = self.get_channel(target)

                logger.info(
                    f'Sending "{message}" on Discord to {discord_channel}.'
                )
                while self.message_queue[target]:
                    message, embed = self.message_queue[target].popleft()
                    await discord_channel.send(
                        **{('embed' if embed else 'content'): message}
                    )
            finally:
                self.message_lock[target] = False

    async def get_dm_channel_id(self, user_id):
        discord_user = await self.fetch_user(user_id)
        if not discord_user.dm_channel:
            await discord_user.create_dm()
        return discord_user.dm_channel.id

    async def on_message(self, message):
        if not message.author.bot:
            await self.bot.dispatch_command(
                self,
                message.channel.id,
                message.author.id,
                message.content,
                private=isinstance(message.channel, discord.DMChannel),
            )
