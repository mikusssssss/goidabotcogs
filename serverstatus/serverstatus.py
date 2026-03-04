from redbot.core import commands
import discord
import aiohttp
from datetime import datetime, timezone

SERVERS = {
    "Goob Station": [
        ("Goob Alpha", "https://alpha.goobstation.com/status"),
        ("Goob Sigma", "https://sigma.goobstation.com/status"),
        ("Goob Omega", "https://omega.goobstation.com/status"),
    ],
    "Monolith Station": [
        ("Monolith Inferno", "https://inferno.monolithstation.com/status"),
    ],
    "RMC": [
        ("Alamo", "https://alamo.rouny-ss14.com/status"),
    ],
}

def format_duration(start_time_str):
    try:
        start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = now - start_time
        total_minutes = int(delta.total_seconds() // 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"
    except Exception:
        return "Unknown"

class serverstatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverstatus")
    async def serverstatus(self, ctx):
        embed = discord.Embed(
            title="SS14 Server Status",
            color=discord.Color.blue()
        )

        async with aiohttp.ClientSession() as session:
            for host, servers in SERVERS.items():
                field_value = ""
                for name, url in servers:
                    try:
                        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                            if resp.status == 200:
                                data = await resp.json(content_type=None)
                                players = data.get("players", "?")
                                soft_max = data.get("soft_max_players", "?")
                                map_name = data.get("map", "?")
                                real_name = data.get("name", name)
                                round_start = data.get("round_start_time")
                                run_level = data.get("run_level", 0)

                                if run_level == 0:
                                    shift = " Lobby"
                                elif round_start:
                                    shift = f"{format_duration(round_start)}"
                                else:
                                    shift = "Unknown"

                                field_value += f"🟢 **{real_name}**\nPlayers: {players}/{soft_max} | Map: {map_name} | Shift: {shift}\n\n"
                            else:
                                field_value += f"🔴 **{name}**\nServer unreachable\n\n"
                    except Exception:
                        field_value += f"🔴 **{name}**\nServer unreachable\n\n"

                embed.add_field(name=f"━━━ {host} ━━━", value=field_value.strip(), inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(serverstatus(bot))
