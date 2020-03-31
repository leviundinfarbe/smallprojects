#!/usr/bin/env python3
from random import randrange
import linecache
import re

import discord
from discord.ext import commands

class Tunes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="tune", description="Want or have a tune?", category="Tunes")
    async def tune(self, ctx, arg="r"):
        if arg == "r":
            with open('music', 'r') as f:
                lines = f.readlines()
                nr = randrange(len(lines))
                await ctx.channel.send("#{}: {}".format(str(nr+1), lines[nr].split("\t")[0]))

        elif re.match(r'\d+$', arg):
            try:
                line = linecache.getline('music', int(arg))
                await ctx.channel.send(line.split('\t')[0])
            except:
                await ctx.channel.send("Sorry kid, I don't have that tune.")

        else:
            try:
                if re.match(r'spotify:album:', arg):
                    url = "https://open.spotify.com/album/" + arg[14:]
                elif re.match(r'https://open\.spotify\.com/album/', arg) or re.match(r'https://w{,3}\.?youtube\.com/playlist?list=', arg):
                    url = arg
                elif re.match(r'https://www.youtube.com/watch\?v=.*?&list=.*?$', arg):
                    r = re.match(r'(https://www.youtube.com/)watch\?v=.*?&(list=.*?$)', arg)
                    url = r.group(1) + 'playlist?' + r.group(2)
            except:
                pass

            try:
                with open("music", "a") as f:
                    f.write('\n' + url)
                with open("music", "r") as f:
                    nr = len(f.readlines())
                await ctx.channel.send(f"Saved as #{nr}.")
            except:
                await ctx.channel.send("Not a valid URL.")

def setup(bot):
    bot.add_cog(Tunes(bot))
