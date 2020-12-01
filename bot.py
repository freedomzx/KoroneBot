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
import helpStrings
from helpStrings import *

from PyDictionary import PyDictionary
from random_word import RandomWords
from googletrans import Translator

import mysql.connector
from mysql.connector import Error
import pandas as pd

client = discord.Client()

def get_prefix(bot, message):
    prefixes = ['!']

    return commands.when_mentioned_or(*prefixes)(bot, message)

#list of files/cogs to use
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
activityIterator = 0

@tasks.loop(minutes=1)
async def background_task():
    global activityIterator
    await bot.change_presence(status = discord.Status.do_not_disturb, activity=activityList[activityIterator])
    activityIterator += 1
    if activityIterator == len(activityList):
        activityIterator = 0

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------------')
    await bot.change_presence(status = discord.Status.do_not_disturb)
    background_task.start()


bot.run(token) #token is hidden from public repository