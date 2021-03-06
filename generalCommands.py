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

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #catch errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #catch insufficient arguments
        if isinstance(error, commands.CommandNotFound):
            return
            #ignore not found errors

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required arguments.  Check README for proper usage.")
            print("MissingRequiredArgument error in command {}".format(ctx.command))
            return

        elif isinstance(error, commands.TooManyArguments):
            await ctx.send("Too many arguments.  Check README for proper usage.")
            print("TooManyArguments error in command {}".format(ctx.command))
            return

        # elif isinstance(error, commands.CommandInvokeError):
        #     await ctx.send("Error in decoding the json.  Check your syntax.")
        #     print("JSONDecodeError in command {}".format(ctx.command))
        #     return

        #previous if/else didn't catch it, its a more obscure error.  print the traceback
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    #randomly responds to a question given a short list of answers
    @commands.command(name="eightBall", help = eightBallHelp, brief = eightBallHelpShort)
    async def eightBall(self, ctx, *args):
        if not args:
            await ctx.send("Hueh? Add a question after the command!")
        else:
            num = random.randint(1, 19)
            message = ""
            for i in args:
                message = message + i + " "

            embedSend = discord.Embed(
                title = message[:-1],
                description = ballresponses[num]
            )
            embedSend.set_thumbnail(url="https://magic-8ball.com/assets/images/magicBallStart.png")
            await ctx.send(embed=embedSend)

    #get insulted!
    @commands.command(name="insult", help = insultHelp, brief = insultHelpShort)
    async def insult(self, ctx):
        response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")
        hurtfulStuff = response.json()
        await ctx.send(hurtfulStuff["insult"])

    #roll a random # between 1 and a given cap
    @commands.command(name="roll", help = rollHelp, brief = rollHelpShort)
    async def roll(self, ctx):
        await ctx.send("Please enter the cap for the roll range.")
        try:
            def rollCheck(message):
                if message.author != ctx.message.author:
                    return False
                else:
                    return type(int(message.content)) is int and message.author == ctx.message.author

            msg = await self.bot.wait_for("message", check=rollCheck)
            #await ctx.send(str(random.randint(1, int(msg.content))))
            embedSend = discord.Embed(
                title = "Roll from 1 to " + msg.content,
                description = str(random.randint(1, int(msg.content)))
            )
            embedSend.set_thumbnail(url="https://gilkalai.files.wordpress.com/2017/09/dice.png")
            await ctx.send(embed=embedSend)
        except ValueError:
            await ctx.send("Invalid input.")

    #stock info over past 5 days for a company
    @commands.command(name="stocks", help = stocksHelp, brief = stocksHelpShort)
    async def stocks(self, ctx):
        #regular check, check consistency between author and channel
        def check(message):
            return message.channel == ctx.message.channel and message.author == ctx.message.author
        await ctx.send("Stocks for who?  Please enter the company's ticker.")

        msg = await self.bot.wait_for("message", check = check)
        company = yfinance.Ticker(msg.content)
        dataframe = company.history(period="5d").to_string()

        if dataframe.startswith("Empty DataFrame"):
            await ctx.send("Can't find the ticker of: " + msg.content + ".")
        else:
            embedSend = discord.Embed(
                title = "Stock information over the last 5 days for: " + msg.content
            )
            await ctx.send(embed=embedSend)
            await ctx.send("```" + dataframe + "```")

    #translate a sentence from english into a language
    @commands.command(name="translate", help = translateHelp, brief = translateHelpShort)
    async def translate(self, ctx):
        #regular check, check consistency between author and channel
        def check(message):
            return message.channel == ctx.message.channel and message.author == ctx.message.author
        await ctx.send("Please enter a word or a phrase.")

        msg = await self.bot.wait_for("message", check = check)
        sentence = msg.content
        #print(sentence)

        await ctx.send("Please enter the language code to translate to.  (consult https://sites.google.com/site/opti365/translate_codes).")
        msg = await self.bot.wait_for("message", check = check)
        language = msg.content
        #print(language)

        # try:
        translated = translator.translate(sentence, lang_tgt=language)
        toSend = ""

        # if only 1 def
        if isinstance(translated, str):
            toSend = translated
        # if multiple defs
        elif isinstance(translated, list):
            for i in range(len(translated)):
                toSend += translated[i]
                if i != len(translated) -1:
                    toSend += ', '

        embedSend = discord.Embed(
            title = "Translation of \"" + sentence + "\" to " + language,
            description = toSend
        )
        await ctx.send(embed=embedSend)
        # except AttributeError:
        #     await ctx.send("Hmm... Something didn't work.  Check your grammar, maybe?  This API fails without proper grammar for whatever reason.")

     #get the weather of a certain place
    @commands.command(name="weather", help = weatherHelp, brief = weatherHelpShort)
    async def weather(self, ctx):
        #regular check, check consistency between author and channel
        def check(message):
            return message.channel == ctx.message.channel and message.author == ctx.message.author
        await ctx.send("Please enter the zip code: ")

        msg = await self.bot.wait_for("message", check=check)
        zipcode = msg.content
        await ctx.send("Please enter the country code (check https://countrycode.org/ and use the 2-letter ISO code): ")
        msg = await self.bot.wait_for("message", check=check)
        countrycode = msg.content
        url = "http://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + "," + countrycode + "&appid=" + weatherapitoken
        response = requests.get(url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]
            tempK = y["temp"]
            tempF = tempK * (9/5) - 459.67
            tempC = tempK - 273.15
            pressure = y["pressure"]
            humidity = y["humidity"]
            z = x["weather"]
            weather = z[0]["description"]
            toSend = "Temperature: " + str(tempK) + "K/" + str(tempF) + "F/" + str(tempC) + "C\nPressure: " + str(pressure) + "\nHumidity: " + str(humidity) + "\nWeather: " + str(weather)
            embedSend = discord.Embed(
                title = "Weather in " + x["name"],
                description = toSend
            )
            await ctx.send(embed=embedSend)
        else:
            await ctx.send("Hmm... Couldn't find the specified location's weather.")

    @commands.command(name="whoami", help = whoamiHelp, brief = whoamiHelpShort)
    async def whoami(self, ctx):
        user = ctx.message.author

        embedSend = discord.Embed(
            title="About {user}".format(user = user.name)
        )
        embedSend.set_thumbnail(url=user.avatar_url)
        embedSend.add_field(name="Server Join Date", value=user.joined_at, inline=False)
        embedSend.add_field(name="Discord Account Creation Date", value=user.created_at, inline=False)
        embedSend.add_field(name="User ID", value=user.id, inline=False)
        embedSend.add_field(name="Username Discriminator", value=user.discriminator, inline=False)

        await ctx.send(embed=embedSend)

def setup(bot):
    bot.add_cog(GeneralCommands(bot))