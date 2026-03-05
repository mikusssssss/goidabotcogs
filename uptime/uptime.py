from redbot.core import commands, Config
import discord
from datetime import datetime, timezone

class Uptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1122334455)
        self.config.register_global(
            first_seen=None,
            total_uptime_seconds=0,
            last_start=None
        )
        self.start_time = datetime.now(timezone.utc)

    async def cog_load(self):
        now = datetime.now(timezone.utc).timestamp()
        async with self.config.all() as data:
            if data["first_seen"] is None:
                data["first_seen"] = now
            data["last_start"] = now

    async def cog_unload(self):
        now = datetime.now(timezone.utc).timestamp()
        last_start = await self.config.last_start()
        if last_start:
            session_seconds = now - last_start
            async with self.config.all() as data:
                data["total_uptime_seconds"] += session_seconds

    def format_duration(self, seconds):
        seconds = int(seconds)
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        parts = []
        if days: parts.append(f"{days}d")
        if hours: parts.append(f"{hours}h")
        if minutes: parts.append(f"{minutes}m")
        if secs: parts.append(f"{secs}s")
        return " ".join(parts) if parts else "0s"

    @commands.command(name="botstatus")
    async def uptime(self, ctx):
        now = datetime.now(timezone.utc)
        session_seconds = (now - self.start_time).total_seconds()

        data = await self.config.all()
        first_seen = data["first_seen"]
        total_uptime_seconds = data["total_uptime_seconds"] + session_seconds

        if first_seen:
            total_possible = now.timestamp() - first_seen
            uptime_percent = (total_uptime_seconds / total_possible) * 100 if total_possible > 0 else 100
        else:
            uptime_percent = 100

        color = await self.bot._config.color()
        embed = discord.Embed(title="Bot Uptime", color=discord.Color(color))
        embed.add_field(name="Current Session", value=self.format_duration(session_seconds), inline=False)
        embed.add_field(name="Total Uptime", value=self.format_duration(total_uptime_seconds), inline=False)
        embed.add_field(name="Uptime Percentage", value=f"{uptime_percent:.2f}%", inline=False)
        embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Uptime(bot))