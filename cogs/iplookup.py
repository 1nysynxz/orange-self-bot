import discord
from discord.ext import commands
import aiohttp

class IPLookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="iplookup", aliases=["ip", "whois"])
    async def iplookup(self, ctx, ip: str):
        """Fetches IP info and generates a Google Maps link."""

        if ctx.author.id == self.bot.user.id:
            await ctx.message.edit(content=f"🔍 **Scanning IP:** `{ip}`...")

        fields = "status,message,country,regionName,city,zip,isp,org,as,query,lat,lon"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"http://ip-api.com/json/{ip}?fields={fields}", timeout=10
                ) as response:
                    data = await response.json()

            if data.get("status") == "fail":
                error_msg = f"❌ **Error:** `{data.get('message', 'Invalid IP')}`"
                if ctx.author.id == self.bot.user.id:
                    return await ctx.message.edit(content=error_msg)
                return await ctx.send(error_msg)

            lat = data.get('lat')
            lon = data.get('lon')
            map_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

            info = f"""
```ansi
[2;34m--- [ IP INFORMATION ] ---[0m
[2;33mIP:[0m       [2;37m{data.get('query')}[0m
[2;33mCITY:[0m     [2;37m{data.get('city')}[0m
[2;33mREGION:[0m   [2;37m{data.get('regionName')}[0m
[2;33mCOUNTRY:[0m  [2;37m{data.get('country')}[0m
[2;33mISP:[0m      [2;37m{data.get('isp')}[0m
[2;33mASN:[0m      [2;37m{data.get('as')}[0m```

[2;32m[CLICK FOR MAP LOCATION](<{map_link}>)
"""

            if ctx.author.id == self.bot.user.id:
                await ctx.message.edit(content=info)
            else:
                await ctx.send(info)

        except Exception as e:
            print(f"IPLookup Error: {e}")
            await ctx.send(f"⚠️ Error: {e}")


def setup(bot):
    bot.add_cog(IPLookup(bot))