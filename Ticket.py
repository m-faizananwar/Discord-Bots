import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import config
import asyncio

intents = discord.Intents.default()
intents.messages = True  
channel_id = 1271070409789542502
staff_role_id = 1271070788077748294  
bot = commands.Bot(command_prefix='!', intents=intents)

class TicketModal(Modal):
    def __init__(self):
        super().__init__(title="Create a Ticket")

        self.product = TextInput(
            label="What product do you want to buy?",
            placeholder="Enter the product name here...",
            required=True
        )
        self.add_item(self.product)

        self.payment_method = TextInput(
            label="Payment Method (Credit Card, PayPal, Crypto)",
            placeholder="Enter your payment method here...",
            required=True
        )
        self.add_item(self.payment_method)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message("Creating your ticket...", ephemeral=True)  # Respond immediately

            ticket_channel = await interaction.guild.create_text_channel(f"ticket-{interaction.user.name}")
            await ticket_channel.set_permissions(interaction.guild.default_role, read_messages=False)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)

            embed = discord.Embed(title="Ticket Details", description="Dear reader, thank you for opening a ticket. Our team will assist you as soon as possible. Could you provide additional information about why you are creating a ticket?", color=discord.Color.blue())
            embed.add_field(name="Created by", value=interaction.user.mention)
            embed.add_field(name="Product", value=self.product.value)
            embed.add_field(name="Payment Method", value=self.payment_method.value)
            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1269541440547979294/1270821851806826637/veno.jpg?ex=66b51894&is=66b3c714&hm=b086cc1ca6e81ac346cb29ab40ca27658529831ec009023bd0e03b328a5eab7c&=&format=webp&width=700&height=700")

            await ticket_channel.send(embed=embed)
            await ticket_channel.send("Manage your ticket:", view=ManageTicketView(ticket_channel))

            followup = await interaction.followup.send(f"Ticket created: {ticket_channel.mention}", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to create channels or manage permissions.", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.green)
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_modal(TicketModal())

class ManageTicketView(View):
    def __init__(self, ticket_channel: discord.TextChannel):
        super().__init__(timeout=None)
        self.ticket_channel = ticket_channel

    @discord.ui.button(label="Claim Ticket", style=discord.ButtonStyle.primary)
    async def claim_ticket(self, interaction: discord.Interaction, button: Button):
        if staff_role_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You do not have permission to claim this ticket.", ephemeral=True)
            return

        await self.ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        self.children[0].label = "Unclaim Ticket"
        self.children[0].style = discord.ButtonStyle.secondary
        self.children[0].callback = self.unclaim_ticket
        await interaction.response.edit_message(view=self)

    async def unclaim_ticket(self, interaction: discord.Interaction, button: Button):
        if staff_role_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You do not have permission to unclaim this ticket.", ephemeral=True)
            return

        await self.ticket_channel.set_permissions(interaction.user, overwrite=None)
        self.children[0].label = "Claim Ticket"
        self.children[0].style = discord.ButtonStyle.primary
        self.children[0].callback = self.claim_ticket
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger)
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        if staff_role_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You do not have permission to close this ticket.", ephemeral=True)
            return

        await self.ticket_channel.delete()
        await interaction.response.send_message("Ticket closed.", ephemeral=True)

    @discord.ui.button(label="Add User", style=discord.ButtonStyle.success)
    async def add_user(self, interaction: discord.Interaction, button: Button):
        if staff_role_id not in [role.id for role in interaction.user.roles]:
            await interaction.response.send_message("You do not have permission to add users to this ticket.", ephemeral=True)
            return

        await interaction.response.send_message("Please mention the user to add them to the ticket.", ephemeral=True)
        
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await bot.wait_for('message', check=check, timeout=30.0)
            user = msg.mentions[0] if msg.mentions else None
            if user is None:
                await interaction.channel.send("User not found.")
                return

            await self.ticket_channel.set_permissions(user, read_messages=True, send_messages=True)
            await interaction.channel.send(f"{user.mention} added to the ticket.")
        except asyncio.TimeoutError:
            await interaction.channel.send("You took too long to respond, please try again.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await asyncio.sleep(2)  
    channel = bot.get_channel(channel_id)  
    if channel:
        await channel.send("Click the button to create a ticket:", view=TicketView())
    else:
        print("Channel not found or bot has no access to it.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

bot.run(config.DISCORD_TOKEN)
