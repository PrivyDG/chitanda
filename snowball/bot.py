from types import GeneratorType

from pydle import ClientPool as IRCClientPool
from snowball.commands import load_commands
from snowball.listeners import IRCListener, DiscordListener
from snowball.config import Config

class Snowball:

    commands = {}

    def __init__(self):
        self.config = Config()
        self.irc_listeners = {}
        self.discord_listener = None
        load_commands()

    def connect(self):
        if self.config['irc_servers']:
            self._connect_irc()
        if self.config['discord_token']:
            self._connect_discord(discord_token)

    def _connect_irc(self):
        pool = IRCClientPool()
        for server in self.config['irc_servers']:
            self.irc_listeners[server.hostname] = IRCListener(
                server.nickname,
                username=server.nickname,
                realname=server.nickname,
            )
            asyncio.ensure_future(
                pool.connect(
                    self.irc_listeners[server.hostname],
                    server.hostname,
                    server.port,
                    tls=server.tls,
                    tls_verify=server.tls_verify,
                )
            )
            self.irc_listeners[server.hostname] = client

    def _connect_discord(self):
        self.discord_listener = DiscordListener(self)
        self.discord_listener.run(self.config['discord_token'])

    def dispatch_command(self, listener, target, author, message):
        try:
            command = self.bot.commands[message.split(' ', 1)[0].lower()]
        except (IndexError, KeyError):
            return

        response = command.call(self, listener, author, message)
        if isinstance(response, GeneratorType):
            for message in response:
                asyncio.create_task(listener.message(target, message))
        else:
            asyncio.create_task(listener.message(target, message))
