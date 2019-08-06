import asyncio
import logging
from collections import defaultdict

from snowball.database import database

logger = logging.getLogger(__name__)


def setup(bot):
    _add_handlers_to_irc_listener()
    channels = _get_channels_to_rejoin()
    asyncio.ensure_future(_rejoin_channels(bot, channels))


def _add_handlers_to_irc_listener():
    from snowball.bot import IRCListener

    async def on_join(self, channel, user):
        if self.is_same_nick(self.nickname, user):
            with database() as (conn, cursor):
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO irc_channels (name, server)
                    VALUES (?, ?)
                    """,
                    (channel, self.hostname),
                )
                cursor.execute(
                    """
                    UPDATE irc_channels SET active = 1
                    WHERE name = ? AND server = ?
                    """,
                    (channel, self.hostname),
                )
                conn.commit()

        await super(IRCListener, self).on_join(channel, user)

    IRCListener.on_join = on_join

    async def on_part(self, channel, user, reason):
        if self.is_same_nick(self.nickname, user):
            with database() as (conn, cursor):
                cursor.execute(
                    """
                    UPDATE irc_channels SET active = 0
                    WHERE name = ? AND server = ?
                    """,
                    (channel, self.hostname),
                )
                conn.commit()

        await super(IRCListener, self).on_part(channel, user, reason)

    IRCListener.on_part = on_part


def _get_channels_to_rejoin():
    # Map server to a list of channels
    channels = defaultdict(list)

    with database() as (conn, cursor):
        cursor.execute(
            """
            SELECT name, server
            FROM irc_channels
            WHERE active = 1
            """
        )
        for row in cursor.fetchall():
            channels[row['server']].append(row['name'])

    return channels


async def _rejoin_channels(bot, channels):
    """
    Loop until the IRC listeners establish ther connections to the
    IRC servers, then join the channels the bot was previously in.
    """
    while True:
        for server, chan_names in list(channels.items()):
            if (
                server in bot.irc_listeners
                and bot.irc_listeners[server].performed
            ):
                for name in chan_names:
                    logger.info(f'Rejoining IRC channel {name} on {server}.')
                    await bot.irc_listeners[server].join(name)
                del channels[server]

        if not channels:
            logger.info('All IRC channels rejoined.')
            break
        await asyncio.sleep(0.1)
