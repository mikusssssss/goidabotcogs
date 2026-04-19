from redbot.core import commands, Config
import discord
import asyncio

class YaraBoobs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=6969696969)
        self.config.register_global(size=0, upgrades=0)
        self.pending = 0
        self.last_ctx = None
        self.batch_task = None

    async def flush_pending(self):
        await asyncio.sleep(5)
        if self.pending == 0:
            return

        upgrades = await self.config.upgrades()
        cm_per_use = 2 + upgrades
        total_cm = self.pending * cm_per_use
        uses = self.pending
        self.pending = 0

        size = await self.config.size()
        size += total_cm
        await self.config.size.set(size)

        color = await self.bot._config.color()
        embed = discord.Embed(
            title="yaras current boob size",
            description=f"yaras boobs are currently **{size} cm** in size.\n+{total_cm} cm from {uses} use(s)!",
            color=discord.Color(color)
        )
        embed.set_footer(text="goidabot", icon_url=self.bot.user.display_avatar.url)
        await self.last_ctx.send(embed=embed)

    @commands.command(name="yaraboobs")
    async def yaraboobs(self, ctx):
        self.pending += 1
        self.last_ctx = ctx

        if self.batch_task is None or self.batch_task.done():
            self.batch_task = asyncio.create_task(self.flush_pending())

    @commands.command(name="boobshop")
    async def boobshop(self, ctx):
        upgrades = await self.config.upgrades()
        size = await self.config.size()
        next_cost = (upgrades + 1) * 100
        cm_per_use = 2 + upgrades

        color = await self.bot._config.color()
        embed = discord.Embed(
            title="Boob Upgrade Shop",
            color=discord.Color(color)
        )
        embed.add_field(name="Current Size Bank", value=f"{size} cm", inline=False)
        embed.add_field(name="Current Upgrades", value=f"{upgrades} (+{cm_per_use} cm per use)", inline=False)
        embed.add_field(name="Next Upgrade Cost", value=f"{next_cost} cm", inline=False)
        embed.add_field(name="How to buy", value="`.boobbuy` to purchase the next upgrade", inline=False)
        embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="boobbuy")
    async def boobbuy(self, ctx):
        upgrades = await self.config.upgrades()
        size = await self.config.size()
        next_cost = (upgrades + 1) * 100

        if size < next_cost:
            await ctx.send(f"Not enough cm! You need **{next_cost}** cm but only have **{size}**.")
            return

        await self.config.size.set(size - next_cost)
        await self.config.upgrades.set(upgrades + 1)

        new_upgrades = upgrades + 1
        color = await self.bot._config.color()
        embed = discord.Embed(
            title="Upgrade Purchased!",
            description=f"Upgrade {new_upgrades} bought for {next_cost} cm!\nYaraboobs now gives **{2 + new_upgrades} cm** per use.",
            color=discord.Color(color)
        )
        embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(YaraBoobs(bot))
