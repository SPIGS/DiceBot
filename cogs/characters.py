import discord
from discord.ext import commands
import asyncio
import json
import os

class CharacterManagement:

    def __init__(self, bot):
        self.bot = bot
        if not os.path.isfile("json/meta.json"):
            data = {}
            data['authors'] = {}
            with open('json/meta.json', "w+") as f:
                json.dump(data, f)


    def getMessageSource (self, ctx):
        if not ctx.message.channel:
            return ctx.message.author
        else:
            return ctx.message.channel

    def addCharacter (self, ctx, name, metadata):
        #TODO this is for testing purposes
        charactersheet = {}
        charactersheet['info'] = {
            "name": name,
            "race":"elf",
            "class":"fighter"
            }
        charactersheet['stats'] ={}
        charactersheet['stats']['ability']={"strength": 1}
        charactersheet['inventory']= ["sword", "shield", "armor"]

        print (str(charactersheet))
        with open ('json/' + name + '.json', "w+") as f:
            json.dump(charactersheet, f)

        metadata['authors'][str(ctx.message.author)] = str(name)
        with open('json/meta.json', 'w') as f:
            json.dump(metadata, f)


    def removeCharacter (self, ctx, name):
        #TODO
        pass

    @commands.command(name="deletecharacter", pass_context=True, aliases=["deletechar"], description="Deletes a character of a given name.")
    async def deletecharacter(self, ctx, name):
        #TODO
        pass

    @commands.command(name="createcharacter", pass_context=True, aliases=["createchar"], description="Creates a character of a given name.")
    async def createcharacter(self, ctx, *, name):
        roles = []

        for role in ctx.message.author.roles:
            roles.append(str(role))

        if "Dungeon Master" in roles:
            await self.bot.send_message(ctx.message.author, "This command can only be used by Players.")
        else:
            if os.path.isfile("json/" + name + ".json"):
                await self.bot.send_message(ctx.message.author, "That character already exists.")
            else:
                metadata = json.load(open('json/meta.json'))
                authors = metadata['authors']

                if str(ctx.message.author) in authors:
                    print (str(ctx.message.author) + " already has a character.")
                else:
                    print(str(ctx.message.author) + " does not have a character. Creating one.")
                    await self.bot.send_message(ctx.message.author, "Welcome, " + name + "!")
                    await self.bot.change_nickname(ctx.message.author, name)
                    self.addCharacter(ctx, name, metadata)

def setup (bot):
    bot.add_cog(CharacterManagement(bot))
