#!/usr/bin/env python3
import time
import re

import asyncio
import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        text = ctx.content
        lowtext = text.lower()

        if re.search(r'<word trigger>', lowtext):
            try:
                channel = ctx.author.voice.channel
                v = await channel.connect()
                stream = open('audiofile', 'rb')
                player = v.play(discord.PCMAudio(stream))
                while v.is_playing():
                    await asyncio.sleep(1)
                v.stop()
                await v.disconnect()
            except:
                await ctx.channel.send("You aren't connected to a voicechannel.")


        elif re.search(r'echo', lowtext):
            time.sleep(0.3)
            await ctx.channel.send('```\n' + text.upper() + '\n```')
            time.sleep(0.9)
            await ctx.channel.send('```\n' + lowtext.translate(str.maketrans('abcdefghijklmnopqrstuvwxyz1234567890-+!()=?.,', 'ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ₁₂₃₄₅₆₇₈₉₀₋₊ᵎ₍₎₌ˀ.,')) + '\n```')
            time.sleep(1.2)
            await ctx.channel.send('```\n' + text.translate(str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-+!()=?.,', 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᵠᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ¹²³⁴⁵⁶⁷⁸⁹⁰⁻⁺ᵎ⁽⁾⁼ˀ⋅⋅')) + '\n```')

def setup(bot):
    bot.add_cog(Events(bot))
