import discord
from discord.ext import commands
import json
import os
import sys

# ================= PATCH START =================
from discord.enums import FriendFlags

# We return 0 directly to bypass all Enum creation errors
def _patched_from_dict(cls, data):
    return 0 

type.__setattr__(FriendFlags, '_from_dict', classmethod(_patched_from_dict))
# ================= PATCH END ===================

# Load Configuration
with open('config.json') as f:
    config = json.load(f)

# Initialize Bot
bot = commands.Bot(
    command_prefix=config['prefixes'], 
    self_bot=True, 
    help_command=None
)

@bot.event
async def on_ready():
    # Clears the console for a clean startup
    os.system('cls' if os.name == 'nt' else 'clear')
    print("---------------------------------")
    print(f"🍊 Orange-bot is now ONLINE")
    print(f"Logged in as: {bot.user}")
    print("---------------------------------")
    
    if not os.path.exists('./cogs'):
        os.makedirs('./cogs')
        
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            try:
                bot.load_extension(f'cogs.{file[:-3]}')
                print(f"✅ Loaded: {file}")
            except Exception as e:
                print(f"❌ Failed {file}: {e}")

@bot.event
async def on_message(message):
    access_cog = bot.get_cog('Access')
    
    if access_cog:
        if not access_cog.is_allowed(message.author.id):
            return
    else:
        if message.author.id != bot.user.id:
            return

    content = message.content.lower()
    
    if content == '0':
        prefix = config['prefixes'][0]
        await message.channel.send(f"{prefix}pressure")
        return 

    elif content == 'quit':
        # Check if it was your message before trying to edit
        if message.author.id == bot.user.id:
            await message.edit(content="`[ Orange-bot ] Disconnecting...`")
        os._exit(0)
    
    await bot.process_commands(message)

# Final run command
try:
    bot.run(config['token'])
except Exception as e:
    print(f"FATAL ERROR: {e}")
