import discord
from discord.ext import commands

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def game(self, ctx):
        """Main game command group."""
        if ctx.invoked_subcommand is None:
            msg = "❌ **Usage:** `*game play [name]` or `*game stop`"
            if ctx.author.id == self.bot.user.id:
                await ctx.message.edit(content=msg)
            else:
                await ctx.send(msg)

    @game.command(name="play")
    async def game_play(self, ctx, *, game_name: str):
        """Sets your status to Playing [game_name]"""
        try:
            # Create the Game activity
            activity = discord.Game(name=game_name)
            await self.bot.change_presence(activity=activity)
            
            status_msg = f"🎮 **Status set to:** Playing `{game_name}`"
            
            if ctx.author.id == self.bot.user.id:
                await ctx.message.edit(content=status_msg)
            else:
                await ctx.send(status_msg)
        except Exception as e:
            print(f"Game Error: {e}")

    @game.command(name="stop")
    async def game_stop(self, ctx):
        """Clears your game status."""
        try:
            await self.bot.change_presence(activity=None)
            
            status_msg = "🛑 **Game status cleared.**"
            
            if ctx.author.id == self.bot.user.id:
                await ctx.message.edit(content=status_msg)
            else:
                await ctx.send(status_msg)
        except Exception as e:
            print(f"Game Stop Error: {e}")

def setup(bot):
    bot.add_cog(Game(bot))