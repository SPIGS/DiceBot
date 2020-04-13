import discord
from discord.ext import commands
import asyncio
import re
import json
from gamemode import GameMode

class Reference(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.spells_info = {}
        with open("docs/spells.json", "r", encoding="utf8") as fp:
            self.spells_info = json.load(fp)

        self.equipments_info = {}
        with open("docs/equipment.json", "r", encoding="utf8") as fp:
            self.equipments_info = json.load(fp)

    @commands.command(aliases=["equip", "eq"], pass_context=True, invoke_without_command=True, help='Retrieves info about a piece of equipment given its name or searches for equipment when given a series of search terms.', brief='- provides rules reference for equipment stats.', description='Equipment')
    async def equipment (self, ctx, *, equipment_info):
        item = self.getEquipment(ctx.message.author, equipment_info)
        await ctx.message.channel.send(embed=item)

    @commands.command(aliases=["spell", "sp"], pass_context=True, invoke_without_command=True, help='Retrieves info about a spell given its name or searches for spells when given a series of search terms.', brief='- provides rules reference for spell information.', description='Spells')
    async def spells (self, ctx, *, spell_info):
        spellresult = self.getSpells(ctx.message.author, spell_info)
        await ctx.message.channel.send(embed=spellresult)

    def getSpells (self, author, message):
        message = message.lower()
        searchterms = re.split('(?<!level)\s', message)

        print (str(author) + " is searching for spelss with terms " + str(searchterms))

        embedresult = discord.Embed()
        embedresult.type = "rich"
        usercolour = discord.Colour.dark_purple()
        try:
            usercolour = author.top_role.colour
        except:
            usercolour = discord.Colour.dark_purple()
            
        embedresult.colour = usercolour
        results = ""

        for spell in self.spells_info:
            matches = 0
            if " ".join(searchterms) == spell['name'].lower():
                print("hello")
                embedresult.clear_fields()
                embedresult.title = spell['name']
                embedresult.add_field(name=spell['level'], value="\u200b", inline=False)
                desc = spell['desc']
                if (len(desc) <=1000):
                        embedresult.add_field(name="Description:", value=spell['desc'], inline=False)
                else:
                    descarray = desc.split("\n")
                    for a in descarray:
                        if re.search('[a-zA-Z]', a):
                            if (descarray.index(a)==0):
                                if (len(a)<1000):
                                    embedresult.add_field(name="Description:", value=a, inline=False)
                            else:
                                if (len(a)<1000):
                                    embedresult.add_field(name="\u200b",value=a, inline=False)
                embedresult.add_field(name="Casting Time:", value=spell['casting_time'], inline=False)
                embedresult.add_field(name="Duration:", value=spell['duration'], inline=False)
                embedresult.add_field(name="Range:", value=spell['range'], inline = False)
                embedresult.add_field(name="Concentration:", value=spell['concentration'], inline=False)
                embedresult.add_field(name="Ritual:", value=spell['ritual'], inline=False)
                embedresult.add_field(name="Components:", value=spell['components'], inline=False)
                embedresult.add_field(name="Class:", value=spell['class'], inline= False)
                try:
                    embedresult.add_field(name="Higher Levels:", value=spell['higher_level'], inline=False)
                except:
                    embedresult = embedresult

                try:
                    embedresult.add_field(name="Materials:", value=spell['material'], inline=False)
                except:
                    embedresult = embedresult

                return (embedresult)

            for term in searchterms:
                if term in spell['name'].lower():
                    matches = matches + 1
                elif term in spell['class'].lower():
                    matches = matches + 1
                elif term in spell['school'].lower():
                    matches = matches + 1
                elif term in spell['level'].lower():
                    matches = matches + 1

            if matches == len(searchterms):
                results = results+spell['name']+"\n"

        if results != "":
            embedresult.clear_fields()
            if len(results) >= 1024:
                embedresult.add_field(name="Results:", value="Too many results, narrow search", inline=False)
                print ("Too many results to list.")
            else:
                embedresult.add_field(name="Results:", value=results, inline=False)
                print ("Returning matched spells!")
        else:
            embedresult.clear_fields()
            embedresult.add_field(name="Results:", value="No spells found.", inline=False)
            print ("No spells found.")

        return embedresult

    def getEquipment (self, author, message):
        message = message.lower()
        searchterms = message.split(" ")
        print(str(author) + " is searching equipment with terms: " + str(searchterms))
        results = ""

        embedresult = discord.Embed()
        embedresult.type = "rich"
        usercolour = discord.Colour.dark_purple()
        try:
            usercolour = author.top_role.colour
        except:
            usercolour = discord.Colour.dark_purple()
            
        embedresult.colour = usercolour
        embedresult.clear_fields()
        for item in self.equipments_info:
            matches= 0
            if " ".join(searchterms) == item['name'].lower():
                embedresult.clear_fields()
                embedresult.title = item['name']
                embedresult.add_field(name="Type:", value=item['item_type'], inline=False)
                embedresult.add_field(name="Weight", value=item['weight'], inline=False)
                embedresult.add_field(name="Cost", value=item['cost'], inline=False)
                try:
                    embedresult.add_field(name="Damage:", value=item['damage'], inline=False)
                except:
                    embedresult = embedresult
                try:
                    embedresult.add_field(name="Damage Type:", value=item['damage_type'], inline=False)
                except:
                    embedresult = embedresult
                try:
                    embedresult.add_field(name="Properties", value=item['property'], inline=False)
                except:
                    embedresult = embedresult
                try:
                    embedresult.add_field(name="Armor Class", value=item['armor_class'], inline=False)
                except:
                    embedresult = embedresult
                try:
                    embedresult.add_field(name="Strength Requirement", value=item['strength_req'], inline=False)
                except:
                    embedresult = embedresult
                try:
                    embedresult.add_field(name="Stealth:", value=item['stealth'], inline=False)
                except:
                    embedresult = embedresult
                try:
                    embedresult.add_field(name="Don Time:", value=item['don_time'], inline=False)
                except:
                    embedresult = embedresult
                try:
                    embedresult.add_field(name="Doff Time", value=item['doff_time'], inline=False)
                except:
                    embedresult = embedresult
                try:
                    embedresult.add_field(name="Contents:", value=item['contents'], inline=False)
                except:
                    embedresult = embedresult
                try:
                    embedresult.add_field(name="Capacity:", value=item['capacity'], inline=False)
                except:
                    embedresult = embedresult

                return embedresult

            for term in searchterms:
                if term in item['name'].lower():
                    matches = matches + 1
                elif term in item['item_type'].lower():
                    matches = matches + 1

            if matches == len(searchterms):
                results = results + item['name']+"\n"

        if results != "":
            embedresult.clear_fields()
            if len(results) >= 1024:
                embedresult.add_field(name="Results:", value="Too many results, narrow search", inline=False)
                print ("Too many results to list.")
            else:
                embedresult.add_field(name="Results:", value=results, inline=False)
                print ("Returning matched equipment!")
        else:
            embedresult.clear_fields()
            embedresult.add_field(name="Results:", value="No equipment found.", inline=False)
            print("No equipment found.")

        return embedresult

def setup(bot):
    bot.add_cog(Reference(bot))
