import discord
from discord.ext import commands
import asyncio
import random
import re
from gamemode import GameMode, get_good_reaction, get_bad_reaction

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='roll', aliases=['r'], pass_context=True, invoke_without_command=True, help='Rolls and performs addition, subtraction, and multiplcation with dice. Examples: \n`.roll 1d20` Rolls one twenty-sided die. \n`.roll 2d6+3` Rolls two six-sided die and adds a modifier of three.\n`.roll 1d20-1d4+1` Rolls one twenty-sided die, subtracts the result of a four-sided die, and adds a modifier of one.\n`.roll 1d12x2` Rolls a twelve-sided die and multiplies the result by two.', brief='- Rolls dice.', description='Roll')
    async def roll(self, ctx, *, dice : str):
        author = ctx.message.author
        #log info
        print(str(author) + " is attempting to roll " + str(dice) + "!")
        result, natural = self.getRoll(dice=dice, author=author)
        await ctx.message.channel.send(embed=result)
        if natural == 1:
            await ctx.message.channel.send(file=discord.File(get_bad_reaction(self.bot.current_gamemode)))
        elif natural == 20:
            await ctx.message.channel.send(file=discord.File(get_good_reaction(self.bot.current_gamemode)))

    @roll.group(name='stats', pass_context=True, invoke_without_command=True, help='Rolls 6 attribute stats. Equivalent to rolling 4d6 and subtracting the lowest result, six times.', brief=' - Rolls 6 attribute stats.', description='Stats')
    async def stats(self, ctx):
        author = ctx.message.author
        stats = getStats(author)
        await ctx.message.channel.send(embed=stats)

    def getRoll (self, dice, author):
        #token specification
        token_spec = [
            ('DICE', r'\d+d\d+'),
            ('OPERATOR', r'\+|-|x'),
            ('MODIFIER', r'\d+(?!d)|d+(?<!d)'),
            ('ILLEGAL', r'.')
        ]
        #get rid of whitespace in string
        dice_no_whitespace = dice.replace(' ', '')

        #make the regex
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)
        
        match_objects = []
        for mo in re.finditer(tok_regex, dice_no_whitespace):
            match_objects.append(mo)
        remaining_tokens = len(match_objects)
        
        parsed_tokens = []
        result_string = ''
        valid = True
        previous_token = None
        #check if the grammar is right
        for token in match_objects:
            remaining_tokens = remaining_tokens -1
            kind = token.lastgroup
            value = token.group()
            if kind == 'DICE':
                if previous_token in (None, 'OPERATOR'):
                    parsed_tokens.append(['DICE', value])
                    previous_token = 'DICE'
                else:
                    result_string = 'Error: Value is not a valid roll!'
                    valid = False
                    break

            elif kind == 'OPERATOR':
                if (previous_token in ('DICE', 'MODIFIER')) and (remaining_tokens > 0):
                    parsed_tokens.append(['OPERATOR', value])
                    previous_token = 'OPERATOR'
                else:
                    valid = False
                    result_string = 'Error: The supplied operator is not valid!'
                    break

            elif kind == 'MODIFIER':
                if previous_token in (None, 'OPERATOR'):
                    parsed_tokens.append(['MODIFIER', value])
                    previous_token = 'MODIFIER'
                else:
                    valid = False
                    result_string = 'Error: The supplied modifier is not valid!'
                    break
            elif kind == 'ILLEGAL':
                valid = False
                result_string = 'Error: Roll contains an invalid string!'
                break
        
        #if still valid, check if the dices values break any rules 
        if valid:
            for token in parsed_tokens:
                if token[0] == 'DICE':
                    amount, sides = re.findall(r'\d+', token[1])
                    if int(amount) > 20:
                        valid = False
                        result_string = 'Error: Too many dice!'
                        break
                    elif int(amount) <= 0:
                        valid = False
                        result_string = "Error: Invalid number of dice!"
                    if int(sides) > 100:
                        valid = False
                        result_string = 'Error: Too many sides!'
                    elif int(sides) == 0:
                        result_string = "Error: Can't roll a dice with 0 sides!"
                        valid = False
                    elif int(sides) < 0:
                        result_string = "Error: Can't roll a dice with negative sides!"
                        valid = False
        
        total = 0
        natural = None
        if valid:
            #evaluate the roll
            current_operator = '+'
            for token in parsed_tokens:
                
                if token[0] == 'DICE':
                    result_string = result_string + '[ '
                    #evaluate the dice and add it to the result string
                    dice_total = 0
                    amount, sides = re.findall(r'\d+', token[1])
                    for i in range(0, int(amount)):
                        dice_result = random.randint(1, int(sides))
                        dice_total += dice_result

                        #do check for nat 1 or nat 20
                        if int(amount) == 1 and int(sides) == 20:
                            if dice_result == 20 or dice_result == 1:
                                natural = dice_result

                        result_string = result_string + str(dice_result)
                        if int(amount) - (i+1) > 0:
                            result_string = result_string + ' + '
                    if current_operator == '+':
                        total += dice_total
                    elif current_operator == '-':
                        total -= dice_total
                    elif current_operator == 'x':
                        total *= dice_total
                    result_string = result_string + ' ]'
                
                elif token[0] == 'OPERATOR':
                    current_operator = token[1]
                    result_string = result_string + " " + token[1] + " "

                elif token[0] == 'MODIFIER':
                    if current_operator == '+':
                        total += int(token[1])
                    elif current_operator == '-':
                        total -= int(token[1])
                    elif current_operator == 'x':
                        total *= int(token[1])
                    result_string = result_string + " " + token[1]
            result_string = result_string + " = " + str(total)

        #initiate embeded result that will be displayed.
        embedresult = discord.Embed()
        embedresult.type = "rich"
        usercolour = discord.Colour.dark_purple()
        try:
            usercolour = author.top_role.colour
        except:
            usercolour = discord.Colour.dark_purple()

        embedresult.colour = usercolour
        embedresult.clear_fields()
        embedresult.title = result_string
        print("Result: " + result_string)
        return embedresult, natural

def getStats (author):
    #log info
    print (str(author) + " is rolling stats!")

    #initiate embeded result that will be displayed.
    result_string = "[ "
    embedresult = discord.Embed()
    embedresult.type = "rich"
    usercolour = discord.Colour.dark_purple()
    try:
        usercolour = author.top_role.colour
    except:
        usercolour = discord.Colour.dark_purple()
    embedresult.colour = usercolour
    embedresult.clear_fields()

    for x in range(6):
        dice = []
        for _y in range(4):
            dice.append(random.randint(1,6))
        stat = sum(dice) - min(dice)
        if x != 5:
            result_string= result_string + str(stat) + ", "
        else:
             result_string = result_string + str(stat)
    result_string = result_string + " ]"

    embedresult.title = result_string
    return embedresult

def setup(bot):
    bot.add_cog(Dice(bot))
