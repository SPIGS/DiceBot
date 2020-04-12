import discord
import re
import json

def getSpells (author, message, spells):
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

    for spell in spells:
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
