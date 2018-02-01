import discord
from discord.ext import commands
import asyncio
import re
import random
import json
import Roll
import Spell
import Equipment

bot_prefix='.'
bot = commands.Bot(command_prefix=bot_prefix)

spells = {}
with open("json/spells.json", "r", encoding="utf8") as fp:
    spells = json.load(fp)

equipments ={}
with open("json/equipment.json", "r", encoding="utf8") as fp:
    equipments = json.load(fp)

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

def isDungeonMaster (message):
    author = message.author
    rolenames = []
    for role in author.roles:
        rolenames.append(role.name)

    if "Dungeon Master" in rolenames:
        return True
    else:
        return False

@bot.event
async def on_ready():
    print ("Let's Roll!")
    print (bot.user.name)
    print (bot.user.id)
    await bot.change_presence(game=discord.Game(name='v1.0-5e | !help'))

@bot.command(pass_context=True, description="Rolls dice. \nExamples: \n.roll 1d20 Rolls one twenty-sided die. \n.roll 2d6+3 Rolls two six-sided die and adds a modifier of three. \nMake sure there are no spaces.")
async def roll(ctx, dice : str):
    author = ctx.message.author

    if dice != 'stats':
        result, natural = Roll.getRoll(dice=dice, author=author)
        await bot.send_message(destination=ctx.message.channel, embed=result)
        if natural == 1:
            await bot.send_file(destination=ctx.message.channel, fp="_static/nat1.png")
        elif natural == 20:
            await bot.send_file(destination=ctx.message.channel, fp="_static/nat20.jpg")
    elif dice == 'stats':
        stats = Roll.getStats(author)
        await bot.send_message(destination=ctx.message.channel, embed=stats)
    else:
        await bot.send_message(ctx.message.channel, "Hello")

@bot.command(pass_context=True, description="Retrieves info about a spell given its name.")
async def spell(ctx, *, spellname):
    spellresult = Spell.getSpells(ctx.message.author, spellname, spells)
    await bot.send_message(destination=ctx.message.channel, embed=spellresult)

@bot.command(pass_context=True, description="Searches for equipment by name and/or type.")
async def equipment(ctx, *, equipmentname):
    item = Equipment.getEquipment(ctx.message.author, equipmentname, equipments)
    await bot.send_message(destination=ctx.message.channel, embed=item)

@bot.command(pass_context=True, description="Clears the text chat; for use by channel administators only.")
async def clear(ctx):
    if canClearChat(ctx.message):
        async for msg in bot.logs_from(ctx.message.channel):
            await bot.delete_message(msg)
    else:
        await bot.say("You do not have permissions to do that.")

@bot.command(pass_context=True, description="Gives a player an item. Only usable by DM.")
async def give(ctx, player, amount, item):
    if isDungeonMaster(ctx.message):
        await bot.send_message(ctx.message.channel, "Can give player and item.")
    else:
        await bot.send_message(ctx.message.channel, "You do not have permission to do that.")

bot.run("insert your bot token here")
