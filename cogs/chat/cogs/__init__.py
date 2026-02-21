"""Cogs module - Discord command handlers."""

from .chat_cog import ChatCog
from .music_cog import MusicCog
from .stats_cog import StatsCog
from .admin_cog import AdminCog

__all__ = [
    "ChatCog",
    "MusicCog",
    "StatsCog",
    "AdminCog",
]
