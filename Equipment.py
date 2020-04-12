import discord
import re
import json

def getEquipment (author, message, equipment):
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
    for item in equipment:
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
