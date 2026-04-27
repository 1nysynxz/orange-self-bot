import discord
from discord.ext import commands
import random
import asyncio

class TrollsV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.alien_mode = False
        self.lastword_mode = False

    @commands.command(aliases=['stopal'])
    async def al(self, ctx):
        """Toggle for Alien/Distorted text loop"""
        if ctx.invoked_with == 'stopal':
            self.alien_mode = False
            return await ctx.send("Alien mode off.")
        
        self.alien_mode = True
        await ctx.message.delete()
        chars = "⟁⟠⟢⟝⟞⟟⟠⟡⟢⟣⟤⟥"
        while self.alien_mode:
            msg = "".join(random.choice(chars) for _ in range(15))
            await ctx.send(msg)
            await asyncio.sleep(0.5)

    @commands.command()
    async def lastwordenable(self, ctx):
        """Automatically replies to anyone who speaks last"""
        self.lastword_mode = True
        await ctx.message.edit(content="✅ Last Word Enabled.")

    @commands.command()
    async def lastwordoff(self, ctx):
        self.lastword_mode = False
        await ctx.message.edit(content="❌ Last Word Disabled.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.lastword_mode and message.author.id != self.bot.user.id:
            if not message.guild: return # Prevent DM loops
            await asyncio.sleep(1)
            await message.channel.send("I always get the last word.")

    @commands.command()
    async def autoreaction(self, ctx, emoji: str):
        """Tells the bot to react to every new message with a specific emoji"""
        self.bot.auto_emoji = emoji
        await ctx.message.edit(content=f"✅ Auto-reacting with {emoji}")

    @commands.command()
    async def reactionoff(self, ctx):
        self.bot.auto_emoji = None
        await ctx.message.edit(content="❌ Auto-reaction off.")

def setup(bot):
    bot.add_cog(TrollsV2(bot))
