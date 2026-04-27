import discord
from discord.ext import commands
import random

class TrollsExtra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pp(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        size = "=" * random.randint(1, 15)
        await ctx.message.edit(content=f"{user.name}'s size: 8{size}D")

    @commands.command()
    async def aura(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        await ctx.message.edit(content=f"✨ {user.name} has **{random.randint(-1000, 5000)}** Aura.")

    @commands.command()
    async def seed(self, ctx):
        await ctx.message.edit(content="🌱 *Seed planted in this chat.*")

    @commands.command()
    async def autobold(self, ctx):
        """Every message you send will be bolded automatically"""
        # Note: Requires a listener in main.py or here
        await ctx.send("✅ Auto-Bold: **ON**")

def setup(bot): bot.add_cog(TrollsExtra(bot))
