#!/usr/bin/env python3
from random import randrange
import linecache
import re

import discord
from discord.ext import commands

class Quotes(commands.Cog):
    """context is a social construct we don't need"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addq", aliases=["add"], description="add a quote")
    async def addq(self, ctx, q):
        with open('quotes', 'a') as stream:
            stream.write(f'\n{q}')
        with open('quotes', 'r') as stream:
            nr = len(stream.readlines())
        await ctx.channel.send(f'Quote #{nr} saved.')

    @commands.command(name="ranq", aliases=["random"], description="get a random quote")
    async def ranq(self, ctx):
        with open('quotes', 'r') as stream:
            lines = stream.readlines()
            nr = randrange(len(lines))
            await ctx.channel.send(f'#{str(nr+1)}: {lines[nr]}')

    @commands.command(name="q", description="get specific quote by number")
    async def q(self, ctx, nr):
        try:
            line = linecache.getline('quotes', int(nr))
            await ctx.channel.send(line)
        except:
            await ctx.channel.send("I can't seem to find that Quote.")

    @commands.command(name="search", description="search quotes for keyword")
    async def search(self, ctx, s):
        with open('quotes', 'r') as stream:
            hits = list()
            for c, line in enumerate(stream):
                if re.search(s.replace('<@!', '<@').lower(), line.lower()):
                    hits.append((c+1, line.strip()))
            result = '\n'.join([f"#{hit[0]}: {hit[1]}" for hit in hits])
            if len(result) > 2000:
                result = ', '.join([f"#{hit[0]}" for hit in hits])
            if len(result) > 2000:
                await ctx.channel.send('Search is to vague. Too much to handle.')
            elif result == "":
                await ctx.channel.send("I can't seem to find that Quote.")
            else:
                await ctx.channel.send(result)

def setup(bot):
    bot.add_cog(Quotes(bot))
