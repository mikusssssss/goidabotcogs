from .krawheggs import Krawheggs

async def setup(bot):
    await bot.add_cog(Krawheggs(bot))
