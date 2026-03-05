from .statuspage import StatusPage

async def setup(bot):
    await bot.add_cog(StatusPage(bot))