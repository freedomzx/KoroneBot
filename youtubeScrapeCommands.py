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

# import google_auth_oauthlib.flow
# import googleapiclient.discovery
# import googleapiclient.errors

# base = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId="
# second = "&type=video&eventType=live&key=" + googleAPIKey

class YoutubeScrapeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="vtuberLives")
    async def vtuberLives(self, ctx):
        await ctx.send("Scraping through the channels in the vtuber list I have, give me a few moments...")
        print("Request for: live VTubers")

        # check for {"text":" watching"}
        # make it look like the bot is typing while it searches up all the live list
        liveDict = {}
        async with ctx.channel.typing():
            base = "https://www.youtube.com/channel/"
            checkString = "{\"text\":\" watching\"}"
            embedSend = discord.Embed(
                title="Currently Live",
            )
            embedSend.set_thumbnail(url="https://w7.pngwing.com/pngs/963/811/png-transparent-youtube-logo-youtube-red-logo-computer-icons-youtube-television-angle-rectangle.png")
            #go through all the sections of vtubers, check if anyone in any section is streaming.  if they are, add that field + the streamer into the embed
            at_least_one = False
            for group, vtubers in vtuberChannelIDs.items():
                sectionLiveList = []
                for key in vtubers:
                    request = requests.get(base + vtubers[key])
                    if checkString in request.text:
                        sectionLiveList.append(key)
                        liveDict[key] = vtubers[key]
                if sectionLiveList:
                    embedSend.add_field(name=group, value=", ".join(sectionLiveList), inline=False)
                    at_least_one = True
            #if nobody at all is streaming, say so and return
            if at_least_one:
                await ctx.send(embed=embedSend)
            else:
                await ctx.send("Looks like no one on my list is live.")
                return
                
        #if they want the links, get it from the liveDict dictioanry
        await ctx.send("Do you want the links to the streams? (yes/no)")

        def check(message):
            return message.channel == ctx.message.channel and message.author == ctx.message.author and (message.content.lower() == "yes" or message.content.lower() == "no")

        msg = await self.bot.wait_for("message", check=check)
        if msg.content.lower() == "no":
            return
        elif msg.content.lower() == "yes":
            liveLinks = ""
            for vtuber, channelId in liveDict.items():
                liveLinkURL = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channelId}&eventType=live&type=video&key={YOUR_API_KEY}".format(channelId=channelId, YOUR_API_KEY=googleAPIKey)
                videoRequest = requests.get(liveLinkURL)
                videoRequest = videoRequest.json()
                videoURL = "https://www.youtube.com/watch?v={videoID}".format(videoID = videoRequest["items"][0]["id"]["videoId"])
                liveLinks += videoURL + "\n"
            await ctx.send(liveLinks)

    @commands.command(name="channelinfo")
    async def channelinfo(self, ctx, arg1):
        #sub/viewer/video count
        url = "https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id=" + arg1 + "&key=" + googleAPIKey

        request = requests.get(url)
        request = request.json()

        print("Request for channel: " + arg1)

        thumbnail = request["items"][0]["snippet"]["thumbnails"]["high"]["url"]
        channelTitle = request["items"][0]["snippet"]["title"]
        channelDescription = request["items"][0]["snippet"]["description"]
        publishDate = request["items"][0]["snippet"]["publishedAt"]
        subCount = request["items"][0]["statistics"]["subscriberCount"]
        viewCount = request["items"][0]["statistics"]["viewCount"]
        videoCount = request["items"][0]["statistics"]["videoCount"]

        embedSend = discord.Embed(
            title="Statistics for channel: " + channelTitle
        )
        embedSend.set_thumbnail(url=thumbnail)
        embedSend.add_field(name="Channel Description", value=channelDescription, inline=False)
        embedSend.add_field(name="Subscriber Count", value=subCount, inline=False)
        embedSend.add_field(name="Total Views", value=viewCount, inline=False)
        embedSend.add_field(name="Total Videos", value=videoCount, inline=False)
        embedSend.add_field(name="Publish Date", value=publishDate, inline=False)

        await ctx.send(embed=embedSend)

def setup(bot):
    bot.add_cog(YoutubeScrapeCommands(bot))