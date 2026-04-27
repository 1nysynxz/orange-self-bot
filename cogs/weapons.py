import discord
from discord.ext import commands
import asyncio

class Weapons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.weapon_active = False

    @commands.command(aliases=['uzi', 'ak47'])
    async def m16(self, ctx):
        """Rapid fire weapon-style spam"""
        self.weapon_active = True
        await ctx.message.delete()
        while self.weapon_active:
            await ctx.send("💥 **RATATA-TA-TA!** 💥")
            await asyncio.sleep(0.2)

    @commands.command()
    async def stopweapon(self, ctx):
        self.weapon_active = False

    @commands.command()
    async def gc1(self, ctx, user: discord.User):
        """Forces a user into a new Group Chat loop"""
        for i in range(3):
            group = await ctx.author.create_group([user])
            await group.send(f"Welcome to GC {i+1}")
            await asyncio.sleep(1)

    @commands.command()
    async def flow(self, ctx):
        """Status check of all systems"""
        await ctx.message.edit(content="🟢 **System Flow: OPTIMAL**\nLatency: " + str(round(self.bot.latency * 1000)) + "ms")

def setup(bot): bot.add_cog(Weapons(bot))
