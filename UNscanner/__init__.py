from .unscanner import StatusPage

async def setup(bot):
    await bot.add_cog(StatusPage(bot))
