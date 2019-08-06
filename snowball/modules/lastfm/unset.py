from snowball.database import database
from snowball.util import args, auth_only, register


@register('unsetplaying')
@auth_only
@args(r'$')
async def call(bot, listener, target, author, args, private, username):
    """Unset your Last.FM name."""
    with database() as (conn, cursor):
        cursor.execute(
            """
            SELECT 1
            FROM lastfm
            WHERE user = ?  AND listener = ?
            """,
            (username, str(listener)),
        )
        if cursor.fetchone():
            cursor.execute(
                """
                DELETE FROM lastfm
                WHERE user = ?  AND listener = ?
                """,
                (username, str(listener)),
            )
            conn.commit()
            return 'Unset Last.FM username.'
        return 'No Last.FM username to unset.'
