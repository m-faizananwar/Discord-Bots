import discord
from discord.ext import commands
import config


intents= discord.Intents.all()
bot = commands.Bot(command_prefix='?',intents = intents)

@bot.event
async def on_ready():
    await bot.load_extension("cog.mod")
    print("Cog loaded into bot")
    await bot.tree.sync()
    print('bot is ready')


@bot.tree.command()
@commands.has_permissions(manage_messages = True)
@commands.bot_has_permissions(manage_messages = True)
async def embed(interaction: discord.Interaction,title : str,message : str):
    embed = discord.Embed(
        title=f"{title}",
        description=f"{message}",
        color=discord.Color.red()
    )
    embed.add_field(name="Field 1", value="This is value 1", inline=True)
    embed.add_field(name="Field 2", value="This is value 2", inline=True)
    embed.add_field(name="Field 3", value="This is value 3", inline=True)
    embed.set_thumbnail(url="https://th.bing.com/th/id/R.52a5005217c9d4c478eecc88473c8824?rik=%2fSqhIk9gnl02VA&pid=ImgRaw&r=0")
    embed.set_image(url="https://th.bing.com/th/id/OIP.oFcT19FDJgvwe8CGAOnnCAHaD6?rs=1&pid=ImgDetMain")
    embed.set_footer(
        text="This is a footer",
        icon_url="https://th.bing.com/th/id/OIP.yn1Iug0xYSpiToqfvwnkQgHaF7?rs=1&pid=ImgDetMain"  # Example icon URL
    )

    await interaction.response.send_message(embed=embed)


@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.event
async def on_message(msg):
    print(msg.content)
    if msg.guild and msg.guild.id == 1003142238882242570:
        if msg.author == bot.user:
            return
        else:
            await msg.reply("Hi nigga") 
    await bot.process_commands(msg)
            
@bot.event
async def on_guild_role_create(role : discord.Role):
    print(f"Role created: {role.name}")
    print(f"Role Color {role.color}")

@bot.tree.command() 
async def ping(interaction : discord.Interaction):
    await interaction.response.send_message("Pong!",ephemeral = True)

@bot.tree.command()
async def ahmed(interaction : discord.Interaction):
     await interaction.response.send_message("Ahmed (a chubby) chump" ,ephemeral = True)

@bot.tree.command()
@commands.has_permissions(manage_messages = True)
@commands.bot_has_permissions(manage_messages = True)
async def clear(interaction: discord.Interaction,*,amount : int):
    await interaction.response.defer(thinking=True, ephemeral=True)
    await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"Deleted {amount} messages",ephemeral=True)

@clear.error
async def clear_error(interaction,error):
    if isinstance(error,commands.MissingPermissions):
        await interaction.response.send("You don't have permission to use this command")
    elif isinstance(error,commands.BotMissingPermissions):
        await interaction.response.send("I don't have permission to use this command")
    
bot.run(config.DISCORD_TOKEN)