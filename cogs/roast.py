import discord
from discord.ext import commands
import random
import asyncio
import os

class Roasts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roasts_path = "roasts.txt"

    def get_roasts(self):
        """Reads roasts from the txt file and returns a list."""
        if not os.path.exists(self.roasts_path):
            return ["⚠️ Error: container/roasts.txt not found!"]
        
        with open(self.roasts_path, "r", encoding="utf-8") as f:
            roasts = [line.strip() for line in f.readlines() if line.strip()]
        return roasts if roasts else ["⚠️ Roast file is empty!"]

    @commands.command(name="roast")
    async def roast(self, ctx, target: str = None, amount: int = 1):
        """Usage: *roast @user [amount up to 10000]"""
        
        if not target:
            return await ctx.send("❌ **Mention someone to roast, nigga.**")

        # Cap the amount at 10,000
        if amount > 10000:
            amount = 10000
        
        roast_list = self.get_roasts()
        
        # If the file is missing or empty, stop here
        if "⚠️" in roast_list[0]:
            return await ctx.send(roast_list[0])

        # Delete the trigger message for cleanliness
        try:
            await ctx.message.delete()
        except:
            pass

        for i in range(amount):
            try:
                # Pick a random roast from your file
                selected_roast = random.choice(roast_list)
                await ctx.send(f"{target} {selected_roast}")
                
                # Tiny delay to prevent getting disabled by Discord
                if amount > 1:
                    await asyncio.sleep(0.4) 
            except Exception as e:
                print(f"Roast Error: {e}")
                break

def setup(bot):
    bot.add_cog(Roasts(bot))
