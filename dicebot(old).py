import discord
from discord.ext import commands
import asyncio
import re
import random
import json
import Roll
import Spell
import Equipment
from enum import Enum

class GameMode (Enum):
    WIZARDS_FIFTH_ED = 1
    STAR_WARS_FIFTH_ED = 2

current_game_mode = GameMode.WIZARDS_FIFTH_ED

bad_reactions = ["cringe.jpg", "mike.jpg","nat1.gif", "nat1.jpg", "jazz.jpg"]
good_reactions = ["heisenberg.gif", "joji.jpg", "mcmahon.gif", "nat20.jpg"]

bot_prefix='.'
bot = commands.Bot(command_prefix=bot_prefix)

spells = {}
with open("docs/spells.json", "r", encoding="utf8") as fp:
    spells = json.load(fp)

equipments ={}
with open("docs/equipment.json", "r", encoding="utf8") as fp:
    equipments = json.load(fp)

@bot.event
async def on_ready():
    print ("Let's Roll!")
    print (bot.user.name)
    print (bot.user.id)
    await bot.change_presence(activity=discord.Game(name='D&D 5th Edition | !help'))

@bot.command(pass_context=True, description="Rolls dice. \nExamples: \n\".roll 1d20\" Rolls one twenty-sided die. \n\".roll 2d6+3\" Rolls two six-sided die and adds a modifier of three. \n\".roll stats\" Automatically rolls 6 attribute stats using 5e rules. \nMake sure there are no spaces.")
async def roll(ctx, dice : str):
    author = ctx.message.author
    if dice != 'stats':
        result, natural = Roll.getRoll(dice=dice, author=author)
        await ctx.message.channel.send(embed=result)
        if natural == 1:
            path = random.choice(bad_reactions)
            await ctx.message.channel.send(file=discord.File("resources/reactions/5e/bad/" + path))
        elif natural == 20:
            path = random.choice(good_reactions)
            await ctx.message.channel.send(file=discord.File("resources/reactions/5e/good/" + path))
    elif dice == 'stats':
        stats = Roll.getStats(author)
        await ctx.message.channel.send(embed=stats)
    else:
        await ctx.message.channel.send("Hello")

@bot.command(pass_context=True, description="Retrieves info about a spell given its name.")
async def spell(ctx, *, spellname):
    spellresult = Spell.getSpells(ctx.message.author, spellname, spells)
    await ctx.message.channel.send(embed=spellresult)

@bot.command(pass_context=True, description="Searches for equipment by name and/or type.")
async def equipment(ctx, *, equipmentname):
    item = Equipment.getEquipment(ctx.message.author, equipmentname, equipments)
    await ctx.message.channel.send(embed=item)

bot.run("ENTER ID HERE")
