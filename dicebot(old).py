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

sw_bad_reactions = ["bad1.gif", "bad2.gif", "bad3.gif", "bad4.gif", "bad5.gif", "bad6.jpg", "bad7.jpg", "bad8.jpg", "bad9.gif", "bad10.gif"]
sw_good_reactions = ["good1.gif", "good2.gif", "good3.gif", "good4.gif","good5.gif","good6.gif", "good7.gif", "good8.gif"]

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
    await bot.change_presence(activity=discord.Game(name='D&D 5th Edition | !help'))

@bot.command(pass_context=True, description="Rolls dice. \nExamples: \n\".roll 1d20\" Rolls one twenty-sided die. \n\".roll 2d6+3\" Rolls two six-sided die and adds a modifier of three. \n\".roll stats\" Automatically rolls 6 attribute stats using 5e rules. \nMake sure there are no spaces.")
async def roll(ctx, dice : str):
    author = ctx.message.author
    if dice != 'stats':
        result, natural = Roll.getRoll(dice=dice, author=author)
        await ctx.message.channel.send(embed=result)
        if natural == 1:
            if current_game_mode == GameMode.WIZARDS_FIFTH_ED:
                path = random.choice(bad_reactions)
                await ctx.message.channel.send(file=discord.File("_static/5e/bad/" + path))
            elif current_game_mode == GameMode.STAR_WARS_FIFTH_ED:
                path = random.choice(sw_bad_reactions)
                await ctx.message.channel.send(file=discord.File("_static/sw5e/bad/" + path))
            else:
                path = random.choice(bad_reactions)
                await ctx.message.channel.send(file=discord.File("_static/5e/bad/" + path))
        elif natural == 20:
            if current_game_mode == GameMode.WIZARDS_FIFTH_ED:
                path = random.choice(good_reactions)
                await ctx.message.channel.send(file=discord.File("_static/5e/good/" + path))
            elif current_game_mode == GameMode.STAR_WARS_FIFTH_ED:
                path = random.choice(sw_good_reactions)
                await ctx.message.channel.send(file=discord.File("_static/sw5e/good/" + path))
            else:
                path = random.choice(good_reactions)
                await ctx.message.channel.send(file=discord.File("_static/5e/good/" + path))
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

@bot.command(pass_context=True, description="Switches gamemode.")
async def gameset (ctx, *, gamemode):
    global current_game_mode
    wizard_fifth_aliases = ['5e', 'fifth edition', 'dnd 5e', 'd&d 5e']
    star_wars_aliases = ['sw5e', 'star wars', 'star wars 5e', 'star wars fifth edition']
    
    embedresult = discord.Embed()
    embedresult.type = "rich"
    usercolour = discord.Colour.dark_purple()
    try:
        usercolour = author.top_role.colour
    except:
        usercolour = discord.Colour.dark_purple()
        
    embedresult.colour = usercolour
    embedresult.clear_fields()
    
    new_gamemode = gamemode.lower()
    if new_gamemode in wizard_fifth_aliases:
        print("Changing gamemode to D&D 5th edition.")
        await bot.change_presence(activity=discord.Game(name='D&D 5th Edition | !help'))
        current_game_mode = GameMode.WIZARDS_FIFTH_ED
        embedresult.add_field(name='Game changed to Dungeons & Dragons 5th Edition', value="Don't split the party!", inline=False)
    elif new_gamemode in star_wars_aliases:
        print("Changing gamemode to Star Wars 5th edition.")
        await bot.change_presence(activity=discord.Game(name='Star Wars 5th Edition | !help'))
        current_game_mode = GameMode.STAR_WARS_FIFTH_ED
        print(current_game_mode)
        embedresult.add_field(name='Game changed to Star Wars 5th Edition', value="May the Force be with you.", inline=False)
    else:
        embedresult.add_field(name='Error: No such game available.', value="\u200b", inline=False)
    
    await ctx.message.channel.send(embed=embedresult)


bot.run("ENTER ID HERE")
