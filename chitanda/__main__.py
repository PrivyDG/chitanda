import asyncio
import json

import click

import chitanda.database  # noqa
from chitanda import cmdgroup, create_app_dirs, huey
from chitanda.bot import Chitanda
from chitanda.config import BLANK_CONFIG, CONFIG_PATH
from chitanda.database import (
    confirm_database_is_updated,
    create_database_if_nonexistent,
)


@cmdgroup.command()
def run():
    """Run the bot."""
    huey.start()
    bot = Chitanda()
    bot.connect()
    asyncio.get_event_loop().run_forever()


@cmdgroup.command()
def config():
    """Edit the configuration file."""
    if not CONFIG_PATH.is_file():
        with open(CONFIG_PATH, 'w') as f:
            json.dump(BLANK_CONFIG, f, indent=4)
    click.edit(filename=CONFIG_PATH)


def main():
    create_app_dirs()
    create_database_if_nonexistent()
    confirm_database_is_updated()
    cmdgroup()


if __name__ == '__main__':
    main()
