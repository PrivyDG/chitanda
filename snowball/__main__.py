import asyncio

from snowball import cmdgroup
from snowball.bot import Snowball
from snowball.tasks import huey
from snowball.migrate import migrate  # noqa


@cmdgroup.command()
def run():
    """Run the bot."""
    huey.start()
    bot = Snowball()
    bot.connect()
    asyncio.get_event_loop().run_forever()
