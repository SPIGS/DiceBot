import discord
from discord.ext import commands
import asyncio
import os.path
from os import path
from gamemode import GameMode

token = ""
command_prefix = ""

extensions = ["cogs.roll", "cogs.reference", "cogs.utility"]

def load_user_info():
    global token
    global command_prefix
    with open("docs/user.info", 'r') as user_info:
        lines = user_info.read().splitlines()
        token = lines[0]
        command_prefix = lines[1]

bot = commands.Bot(command_prefix="!") 

if __name__ == '__main__':
    if path.exists("docs/user.info"):
        print("User info exists; starting bot...")
        load_user_info()
    else:
        print("User info not found; prompting for info...")
        token = input("Enter your bot's token: ")
        command_prefix = input("Enter your bot's command prefix: ")
        
        with open("docs/user.info", 'w') as user_file:
            user_file.write(token + "\n")
            user_file.write(command_prefix)
        
        load_user_info()
    
    bot.command_prefix = command_prefix
    bot.remove_command("help")
    for extension in extensions:
        bot.load_extension(extension)
    bot.current_gamemode = GameMode.WIZARDS_FIFTH_ED


@bot.event
async def on_ready():
    print("Let's Roll!")
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(activity=discord.Game(name='D&D 5th Edition | ' + bot.command_prefix + 'help'))
    
bot.run(token, bot=True, reconnect=True)



