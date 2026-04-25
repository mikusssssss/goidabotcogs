from redbot.core import commands
import discord
import aiohttp
from datetime import datetime, timezone

SERVERS = {
    "Monolith Station": [
        ("Monolith Inferno", "https://inferno.monolithstation.com/status"),
    ],
    "RMC": [
        ("Alamo", "https://alamo.rouny-ss14.com/status"),
    ],
    "Goob Station": [
        ("Goob Alpha", "https://alpha.goobstation.com/status"),
        ("Goob Sigma", "https://sigma.goobstation.com/status"),
    ],
}

PLAYTESTS = {
    "CMU": [
        ("CMU", "https://cmu.cm-ss13.com/status"),
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

async def fetch_server(session, name, url):
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
                    shift = "Lobby"
                elif round_start:
                    shift = format_duration(round_start)
                else:
                    shift = "Unknown"
                return f"🟢 **{real_name}**\nPlayers: {players}/{soft_max} | Map: {map_name} | Shift: {shift}\n\n"
            else:
                return f"🔴 **{name}**\nServer unreachable\n\n"
    except Exception:
        return f"🔴 **{name}**\nServer unreachable\n\n"

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
                    field_value += await fetch_server(session, name, url)
                embed.add_field(name=f"━━━ {host} ━━━", value=field_value.strip(), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="playtests")
    async def playtests(self, ctx):
        embed = discord.Embed(
            title="Playtest Server Status",
            color=discord.Color.blue()
        )
        async with aiohttp.ClientSession() as session:
            for host, servers in PLAYTESTS.items():
                field_value = ""
                for name, url in servers:
                    field_value += await fetch_server(session, name, url)
                embed.add_field(name=f"━━━ {host} ━━━", value=field_value.strip(), inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(serverstatus(bot))
