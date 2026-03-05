from .uptime import Uptime

async def setup(bot):
    await bot.add_cog(Uptime(bot))