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
from discord.ext import commands, tasks
from discord.ext.commands import Bot

import tokendef
from tokendef import *
import definitions
from definitions import *
import commandhelpers
from commandhelpers import *
import helpStrings
from helpStrings import *

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

#background task to change status every 30 seconds. can be changed to do other stuff too
@tasks.loop(seconds=30)
async def background_task():
    #print("Bot Status Change (30 Seconds)")
    randomIndex = random.randint(1, len(activityList)-1)
    await bot.change_presence(status = discord.Status.do_not_disturb, activity=activityList[randomIndex])

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------------')
    background_task.start()


bot.run(token) #token is hidden from public repository