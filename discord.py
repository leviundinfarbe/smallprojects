#!/usr/bin/env python3
# A Discord-Bot using discord.py: https://github.com/Rapptz/discord.py
# A bot for random images and quotes-handling. Also have a look at the Telegram-implementation

from bs4 import BeautifulSoup
from random import randrange
from os import listdir
import linecache, requests, discord, time, re

client = discord.Client()
TOKEN = '<your bot-token>'
usage = '<define a usage message>'

def picfromfolder(folder): # returns a random file (image) from <folder>
    filename = filelist[randrange(0, len(listdir(folder)))]
    return f'{folder}/{filename}'

@client.event
async def on_message(message):
    if message.author.bot: # checks if the message comes from a bot, otherwise the bot may answer itself and get stuck in a loop
        return
    text = message.content
    text = text.replace('<@!', '<@') # Discord user-ids are automatically escaped so this unescapes them for search and stuff
    lowtext = text.lower()

    if re.match(r'!add', lowtext):
        text = text[len(re.match(r'!add\s*', lowtext).group()):]
        with open('quotes.txt', 'a') as stream:
            stream.write(f'\n{text}') # append quote to file
        with open('quotes.txt', 'r') as stream:
            nr = len(stream.readlines()) # nr of latest quote
        await message.channel.send(f'Quote #{nr} saved.')

    elif re.match(r'!random', lowtext):
        with open('quotes.txt', 'r') as stream:
            lines = stream.readlines()
            nr = randrange(len(lines))
            await message.channel.send(f'#{str(nr+1)}: {lines[nr]}')

    elif re.match(r'!\d+\s*$', lowtext):
        nr = re.match(r'!(\d+)\s*$', text)
        line = linecache.getline('quotes.txt', int(nr.group(1))) # returns text of specific line
        if line != "":
            await message.channel.send(line)
        else:
            await message.channel.send("Quote does not exist.")

    elif re.match(r'!search\s+.*', lowtext):
        pattern = re.match(r'![S,s]earch\s+(.*)', text)
        with open('quotes.txt', 'r') as stream:
            hits = list()
            ctr = 1
            for line in stream:
                if re.search(pattern.group(1).lower(), line.lower()):
                    hits.append((ctr, line.strip()))
                ctr += 1
            result = '\n'.join([f"#{hit[0]}: {hit[1]}" for hit in hits])
            if len(result) > 2000: # characterlimit of Discord
                result = ', '.join([f"#{hit[0]}" for hit in hits])
            if len(result) > 2000: # characterlimit of Discord
                await message.channel.send('Search is to vague.')
            elif result == "":
                await message.channel.send("Quote does not exist.")
            else:
                await message.channel.send(result)

    elif re.match(r'!help', lowtext):
        await message.channel.send(usage)

    elif re.match(r'!cat', lowtext):
        catimg = requests.get('https://thiscatdoesnotexist.com/', headers={'User-Agent':'An Awesome User Agent'})
        with open('cat.png', 'wb') as f:
            f.write(catimg.content) # Image needs to be saved, because the images all use the domain as path.
        await message.channel.send(file=discord.File('cat.png'))

    elif re.match(r'^!yoda', text):
        await message.channel.send(file=discord.File(picfromfolder('yoda')))

    elif re.match(r'^!pus', text):
        await message.channel.send(file=discord.File(picfromfolder('platypus')))

    elif re.match(r'^!ray', text):
        await message.channel.send(file=discord.File(picfromfolder('ray/')))

    elif re.match(r'!dog', lowtext):
        dogtml = requests.get('https://random.dog').text
        soup = BeautifulSoup(dogtml, 'html.parser')
        imgblock = str(soup.find('img', id='dog-img'))
        img = re.search(r'src="(.+?)"', imgblock)
        await message.channel.send('https://random.dog/' + img.group(1))

    elif re.search(r'echo', lowtext): # very useless but fun command to annoy your friends or even yourself, does not check length of message!
        SUB = str.maketrans('abcdefghijklmnopqrstuvwxyz1234567890-+!()=?.,', 'ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ₁₂₃₄₅₆₇₈₉₀₋₊ᵎ₍₎₌ˀ.,')
        SUP = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-+!()=?.,', 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᵠᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ¹²³⁴⁵⁶⁷⁸⁹⁰⁻⁺ᵎ⁽⁾⁼ˀ⋅⋅')
        time.sleep(0.3)
        await message.channel.send('```\n' + text.upper() + '\n```')
        time.sleep(0.9)
        await message.channel.send('```\n' + lowtext.translate(SUB) + '\n```')
        time.sleep(1.2)
        await message.channel.send('```\n' + text.translate(SUP) + '\n```')

    else:
        if re.search(r'uwu', lowtext):
            await message.channel.send('uwu')
        if re.search(r'owo', lowtext):
            await message.channel.send('òwó')

client.run(TOKEN)