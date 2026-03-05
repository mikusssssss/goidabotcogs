from redbot.core import commands
import discord
import re

class SayHello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_embed_color(self, guild):
        color = await self.bot._config.color()
        return discord.Color(color)

    def extract_outside_content(self, message: str):
        # Extract mentions and links
        pattern = r'(<[@#&!][0-9]+>|<@&[0-9]+>|https?://\S+)'
        outside = " ".join(re.findall(pattern, message))
        return outside if outside else None

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
        embed.set_footer(text=f"goidabot | {interaction.user.name}", icon_url=self.bot.user.display_avatar.url)
        outside = self.extract_outside_content(message)
        await interaction.response.send_message(content=outside, embed=embed)

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
        embed.set_footer(text=f"goidabot | {interaction.user.name}", icon_url=self.bot.user.display_avatar.url)
        outside = self.extract_outside_content(message)
        await interaction.response.send_message(content=outside, embed=embed)

async def setup(bot):
    await bot.add_cog(SayHello(bot))
