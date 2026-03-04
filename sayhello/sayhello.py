from redbot.core import commands
import discord

class SayHello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="say", description="Make the bot repeat your message")
    async def say(self, interaction: discord.Interaction, message: str):
        embed = discord.Embed(
            description=message,
            color=interaction.user.color
        )
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url
        )
        embed.set_footer(text=f"Sent by {interaction.user.display_name}")
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name="saywithimage", description="Make the bot repeat your message with an image")
    async def saywithimage(self, interaction: discord.Interaction, message: str, image: discord.Attachment):
        embed = discord.Embed(
            description=message,
            color=interaction.user.color
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
