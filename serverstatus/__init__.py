from .serverstatus import serverstatus

async def setup(bot):
    await bot.add_cog(serverstatus(bot))
