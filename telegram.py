#!/usr/bin/env python3
# A Telegram-Bot using aiogram: https://github.com/aiogram/aiogram
# For random images and to get quotes, quotes can only be added manually or via
# Discord-Bot (look at discord.py) because of handling @-handles and because
# Telegram-Bots are public so everyone could add quotes.

from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
from random import randrange
from os import listdir
import requests, re, linecache

alias = {
    '<@discord user-id>':'name', # dictionary for conversion of Discord user-ids to specified names
}

TGTOKEN = '<your bot-token>'
usage = '<define a usage message>'

bot = Bot(token=TGTOKEN)
dp = Dispatcher(bot)

def picfromfolder(folder): # returns a random file (image) from <folder>
    filelist = listdir(folder)
    filename = filelist[randrange(0, len(filelist))]
    f = open(f'{folder}/{filename}', 'rb')
    return f

@dp.message_handler(commands=['help'])
async def incomming(message: types.Message):
    await message.reply(usage, 'Markdown') # 'Markdown' enables **bold** and other stylings

@dp.message_handler(commands=['cat'])
async def incoming(message: types.Message):
    catimg = requests.get('https://thiscatdoesnotexist.com/', headers={'User-Agent':'An Awesome User Agent'})
    with open('cat.png', 'wb') as f:
        f.write(catimg.content) # Image needs to be saved, because the images all use the domain as path.
    with open('cat.png', 'rb') as f:
        await message.answer_photo(f)

@dp.message_handler(commands=['dog'])
async def incoming(message: types.Message):
    dogtml = requests.get('https://random.dog').text
    soup = BeautifulSoup(dogtml, 'html.parser')
    imgblock = str(soup.find('img', id='dog-img'))
    img = re.search(r'src="(.+?)"', imgblock)
    await message.reply('https://random.dog/' + img.group(1))

@dp.message_handler(commands=['yoda'])
async def incoming(message: types.Message):
    await message.answer_photo(picfromfolder('yoda')) # a local folder with baby-yoda images, won't upload it here because of copyright
    f.close()

@dp.message_handler(commands=['pus'])
async def incoming(message: types.Message):
    await message.answer_photo(picfromfolder('platypus')) # a local folder with platypus images, won't upload it here because of copyright
    f.close()

@dp.message_handler(commands=['ray'])
async def incoming(message: types.Message):
    await message.answer_photo(picfromfolder('ray')) # a local folder with ray images, won't upload it here because of copyright
    f.close()

@dp.message_handler(commands=['random']) # usage: /random; returns a random quote
async def incoming(message: types.Message):
    with open('quotes.txt', 'r') as f:
        lines = f.readlines()
        nr = randrange(len(lines))
        for a in alias:
            lines[nr] = lines[nr].replace(a, alias[a])
        await message.reply(f'#{str(nr+1)}: {lines[nr]}')

@dp.message_handler(commands=['q']) # usage: /q <nr>; returns quote with specified number
async def incoming(message: types.Message):
    nr = re.match(r'/q\s*(\d+)\s*$', message['text'])
    line = linecache.getline('quotes.txt', int(nr.group(1)))
    for a in alias:
        line = line.replace(a, alias[a])
    if line != "":
        await message.reply(line)
    else:
        await message.reply("I can't seem to find that Quwuote.")

@dp.message_handler(commands=['search']) # usage: /search <keyword>; returns all quotes with specified keyword
async def incoming(message: types.Message):
    pattern = re.match(r'/search\s+(.*)', message['text'])
    with open('quotes.txt', 'r') as stream:
        hits = list()
        ctr = 1
        for line in stream:
            for a in alias:
                line = line.replace(a, alias[a])
            if re.search(pattern.group(1).lower(), line.lower()):
                hits.append((ctr, line.strip()))
            ctr += 1
        result = '\n'.join([f"#{hit[0]}: {hit[1]}" for hit in hits])
        if len(result) > 2000:
            result = ', '.join([f"#{hit[0]}" for hit in hits])
        if len(result) > 2000:
            await message.reply('Search is to vague. Too much to handle.')
        elif result == "":
            await message.reply("I can't seem to find that Quwuote.")
        else:
            await message.reply(result)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)