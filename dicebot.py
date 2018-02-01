import discord
from discord.ext import commands
import asyncio

extensions = ["cogs.characters", "cogs.dice", "cogs.equipment", "cogs.spells"]

bot = commands.Bot(command_prefix='.')

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('failed to load extension')

@bot.event
async def on_ready():
    print ("Let's Roll!")
    print (bot.user.name)
    print (bot.user.id)
    await bot.change_presence(game=discord.Game(name='5e | !help'))

@bot.command(pass_context=True, description="Clears the text chat; for use by channel administators only.", aliases=["clr","cls"])
async def clear(ctx):
    if canClearChat(ctx.message):
        async for msg in bot.logs_from(ctx.message.channel):
            await bot.delete_message(msg)
    else:
        await bot.say("You do not have permissions to do that.")

def canClearChat(message):
    author = message.author
    rolenames = []
    for role in author.roles:
        rolenames.append(role.name)

    if "Owner" in rolenames:
        return True
    elif "Admin" in rolenames:
        return True
    else:
        return False


bot.run("insert your token here")
