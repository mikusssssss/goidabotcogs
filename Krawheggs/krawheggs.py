from redbot.core import commands, Config
import discord

class Krawheggs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567891)
        self.config.register_global(count=0, upgrades=0)

    @commands.command(name="krawheggs")
    async def krawheggs(self, ctx):
        upgrades = await self.config.upgrades()
        eggs_per_use = 2 + upgrades
        count = await self.config.count()
        count += eggs_per_use
        await self.config.count.set(count)

        color = await self.bot._config.color()
        embed = discord.Embed(
            title="krawhs eggs",
            description=f"krawh has laid **{count} eggs**.\n+{eggs_per_use} this use!",
            color=discord.Color(color)
        )
        embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="eggshop")
    async def eggshop(self, ctx):
        upgrades = await self.config.upgrades()
        count = await self.config.count()
        next_cost = (upgrades + 1) * 100
        eggs_per_use = 2 + upgrades

        color = await self.bot._config.color()
        embed = discord.Embed(
            title="Egg Upgrade Shop",
            color=discord.Color(color)
        )
        embed.add_field(name="Current Egg Bank", value=f"{count} eggs", inline=False)
        embed.add_field(name="Current Upgrades", value=f"{upgrades} (+{eggs_per_use} eggs per use)", inline=False)
        embed.add_field(name="Next Upgrade Cost", value=f"{next_cost} eggs", inline=False)
        embed.add_field(name="How to buy", value="`.eggbuy` to purchase the next upgrade", inline=False)
        embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="eggbuy")
    async def eggbuy(self, ctx):
        upgrades = await self.config.upgrades()
        count = await self.config.count()
        next_cost = (upgrades + 1) * 100

        if count < next_cost:
            await ctx.send(f"Not enough eggs! You need **{next_cost}** eggs but only have **{count}**.")
            return

        await self.config.count.set(count - next_cost)
        await self.config.upgrades.set(upgrades + 1)

        new_upgrades = upgrades + 1
        color = await self.bot._config.color()
        embed = discord.Embed(
            title="Upgrade Purchased!",
            description=f"Upgrade {new_upgrades} bought for {next_cost} eggs!\nKrawheggs now gives **{2 + new_upgrades} eggs** per use.",
            color=discord.Color(color)
        )
        embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Krawheggs(bot))
