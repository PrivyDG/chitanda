import asyncio
import logging
from types import GeneratorType

from snowball import BotError
from snowball.commands import load_commands
from snowball.config import config
from snowball.listeners import DiscordListener, IRCListener

logger = logging.getLogger(__name__)


class Snowball:

    commands = {}

    def __init__(self):
        self.irc_listeners = {}
        self.discord_listener = None
        load_commands(self)

    def connect(self):
        logger.info('Initiating connection to listeners.')
        if config['irc_servers']:
            logger.info('IRC Servers found, connecting...')
            self._connect_irc()
        if config['discord_token']:
            logger.info('Discord token found, connecting...')
            self._connect_discord()

    def _connect_irc(self):
        for hostname, server in config['irc_servers'].items():
            logger.info(f'Connecting to IRC server: {hostname}.')
            self.irc_listeners[hostname] = IRCListener(
                self, server['nickname'], hostname
            )
            asyncio.ensure_future(
                self.irc_listeners[hostname].connect(
                    hostname,
                    server['port'],
                    tls=server['tls'],
                    tls_verify=server['tls_verify'],
                )
            )

    def _connect_discord(self):
        self.discord_listener = DiscordListener(self)
        self.discord_listener.run(config['discord_token'])

    async def dispatch_command(
        self,
        listener,
        target,
        author,
        message,
        private,
    ):
        logger.info(
            f'Message received on {listener} in channel {target} '
            f'from {author}: {message}'
        )
        try:
            if not message.startswith(config['trigger_character']):
                return

            trigger = message.split(' ', 1)[0].lower()
            command = self.commands[trigger[1:]]
        except (IndexError, KeyError):
            return

        logger.info(f'Command triggered: {trigger}.')
        try:
            response = command.call(
                self,
                listener,
                target,
                author,
                message.split(' ', 1)[1] if ' ' in message else '',
                private,
            )
        except BotError as e:
            logger.info(f'Error triggered by {author}: {e}.')
            response = {
                'target': target,
                'message': f'Error: {e}',
            }

        if response:
            await self._send_response(listener, target, response)

    async def _send_response(self, listener, target, response):
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
