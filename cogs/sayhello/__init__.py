from .sayhello import SayHello

async def setup(bot):
    await bot.add_cog(SayHello(bot))
