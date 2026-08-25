from redbot.core import commands, Config
import discord
import re
import random

def uwuify(text: str) -> str:
    text = re.sub(r'r|l', 'w', text)
    text = re.sub(r'R|L', 'W', text)
    text = re.sub(r'n([aeiou])', r'ny\1', text)
    text = re.sub(r'N([aeiou])', r'Ny\1', text)
    text = re.sub(r'N([AEIOU])', r'NY\1', text)
    text = re.sub(r'th\b', 'd', text)
    text = re.sub(r'Th\b', 'D', text)
    faces = ["OwO", "UwU", ">w<", "^w^", "uwu", "owo"]
    text = re.sub(r'!+', lambda m: f' {random.choice(faces)}!', text)
    text = re.sub(r'spits on you', 'paws at you', text, flags=re.IGNORECASE)
    text = re.sub(r'steamhappy', 'paws!!', text, flags=re.IGNORECASE)
    text = re.sub(r'spits at you', 'paws at you', text, flags=re.IGNORECASE)
    text = re.sub(r'murder', 'boop', text, flags=re.IGNORECASE)
    text = re.sub(r'hurt', 'boop', text, flags=re.IGNORECASE)
    text = re.sub(r'punch', 'boop', text, flags=re.IGNORECASE)
    text = re.sub(r'kill', 'hug', text, flags=re.IGNORECASE)
    text = re.sub(r'kys', 'love yourself', text, flags=re.IGNORECASE)
    text = re.sub(r'stab', 'boop', text, flags=re.IGNORECASE)
    text = re.sub(r'shoot', 'kiss', text, flags=re.IGNORECASE)
    text = re.sub(r'suicide', 'love', text, flags=re.IGNORECASE)
    text = re.sub(r'fuck', 'love', text, flags=re.IGNORECASE)
    text = re.sub(r'hate', 'love', text, flags=re.IGNORECASE)
    text = re.sub(r'murder', 'boop', text, flags=re.IGNORECASE)
    text = re.sub(r'feroxi', 'FEROXI ARE THE BEST SPECIES', text, flags=re.IGNORECASE)
    return text

class UwuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=4242424242)
        self.config.register_guild(
            webhook_id=None,
            webhook_token=None,
            channel_id=None,
            targets=[]
        )

    @commands.command(name="uwuify")
    @commands.has_permissions(manage_messages=True)
    async def uwuify_cmd(self, ctx, member: discord.Member, duration: str = None):
        async with self.config.guild(ctx.guild).targets() as targets:
            if member.id in targets:
                await ctx.send(f"{member.display_name} is already being uwuified!")
                return
            if len(targets) >= 20:
                await ctx.send("Maximum of 20 members can be uwuified at once!")
                return
            targets.append(member.id)

        channel_id = await self.config.guild(ctx.guild).channel_id()
        if not channel_id:
            webhook = await ctx.channel.create_webhook(name="uwuify")
            await self.config.guild(ctx.guild).webhook_id.set(webhook.id)
            await self.config.guild(ctx.guild).webhook_token.set(webhook.token)
            await self.config.guild(ctx.guild).channel_id.set(ctx.channel.id)
            await ctx.send(f"uwuify set up in {ctx.channel.mention}! Now uwuifying {member.display_name}.")
        else:
            await ctx.send(f"Now uwuifying {member.display_name}!")

        if duration:
            seconds = self.parse_duration(duration)
            if seconds:
                await discord.utils.sleep_until(discord.utils.utcnow().__class__.utcnow().replace(tzinfo=None))
                import asyncio
                await asyncio.sleep(seconds)
                async with self.config.guild(ctx.guild).targets() as targets:
                    if member.id in targets:
                        targets.remove(member.id)

    @commands.command(name="uwustop")
    @commands.has_permissions(manage_messages=True)
    async def uwustop(self, ctx, member: discord.Member):
        async with self.config.guild(ctx.guild).targets() as targets:
            if member.id in targets:
                targets.remove(member.id)
                await ctx.send(f"Stopped uwuifying {member.display_name}.")
            else:
                await ctx.send(f"{member.display_name} isn't being uwuified.")

    @commands.command(name="uwulist")
    async def uwulist(self, ctx):
        targets = await self.config.guild(ctx.guild).targets()
        if not targets:
            await ctx.send("Nobody is being uwuified right now.")
            return
        members = [ctx.guild.get_member(uid) for uid in targets]
        names = [m.display_name if m else str(uid) for m, uid in zip(members, targets)]
        await ctx.send("Currently uwuifying: " + ", ".join(names))

    def parse_duration(self, duration: str):
        match = re.fullmatch(r'(\d+)(s|m|h)', duration)
        if not match:
            return None
        value, unit = int(match.group(1)), match.group(2)
        return value * {"s": 1, "m": 60, "h": 3600}[unit]

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return

        targets = await self.config.guild(message.guild).targets()
        if message.author.id not in targets:
            return

        channel_id = await self.config.guild(message.guild).channel_id()
        if message.channel.id != channel_id:
            return

        webhook_id = await self.config.guild(message.guild).webhook_id()
        webhook_token = await self.config.guild(message.guild).webhook_token()
        if not webhook_id or not webhook_token:
            return

        uwu_text = uwuify(message.content) if message.content else ""

        try:
            await message.delete()
        except discord.Forbidden:
            return

        webhook = discord.Webhook.partial(webhook_id, webhook_token, client=self.bot)
        await webhook.send(
            content=uwu_text or None,
            username=message.author.display_name,
            avatar_url=message.author.display_avatar.url,
            files=[await a.to_file() for a in message.attachments] if message.attachments else []
        )

async def setup(bot):
    await bot.add_cog(UwuCog(bot))
