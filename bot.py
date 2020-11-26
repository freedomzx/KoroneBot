import discord
import random
import asyncio
import sys
import time
import yfinance
import json
import requests
import datetime
import traceback
from discord.ext import commands
from discord.ext.commands import Bot

import tokendef
from tokendef import *
import definitions
from definitions import *
import commandhelpers
from commandhelpers import *

from PyDictionary import PyDictionary
from random_word import RandomWords
from googletrans import Translator

import mysql.connector
from mysql.connector import Error
import pandas as pd

client = discord.Client()

#list of files/cogs to use
def get_prefix(bot, message):
    prefixes = ['!']

    return commands.when_mentioned_or(*prefixes)(bot, message)

extensionList = [
                'generalCommands',
                'sqlCommands' ,
                'pokedexCommands',
                'youtubeScrapeCommands'
                ]

bot = commands.Bot(command_prefix='!', case_insensitive=True)

if __name__ == "__main__":
    for extension in extensionList:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------------')
    statusText = discord.Game(name = "not yandere sim!")
    await bot.change_presence(status = discord.Status.do_not_disturb, activity = statusText)
    print('set status as \"' + statusText.name + "\"\n------------------")

bot.run(token) #token is hidden from public repository