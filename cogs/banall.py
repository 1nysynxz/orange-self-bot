import discord
from discord.ext import commands
import asyncio

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="banall")
    async def ban_all(self, ctx):
        """Bans every member in the server if permissions allow."""
        if not ctx.guild:
            return

        # Check for permissions before attempting
        if not ctx.guild.me.guild_permissions.ban_members and not ctx.guild.me.guild_permissions.administrator:
            msg = "❌ **Error:** I don't have `Ban Members` or `Administrator` permissions."
            if ctx.author.id == self.bot.user.id:
                return await ctx.message.edit(content=msg)
            return await ctx.send(msg)

        if ctx.author.id == self.bot.user.id:
            await ctx.message.edit(content="🚀 **Banning all members...**")
        else:
            await ctx.send("🚀 **Banning all members...**")

        ban_count = 0
        fail_count = 0

        # Create a list of members excluding yourself and the bot
        targets = [m for m in ctx.guild.members if m.id != self.bot.user.id and m.id != ctx.guild.owner_id]

        async def fast_ban(member):
            nonlocal ban_count, fail_count
            try:
                await member.ban(reason="Nuked by Orange")
                ban_count += 1
            except:
                fail_count += 1

        # Use asyncio.gather to ban everyone at the same time (Super Fast)
        tasks = [fast_ban(member) for member in targets]
        await asyncio.gather(*tasks)

        final_msg = f"✅ **Finished.** Banned: `{ban_count}` | Failed: `{fail_count}`"
        await ctx.send(final_msg)

def setup(bot):
    bot.add_cog(Ban(bot))