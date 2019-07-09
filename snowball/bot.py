import asyncio
import logging
from types import GeneratorType

from pydle import ClientPool as IRCClientPool

from snowball.commands import load_commands
from snowball.config import Config
from snowball.listeners import DiscordListener, IRCListener

logger = logging.getLogger(__name__)


class Snowball:

    commands = {}

    def __init__(self):
        self.config = Config()
        self.irc_listeners = {}
        self.discord_listener = None
        load_commands()

    def connect(self):
        logger.info('Initiating connection to listeners.')
        if self.config['irc_servers']:
            logger.info('IRC Servers found, connecting...')
            self._connect_irc()
        if self.config['discord_token']:
            logger.info('Discord token found, connecting...')
            self._connect_discord()

    def _connect_irc(self):
        pool = IRCClientPool()
        for hostname, server in self.config['irc_servers'].items():
            logger.info(f'Connecting to IRC server: {hostname}.')
            self.irc_listeners[hostname] = IRCListener(
                self, server['nickname'], hostname
            )
            pool.connect(
                self.irc_listeners[hostname],
                hostname,
                server['port'],
                tls=server['tls'],
                tls_verify=server['tls_verify'],
            )

    def _connect_discord(self):
        self.discord_listener = DiscordListener(self)
        self.discord_listener.run(self.config['discord_token'])

    async def dispatch_command(self, listener, target, author, message):
        logger.info(
            f'Message received on {listener.__class__.__name__} in '
            f'channel {target} from {author}: {message}'
        )
        try:
            if not message.startswith(self.config['trigger_character']):
                return

            trigger = message.split(' ', 1)[0].lower()
            command = self.commands[trigger[1:]]
        except (IndexError, KeyError):
            return

        logger.info(f'Command triggered: {trigger}.')
        response = command.call(self, listener, target, author, message)

        if isinstance(response, GeneratorType):
            logger.info('Response received as generator, sending to target.')
            for resp in response:
                if isinstance(resp, str):
                    resp = {'target': target, 'message': resp}
                await listener.message(**resp)
        elif isinstance(response, str):
            logger.info('Response received as str, sending to target.')
            await listener.message(target, response)
        else:
            logger.info('Response received as dict, sending to target.')
            await listener.message(**response)
