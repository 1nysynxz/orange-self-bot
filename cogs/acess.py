import discord
from discord.ext import commands
import json
import os

class Access(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "whitelisted.json"
        self.whitelisted = self.load_db()

    def load_db(self):
        """Loads whitelisted IDs from JSON or creates it if missing."""
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump([], f)
            return []
        
        with open(self.db_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def save_db(self):
        """Saves current whitelist to the JSON file."""
        with open(self.db_path, "w") as f:
            json.dump(self.whitelisted, f)

    def is_allowed(self, user_id):
        """Checks if a user is the owner or in the whitelist."""
        if user_id == self.bot.user.id:
            return True
        return user_id in self.whitelisted

    @commands.command()
    async def tokenadd(self, ctx, user_id: int):
        """Adds a user to the whitelist."""
        if user_id not in self.whitelisted:
            self.whitelisted.append(user_id)
            self.save_db()
            await ctx.message.edit(content=f"✅ **ID `{user_id}` added to whitelist.**")
        else:
            await ctx.message.edit(content="⚠️ **User is already whitelisted.**")

    @commands.command()
    async def tokendelete(self, ctx, user_id: int):
        """Removes a user from the whitelist."""
        if user_id in self.whitelisted:
            self.whitelisted.remove(user_id)
            self.save_db()
            await ctx.message.edit(content=f"❌ **ID `{user_id}` removed from whitelist.**")
        else:
            await ctx.message.edit(content="⚠️ **User not found in list.**")

    @commands.command()
    async def whitelist(self, ctx):
        """Displays all whitelisted users."""
        if not self.whitelisted:
            await ctx.message.edit(content="📝 **Whitelist is currently empty.**")
        else:
            ids = "\n".join([f"`{i}`" for i in self.whitelisted])
            await ctx.message.edit(content=f"📜 **Whitelisted IDs:**\n{ids}")

def setup(bot):
    bot.add_cog(Access(bot))
