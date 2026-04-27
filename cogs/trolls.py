import discord
from discord.ext import commands

class Trolls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mimic_target = None

    @commands.command()
    async def mimic(self, ctx, user: discord.Member):
        self.mimic_target = user.id
        await ctx.message.edit(content=f"Now mimicking {user.name}")

    @commands.command()
    async def stopmimic(self, ctx):
        self.mimic_target = None
        await ctx.message.edit(content="Mimic off.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.mimic_target and message.author.id == self.mimic_target:
            await message.channel.send(message.content)

    @commands.command()
    async def gay(self, ctx):
        await ctx.message.edit(content=f"🏳️‍🌈 {ctx.author.name} is **{random.randint(0,100)}%** gay.")

def setup(bot): bot.add_cog(Trolls(bot))
