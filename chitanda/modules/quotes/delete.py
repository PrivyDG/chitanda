from chitanda import BotError
from chitanda.database import database
from chitanda.util import admin_only, args, channel_only, register

from . import fetch


@register('delquote')
@channel_only
@admin_only
@args(r'(.+)')
async def call(*, bot, listener, target, author, args, private):
    """Delete a quote from the database."""
    quote_ids = _parse_quote_ids(args[0])
    with database() as (conn, cursor):
        yield 'Deleted the following quotes:'
        for quote in fetch.fetch_quotes(
            cursor, target, listener, quote_ids.copy()
        ):
            yield quote

        cursor.execute(
            """
            DELETE FROM quotes
            WHERE
                channel = ?
                AND listener = ?
                AND id IN ("""
            + (','.join(['?'] * len(quote_ids)))
            + """)
            """,
            (target, str(listener), *quote_ids),
        )

        conn.commit()


def _parse_quote_ids(message):
    try:
        quote_ids = [int(qid) for qid in message.split(' ')]
    except ValueError:
        raise BotError('Quote IDs must be integers.')
    return quote_ids
