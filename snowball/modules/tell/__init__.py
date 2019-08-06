import logging

from snowball.database import database

logger = logging.getLogger(__name__)


def setup(bot):
    async def tell_handler(listener, target, author, message, private):
        if private:
            return

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
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    logger.info(
                        f'Sending tell to {author} in {target} on {listener}.'
                    )
                    await listener.message(target, (
                        f'{author}: On {row["time"]}, {row["sender"]} '
                        f'said: {row["message"]}'
                    ))
                    cursor.execute(
                        'DELETE FROM tells WHERE id = ?', (row['id'], )
                    )
                conn.commit()

    bot.message_handlers.append(tell_handler)
