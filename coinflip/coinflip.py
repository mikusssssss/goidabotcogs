from redbot.core import commands, Config
import discord
import random

class SideView(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=30)
        self.user = user
        self.side = None

    @discord.ui.button(label="Heads", style=discord.ButtonStyle.primary)
    async def heads(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("This isn't for you!", ephemeral=True)
            return
        self.side = "Heads"
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label="Tails", style=discord.ButtonStyle.secondary)
    async def tails(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.user:
            await interaction.response.send_message("This isn't for you!", ephemeral=True)
            return
        self.side = "Tails"
        self.stop()
        await interaction.response.defer()

class ChallengeView(discord.ui.View):
    def __init__(self, challenger, opponent):
        super().__init__(timeout=30)
        self.challenger = challenger
        self.opponent = opponent
        self.accepted = None

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.opponent:
            await interaction.response.send_message("This challenge isn't for you!", ephemeral=True)
            return
        self.accepted = True
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.danger)
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
        self.config = Config.get_conf(self, identifier=1029384756)
        self.config.register_user(wins=0, losses=0)

    async def record_win(self, user):
        await self.config.user(user).wins.set(await self.config.user(user).wins() + 1)

    async def record_loss(self, user):
        await self.config.user(user).losses.set(await self.config.user(user).losses() + 1)

    @commands.command(name="coinflip")
    async def coinflip(self, ctx, opponent: discord.Member = None):
        color = await self.bot._config.color()

        if opponent is None:
            view = SideView(ctx.author)
            embed = discord.Embed(
                title="Coin Flip",
                description="Pick your side!",
                color=discord.Color(color)
            )
            embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
            msg = await ctx.send(embed=embed, view=view)
            await view.wait()

            if view.side is None:
                await msg.edit(content="You didn't pick a side in time!", embed=None, view=None)
                return

            result = random.choice(["Heads", "Tails"])
            won = view.side == result
            if won:
                await self.record_win(ctx.author)
            else:
                await self.record_loss(ctx.author)

            embed = discord.Embed(
                title="Coin Flip",
                description=f"You picked **{view.side}** — it landed on **{result}**!\n\n{'You win!' if won else 'You lose!'}",
                color=discord.Color.green() if won else discord.Color.red()
            )
            embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
            await msg.edit(embed=embed, view=None)
            return

        if opponent == ctx.author:
            await ctx.send("You can't flip against yourself!")
            return

        if opponent.bot:
            await ctx.send("You can't flip against a bot!")
            return

        view = ChallengeView(ctx.author, opponent)
        embed = discord.Embed(
            title="Coin Flip Challenge",
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

        view = SideView(ctx.author)
        embed = discord.Embed(
            title="Pick Your Side",
            description=f"{ctx.author.mention}, pick your side!",
            color=discord.Color(color)
        )
        embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        await msg.edit(embed=embed, view=view)
        await view.wait()

        if view.side is None:
            await msg.edit(content=f"{ctx.author.mention} didn't pick a side in time. Challenge cancelled!", embed=None, view=None)
            return

        challenger_side = view.side
        opponent_side = "Tails" if challenger_side == "Heads" else "Heads"
        result = random.choice(["Heads", "Tails"])
        winner = ctx.author if result == challenger_side else opponent
        loser = opponent if winner == ctx.author else ctx.author

        await self.record_win(winner)
        await self.record_loss(loser)

        result_embed = discord.Embed(
            title="Coin Flip Results",
            description=f"The coin landed on **{result}**!",
            color=discord.Color(color)
        )
        result_embed.add_field(name=ctx.author.display_name, value=f"**{challenger_side}**", inline=True)
        result_embed.add_field(name=opponent.display_name, value=f"**{opponent_side}**", inline=True)
        result_embed.add_field(name="Winner", value=f"{winner.mention}!", inline=False)
        result_embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        await msg.edit(embed=result_embed, view=None)

    @commands.command(name="flipleaderboard")
    async def flipleaderboard(self, ctx):
        color = await self.bot._config.color()
        all_data = await self.config.all_users()

        if not all_data:
            await ctx.send("No coinflip data yet!")
            return

        entries = []
        for user_id, data in all_data.items():
            wins = data.get("wins", 0)
            losses = data.get("losses", 0)
            total = wins + losses
            percent = (wins / total * 100) if total > 0 else 0
            entries.append((user_id, wins, losses, percent))

        entries.sort(key=lambda x: x[1], reverse=True)

        embed = discord.Embed(
            title="Coin Flip Leaderboard",
            color=discord.Color(color)
        )

        medals = ["1.", "2.", "3."]
        leaderboard = ""
        for i, (user_id, wins, losses, percent) in enumerate(entries[:10]):
            member = ctx.guild.get_member(user_id) if ctx.guild else None
            user = member or await self.bot.fetch_user(user_id)
            name = user.display_name if hasattr(user, "display_name") else str(user)
            medal = medals[i] if i < 3 else f"{i+1}."
            leaderboard += f"{medal} **{name}** — {wins}W / {losses}L ({percent:.1f}%)\n"

        embed.description = leaderboard
        embed.set_footer(text=f"goidabot | {ctx.author.name}", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CoinFlip(bot))
