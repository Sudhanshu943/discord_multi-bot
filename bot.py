import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
import asyncio

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

# Reduce gateway verbosity
logging.getLogger('discord.gateway').setLevel(logging.WARNING)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True  # Required for voice connections
intents.guild_messages = True
intents.members = True  # Fixed: was guild_members


bot = commands.Bot(
    command_prefix='!',
    intents=intents,
    max_messages=1000,  # Help with message caching
    heartbeat_timeout=60,  # Increase heartbeat timeout
    guild_ready_timeout=10,  # Wait longer for guild ready
)

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

@bot.event
async def on_disconnect():
    logger.warning("Bot disconnected from Discord Gateway")

@bot.event
async def on_resume():
    logger.info("Bot resumed connection to Discord Gateway")


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
    """Main function with reconnection handling"""
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            async with bot:
                await load_cogs()
                logger.info("Starting bot...")
                await bot.start(TOKEN)
                retry_count = 0  # Reset on successful connection
        except discord.LoginFailure:
            logger.error("Invalid token - cannot reconnect")
            break
        except Exception as e:
            retry_count += 1
            logger.error(f"Error (attempt {retry_count}/{max_retries}): {e}")
            if retry_count < max_retries:
                wait_time = min(5 * retry_count, 30)  # Exponential backoff
                logger.info(f"Reconnecting in {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                logger.error("Max retries reached. Exiting.")
                break

if __name__ == '__main__':
    asyncio.run(main())
