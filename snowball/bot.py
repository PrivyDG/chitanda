import asyncio
import logging
import sys
from types import AsyncGeneratorType, GeneratorType

from aiohttp import web
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
        self.message_handlers = []
        if config['webserver']['enable']:
            self.web_application = web.Application()
        load_commands(self)
        if config['webserver']['enable']:
            self.webserver = self._start_webserver()

    def _start_webserver(self):
        try:
            return asyncio.ensure_future(
                asyncio.get_event_loop().create_server(
                    self.web_application.make_handler(),
                    host='0.0.0.0',
                    port=int(config['webserver']['port']),
                )
            )
        except ValueError:
            logging.critical('Invalid port value for webserver.')
            sys.exit(1)

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

    async def handle_message(self, listener, target, author, message, private):
        for handler in self.message_handlers:
            await handler(listener, target, author, message, private)

    async def dispatch_command(
        self, listener, target, author, message, private,
    ):
        logger.info(
            f'Message received on {listener} in channel {target} '
            f'from {author}: {message}'
        )
        try:
            if not message.startswith(config['trigger_character']):
                return

            trigger, message = self._resolve_alias(*message[1:].split(' ', 1))
            command = self.commands[trigger]
        except (IndexError, KeyError):
            return

        logger.info(f'Command triggered: {trigger}.')
        response = command.call(
            self, listener, target, author, message, private,
        )
        try:
            if response:
                await self._send_response(listener, target, response)
        except BotError as e:
            logger.info(f'Error triggered by {author}: {e}.')
            await listener.message(target, f'Error: {e}')

    def _resolve_alias(self, trigger, message=''):
        try:
            return (f'{config["aliases"][trigger]} {message}').split(' ', 1)
        except KeyError:
            return trigger, message

    async def _send_response(self, listener, target, response):
        if isinstance(response, AsyncGeneratorType):
            logger.info('AsyncGenerator response received, sending to target.')
            async for resp in response:
                await listener.message(**self._package_response(resp, target))
            return

        response = await response
        if isinstance(response, GeneratorType):
            logger.info('Generator response received, sending to target.')
            for resp in response:
                await listener.message(**self._package_response(resp, target))
        elif isinstance(response, dict):
            logger.info('Dict response received, sending to target.')
            await listener.message(**response)
        else:
            logger.info('Str response received, sending to target.')
            await listener.message(target, str(response))

    def _package_response(self, resp, target):
        if not isinstance(resp, dict):
            resp = {'target': target, 'message': str(resp)}
        return resp
