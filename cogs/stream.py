import discord
from discord.ext import commands

class Stream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stream(self, ctx, *, message: str):
        """Sets your status to Streaming. Usage: *stream <message>"""
        # Change the URL to your own Twitch link if you want
        stream_url = "https://www.twitch.tv/discord"
        
        await self.bot.change_presence(
            activity=discord.Streaming(
                name=message, 
                url=stream_url
            )
        )

        success_msg = f"💜 **Streaming status set to:** `{message}`"

        # Edit our own message or send a new one for whitelisted users
        if ctx.author.id == self.bot.user.id:
            await ctx.message.edit(content=success_msg)
        else:
            await ctx.send(success_msg)

    @commands.command()
    async def stopstream(self, ctx):
        """Clears your streaming status."""
        await self.bot.change_presence(activity=None)
        
        stop_msg = "✅ **Status cleared.**"
        
        if ctx.author.id == self.bot.user.id:
            await ctx.message.edit(content=stop_msg)
        else:
            await ctx.send(stop_msg)

def setup(bot):
    bot.add_cog(Stream(bot))
