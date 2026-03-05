from redbot.core import commands
import discord
import random

class ChallengeView(discord.ui.View):
    def __init__(self, challenger, opponent):
        super().__init__(timeout=30)
        self.challenger = challenger
        self.opponent = opponent
        self.accepted = None

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success, emoji="✅")
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.opponent:
            await interaction.response.send_message("This challenge isn't for you!", ephemeral=True)
            return
        self.accepted = True
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger, emoji="❌")
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.opponent:
            await interaction.response.send_message("This challenge isn't for you!", ephemeral=True)
            return
        self.accepted = False
        self.stop()
        await interaction.response.defer()

class CoinFlip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coinflip")
    async def coinflip(self, ctx, opponent: discord.Member = None):
        color = await self.bot._config.color()

        if opponent is None:
            result = random.choice(["Heads", "Tails"])
            embed = discord.Embed(
                title="Coin Flip",
                description=f"**{result}!**",
                color=discord.Color(color)
            )
            embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
            await ctx.send(embed=embed)
            return

        if opponent == ctx.author:
            await ctx.send("You can't flip against yourself!")
            return

        if opponent.bot:
            await ctx.send("You can't flip against a bot!")
            return

        view = ChallengeView(ctx.author, opponent)
        embed = discord.Embed(
            title="🪙 Coin Flip Challenge",
            description=f"{ctx.author.mention} has challenged {opponent.mention} to a coin flip!\n\n{opponent.mention}, do you accept?",
            color=discord.Color(color)
        )
        embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        msg = await ctx.send(embed=embed, view=view)

        await view.wait()

        if view.accepted is None:
            await msg.edit(content=f"{opponent.mention} didn't respond in time. Challenge cancelled!", embed=None, view=None)
            return

        if not view.accepted:
            await msg.edit(content=f"{opponent.mention} declined the challenge.", embed=None, view=None)
            return

        # flip the coins
        author_flip = random.choice(["Heads", "Tails"])
        opponent_flip = random.choice(["Heads", "Tails"])

        # keep flipping until someone wins
        while author_flip == opponent_flip:
            author_flip = random.choice(["Heads", "Tails"])
            opponent_flip = random.choice(["Heads", "Tails"])

        winner = ctx.author if author_flip == "Heads" else opponent

        result_embed = discord.Embed(
            title="🪙 Coin Flip Results",
            color=discord.Color(color)
        )
        result_embed.add_field(name=ctx.author.display_name, value=f"**{author_flip}**", inline=True)
        result_embed.add_field(name=opponent.display_name, value=f"**{opponent_flip}**", inline=True)
        result_embed.add_field(name="Winner", value=f"{winner.mention}!", inline=False)
        result_embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        await msg.edit(embed=result_embed, view=None)

async def setup(bot):
    await bot.add_cog(CoinFlip(bot))
