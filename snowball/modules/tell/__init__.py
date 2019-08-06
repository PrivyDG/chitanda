import logging
from datetime import datetime

from snowball.database import database
from snowball.util import args, channel_only, register

logger = logging.getLogger(__name__)

TIME_FORMAT = '%b %d, %Y %H:%M:%S'


def setup(bot):
    bot.message_handlers.append(tell_handler)


async def tell_handler(listener, target, author, message, private):
    if private:
        return

    for row in _fetch_tells(target, listener, author):
        time = datetime.fromisoformat(row['time']).strftime(TIME_FORMAT)
        logger.info(f'Sent tell to {author} in {target} on {listener}.')
        yield f'{author}: On {time}, {row["sender"]} said: {row["message"]}'
        _delete_tell(row['id'])


@register('tell')
@channel_only
@args(r'([^ ]+) (.+)')
async def call(bot, listener, target, author, args, private):
    """Save a message for a user the next time they are seen."""
    with database() as (conn, cursor):
        cursor.execute(
            """
            INSERT INTO tells (
                channel, listener, message, recipient, sender
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                target,
                str(listener),
                args[1],
                args[0],
                author,
            ),
        )
        conn.commit()
    logger.info(f'Added a tell for {args[0]} in {target} on {listener}')
    return f'{args[0]} will be told when next seen.'


def _fetch_tells(target, listener, author):
    with database() as (conn, cursor):
        cursor.execute(
            """
            SELECT
                id,
                message,
                time,
                sender
            FROM tells
            WHERE
                channel = ?
                AND listener = ?
                AND recipient = ?
            ORDER BY id ASC
            """,
            (target, str(listener), author),
        )
        return cursor.fetchall()


def _delete_tell(tell_id):
    logger.debug(f'Deleting tell {tell_id}.')
    with database() as (conn, cursor):
        cursor.execute('DELETE FROM tells WHERE id = ?', (tell_id, ))
        conn.commit()
