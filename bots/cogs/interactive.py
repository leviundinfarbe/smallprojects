#!/usr/bin/env python3
import discord
from discord.ext import commands

class Interactive(commands.Cog):
    """i love u!"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="hug", description="hug someone <3", category="Interactive")
    async def hug(self, ctx, content):
        await ctx.channel.send(f"*<@{ctx.author.id}> hugs {content.replace('<@!', '<@')}!*")

def setup(bot):
    bot.add_cog(Interactive(bot))
