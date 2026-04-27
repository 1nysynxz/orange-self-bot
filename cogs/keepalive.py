import discord
from discord.ext import commands
import asyncio

class KeepAlive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="247")
    async def twenty_four_seven(self, ctx):
        """Sets status to DND and ensures the bot stays active."""
        # Set status to Do Not Disturb
        await self.bot.change_presence(status=discord.Status.dnd)
        
        msg = "🌙 **24/7 Mode Activated.** Status set to **DND**."
        
        if ctx.author.id == self.bot.user.id:
            await ctx.message.edit(content=msg)
        else:
            await ctx.send(msg)

    @commands.command()
    async def stop247(self, ctx):
        """Resets status to Online."""
        await self.bot.change_presence(status=discord.Status.online)
        
        msg = "☀️ **24/7 Mode Deactivated.** Status set to **Online**."
        
        if ctx.author.id == self.bot.user.id:
            await ctx.message.edit(content=msg)
        else:
            await ctx.send(msg)

def setup(bot):
    bot.add_cog(KeepAlive(bot))
