from .serverwhitelist import ServerWhitelist

async def setup(bot):
    await bot.add_cog(ServerWhitelist(bot))