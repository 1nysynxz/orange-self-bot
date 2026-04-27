import discord
from discord.ext import commands
import asyncio

class GCManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.changing = {} # Dictionary to track loops for different GCs

    @commands.command()
    async def gcn(self, ctx, *, name: str):
        """Loops GC name change with a counter. Usage: *gcn <name>"""
        if not isinstance(ctx.channel, discord.GroupChannel):
            return await ctx.send("❌ **This command only works in Group Chats!**")

        channel_id = ctx.channel.id
        self.changing[channel_id] = True
        count = 1

        # Delete the command trigger to stay stealthy
        await ctx.message.delete()

        while self.changing.get(channel_id):
            try:
                new_name = f"{name} {count}"
                await ctx.channel.edit(name=new_name)
                count += 1
                # Discord has heavy rate limits for GC name changes. 
                # 1.5 to 2 seconds is the safest speed to avoid a temporary ban.
                await asyncio.sleep(1.5) 
            except discord.HTTPException:
                # If we hit a rate limit, wait a bit longer
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Error in GCN: {e}")
                break

    @commands.command()
    async def gcnstop(self, ctx):
        """Stops the GC name changing loop."""
        channel_id = ctx.channel.id
        if channel_id in self.changing:
            self.changing[channel_id] = False
            await ctx.send("🛑 **GC Name loop stopped.**", delete_after=3)
        else:
            await ctx.send("⚠️ **No loop is running in this channel.**", delete_after=3)

def setup(bot):
    bot.add_cog(GCManager(bot))
