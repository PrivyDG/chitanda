from snowball.database import database
from snowball.util import args, channel_only, register


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
    return f'{args[0]} will be told when next seen.'
