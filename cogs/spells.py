import discord
from discord.ext import commands
import asyncio
import re
import json

class Spells:

    def __init__(self, bot):
        self.bot = bot

        spells = {}
        with open("json/spells.json", "r", encoding="utf8") as fp:
            spells = json.load(fp)
        self.spells = spells

    def getMessageSource (self, ctx):
        if not ctx.message.channel:
            return ctx.message.author
        else:
            return ctx.message.channel

    @commands.command(name="spell", pass_context=True, description="Retrieves info about a spell given its name.")
    async def spell (self, ctx, *, spellname):
        messageSource = self.getMessageSource(ctx)
        spellresult = self.getSpells(ctx.message.author, ctx, spellname)
        await self.bot.send_message(destination=messageSource, embed=spellresult)

    def getSpells(self, author, ctx, message):
        message = message.lower()
        searchterms = re.split('(?<!level)\s', message)

        print (str(author) + " is searching for spelss with terms " + str(searchterms))

        embedresult = discord.Embed()
        embedresult.type = "rich"
        usercolor = discord.Color.dark_purple()

        if not ctx.message.server:
            usercolor = discord.Color.dark_grey()
        else:
            for role in author.roles:
                if role.is_everyone == False:
                    usercolor = role.colour

        results = ""
        embedresult.colour = usercolor

        for spell in self.spells:
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

def setup (bot):
    bot.add_cog(Spells(bot))
