import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sniped = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.sniped[message.channel.id] = (message.content, message.author)

    @commands.command()
    async def snipe(self, ctx):
        if ctx.channel.id in self.sniped:
            content, author = self.sniped[ctx.channel.id]
            await ctx.send(f"**{author}:** {content}")
        else: await ctx.send("Nothing to snipe.")

    @commands.command()
    async def pfp(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        await ctx.send(user.avatar_url)

    @commands.command()
    async def purge(self, ctx, num: int):
        await ctx.message.delete()
        async for m in ctx.channel.history(limit=num):
            if m.author == self.bot.user:
                try: await m.delete()
                except: pass

def setup(bot): bot.add_cog(Utility(bot))
