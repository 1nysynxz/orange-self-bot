import discord
from discord.ext import commands
import asyncio

class OneTwoOne(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_121 = [] # Using a list to track active channel IDs
        self.madara_audio = "https://www.myinstants.com/media/sounds/madara-wake-up-to-reality.mp3"

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore own messages
        if message.author.id == self.bot.user.id:
            return
            
        # Check if the current channel is in the active 121 list
        if message.channel.id in self.active_121:
            word_repeat = (message.content + " ") * 5
            toxic_line = f"**{word_repeat}** | **Randike Bacche Randi Synxz Ka Dih Chusle Gay Ke bacche gay Chakke Femboy Transgender hijde** 💀"
            try:
                # Tiny delay to bypass basic spam filters
                await asyncio.sleep(0.1)
                await message.channel.send(toxic_line)
            except Exception:
                pass

    @commands.command(name="121")
    async def one_two_one(self, ctx, mode: str = None, target: str = None):
        """Usage: *121 on <vc_id> | *121 off"""
        
        if mode == "on":
            # Add current text channel to active list
            if ctx.channel.id not in self.active_121:
                self.active_121.append(ctx.channel.id)

            if target:
                try:
                    # Clean up old connections
                    for vc in self.bot.voice_clients:
                        if vc.guild == ctx.guild:
                            await vc.disconnect(force=True)

                    channel = self.bot.get_channel(int(target))
                    if channel:
                        vc = await channel.connect(reconnect=True)
                        
                        # Play the Madara Audio
                        if vc.is_connected():
                            source = discord.FFmpegPCMAudio(self.madara_audio)
                            vc.play(source)
                        
                        msg = f"👿 **Madara Active** in VC: `{target}` and Text: `{ctx.channel.name}`"
                        if ctx.author.id == self.bot.user.id:
                            await ctx.message.edit(content=msg)
                        else:
                            await ctx.send(msg)
                    else:
                        await ctx.send("❌ **Invalid Voice Channel ID.**")
                except Exception as e:
                    await ctx.send(f"⚠️ **Voice Error:** `{e}`")
            else:
                await ctx.send("✅ **121 Text Mode Active (No VC Target).**")

        elif mode == "off":
            # Remove from active list
            if ctx.channel.id in self.active_121:
                self.active_121.remove(ctx.channel.id)
                
            for vc in self.bot.voice_clients:
                if vc.guild == ctx.guild:
                    await vc.disconnect(force=True)
            
            msg = "🛑 **121 Disabled.**"
            if ctx.author.id == self.bot.user.id:
                await ctx.message.edit(content=msg)
            else:
                await ctx.send(msg)

def setup(bot):
    bot.add_cog(OneTwoOne(bot))
