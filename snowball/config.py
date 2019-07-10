import json
import logging
import sys

from snowball import CONFIG_PATH

logger = logging.getLogger(__name__)

BLANK_CONFIG = {
    'trigger_character': '!',
    'irc_servers': {},
    'discord_token': '',
    'modules_enabled': [],
    'admins': {},
}


class Config:
    def __init__(self):
        self.config = self.load_config()

    def __getitem__(self, key):
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
