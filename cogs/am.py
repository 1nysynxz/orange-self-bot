import discord
from discord.ext import commands
import random
import os
import asyncio

class AutoMessager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.target_users = set()  # Stores IDs of users to auto-roast
        self.roasts_path = "roasts.txt"
        self.roast_cache = []
        self.load_roasts()

    def load_roasts(self):
        """Loads roasts into memory for maximum speed."""
        if os.path.exists(self.roasts_path):
            with open(self.roasts_path, "r", encoding="utf-8") as f:
                self.roast_cache = [line.strip() for line in f.readlines() if line.strip()]
        if not self.roast_cache:
            self.roast_cache = ["You're so slow even my roast file didn't load."]

    @commands.Cog.listener()
    async def on_message(self, message):
        # Don't reply to yourself or bots
        if message.author.id == self.bot.user.id or message.author.bot:
            return

        # Check if the sender is in the target list
        if message.author.id in self.target_users:
            try:
                roast = random.choice(self.roast_cache)
                # No delay for "Super Fast" mode
                await message.channel.send(f"{message.author.mention} {roast}")
            except Exception as e:
                print(f"AM Error: {e}")

    @commands.command(name="am")
    async def auto_message(self, ctx, mode: str = None, user: discord.User = None):
        """Usage: *am on @user | *am off @user"""
        if not mode or not user:
            return await ctx.send("❌ **Usage:** `*am on @user` or `*am off @user`", delete_after=5)

        if mode.lower() == "on":
            self.target_users.add(user.id)
            msg = f"🎯 **AM ENABLED** for {user.name}. Prepare for hell."
        elif mode.lower() == "off":
            self.target_users.discard(user.id)
            msg = f"🏳️ **AM DISABLED** for {user.name}."
        else:
            return await ctx.send("❌ Invalid mode. Use `on` or `off`.")

        if ctx.author.id == self.bot.user.id:
            await ctx.message.edit(content=msg)
        else:
            await ctx.send(msg)

    @commands.command(name="am_reload")
    async def reload_roasts(self, ctx):
        """Reloads the roasts from the file without restarting."""
        self.load_roasts()
        await ctx.send("✅ **Roast cache updated!**")

def setup(bot):
    bot.add_cog(AutoMessager(bot))