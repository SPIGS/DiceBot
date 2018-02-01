import discord
from discord.ext import commands
import random
import asyncio
import re

class DiceCog:

    def __init__ (self, bot):
        self.bot = bot

    @commands.command(name="roll", pass_context=True)
    async def roll (self, ctx, dice : str):
        print ("test")
        
#def setup is necessary
def setup (bot):
    bot.add_cog(DiceCog(bot))
