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

start = "https://pokeapi.co/api/v2/"

class PokedexCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #get the back/front sprite for a pokemon
    @commands.command(name="pokesprite")
    async def pokesprite(self, ctx, arg1, arg2, arg3):
        #regular check, check consistency between author and channel
        def check(message):
            return message.channel == ctx.message.channel and message.author == ctx.message.author
        pokemon = arg1
        position = arg2
        color = arg3

        url = start + "pokemon/" + pokemon
        request = requests.get(url)
        request = request.json()

        specs = ""
        if position == "front" or position == "back":
            specs += position
        else:
            await ctx.send("Hmm... The position argument isn't quite what I'm looking for.  Put in either: front, back")

        if color == "shiny" or color == "default":
            specs += "_" + color
        else:
            await ctx.send("Hmm... The color argument isn't quite what I'm looking for.  Put in either: shiny, default")

        #print(request["sprites"][specs])
        sprite = request["sprites"][specs]
        if sprite is None:
            await ctx.send("Uhh... Doesn't exist.")
        else:
            await ctx.send(sprite)

    #get the typing of a pokemon

def setup(bot):
    bot.add_cog(PokedexCommands(bot))