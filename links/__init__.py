from .links import Links

async def setup(bot):
    await bot.add_cog(Links(bot))