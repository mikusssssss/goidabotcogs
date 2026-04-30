from redbot.core import commands
import discord

TARGET_USER_ID = 675095792419340319
TARGET_GUILD_ID = 1498307093369716848

class IsPiersonGoneYet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ispiersongoneyet")
    async def ispiersongoneyet(self, ctx):
        guild = self.bot.get_guild(TARGET_GUILD_ID)
        if guild is None:
            await ctx.send("not present in server")
            return

        member = guild.get_member(TARGET_USER_ID)
        color = await self.bot._config.color()
        embed = discord.Embed(color=discord.Color(color))

        if member:
            embed.title = "no he is not"
            embed.description = "Pierson is unfortunately still here."
        else:
            embed.title = "PIERSON IS DEAD"
            embed.description = "soldiers reading a certain newspaper in ww2 image"

        embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(IsPiersonGoneYet(bot))
