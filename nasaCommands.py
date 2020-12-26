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
import helpStrings
from helpStrings import *

from PyDictionary import PyDictionary
from random_word import RandomWords

import mysql.connector
from mysql.connector import Error
import pandas as pd

class NasaCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #get the astronomy picture of the day
    @commands.command(name="apod", help=apodHelp, brief=apodHelpShort)
    async def apod(self, ctx):
        url = "https://api.nasa.gov/planetary/apod?api_key=" + nasaAPIKey

        request = requests.get(url)
        request = request.json()

        embedSend = discord.Embed(
            title="Astronomy Picture of the Day"
        )
        embedSend.add_field(name="Title", value=request["title"], inline=False)
        embedSend.add_field(name="Date", value=request["date"], inline=False)
        embedSend.add_field(name="Explanation", value=request["explanation"], inline=False)
        embedSend.add_field(name="Copyright", value=request["copyright"], inline=False)
        embedSend.set_thumbnail(url=request["url"])

        await ctx.send(embed=embedSend)


def setup(bot):
    bot.add_cog(NasaCommands(bot))