import asyncio
import logging
import sys
from types import AsyncGeneratorType, GeneratorType

from aiohttp import web

from chitanda import BotError
from chitanda.config import config
from chitanda.listeners import DiscordListener, IRCListener
from chitanda.modules import load_commands

logger = logging.getLogger(__name__)


class NoCommandFound(BotError):
    pass


class Chitanda:

    commands = {}

    def __init__(self):
        self.irc_listeners = {}
        self.discord_listener = None
        self.message_handlers = []
        self.response_handlers = []
        if config['webserver']['enable']:
            self.web_application = web.Application()

    def start(self):
        load_commands(self)
        if self.web_application():
            self.webserver = self._start_webserver()

        self.connect()

    def _start_webserver(self):
        try:
            return asyncio.ensure_future(
                asyncio.get_event_loop().create_server(
                    self.web_application.make_handler(),
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
        logger.debug(
            f'New message in {target} on {listener} from {author}: {message}'
        )
        for handler in self.message_handlers:
            response = handler(listener, target, author, message, private)
            await self.handle_response(listener, target, response)

        await self.dispatch_command(listener, target, author, message, private)

    async def dispatch_command(
        self, listener, target, author, message, private
    ):
        try:
            trigger, command, message = self._parse_command(message)
            logger.info(f'Command triggered: {trigger}.')

            response = command.call(
                bot=self,
                listener=listener,
                target=target,
                author=author,
                message=message,
                private=private,
            )

            if response:
                await self.handle_response(listener, target, response)
        except NoCommandFound:
            pass
        except BotError as e:
            logger.info(f'Error triggered by {author}: {e}.')
            await listener.message(target, f'Error: {e}')

    def _parse_command(self, message):
        try:
            if message.startswith(config['trigger_character']):
                split_message = message[1:].split(' ', 1)
                trigger, message = self._resolve_alias(*split_message)
                return trigger, self.commands[trigger], message
        except (IndexError, KeyError):
            pass
        raise NoCommandFound

    def _resolve_alias(self, trigger, message=''):
        try:
            return (f'{config["aliases"][trigger]} {message}').split(' ', 1)
        except KeyError:
            return trigger, message

    async def handle_response(self, listener, target, response):
        logger.debug(f'Response received of type: {type(response)}.')

        if isinstance(response, AsyncGeneratorType):
            async for resp in response:
                await self._handle_response_message(listener, target, resp)
            return

        response = await response

        if isinstance(response, GeneratorType):
            for resp in response:
                await self._handle_response_message(listener, target, resp)
        elif response:
            await self._handle_response_message(listener, target, response)

    async def _handle_response_message(self, listener, target, response):
        pr = self._pack_response(response, target)
        await self.call_response_handlers(listener, target, pr['message'])
        await listener.message(**pr)

    def _pack_response(self, response, target):
        if isinstance(response, dict):
            return response
        return {'target': target, 'message': str(response)}

    async def call_response_handlers(self, listener, target, response):
        for handler in self.response_handlers:
            handler(listener, target, response)
