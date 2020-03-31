#!/usr/bin/env python3
from bs4 import BeautifulSoup
from random import randrange
from os import listdir
import linecache
import requests
import time
import re

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters

TOKEN = ""
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher


def start(update, ctx):
    ctx.bot.send_message(chat_id=update.effective_chat.id, text="Hello friend.")

start_handler = CommandHandler('start', start)
dp.add_handler(start_handler)


def cat(update, ctx):
    catimg = requests.get('https://thiscatdoesnotexist.com/', headers={'User-Agent':'Ken sent me'})
    with open('cat.png', 'wb') as f:
        f.write(catimg.content)
    ctx.bot.send_photo(chat_id=update.effective_chat.id, photo=open('cat.png', 'rb'), caption='by thiscatdoesnotexist.com')

cat_handler = CommandHandler('cat', cat)
dp.add_handler(cat_handler)


def dog(update, ctx):
    img = None
    c = 0
    while img == None and c < 10:
        dogtml = requests.get('https://random.dog').text
        soup = BeautifulSoup(dogtml, 'html.parser')
        imgblock = str(soup.find('img', id='dog-img'))
        img = re.search(r'src="(.+?)"', imgblock)
        c += 1
    try:
        ctx.bot.send_message(chat_id=update.effective_chat.id, text='https://random.dog/' + img.group(1))
    except:
        ctx.bot.send_message(chat_id=update.effective_chat.id, text='https://random.dog might be down.')

dog_handler = CommandHandler('dog', dog)
dp.add_handler(dog_handler)


def pic(update, ctx):
    filelist = listdir('folder')
    filename = filelist[randrange(0, len(filelist))]
    f = open(f'{'folder'}/{filename}', 'rb')
    ctx.bot.send_photo(chat_id=update.effective_chat.id, photo=f)
    f.close()

pic_handler = CommandHandler('pic', pic)
dp.add_handler(pic_handler)


def tune(update, ctx):
    if ctx.args == []:
        with open('music', 'r') as f:
            lines = f.readlines()
            nr = randrange(len(lines))
            ctx.bot.send_message(chat_id=update.effective_chat.id, text="#{}: {}".format(str(nr+1), lines[nr].split("\t")[0]))

    else:
        for arg in ctx.args:
            if re.match(r'\d+$', arg):
                try:
                    line = linecache.getline('music', int(arg))
                    ctx.bot.send_message(chat_id=update.effective_chat.id, text=line.split('\t')[0])
                except:
                    ctx.bot.send_message(chat_id=update.effective_chat.id, text="Sorry kid, I don't have that tune.")

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
                    ctx.bot.send_message(chat_id=update.effective_chat.id, text=f"Saved as #{nr}.")
                except:
                    ctx.bot.send_message(chat_id=update.effective_chat.id, text="Not a valid URL.")

tune_handler = CommandHandler('tune', tune)
dp.add_handler(tune_handler)


def random(update, ctx):
    with open('quotes', 'r') as f:
        lines = f.readlines()
        nr = randrange(len(lines))
        ctx.bot.send_message(chat_id=update.effective_chat.id, text=f'#{str(nr+1)}: {lines[nr]}')

random_handler = CommandHandler('random', random)
dp.add_handler(random_handler)


def q(update, ctx):
    for arg in ctx.args:
        try:
            line = linecache.getline('quotes', int(arg))
            if line != "":
                ctx.bot.send_message(chat_id=update.effective_chat.id, text=f"#{arg}: {line}")
            else:
                ctx.bot.send_message(chat_id=update.effective_chat.id, text="I can't seem to find that Quote.")
        except:
            ctx.bot.send_message(chat_id=update.effective_chat.id, text="Not a valid argument.")

q_handler = CommandHandler('q', q)
dp.add_handler(q_handler)


def search(update, ctx):
    pattern = ' '.join(ctx.args)

    with open('quotes', 'r') as f:
        hits = list()
        for c, line in enumerate(f):
            if re.search(' '.join(ctx.args).lower(), line.lower()):
                hits.append((c+1, line.strip()))
        result = '\n'.join([f"#{hit[0]}: {hit[1]}" for hit in hits])
        if len(result) > 2000:
            result = ', '.join([f"#{hit[0]}" for hit in hits])
        if len(result) > 2000:
            ctx.bot.send_message(chat_id=update.effective_chat.id, text="Search is to vague. Too much to handle.")
        elif result == "":
            ctx.bot.send_message(chat_id=update.effective_chat.id, text="I can't seem to find that Quote.")
        else:
            ctx.bot.send_message(chat_id=update.effective_chat.id, text=result)

search_handler = CommandHandler('search', search)
dp.add_handler(search_handler)


def echo(update, ctx):
    text = update.message.text
    lowtext = text.lower()

    if re.search(r'echo', lowtext):
        time.sleep(0.3)
        ctx.bot.send_message(chat_id=update.effective_chat.id, text=text.upper())
        time.sleep(0.9)
        ctx.bot.send_message(chat_id=update.effective_chat.id, text=lowtext.translate(str.maketrans('abcdefghijklmnopqrstuvwxyz1234567890-+!()=?.,', 'ᴀʙᴄᴅᴇғɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ₁₂₃₄₅₆₇₈₉₀₋₊ᵎ₍₎₌ˀ.,')))
        time.sleep(1.2)
        ctx.bot.send_message(chat_id=update.effective_chat.id, text=text.translate(str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-+!()=?.,', 'ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᵠᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ¹²³⁴⁵⁶⁷⁸⁹⁰⁻⁺ᵎ⁽⁾⁼ˀ⋅⋅')))

    elif re.search(r'yeet', lowtext):
        ctx.bot.send_photo(chat_id=update.effective_chat.id, photo=open('keyboy.png', 'rb'), caption='yeet')

    else:
        if re.search(r'uwu', lowtext):
            ctx.bot.send_message(chat_id=update.effective_chat.id, text="uwu")
        if re.search(r'owo', lowtext):
            ctx.bot.send_message(chat_id=update.effective_chat.id, text="òwó")
        if re.search(r'µwµ', lowtext):
            ctx.bot.send_message(chat_id=update.effective_chat.id, text="µwµ")
        if re.search(r'qwq', lowtext):
            ctx.bot.send_message(chat_id=update.effective_chat.id, text="qwq")

echo_handler = MessageHandler(Filters.text, echo)
dp.add_handler(echo_handler)

updater.start_polling()

updater.idle()
