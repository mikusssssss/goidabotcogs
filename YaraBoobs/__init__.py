from .yaraboobs import YaraBoobs

async def setup(bot):
    await bot.add_cog(YaraBoobs(bot))
