from redbot.core import commands, Config
import discord

class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1357924680)
        self.config.register_global(
            starboard_channel=None,
            threshold=6,
            emoji="⭐",
            posted_messages=[]
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        config = await self.config.all()
        channel_id = config["starboard_channel"]
        threshold = config["threshold"]
        emoji = config["emoji"]
        posted = config["posted_messages"]

        if not channel_id:
            return

        if str(payload.emoji) != emoji:
            return

        if payload.message_id in posted:
            return

        channel = self.bot.get_channel(payload.channel_id)
        if not channel:
            return

        message = await channel.fetch_message(payload.message_id)
        if not message:
            return

        reaction = discord.utils.get(message.reactions, emoji=emoji)
        if not reaction or reaction.count < threshold:
            return

        starboard_channel = self.bot.get_channel(channel_id)
        if not starboard_channel:
            return

        embed = discord.Embed(
            description=message.content or "",
            color=discord.Color.gold(),
            timestamp=message.created_at
        )
        embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)

        if message.attachments:
            attachment = message.attachments[0]
            if attachment.content_type and attachment.content_type.startswith("image"):
                embed.set_image(url=attachment.url)
            else:
                embed.add_field(name="Attachment", value=f"[{attachment.filename}]({attachment.url})", inline=False)

        embed.add_field(name="Source", value=f"[Jump!]({message.jump_url})", inline=False)
        embed.set_footer(text=f"{reaction.count} {emoji} #{channel.name} • {message.id}")

        await starboard_channel.send(embed=embed)

        async with self.config.posted_messages() as posted_messages:
            posted_messages.append(payload.message_id)

    @commands.group(name="starboard")
    @commands.is_owner()
    async def starboard(self, ctx):
        pass

    @starboard.command(name="setchannel")
    @commands.is_owner()
    async def setchannel(self, ctx, channel: discord.TextChannel):
        await self.config.starboard_channel.set(channel.id)
        await ctx.send(f"Starboard channel set to {channel.mention}.")

    @starboard.command(name="setthreshold")
    @commands.is_owner()
    async def setthreshold(self, ctx, threshold: int):
        await self.config.threshold.set(threshold)
        await ctx.send(f"Starboard threshold set to {threshold}.")

    @starboard.command(name="setemoji")
    @commands.is_owner()
    async def setemoji(self, ctx, emoji: str):
        await self.config.emoji.set(emoji)
        await ctx.send(f"Starboard emoji set to {emoji}.")

    @starboard.command(name="settings")
    @commands.is_owner()
    async def settings(self, ctx):
        config = await self.config.all()
        channel = f"<#{config['starboard_channel']}>" if config["starboard_channel"] else "Not set"
        await ctx.send(f"Channel: {channel}\nThreshold: {config['threshold']}\nEmoji: {config['emoji']}")

async def setup(bot):
    await bot.add_cog(Starboard(bot))
