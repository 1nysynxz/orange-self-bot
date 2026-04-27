import discord
from discord.ext import commands
import asyncio
import random

class Packing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pressing = False

    @commands.command(aliases=['stoppressure'])
    async def pressure(self, ctx):
        self.pressing = True
        await ctx.message.delete()
        while self.pressing:
            await ctx.send(f"GET PRESSURED {random.randint(1,999)}")
            await asyncio.sleep(0.4)

    @commands.command()
    async def stopap(self, ctx): self.pressing = False

    @commands.command()
    async def insult(self, ctx, user: discord.Member = None):
        insults = ["Absolute clown", "No motion", "Duck", "Zero speed", "L user"]
        target = user.mention if user else "Everyone"
        await ctx.message.edit(content=f"{target} {random.choice(insults)}")

def setup(bot): bot.add_cog(Packing(bot))
