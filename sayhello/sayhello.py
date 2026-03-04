from redbot.core import commands
from redbot.core.utils.chat_formatting import *
import discord

class SayHello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_embed_color(self, guild):
        from redbot.core import Config
        color = await self.bot._config.color()
        return discord.Color(color)

    @discord.app_commands.command(name="say", description="Make the bot repeat your message")
    async def say(self, interaction: discord.Interaction, message: str):
        color = await self.get_embed_color(interaction.guild)
        embed = discord.Embed(
            description=message,
            color=color
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url
        )
        embed.set_footer(text=f"Sent by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name="saywithimage", description="Make the bot repeat your message with an image")
    async def saywithimage(self, interaction: discord.Interaction, message: str, image: discord.Attachment):
        color = await self.get_embed_color(interaction.guild)
        embed = discord.Embed(
            description=message,
            color=color
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url
        )
        embed.set_image(url=image.url)
        embed.set_footer(text=f"Sent by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(SayHello(bot))
