import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[{asctime}] [{levelname:<8}] {name}: {message}',
    datefmt='%Y-%m-%d %H:%M:%S',
    style='{',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8', mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('discord')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info(f'{bot.user} is online!')
    logger.info(f'Connected to {len(bot.guilds)} guilds')
    
    # For testing: sync to specific guild (instant)
    TEST_GUILD_ID = 1288847751123042334  # Replace with your server ID
    
    try:
        guild = discord.Object(id=TEST_GUILD_ID)
        bot.tree.copy_global_to(guild=guild)  # Copy global commands to guild
        synced = await bot.tree.sync(guild=guild)  # Guild-specific sync (instant)
        logger.info(f"✅ Synced {len(synced)} commands to test guild (instant)")
        
        # Optional: Also sync globally (takes 1 hour)
        # await bot.tree.sync()
    except Exception as e:
        logger.error(f"❌ Failed to sync commands: {e}")


# Load cogs
async def load_cogs():
    for filename in os.listdir('./cogs'):
        # Skip __pycache__ and __init__.py
        if filename.startswith('_') or filename == '__pycache__':
            continue
        
        # Load .py files
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f"✅ Loaded {filename[:-3]}")
            except Exception as e:
                logger.error(f"❌ Failed to load {filename}: {e}")
        
        # Load package directories (must have __init__.py)
        elif os.path.isdir(f'./cogs/{filename}'):
            init_path = f'./cogs/{filename}/__init__.py'
            if os.path.exists(init_path):
                try:
                    await bot.load_extension(f'cogs.{filename}')
                    logger.info(f"✅ Loaded {filename}")
                except Exception as e:
                    logger.error(f"❌ Failed to load {filename}: {e}")

# Sync command (for testing - instant sync to specific guild)
@bot.command()
@commands.is_owner()
async def sync(ctx, guild_id: int = None):
    """Sync slash commands (owner only)"""
    try:
        if guild_id:
            guild = discord.Object(id=guild_id)
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            await ctx.send(f"✅ Synced {len(synced)} commands to guild {guild_id}")
        else:
            synced = await bot.tree.sync()
            await ctx.send(f"✅ Synced {len(synced)} commands globally")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

import asyncio
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
