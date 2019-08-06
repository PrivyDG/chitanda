from snowball.database import database
from snowball.util import args, auth_only, register


@register('setplaying')
@auth_only
@args(r'([^ ]+)$')
async def call(*, bot, listener, target, author, args, private, username):
    """Set a Last.FM name for the nowplaying command."""
    lastfm = args[0]
    with database() as (conn, cursor):
        cursor.execute(
            """
            INSERT OR IGNORE INTO lastfm (
                user, listener, lastfm
            ) VALUES (?, ?, ?)
            """,
            (username, str(listener), lastfm),
        )
        cursor.execute(
            'UPDATE lastfm SET lastfm = ? WHERE user = ? AND listener = ?',
            (lastfm, username, str(listener)),
        )
        conn.commit()
    return f'Set Last.FM username to {lastfm}.'
