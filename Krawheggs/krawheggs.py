from redbot.core import commands, Config
import discord

class Krawheggs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567891)
        self.config.register_global(count=0)

    @commands.command(name="krawheggs")
    async def krawheggs(self, ctx):
        count = await self.config.count()
        count += 1
        await self.config.count.set(count)

        color = await self.bot._config.color()
        embed = discord.Embed(
            title="krawhs eggs",
            description=f"krawh has laid **{count} eggs**.",
            color=discord.Color(color)
        )
        embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Krawheggs(bot))
