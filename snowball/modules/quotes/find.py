from snowball.database import database
from snowball.util import args, channel_only, register


@register('findquote')
@channel_only
@args(r'(.+)')
async def call(*, bot, listener, target, author, args, private):
    """Find a quote by its content."""
    with database() as (conn, cursor):
        cursor.execute(
            """
            SELECT
                id,
                quote,
                time,
                adder
            FROM quotes
            WHERE
                channel = ?
                AND listener = ?
                AND quote LIKE ?
            ORDER BY random()
            LIMIT 3
            """,
            (target, str(listener), f'%{args[0]}%'),
        )
        quotes = cursor.fetchall()
        if quotes:
            for quote in quotes:
                yield f'#{quote["id"]} by {quote["adder"]}: {quote["quote"]}'
        else:
            yield 'No quotes found.'
