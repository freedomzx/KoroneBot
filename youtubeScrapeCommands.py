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

        if not liveList:
            await ctx.send("Huh... Looks like no one is live.")
            return

        liveString = ""
        for i in range(len(liveList)):
            liveString += liveList[i]
            if i != len(liveList)-1:
                liveString += ", "
            
        embedSend = discord.Embed(
            title="List of live VTubers",
        )
        embedSend.set_thumbnail(url="https://w7.pngwing.com/pngs/963/811/png-transparent-youtube-logo-youtube-red-logo-computer-icons-youtube-television-angle-rectangle.png")
        embedSend.add_field(name = "Live", value=liveString)
        await ctx.send(embed=embedSend)

    @commands.command(name="subcount")
    async def subcount(self, ctx, arg1):
        #sub/viewer/video count
        url = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + arg1 + "&key" + googleAPIKey

        request = requests.get(url)
        request = request.json()

        subCount = request["items"]["statistics"]["subscriberCount"]
        viewCount = request["items"]["statistics"]["viewCount"]
        videoCount = request["items"]["statistics"]["videoCount"]
        #channel icon
        url = "https://www.googleapis.com/youtube/v3/channels?part=snippet&id+" + arg1 + "&fields=items%%2Fsnippet%%2Fthumbnails&key=" + googleAPIKey

        embedSend = discord.Embed(
            title="Statistics for channel ID: " + arg1
        )
        embedSend.set_thumbnail(url=url)
        embedSend.add_field(name="Subscriber count", value=subCount, inline=False)
        embedSend.add_field(name="Total views", value=viewCount, inline=False)
        embedSend.add_field(name="Amount of videos", value=videoCount, inline=False)

        ctx.send(embed=embedSend)

def setup(bot):
    bot.add_cog(YoutubeScrapeCommands(bot))