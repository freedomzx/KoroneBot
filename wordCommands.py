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

def getRandomWord():
    # word = random.choice(wordsRequest)
    # word = word.decode("utf-8")
    # return str(word)

    url = "https://api.wordnik.com/v4/words.json/randomWord?hasDictionaryDef=true&maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1&minLength=4&maxLength=-1&api_key=" + wordnikAPIKey
    request = requests.get(url)
    request = request.json()
    return request["word"]

def getGuess(msgContent):
    guess = msgContent[6:len(msgContent)]
    return guess

def fillHMSpaces(word):
    toReturn = []
    for i in word:
        if i == " ":
            toReturn.append(" ")
        elif i == "-":
            toReturn.append("-")
        else:
            toReturn.append("_")
    return toReturn

class WordCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #defines a single word
    @commands.command(name="define", help=defineHelp, brief = defineHelpShort)
    async def define(self, ctx, arg1):
        definition = dictionary.meaning(arg1)
        message = ""
        if definition is None:
            await ctx.send("Hmm... Can't seem to find that word.  Did you misspell or give me too many words?")
        else:
            toSend = ""
            for i in definition:
                toSend += "***" + i + ":***  "
                for j in range(len(definition[i])):
                    toSend += definition[i][j] + ", "
                toSend = toSend[:-2]
                toSend += "\n"

            embedSend = discord.Embed(
                title="Definitions of: " + arg1,
                description=toSend
            )

            await ctx.send(embed=embedSend)
        #there was a bs4 error here, if it happens again go edit C:\Users\<me>\AppData\Local\Programs\Python\Python38-32\lib\site-packages\PyDictionary\utils.py

    #a game of hangman
    @commands.command(name="hangman", help = hangmanHelp, brief = hangmanHelpShort)
    async def hangman(self, ctx):
        await ctx.send("A new game of hangman is starting! To make a guess of a letter or the entire word, send \"guess <guess>\".")
        word = getRandomWord().lower()
        length = len(word)
        guessSpaces = fillHMSpaces(word)

        def hangmanCheck(message):
            if message.content.startswith("guess ") == False or len(message.content) <= 6:
                return False
            else:
                return True

        lives = 7
        print(word)

        while(True):
            toSend = "```" + hangmanLives[lives] + "\n"
            for i in guessSpaces:
                toSend += i + " "
            toSend += "```"
            await ctx.send(toSend)

            msg = await self.bot.wait_for("message", check = hangmanCheck)
            guess = getGuess(msg.content).lower()

            if guess == word:
                await ctx.send("You got it!  The word was: " + word + ".")
                break
            elif len(guess) == 1 and guess in word:
                await ctx.send("That's part of it!")
                #find all indices of the letter in word and replace it
                i = 0
                while i < len(word):
                    if word[i] == guess:
                        guessSpaces[i] = guess
                    i += 1
                #break if winning guess
                if "_" not in guessSpaces:
                    await ctx.send("You win!  The word was: " + word + ".")
                    break
            else:
                await ctx.send("Bad guess.")
                lives -= 1
            
            if lives == 0:
                await ctx.send("Game over!\n```" + hangmanLives[lives] + "```The word was: " + word + ".")
                break

    #get a word of the day
    @commands.command(name="wordoftheday", help = wordofthedayHelp, brief = wordofthedayHelpShort)
    async def wordoftheday(self, ctx):
        url = "https://api.wordnik.com/v4/words.json/wordOfTheDay?api_key=" + wordnikAPIKey
        request = requests.get(url)
        request = request.json()

        embedSend = discord.Embed(
            title="Today's word of the day"
        )
        embedSend.add_field(name="Word", value=request["word"], inline=False)
        embedSend.add_field(name="Definition", value=request["definitions"][0]["text"], inline=False)
        embedSend.add_field(name="Part of Speech", value=request["definitions"][0]["partOfSpeech"], inline=False)
        embedSend.add_field(name="Example of Usage", value=request["examples"][0]["text"], inline=False)

        await ctx.send(embed=embedSend)
    

def setup(bot):
    bot.add_cog(WordCommands(bot))