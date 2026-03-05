from .ispiersongoneyet import IsPiersonGoneYet

async def setup(bot):
    await bot.add_cog(IsPiersonGoneYet(bot))