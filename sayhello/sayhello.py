from redbot.core import commands, Config
import discord
import re

class SayHello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=9876543210)
        self.config.register_user(color=None)

    async def get_embed_color(self, user):
        user_color = await self.config.user(user).color()
        if user_color:
            return discord.Color(user_color)
        color = await self.bot._config.color()
        return discord.Color(color)

    def extract_outside_content(self, message: str):
        pattern = r'(<@!?[0-9]+>|<@&[0-9]+>|<#[0-9]+>)'
        outside = " ".join(re.findall(pattern, message))
        return outside if outside else None

    def strip_outside_content(self, message: str):
        pattern = r'(<@!?[0-9]+>|<@&[0-9]+>|<#[0-9]+>)'
        return re.sub(pattern, '', message).strip()

    @discord.app_commands.command(name="say", description="Make the bot repeat your message")
    async def say(self, interaction: discord.Interaction, message: str):
        color = await self.get_embed_color(interaction.user)
        outside = self.extract_outside_content(message)
        cleaned = self.strip_outside_content(message)
        embed = discord.Embed(description=cleaned, color=color)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"goidabot | {interaction.user.name}", icon_url=self.bot.user.display_avatar.url)
        await interaction.response.send_message(content=outside, embed=embed)

    @discord.app_commands.command(name="saywithimage", description="Make the bot repeat your message with an image")
    async def saywithimage(self, interaction: discord.Interaction, message: str, image: discord.Attachment):
        color = await self.get_embed_color(interaction.user)
        outside = self.extract_outside_content(message)
        cleaned = self.strip_outside_content(message)
        embed = discord.Embed(description=cleaned, color=color)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.set_image(url=image.url)
        embed.set_footer(text=f"goidabot | {interaction.user.name}", icon_url=self.bot.user.display_avatar.url)
        await interaction.response.send_message(content=outside, embed=embed)

    @discord.app_commands.command(name="embed", description="Send a link and embed it")
    async def embed(self, interaction: discord.Interaction, link: str):
    await interaction.response.send_message(content=f"{link}\n{interaction.user.display_name} ||{interaction.user.id}||")

    @discord.app_commands.command(name="setcolor", description="Set your personal embed color (e.g. #ff0000)")
    async def setcolor(self, interaction: discord.Interaction, color: str):
        try:
            color = color.strip().lstrip("#")
            color_int = int(color, 16)
            await self.config.user(interaction.user).color.set(color_int)
            embed = discord.Embed(
                description="Your embed color has been set",
                color=discord.Color(color_int)
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Invalid color! Please use a hex code like `#ff0000`.", ephemeral=True)

    @discord.app_commands.command(name="resetcolor", description="Reset your embed color back to the bot default")
    async def resetcolor(self, interaction: discord.Interaction):
        await self.config.user(interaction.user).color.set(None)
        await interaction.response.send_message("Your embed color has been reset to the bot default", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SayHello(bot))
