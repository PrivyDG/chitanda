from collections import deque, defaultdict
from functools import partial

import discord


class DiscordListener(discord.Client):

    def __init__(self, bot):
        self.bot = bot
        self.message_lock = defaultdict(bool)
        self.message_queue = defaultdict(partial(deque))
        super().__init__()

    async def message(self, channel_id, message):
        self.message_queue[channel_id].append(message)
        if not self.message_lock[channel_id]:
            self.message_lock[channel_id] = True
            discord_channel = self.get_channel(channel_id)
            try:
                while self.message_queue[channel_id]:
                    message = self.message_queue[channel_id].popleft()
                    await discord_channel.send(message)
            finally:
                self.message_lock[channel_id] = False

    async def private_message(self, user_id, message):
        discord_user = self.fetch_user(user_id)
        dm_channel = discord_user.dm_channel
        if dm_channel:
            await self.message(dm_channel.id, message)
        else:
            await discord_user.create_dm()
            await self.message(discord_user.dm_channel.id, message)

    async def on_message(self, message):
        if not message.author.bot:
            self.bot.receive_discord_message(
                self,
                message.channel.id,
                f'<@{message.author.id}',
                message.content,
            )
