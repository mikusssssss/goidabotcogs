from redbot.core import commands

class RouterAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="routerbot")
    async def routerbot(self, ctx):
        await ctx.send("hello i am router and i rout things")

async def setup(bot):
    await bot.add_cog(RouterAI(bot))