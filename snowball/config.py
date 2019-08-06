import json
import logging
import sys

from snowball import CONFIG_DIR

logger = logging.getLogger(__name__)

CONFIG_PATH = CONFIG_DIR / 'config.json'

BLANK_CONFIG = {
    'trigger_character': '!',
    'user_agent': 'snowball irc/discord bot',
    'irc_servers': {},
    'discord_token': '',
    'webserver': {
        'enable': False,
        'port': 38428,
    },
    'modules_enabled': [],
    'aliases': {},
    'admins': {},
}


class Config:
    def __init__(self):
        self.config = None  # Lazy load config.

    def __getitem__(self, key):
        if self.config is None:
            self.config = self.load_config()

        try:
            return self.config[key]
        except TypeError:
            logger.critical('Configuration dictionary missing, exiting.')
            sys.exit(1)

    def reload(self):
        self.config = self.load_config()

    def load_config(self):
        if not CONFIG_PATH.exists():
            return {}
        with open(CONFIG_PATH, 'r') as cf:
            try:
                return json.load(cf)
            except json.decoder.JSONDecodeError:
                logger.critical('Config is not valid JSON.')


config = Config()
