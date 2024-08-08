import discord
from discord.ext import commands
from discord import app_commands
import config

class Bot(commands.Bot):
    def __init__ (self,command_prefix , intents , **kwargs):
        super().__init__(command_prefix = command_prefix , intents = intents , **kwargs)
    
    async def setup_hook(self) -> None:
        await self.load_extension("cog.mod")
        print("Cog loaded into bot")
        await self.tree.sync()
    
    async def on_ready(self):
        print('bot is ready')

if __name__ == "__main__":
    bot = Bot(command_prefix = "|" , intents= discord.Intents.all())

    bot.run(config.DISCORD_TOKEN)