#!/usr/bin/env python3
from bs4 import BeautifulSoup
from random import randrange
from os import listdir
import requests
import re

import discord
from discord.ext import commands

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def picfromfolder(self, folder, nr):
        filelist = listdir(folder)
        if int(nr) <= len(filelist) and int(nr) > 0:
            filename = [e for e in filelist if re.match('{}.'.format(nr), e)]
            return f'{folder}/{filename[0]}'
        else:
            return f'{folder}/{filelist[randrange(0, len(filelist))]}'

    @commands.command(name="pic", description="Some pics")
    async def pic(self, ctx, nr=0):
        await ctx.channel.send(file=discord.File(self.picfromfolder('pic', nr)))

    @commands.command(name="cat", description="thiscatdoesnotexist.com")
    async def cat(self, ctx):
            catimg = requests.get('https://thiscatdoesnotexist.com/', headers={'User-Agent':'Ken sent me'})
            with open('cat.png', 'wb') as f:
                f.write(catimg.content)
            await ctx.channel.send(file=discord.File('cat.png'))

    @commands.command(name="dog", description="random.dog")
    async def dog(self, ctx):
        img = None
        c = 0
        while img == None and c < 10:
            soup = BeautifulSoup(requests.get('https://random.dog').text, 'html.parser')
            img = re.search(r'src="(.+?)"', str(soup.find('img', id='dog-img')))
            c += 1
        try:
            await ctx.channel.send('https://random.dog/' + img.group(1))
        except:
            await ctx.channel.send('https://random.dog might be down.')

def setup(bot):
    bot.add_cog(Images(bot))
