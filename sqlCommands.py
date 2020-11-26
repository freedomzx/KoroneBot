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

connection = create_db_connection(host, username, password, db)  

class SqlCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #for custom commands via sql

    #add a custom command to the DB
    @commands.command(name="addCommand")
    async def addCommand(self, ctx):
        #regualr check to see if channel and author matches up
        def check(message):
            return message.channel == ctx.message.channel and message.author == ctx.message.author
        #get title of command
        await ctx.send("What do you want the name of the command to be? (Don't include the ! prefix, and no spaces allowed.)")
        msg = await self.bot.wait_for('message', check=check)
        commandName = ""
        if " " not in msg.content:
            commandName = msg.content
        else:
            await ctx.send("Hey, I said no spaces!")
            return
        
        #get content of command
        await ctx.send("What do you want the contents of the command to be?  Mind the 2000 character limit.")
        msg = await self.bot.wait_for('message', check=check)
        #minding the character limit
        commandContents = ""
        if len(msg.content) <= (2000 - len(commandName)):
            commandContents = msg.content
        else:
            await ctx.send("Overall string is too big!  Try again with something smaller.")
            return

        #get current time
        x = datetime.datetime.now()
        year = x.strftime("%Y")
        month = x.strftime("%m")
        day = x.strftime("%d")
        fulltime = year + "-" + month + "-" + day

        toQuery = "INSERT INTO COMMANDS VALUES" + " ('" + commandName + "', '" + commandContents + "', '" + str(msg.author) + "', '" + fulltime + "');"
        cursor = execute_query(connection, toQuery)
        embedSend = discord.Embed(
            title="Command added if not already in existence.",
            description="To use the command, do \"!custom <commandName>\"."
        )
        await ctx.send(embed=embedSend)

    #browses the sql database and looks for a given custom command
    @commands.command(name="custom")
    async def custom(self, ctx, arg1):
        cursor = execute_query(connection, "select command_name from commands")
        commandNames = cursor.fetchall()
        toComp = "('" + str(arg1) + "',)"
        for x in commandNames:
            if toComp == str(x):
                toQuery = "select command_contents from commands where command_name = '" + str(arg1) + "'"
                cursor = execute_query(connection, toQuery)
                commandContent = cursor.fetchall()
                #print(str(commandContent[0])[2:-3])
                await ctx.send(str(commandContent[0])[2:-3])

def setup(bot):
    bot.add_cog(SqlCommands(bot))


    