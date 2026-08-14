from .routerai import RouterAI

async def setup(bot):
    await bot.add_cog(RouterAI(bot))