import discord
from discord.ext import commands
import asyncio


extensions = "testcogs.cog"

bot = commands.Bot(command_prefix='.')

if __name__ == '__main__':
    try:
        bot.load_extension('cogs.equipment')
    except Exception as e:
        print('failed to load extension')

@bot.event
async def on_ready():
    print ("Let's Roll!")
    print (bot.user.name)
    print (bot.user.id)
    await bot.change_presence(game=discord.Game(name='v1.0-5e | !help'))

bot.run("")
