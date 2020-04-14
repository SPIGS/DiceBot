import discord
from discord.ext import commands
import asyncio
import random
from gamemode import GameMode

fifth_edition_aliases = ["dungeons and dragons fifth edition", "dungeons & dragons fifth edition", "d&d5e", "dnd5e", "d&d 5e", "dnd 5e", "5e"]
sw_aliases = ["sw5e", "sw 5e", "star wars", "star wars fifth edition"]

dnd_sayings = [["Don't split the party.", "Proverb"],
               ["Rocks fall - everyone dies.", "The DM"],
               ["If it has stats, you can kill it.", "Proverb"],
               ["Roll initiative!", "The DM"],
               ["I cast Magic Missile at the darkness!", "Gallstaf, Sorcerer of Light"],
               ["I pickpocket the guard.", "The Chaotic Neutral Rogue"],
               ["I roll to seduce the dragon.", "The Bard"],
               ["So how do you want to do this?", "The DM"],
               ["Are you sure?", "The DM"]]

sw_sayings = [["May the Force be with you.", "The Jedi"],
              ["This is where the fun begins.", "Anakin Skywalker"],
              ["Hello there!", "Obi-Wan Kenobi"],
              ["I've got a bad feeling about this...", "Han Solo"],
              ["Only a Sith deals in absolutes.", "Obi-Wan Kenobi"],
              ["I'll try spinning - that's a cool trick!", "Anakin Skywalker"],
              ["Execute Order 66", "Sheev Palpatine"],
              ["Just like the simulations!", "Soldiers of the 501st Legion"],
              ["Aren't you a little short for a stormtrooper?", "Leia Organa"],
              ["Be careful not to choke on your aspirations.", "Darth Vader"]]

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["gamemodeset", "setgamemode", "sgm", "gms"], pass_context=True, help='Switches the current game mode to a new one. The currently supported games are:\n - Dungeons and Dragons Fifth Edition\n - Star Wars Fifth Edition', brief='- switches the current game mode.', description='Set Game Mode')
    async def gamemode (self, ctx, gamemode):
        
        embedresult = discord.Embed()
        embedresult.type = "rich"
        usercolour = discord.Colour.dark_purple()
        try:
            usercolour = ctx.message.author.top_role.colour
        except:
            usercolour = discord.Colour.dark_purple()

        embedresult.colour = usercolour
        embedresult.clear_fields()

        new_gamemode = gamemode.lower()
        if new_gamemode in fifth_edition_aliases:
            self.bot.current_gamemode = GameMode.WIZARDS_FIFTH_ED
            await self.bot.change_presence(activity=discord.Game(name='D&D 5th Edition | ' + self.bot.command_prefix + 'help'))
            choice = random.choice(dnd_sayings)
            quote = choice[0]
            originator = choice[1]
            embedresult.title = 'Game changed to Dungeons & Dragons 5th Edition'
            embedresult.add_field(name="*" + quote + "*", value="-" + originator, inline=False)
        elif new_gamemode in sw_aliases:
            self.bot.current_gamemode = GameMode.STAR_WARS_FIFTH_ED
            await self.bot.change_presence(activity=discord.Game(name='Star Wars 5th Edition | ' + self.bot.command_prefix + 'help'))
            embedresult.title = "Game changed to Star Wars 5th Edition"
            choice = random.choice(sw_sayings)
            quote = choice[0]
            originator = choice[1]
            embedresult.add_field(name="*" + quote + "*", value="-" + originator, inline=False)
        else:
            embedresult.add_field(
                name='Error: No such game available.', value="\u200b", inline=False)
        
        await ctx.message.channel.send(embed=embedresult)

    @commands.group(pass_context=True, invoke_without_command=True)
    async def help(self, ctx):
        if is_public_channel(ctx.message.channel):
            await self.send_help_notification(ctx.message.channel)

        await ctx.message.author.send("Default help")

    @help.group(aliases=["equip", "eq"], pass_context=True, invoke_without_command=True)
    async def equipment(self, ctx):
        if is_public_channel(ctx.message.channel):
            await self.send_help_notification(ctx.message.channel)
        equipment_command = self.bot.get_command("equipment")

        await self.send_command_help(ctx.message.author, equipment_command, None)

    @help.group(aliases=["sp", "spell"], pass_context=True, invoke_without_command=True)
    async def spells(self, ctx):
        if is_public_channel(ctx.message.channel):
            await self.send_help_notification(ctx.message.channel)
        spells_command = self.bot.get_command("spells")

        await self.send_command_help(ctx.message.author, spells_command, None)
    
    @help.group(aliases=["r"], pass_context=True, invoke_without_command=True)
    async def roll(self, ctx):
        if is_public_channel(ctx.message.channel):
            await self.send_help_notification(ctx.message.channel)
        roll_command = self.bot.get_command("roll")

        await self.send_command_help(ctx.message.author, roll_command, ["stats"])
        

    @roll.group(pass_context=True, invoke_without_command=True)
    async def stats (self, ctx):
        if is_public_channel(ctx.message.channel):
            await self.send_help_notification(ctx.message.channel)

        stats_command = self.bot.get_command("roll stats")
        await self.send_command_help(ctx.message.author, stats_command, None)

    async def send_help_notification (self, channel):
        embedresult = discord.Embed()
        embedresult.type = "rich"
        usercolour = discord.Colour.dark_purple()
        try:
            usercolour = author.top_role.colour
        except:
            usercolour = discord.Colour.dark_purple()

        embedresult.colour = usercolour
        embedresult.clear_fields()
        embedresult.title = ":white_check_mark: " + "  Help sent! Check your DMs."
        await channel.send(embed=embedresult)

    async def send_command_help (self, author, command, subcommands: [str]):
        embedresult = discord.Embed()
        embedresult.type = "rich"
        usercolour = discord.Colour.dark_purple()
        try:
            usercolour = author.top_role.colour
        except:
            usercolour = discord.Colour.dark_purple()

        embedresult.colour = usercolour
        embedresult.clear_fields()
        embedresult.title = command.name
        embedresult.add_field(name="Description", value=command.help, inline=False)

        if subcommands is not None:
            subcommands_value = ""
            for subcommand in subcommands:
                subcommands_value = subcommands_value + "- " + subcommand + "\n"
            embedresult.add_field(name="Subcommands",
                                  value=subcommands_value, inline=False)

        await author.send(embed=embedresult)

#there is no way to easily test if the message was sent in a TextChannel or in a DMChannel so I'm just going to do this
def is_public_channel(channel):
    try:
        _ = channel.guild
        return True
    except:
        return False

def setup(bot):
    bot.add_cog(Utility(bot))
