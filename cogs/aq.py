import discord
from discord.ext import commands, tasks
import asyncio

class AutoQuest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.aq_active = False
        # Dictionary of all current/common Discord Quest Game IDs
        self.game_ids = {
            "Genshin Impact": 767432128312737792,
            "Honkai: Star Rail": 1104617192241041408,
            "Valorant": 700136079563423744,
            "Minecraft": 1083424117565214720,
            "Call of Duty": 1133527509339553832,
            "League of Legends": 401518684763586560,
            "Apex Legends": 541484311354933258
        }

    @tasks.loop(minutes=15)
    async def quest_cycle(self):
        """Cycles through every game ID to trigger all active quests."""
        if not self.aq_active:
            return

        for game_name, game_id in self.game_ids.items():
            if not self.aq_active:
                break
                
            # Set the spoofed activity
            activity = discord.Activity(
                type=discord.ActivityType.playing,
                application_id=game_id,
                name=game_name,
                details="Completing Quest...",
                assets={'large_image': 'game_icon'} # Generic asset trigger
            )
            
            await self.bot.change_presence(activity=activity, status=discord.Status.online)
            print(f"DEBUG: Now spoofing {game_name} for Orbs.")
            
            # Wait 15 minutes per game to ensure progress hits 100%
            await asyncio.sleep(900) 

    @commands.command(name="aq")
    async def auto_quest(self, ctx, mode: str = None):
        """Usage: *aq on | *aq off"""
        if mode == "on":
            if self.aq_active:
                return await ctx.send("⚠️ Auto-Quest is already running, nigga.")
            
            self.aq_active = True
            if not self.quest_cycle.is_running():
                self.quest_cycle.start()
            
            msg = "🚀 **AUTO-ORBS ENABLED.** The bot will now cycle through all Discord Quests."
            
        elif mode == "off":
            self.aq_active = False
            self.quest_cycle.stop()
            await self.bot.change_presence(activity=None)
            msg = "🛑 **AUTO-ORBS DISABLED.** Presence cleared."
        else:
            return await ctx.send("❌ Use `*aq on` or `*aq off`.")

        if ctx.author.id == self.bot.user.id:
            await ctx.message.edit(content=msg)
        else:
            await ctx.send(msg)

def setup(bot):
    bot.add_cog(AutoQuest(bot))