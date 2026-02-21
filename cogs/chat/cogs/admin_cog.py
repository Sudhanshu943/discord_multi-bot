"""
Admin Commands Cog
===============================

Discord-specific implementation for admin-related commands.
"""

import discord
from discord.ext import commands

import logging

logger = logging.getLogger(__name__)


class AdminCog(commands.Cog):
    """Admin command handler for the chat system."""

    def __init__(self, bot: commands.Bot, rate_limiter, config, storage):
        self.bot = bot
        self.rate_limiter = rate_limiter
        self.config = config
        self.storage = storage

    @commands.group(name="chatadmin", invoke_without_command=True)
    @commands.is_owner()
    async def chat_admin(self, ctx: commands.Context) -> None:
        await ctx.send_help(ctx.command)

    @chat_admin.command(name="reload")
    @commands.is_owner()
    async def reload_config(self, ctx: commands.Context) -> None:
        self.config.reload()
        await ctx.send("✅ Chat configuration reloaded.")

    @chat_admin.command(name="resetuser")
    @commands.is_owner()
    async def reset_user(self, ctx: commands.Context, user_id: int) -> None:
        self.rate_limiter.reset_user(user_id)
        await ctx.send(f"✅ Reset rate limits for user {user_id}.")

    @chat_admin.command(name="resetall")
    @commands.is_owner()
    async def reset_all(self, ctx: commands.Context) -> None:
        self.rate_limiter.reset_all()
        await ctx.send("✅ All rate limits have been reset.")

    @chat_admin.command(name="cleanup")
    @commands.is_owner()
    async def force_cleanup(self, ctx: commands.Context) -> None:
        await self.storage.cleanup_old_memories(days=30)
        await ctx.send("✅ Cleaned up old memories.")
