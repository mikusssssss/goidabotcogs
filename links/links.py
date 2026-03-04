from redbot.core import commands
import discord

class Links(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="links")
    async def links(self, ctx):
        embed = discord.Embed(
            title="goidabot links",
            description="github links, yada yada",
            color=discord.Color.blue()
        )
        embed.add_field(name="GitHub Repo", value="[Click here](https://github.com/mikusssssss/HardFortniteStats)", inline=False)
        embed.add_field(name="Cog GitHub Repo", value="[Click here](https://github.com/mikusssssss/goidabotcogs)", inline=False)
        embed.add_field(name="Report a Bug", value="[Click here](https://github.com/mikusssssss/HardFortniteStats/issues)", inline=False)
        embed.set_footer(text="goidabot")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Links(bot))