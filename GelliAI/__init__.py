from .gelliai import GelliAI

async def setup(bot):
    await bot.add_cog(GelliAI(bot))
