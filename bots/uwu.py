#!/usr/bin/env python3
from bs4 import BeautifulSoup
from random import randrange
from os import listdir
import linecache
import requests
import time
import re

import asyncio
import discord
from discord.ext import commands

TOKEN = ''

bot = commands.Bot(command_prefix="!")

bot.load_extension('cogs.events')
bot.load_extension('cogs.interactive')
bot.load_extension('cogs.images')
bot.load_extension('cogs.quotes')
bot.load_extension('cogs.tunes')

bot.run(TOKEN)
