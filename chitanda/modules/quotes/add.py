from chitanda.database import database
from chitanda.util import args, auth_only, channel_only, register


@register('addquote')
@channel_only
@auth_only
@args(r'(.+)')
async def call(*, bot, listener, target, author, args, private, username):
    """Add a quote to the database."""
    with database() as (conn, cursor):
        new_quote_id = _get_quote_id(cursor, listener, target)
        cursor.execute(
            """
            INSERT INTO quotes (
                id, channel, listener, quote, adder
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                new_quote_id,
                target,
                str(listener),
                args[0],
                username,
            ),
        )
        conn.commit()
    return f'Added quote with ID {new_quote_id}.'


def _get_quote_id(cursor, listener, target):
    cursor.execute(
        """
        SELECT max(id)
        FROM quotes
        WHERE listener = ? AND channel = ?
        """,
        (str(listener), target),
    )
    row = cursor.fetchone()
    return row[0] + 1 if row else 1
