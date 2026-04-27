import discord
from discord.ext import commands
import asyncio

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def split_messages(self, text, limit=1800):
        """Splits text into chunks while leaving room for code block wrappers."""
        return [text[i:i+limit] for i in range(0, len(text), limit)]

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Dynamic help that handles disconnects and long command lists."""
        
        full_help = "[2;34m--- [ ORANGE-BOT COMMAND LIST ] ---[0m\n"
        
        # Build the list from all loaded cogs
        for cog_name, cog in self.bot.cogs.items():
            full_help += f"\n[2;33m[{cog_name.upper()}][0m\n"
            for command in cog.get_commands():
                if not command.hidden:
                    full_help += f"[2;37m{ctx.prefix}{command.name}[0m - {command.help or 'No description'}\n"

        # Add the shortcuts
        full_help += "\n[2;33m[SHORTCUTS][0m\n"
        full_help += "[2;37m0[0m - Trigger pressure\n"
        full_help += "[2;37mquit[0m - Shutdown bot\n"

        chunks = self.split_messages(full_help)
        
        for index, chunk in enumerate(chunks):
            # Wrap each chunk in its own ANSI code block
            formatted_chunk = f"```ansi\n{chunk}\n```"
            
            try:
                if index == 0 and ctx.author.id == self.bot.user.id:
                    await ctx.message.edit(content=formatted_chunk)
                else:
                    await ctx.send(formatted_chunk)
                
                # Small delay between chunks to prevent "ServerDisconnectedError"
                await asyncio.sleep(0.5)
                
            except discord.errors.HTTPException:
                # If the server jitters, wait and try to send as a new message
                await asyncio.sleep(1)
                try:
                    await ctx.send(formatted_chunk)
                except:
                    pass
            except Exception as e:
                print(f"Help Chunk Error: {e}")

def setup(bot):
    bot.add_cog(Help(bot))