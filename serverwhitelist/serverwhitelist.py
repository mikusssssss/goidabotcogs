from redbot.core import commands, Config
import discord

class ServerWhitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.config.register_global(whitelist=[])

    async def cog_check(self, ctx):
        return True

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.guild is None:
            return
        whitelist = await self.config.whitelist()
        if whitelist and message.guild.id not in whitelist:
            ctx = await self.bot.get_context(message)
            if ctx.valid:
                ctx.command = None

    @commands.group(name="whitelist")
    @commands.is_owner()
    async def whitelist(self, ctx):
        """Manage the server whitelist."""
        pass

    @whitelist.command(name="add")
    @commands.is_owner()
    async def whitelist_add(self, ctx, server_id: int):
        """Add a server to the whitelist."""
        async with self.config.whitelist() as whitelist:
            if server_id not in whitelist:
                whitelist.append(server_id)
                await ctx.send(f"Server `{server_id}` added to whitelist.")
            else:
                await ctx.send("That server is already whitelisted.")

    @whitelist.command(name="remove")
    @commands.is_owner()
    async def whitelist_remove(self, ctx, server_id: int):
        """Remove a server from the whitelist."""
        async with self.config.whitelist() as whitelist:
            if server_id in whitelist:
                whitelist.remove(server_id)
                await ctx.send(f"Server `{server_id}` removed from whitelist.")
            else:
                await ctx.send("That server isn't in the whitelist.")

    @whitelist.command(name="list")
    @commands.is_owner()
    async def whitelist_list(self, ctx):
        """List all whitelisted servers."""
        whitelist = await self.config.whitelist()
        if not whitelist:
            await ctx.send("no servers are whitelisted - the bot works everywhere")
        else:
            ids = "\n".join(str(s) for s in whitelist)
            await ctx.send(f"**Whitelisted servers:**\n{ids}")

    @whitelist.command(name="clear")
    @commands.is_owner()
    async def whitelist_clear(self, ctx):
        """Clear the whitelist (bot works everywhere again)."""
        await self.config.whitelist.set([])
        await ctx.send("Whitelist cleared")

async def setup(bot):
    await bot.add_cog(ServerWhitelist(bot))