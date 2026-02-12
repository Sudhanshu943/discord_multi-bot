import discord
from discord.ext import commands
from discord import app_commands
import random

class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Hybrid 8ball
    @commands.hybrid_command(name='8ball', aliases=['eightball'])
    @app_commands.describe(question='Your yes/no question')
    async def eight_ball(self, ctx, *, question: str):
        """Ask the magic 8ball a yes/no question"""
        responses = [
            '🎱 It is certain.',
            '🎱 Without a doubt.',
            '🎱 Yes - definitely.',
            '🎱 You may rely on it.',
            '🎱 As I see it, yes.',
            '🎱 Most likely.',
            '🎱 Outlook good.',
            '🎱 Signs point to yes.',
            '🎱 Reply hazy, try again.',
            '🎱 Ask again later.',
            '🎱 Better not tell you now.',
            '🎱 Cannot predict now.',
            '🎱 Concentrate and ask again.',
            "🎱 Don't count on it.",
            '🎱 My reply is no.',
            '🎱 My sources say no.',
            '🎱 Outlook not so good.',
            '🎱 Very doubtful.'
        ]
        await ctx.send(f'{random.choice(responses)}')

    # Hybrid roll dice
    @commands.hybrid_command(name='roll')
    @app_commands.describe(sides='Number of sides on the dice (2-100)')
    async def roll_dice(self, ctx, sides: int = 6):
        """Roll a dice"""
        if sides < 2 or sides > 100:
            return await ctx.send("❌ Dice must have between 2-100 sides!")
        
        result = random.randint(1, sides)
        await ctx.send(f'🎲 You rolled a **{result}** (d{sides})')

    # Hybrid coin flip
    @commands.hybrid_command(name='flip')
    async def coin_flip(self, ctx):
        """Flip a coin"""
        result = random.choice(['Heads 🪙', 'Tails 🪙'])
        await ctx.send(f'**{result}**')

    # Pure slash command with choices
    @app_commands.command(name='choose')
    @app_commands.describe(
        option1='First option',
        option2='Second option',
        option3='Third option (optional)',
        option4='Fourth option (optional)'
    )
    async def choose(
        self, 
        interaction: discord.Interaction, 
        option1: str, 
        option2: str, 
        option3: str = None, 
        option4: str = None
    ):
        """Choose randomly between options"""
        options = [option1, option2]
        if option3:
            options.append(option3)
        if option4:
            options.append(option4)
        
        choice = random.choice(options)
        await interaction.response.send_message(f"🎯 I choose: **{choice}**")

    # Hybrid serverinfo
    @commands.hybrid_command(name='serverinfo')
    async def server_info(self, ctx):
        """Display server information"""
        guild = ctx.guild
        embed = discord.Embed(title=f"📊 {guild.name}", color=discord.Color.blue())
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        await ctx.send(embed=embed)

    # Hybrid userinfo
    @commands.hybrid_command(name='userinfo')
    @app_commands.describe(member='The user to get info about (optional)')
    async def user_info(self, ctx, member: discord.Member = None):
        """Display user information"""
        member = member or ctx.author
        embed = discord.Embed(title=f"👤 {member}", color=member.color)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
        embed.add_field(name="Status", value=str(member.status).title(), inline=True)
        embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Chat(bot))
