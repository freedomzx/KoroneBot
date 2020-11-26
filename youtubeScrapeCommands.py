import discord
import random
import asyncio
import sys
import time
import yfinance
import json
import requests
import datetime
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

# base = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId="
# second = "&type=video&eventType=live&key=" + googleAPIKey

base = "https://www.youtube.com/channel/"

class YoutubeScrapeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="vtuberLives")
    async def vtuberLives(self, ctx):
        # request = requests.get(base + vtuberChannelIDs["Sakura Miko"] + second)
        # request = request.json()

        await ctx.send("Scraping through the channels of the vtuber list I have, give me a few moments...")

        checkString = "{\"text\":\" watching\"}"
        liveList = []
        
        for key in vtuberChannelIDs:
            request = requests.get(base + vtuberChannelIDs[key])
            if checkString in request.text:
                liveList.append(key)

        liveString = ""
        for i in range(len(liveList)):
            liveString += liveList[i]
            if i != len(liveList)-1:
                liveString += ", "
            
        embedSend = discord.Embed(
            title="List of live VTubers",
            description=liveString
        )
        embedSend.set_thumbnail(url="https://static.wikia.nocookie.net/virtualyoutuber/images/f/f8/Hololive_Logo.png/revision/latest/scale-to-width-down/985?cb=20190623125928")
        await ctx.send(embed=embedSend)
            

def setup(bot):
    bot.add_cog(YoutubeScrapeCommands(bot))