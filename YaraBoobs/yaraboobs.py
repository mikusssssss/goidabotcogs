from redbot.core import commands, Config
import discord

class YaraBoobs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=6969696969)
        self.config.register_global(size=0)

    @commands.command(name="yaraboobs")
    async def yaraboobs(self, ctx):
        size = await self.config.size()
        size += 2
        await self.config.size.set(size)

        color = await self.bot._config.color()
        embed = discord.Embed(
            title="yaras current boob size",
            description=f"yaras boobs are currently **{size} cm** in size",
            color=discord.Color(color)
        )
        embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(YaraBoobs(bot))
