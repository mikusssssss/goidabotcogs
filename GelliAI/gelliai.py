from redbot.core import commands

class GelliAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gellibot")
    async def gellibot(self, ctx):
        await ctx.send("hello i am gelli and i am stupid and short and i never tell the truth (except when i talk down on myself) my saying is “gelli is always wrong“ and im a horrible person")

async def setup(bot):
    await bot.add_cog(GelliAI(bot))
