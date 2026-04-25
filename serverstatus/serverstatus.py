from redbot.core import commands, Config
import discord
import aiohttp
import asyncio
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

def format_duration_seconds(seconds):
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours} hours, {minutes} minutes, and {secs} seconds"

async def fetch_server(session, name, url, extended=False):
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
            if resp.status == 200:
                data = await resp.json(content_type=None)
                players = data.get("players", "?")
                soft_max = data.get("soft_max_players", "?")
                map_name = data.get("map") or "Unknown"
                real_name = data.get("name", name)
                round_start = data.get("round_start_time")
                run_level = data.get("run_level", 0)
                if run_level == 0:
                    shift = "Lobby"
                elif round_start:
                    shift = format_duration(round_start)
                else:
                    shift = "Unknown"
                result = f"🟢 **{real_name}**\nPlayers: {players}/{soft_max} | Map: {map_name} | Shift: {shift}"
                if extended:
                    preset = data.get("preset", "Unknown")
                    round_id = data.get("round_id", "Unknown")
                    result += f"\nPreset: {preset} | Round ID: {round_id}"
                return result + "\n\n"
            else:
                return f"🔴 **{name}**\nServer unreachable\n\n"
    except Exception:
        return f"🔴 **{name}**\nServer unreachable\n\n"

class serverstatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=7788990011)
        self.config.register_global(announce_channel=None)
        self.last_round_ids = {}
        self.last_run_levels = {}
        self.last_round_starts = {}
        self.last_presets = {}
        self.last_maps = {}
        self.tracker_task = self.bot.loop.create_task(self.round_tracker())

    def cog_unload(self):
        self.tracker_task.cancel()

    async def round_tracker(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            try:
                channel_id = await self.config.announce_channel()
                if channel_id:
                    channel = self.bot.get_channel(channel_id)
                    if channel:
                        async with aiohttp.ClientSession() as session:
                            for host, servers in PLAYTESTS.items():
                                for name, url in servers:
                                    try:
                                        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                                            if resp.status == 200:
                                                data = await resp.json(content_type=None)
                                                round_id = data.get("round_id")
                                                run_level = data.get("run_level", 0)
                                                round_start = data.get("round_start_time")
                                                preset = data.get("preset", "Unknown")
                                                map_name = data.get("map") or "Unknown"
                                                real_name = data.get("name", name)

                                                prev_run_level = self.last_run_levels.get(name)
                                                prev_round_id = self.last_round_ids.get(name)
                                                prev_round_start = self.last_round_starts.get(name)

                                                if prev_run_level is not None:
                                                    # Round started
                                                    if prev_run_level == 0 and run_level == 1:
                                                        await channel.send(
                                                            f"A new round is starting!\n"
                                                            f"Round #{round_id} started: With gamemode **\"{preset}\"** on **\"{map_name}\"** on server **\"{real_name}\".**"
                                                        )
                                                    # Round ended
                                                    elif prev_run_level == 1 and run_level == 0:
                                                        duration = ""
                                                        if prev_round_start:
                                                            try:
                                                                start_dt = datetime.fromisoformat(prev_round_start.replace("Z", "+00:00"))
                                                                elapsed = (datetime.now(timezone.utc) - start_dt).total_seconds()
                                                                duration = f" It lasted {format_duration_seconds(elapsed)}."
                                                            except Exception:
                                                                pass
                                                        await channel.send(
                                                            f"Round #{prev_round_id} **\"{self.last_presets.get(name, 'Unknown')}\"** on **\"{self.last_maps.get(name, 'Unknown')}\"** on server **\"{real_name}\"** has ended. Lasted {duration}\n"
                                                            f"New round starting soon."
                                                        )

                                                self.last_round_ids[name] = round_id
                                                self.last_run_levels[name] = run_level
                                                self.last_round_starts[name] = round_start
                                                self.last_presets[name] = preset
                                                self.last_maps[name] = map_name

                                    except Exception:
                                        pass
            except Exception:
                pass
            await asyncio.sleep(20)

    @commands.command(name="setplaytestchannel")
    @commands.is_owner()
    async def setplaytestchannel(self, ctx, channel: discord.TextChannel):
        await self.config.announce_channel.set(channel.id)
        await ctx.send(f"Playtest round announcements will now be sent to {channel.mention}.")

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
                    field_value += await fetch_server(session, name, url, extended=True)
                embed.add_field(name=f"━━━ {host} ━━━", value=field_value.strip(), inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(serverstatus(bot))
