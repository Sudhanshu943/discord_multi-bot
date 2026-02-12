import discord
from discord.ext import commands

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Add commands later

async def setup(bot):
    await bot.add_cog(Chat(bot))
