import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
from bot import Bot

class Mod(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @app_commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.mention} has been kicked for {reason}", ephemeral=True)

    @app_commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member.mention} has been banned for {reason}", ephemeral=True)

    @app_commands.command(name="warn")
    @commands.has_permissions(kick_members=True)
    async def warn(self, interaction: discord.Interaction, member: discord.Member, *, reason: str = "No reason provided"):
        await interaction.response.send_message(f"{member.mention} has been warned for {reason}", ephemeral=True)

    @app_commands.command(name="timeout")
    async def timeout(self, interaction: discord.Interaction, minutes: int, member: discord.Member, *, reason: str = "No reason provided"):
        delta = timedelta(minutes=minutes)
        await member.timeout(delta, reason=reason)
        await interaction.response.send_message(f"{member.mention} has been timed out for {reason}", ephemeral=True)

    @app_commands.command(name="dm")
    @commands.has_permissions(kick_members=True)
    async def dm(self, interaction: discord.Interaction, member: discord.Member, *, message: str):
        await member.send(message)
        await interaction.response.send_message(f"Sent {message} to {member.mention}", ephemeral=True)

async def setup(bot: Bot):
    await bot.add_cog(Mod(bot))
