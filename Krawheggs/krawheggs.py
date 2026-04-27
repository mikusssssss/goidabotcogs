from redbot.core import commands, Config
import discord
import asyncio
from datetime import datetime, timezone

class Krawheggs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567891)
        self.config.register_global(count=0, upgrades=0)
        self.pending = 0
        self.last_use = None
        self.batch_task = None

    async def flush_pending(self):
        await asyncio.sleep(2)
        if self.pending == 0:
            return

        upgrades = await self.config.upgrades()
        eggs_per_use = 2 + upgrades
        total_eggs = self.pending * eggs_per_use
        uses = self.pending
        self.pending = 0

        count = await self.config.count()
        count += total_eggs
        await self.config.count.set(count)

        color = await self.bot._config.color()
        embed = discord.Embed(
            title="krawhs eggs",
            description=f"krawh has laid **{count} eggs**.\n+{total_eggs} eggs from {uses} use(s)!",
            color=discord.Color(color)
        )
        embed.set_footer(text="goidabot", icon_url=self.bot.user.display_avatar.url)
        await self.last_ctx.send(embed=embed)

    @commands.command(name="krawheggs")
    async def krawheggs(self, ctx):
        self.pending += 1
        self.last_ctx = ctx

        if self.batch_task is None or self.batch_task.done():
            self.batch_task = asyncio.create_task(self.flush_pending())

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
