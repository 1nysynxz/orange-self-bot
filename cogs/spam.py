import discord
from discord.ext import commands
import asyncio

class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spamming = {} # Dictionary to track spam status per channel

    @commands.command()
    async def spam(self, ctx, amount: str, *, message: str):
        """Spams a message. Usage: *spam <amount/inf> <msg>"""
        channel_id = ctx.channel.id
        self.spamming[channel_id] = True
        
        # Check if user wants infinite spam
        infinite = False
        if amount.lower() in ["inf", "until", "stop"]:
            infinite = True
        else:
            try:
                count = int(amount)
                if count > 2000: count = 2000 # Limit to 2k as requested
            except ValueError:
                return await ctx.send("⚠️ **Invalid amount. Use a number or 'inf'.**")

        await ctx.message.delete()
        
        i = 0
        while self.spamming.get(channel_id):
            if not infinite and i >= count:
                break
                
            try:
                await ctx.send(message)
                i += 1
                # Small delay to prevent instant account ban
                await asyncio.sleep(0.6) 
            except discord.HTTPException:
                # If rate limited, wait longer
                await asyncio.sleep(5)
            except Exception:
                break
        
        self.spamming[channel_id] = False

    @commands.command()
    async def spamstop(self, ctx):
        """Stops the spam loop in the current channel."""
        self.spamming[ctx.channel.id] = False
        await ctx.send("🛑 **Spam stopped.**", delete_after=3)

def setup(bot):
    bot.add_cog(Spam(bot))
