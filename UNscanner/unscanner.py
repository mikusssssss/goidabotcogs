from redbot.core import commands, Config
import discord
from datetime import datetime, timezone, timedelta

KEYWORDS = ["netanyahu", "big yahu", "jew", "goy", "juda", "mossad", "goyim", "yahu"]
CHALLENGE_NAME = "BIG Y Challenge"
FAIL_MESSAGE = "YOU FAILED!!! THE UN HAS BEEN NOTIFIED. YOU ARE A THIEF!!! YOU ARE A THIEF!!! YOU ARE A THIEF!!!  "
WIN_MESSAGE = "Good! You have not disrespected the best country in the last 2 days! The UN is happy."

class StatusPage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=5566778899)
        self.config.register_global(counts={})

    @commands.command(name="beveragescanner")
    async def status(self, ctx):
        after = datetime.now(timezone.utc) - timedelta(days=2)

        recent_counts = {k: 0 for k in KEYWORDS}
        async for message in ctx.channel.history(after=after, limit=None):
            if message.author.bot:
                continue
            content = message.content.lower()
            for keyword in KEYWORDS:
                if keyword in content:
                    recent_counts[keyword] += 1

        total_detections = sum(recent_counts.values())
        color = await self.bot._config.color()

        if total_detections > 0:
            status = f"{FAIL_MESSAGE}"
        else:
            status = f"{WIN_MESSAGE}"

        embed = discord.Embed(
            title=f"📊 {CHALLENGE_NAME}",
            description=status,
            color=discord.Color(color)
        )

        # Leaderboard
        sorted_counts = sorted(recent_counts.items(), key=lambda x: x[1], reverse=True)
        leaderboard = ""
        medals = ["🥇", "🥈", "🥉"]
        for i, (keyword, count) in enumerate(sorted_counts):
            medal = medals[i] if i < 3 else f"`{i+1}.`"
            leaderboard += f"{medal} **{keyword}** — {count} detection(s)\n"

        embed.add_field(name="━━━ Leaderboard ━━━", value=leaderboard, inline=False)
        embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):

    await bot.add_cog(StatusPage(bot))
