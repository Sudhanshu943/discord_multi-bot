"""
Music Commands Cog
===============================

Discord-specific implementation for music-related commands.
"""

import discord
from discord.ext import commands
from discord import app_commands
from typing import Optional

import logging

logger = logging.getLogger(__name__)


class MusicCog(commands.Cog):
    """Music command handler for the chat system."""

    def __init__(self, bot: commands.Bot, music_integration):
        self.bot = bot
        self.music_integration = music_integration

    @commands.hybrid_command(name="recommendsong", description="Get a song recommendation based on your preferences")
    async def recommend_song(self, ctx: commands.Context, mood: Optional[str] = None):
        recommendations = await self.music_integration.recommend_songs(ctx.author.id, mood=mood)
        if not recommendations:
            await ctx.send("❌ No song recommendations available.")
            return

        embed = discord.Embed(
            title="🎵 Song Recommendations",
            description=f"Here are some songs you might enjoy{(' based on your mood: ' + mood) if mood else ''}!",
            color=discord.Color.green()
        )
        for i, song in enumerate(recommendations[:5], 1):
            embed.add_field(name=f"{i}. {song}", value="Use `/play` command to play", inline=False)
        embed.set_footer(text="Want to play a song? Use /play <song name>")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="createplaylist", description="Create a playlist based on a theme")
    async def create_playlist(self, ctx: commands.Context, theme: str, num_songs: int = 5):
        if num_songs < 1 or num_songs > 20:
            await ctx.send("❌ Number of songs must be between 1 and 20.")
            return

        playlist = await self.music_integration.create_playlist(ctx.author.id, theme, num_songs)
        if not playlist:
            await ctx.send("❌ Failed to create playlist.")
            return

        embed = discord.Embed(
            title=f"📋 Playlist: {theme}",
            description=f"Created a playlist with {len(playlist)} songs!",
            color=discord.Color.blue()
        )
        for i, song in enumerate(playlist, 1):
            embed.add_field(name=f"{i}. {song}", value="Use `/play` command to play", inline=False)
        embed.set_footer(text="Add these songs to queue with /play <song name>")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="musicpreferences", description="View your music preferences")
    async def music_preferences(self, ctx: commands.Context):
        preferences = await self.music_integration.get_or_create_preference(ctx.author.id)
        embed = discord.Embed(title="🎵 Your Music Preferences", color=discord.Color.purple())

        if preferences.favorite_genres:
            embed.add_field(name="Favorite Genres", value=", ".join(preferences.favorite_genres), inline=False)
        if preferences.favorite_artists:
            embed.add_field(name="Favorite Artists", value=", ".join(preferences.favorite_artists), inline=False)
        if preferences.preferred_moods:
            embed.add_field(name="Preferred Moods", value=", ".join(preferences.preferred_moods), inline=False)
        if preferences.last_played_songs:
            embed.add_field(name="Last Played Songs", value=", ".join(preferences.last_played_songs[:3]), inline=False)

        embed.set_footer(text="Preferences are automatically learned from conversations!")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="roastme", description="Get a sarcastic song recommendation")
    async def roast_me(self, ctx: commands.Context):
        song = await self.music_integration.get_sarcastic_song()
        embed = discord.Embed(
            title="🔥 Sarcastic Song Recommendation",
            description=f"I recommend: **{song}**",
            color=discord.Color.orange()
        )
        embed.set_footer(text="Don't take it personally! 😜")
        await ctx.send(embed=embed)
