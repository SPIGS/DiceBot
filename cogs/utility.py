import discord
from discord.ext import commands
import asyncio
from gamemode import GameMode

fifth_edition_aliases = ["dungeons and dragons fifth edition", "dungeons & dragons fifth edition", "d&d5e", "dnd5e", "d&d 5e", "dnd 5e", "5e"]
sw_aliases = ["sw5e", "sw 5e", "star wars", "star wars fifth edition"]  

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["gamemodeset", "setgamemode"], pass_context=True, help='Switches the current game mode to a new one. The currently supported games are:\n - Dungeons and Dragons Fifth Edition\n - Star Wars Fifth Edition', brief='- switches the current game mode.', description='Set Game Mode')
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
            embedresult.add_field(name='Game changed to Dungeons & Dragons 5th Edition',
                                  value="Don't split the party!", inline=False)
        elif new_gamemode in sw_aliases:
            self.bot.current_gamemode = GameMode.STAR_WARS_FIFTH_ED
            await self.bot.change_presence(activity=discord.Game(name='Star Wars 5th Edition | ' + self.bot.command_prefix + 'help'))
            embedresult.add_field(name='Game changed to Star Wars 5th Edition',
                                  value="May the Force be with you.", inline=False)
        else:
            embedresult.add_field(
                name='Error: No such game available.', value="\u200b", inline=False)
        
        await ctx.message.channel.send(embed=embedresult)

    @commands.group(pass_context=True, invoke_without_command=True)
    async def help(self, ctx):
        if self.is_public_channel(ctx.message.channel):
            await self.send_help_notification(ctx.message.channel)

        await ctx.message.author.send("Default help")
        
    
    @help.group(aliases=["r"], pass_context=True, invoke_without_command=True)
    async def roll(self, ctx):
        if self.is_public_channel(ctx.message.channel):
            await self.send_help_notification(ctx.message.channel)
            
        await ctx.message.author.send("Roll help")
        

    @roll.group(pass_context=True, invoke_without_command=True)
    async def stats (self, ctx):
        if self.is_public_channel(ctx.message.channel):
            await self.send_help_notification(ctx.message.channel)

        await ctx.message.author.send("Roll help")

    #there is no way to easily test if the message was sent in a TextChannel or in a DMChannel so I'm just going to do this
    def is_public_channel (self, channel):
        try:
            _ = channel.guild
            return True
        except:
            return False

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
        embedresult.add_field(name="Help sent! Check your DMs.", value="\u200b", inline=False)
        await channel.send(embed=embedresult)


def setup(bot):
    bot.add_cog(Utility(bot))
