import asyncio
import json

import click

from snowball import cmdgroup
from snowball.bot import Snowball
from snowball.config import BLANK_CONFIG
from snowball import CONFIG_PATH
from snowball.tasks import huey


@cmdgroup.command()
def run():
    """Run the bot."""
    huey.start()
    bot = Snowball()
    bot.connect()
    asyncio.get_event_loop().run_forever()


@cmdgroup.command()
def config():
    """Edit the configuration file."""
    if not CONFIG_PATH.is_file():
        with open(CONFIG_PATH, 'w') as f:
            json.dump(BLANK_CONFIG, f, indent=4)
    click.edit(filename=CONFIG_PATH)


@cmdgroup.command()
def migrate():
    """Upgrade the database to the latest migration."""
    pass


cmdgroup()
