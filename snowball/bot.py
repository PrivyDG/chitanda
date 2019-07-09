from types import GeneratorType

from pydle import ClientPool as IRCClientPool
from snowball.commands import load_commands
from snowball.listeners import IRCListener, DiscordListener

class Snowball:

    commands = {}

    def __init__(self):
        self.irc_listeners = {}
        self.discord_listener = None
        load_commands()

    def connect(self):
        irc_servers = self._load_irc_servers()
        if irc_servers:
            self._connect_irc(irc_servers)
        discord_token = self._load_discord_token()
        if discord_token:
            self._connect_discord(discord_token)

    def _connect_irc(self, irc_servers):
        pool = IRCClientPool()
        for server in irc_servers:
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

    def _connect_discord(self, discord_token):
        self.discord_listener = DiscordListener(self)
        self.discord_listener.run(discord_token)

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

    def _load_irc_servers(self):
        pass

    def _load_discord_token(self):
        pass
