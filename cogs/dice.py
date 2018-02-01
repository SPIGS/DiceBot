import discord
from discord.ext import commands
import random
import asyncio
import re

class Dice:

    def __init__ (self, bot):
        self.bot = bot

    @commands.command(name="roll", pass_context=True, no_pm=True, description="Rolls dice. \nExamples: \n.roll 1d20 Rolls one twenty-sided die. \n.roll 2d6+3 Rolls two six-sided die and adds a modifier of three. \nMake sure there are no spaces.")
    async def roll (self, ctx, dice : str):
        author = ctx.message.author
        if dice != 'stats':
            result, natural = self.rollDice(dice=dice, author=author)
            await self.bot.send_message(destination=ctx.message.channel, embed=result)
            if natural == 1:
                await self.bot.send_file(destination=ctx.message.channel, fp="_static/nat1.png")
            elif natural == 20:
                await self.bot.send_file(destination=ctx.message.channel, fp="_static/nat20.jpg")
        elif dice == 'stats':
            stats = self.rollStats(author)
            await self.bot.send_message(destination=ctx.message.channel, embed=stats)
        else:
            await self.bot.send_message(ctx.message.channel, "Hello")

    #returns an embeded result of the roll
    def rollDice (self, dice, author):
        #log info
        print(str(author) + " is attempting to roll " + str(dice) + "!")

        #init variables
        roll_results = []
        modifier = 0
        total = 0
        natural =0

        #initiate embeded result that will be displayed.
        result_string = "["
        embedresult  = discord.Embed()
        embedresult.type = "rich"
        usercolor = discord.Colour.dark_purple()
        for role in author.roles:
            if role.is_everyone == False:
                usercolor = role.colour
        embedresult.colour = usercolor
        embedresult.clear_fields()

        #parse the input
        parsed_roll = re.split('d|\+|-', dice)
        parsed_roll.extend([0] * (3 - len(parsed_roll)))
        print(parsed_roll)

        #assign value to roll
        try :
             roll_results = [0] * int(parsed_roll[0])
        except ValueError:
            result_string = "Error: Value is not a valid roll!"
            print(result_string)
            embedresult.add_field(name=result_string, value="\u200b", inline=False)
            return embedresult, 0

        #assign value to modifier
        try:
            if "-" in dice:
                modifier = -int(parsed_roll[2])
            elif r"+" in dice:
                modifier = int(parsed_roll[2])
        except ValueError:
            result_string = "Error: No valid modifier!"
            print(result_string)
            embedresult.add_field(name=result_string, value="\u200b", inline=False)
            return embedresult, 0

        #test if roll complies with restrictions
        if int(parsed_roll[0]) == 0:
            result_string = "Error : Can't roll 0 dice!"
            print(result_string)
            embedresult.add_field(name=result_string, value="\u200b", inline=False)
            return embedresult, 0

        if int(parsed_roll[0]) >= 20:
            result_string = "Error: Too many dice."
            print (result_string)
            embedresult.add_field(name=result_string, value="\u200b", inline=False)
            return embedresult, 0

        if int(parsed_roll[1]) > 100:
            result_string = "Error: Number of faces is too high."
            print(result_string)
            embedresult.add_field(name=result_string, value="\u200b", inline=False)
            return embedresult, 0

        #roll each die
        for x in range(-1, int(parsed_roll[0])-1):
            try:
                roll_results[x] = random.randint(1, int(parsed_roll[1]))
            except ValueError:
                result_string = "Error: Don't use spaces for the dice argument!"
                print (result_string)
                embedresult.add_field(name=result_string, value="\u200b", inline=False)
                return embedresult, 0


        #get the total
        total = sum(roll_results) + modifier

        #piece together the string that will be ouputed to user
        for x in range (0, len(roll_results)):
            if x != (len(roll_results) -1):
                result_string += (str(roll_results[x]) + r" + ")
            else:
                result_string += (str(roll_results[x]) + " ]")

        if modifier < 0:
            result_string += (" - " + str(parsed_roll[2]))
        else:
            result_string += (r" + " + str(parsed_roll[2]))

        #check if roll was a nat 1 or nat 20
        if (int(parsed_roll[0]) == 1) and (int(parsed_roll[1]) == 20):
            if roll_results[0] == 1:
                natural = 1
            elif roll_results[0] == 20:
                natural = 20
            else:
                natural = 0

        embedresult.add_field(name=result_string + " = " + str(total), value="\u200b", inline=False)

        #return  the result
        print (result_string + " = " + str(total))
        return embedresult, natural



    def rollStats (self, author):
        #log info
        print (str(author) + " is rolling stats!")

        #initiate embeded result that will be displayed.
        result_string = "[ "
        embedresult = discord.Embed()
        embedresult.type = "rich"
        usercolour = discord.Colour.dark_purple()
        for role in author.roles:
            if role.is_everyone == False:
                usercolour = role.colour
        embedresult.colour = usercolour
        embedresult.clear_fields()

        roll_results =[]
        for x in range(6):
            dice = []
            for y in range(4):
                dice.append(random.randint(1,6))
            stat = sum(dice) - min(dice)
            if x != 5:
                result_string= result_string + str(stat) + ", "
            else:
                result_string = result_string + str(stat)
        result_string = result_string + " ]"

        embedresult.add_field(name=result_string, value="\u200b", inline=False)
        return embedresult

#def setup is necessary
def setup (bot):
    bot.add_cog(Dice(bot))
