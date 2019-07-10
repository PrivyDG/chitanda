# flake8: noqa
from enum import Enum

from .discord import DiscordListener
from .irc import IRCListener


class Listeners(Enum):
    IRC = IRCListener
    Discord = DiscordListener
