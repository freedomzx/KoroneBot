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
from googletrans import Translator

import mysql.connector
from mysql.connector import Error
import pandas as pd

#for custom commands via sql
#connect to server
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#connect to specific db in server
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#regular query function, but print statements are specifically for db creation
def create_database(connection, query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}''")

    return cursor

#execute regular query function
def execute_query(connection, query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        connection.commit()
        print(f"Query '{query}' successful")
    except Error as err:
        print(f"Error: '{err}'")

    return cursor
#create and keep open a mysql connection
connection = create_db_connection(host, username, password, db)  

#sqlcommands class cog
class SqlCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    #for custom commands via sql

    #add a custom command to the DB
    @commands.command(name="addCommand", help = addcommandHelp, brief = addcommandHelpShort)
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
    @commands.command(name="custom", help = customHelp, brief = customHelpShort)
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
                return
        await ctx.send("Couldn't find that command.")

    #get commands whose contents contain something
    @commands.command(name="customContains", help = customContainsHelp, brief = customContainsHelpShort)
    async def customContains(self, ctx, arg1):
        query = "select * from commands where command_contents like '%{commandCont}%'".format(commandCont = arg1)
        cursor = execute_query(connection, query)
        commandNames = cursor.fetchall()
        toSend = ""
        print(commandNames)
        for i in range(len(commandNames)):
            toSend += commandNames[i][0]
            if i != len(commandNames) -1:
                toSend += ", "
        embedSend = discord.Embed(
            title="Custom Commands That That Contain: {thing}".format(thing = arg1),
            description=toSend
        )
        await ctx.send(embed=embedSend)

    #gives a list of commands whose command name end with a letter or a string
    @commands.command(name="customEndsWith", help = customEndsWithHelp, brief = customEndsWithHelpShort)
    async def customEndsWith(self, ctx, arg1):
        query = "select command_name from commands where command_name like '%{commandName}'".format(commandName = arg1)
        cursor = execute_query(connection, query)
        commandNames = cursor.fetchall()
        toSend = ""
        for i in range(len(commandNames)):
            toSend += commandNames[i][0]
            if i != len(commandNames) -1:
                toSend += ", "
        embedSend = discord.Embed(
            title="Custom Commands That End With: {thing}".format(thing = arg1),
            description=toSend
        )
        await ctx.send(embed=embedSend)

    #gives misc info of a command (author, creation date)
    @commands.command(name="custominfo", help = customInfoHelp, brief = customInfoHelpShort)
    async def customInfo(self, ctx, arg1):
        query = "select command_creator, creation_date from commands where command_name = \'{commandName}\'".format(commandName = arg1)
        try:
            cursor = execute_query(connection, query)
            commandInfo = cursor.fetchall()
            publisher = commandInfo[0][0]
            dateCreated = commandInfo[0][1].strftime("%m/%d/%Y")
            
            embedSend = discord.Embed(
                title="Information on custom command: !" + arg1
            )
            embedSend.add_field(name="Command Creator", value=publisher, inline=False)
            embedSend.add_field(name="Creation Date", value=dateCreated, inline=False)

            await ctx.send(embed=embedSend)
        except IndexError:
            await ctx.send("Couldn't find that command.")

    #gives a list of all the custom commands
    @commands.command(name="customList", help=customListHelp, brief = customListHelpShort)
    async def customList(self, ctx):
        cursor = execute_query(connection, "select command_name from commands")
        commandNames = cursor.fetchall()
        toSend = ""
        for i in range(len(commandNames)):
            toSend += commandNames[i][0]
            if i != len(commandNames) - 1:
                toSend += ", "
        embedSend = discord.Embed(
            title="Custom Commands List",
            description = toSend
        )
        await ctx.send(embed=embedSend)

    #gives a list of commands whose command name contain a letter or a string
    @commands.command(name="customNameContains", help = customNameContainsHelp, brief = customNameContainsHelpShort)
    async def customNameContains(self, ctx, arg1):
        query = "select command_name from commands where command_name like '%{commandName}%'".format(commandName = arg1)
        cursor = execute_query(connection, query)
        commandNames = cursor.fetchall()
        toSend = ""
        for i in range(len(commandNames)):
            toSend += commandNames[i][0]
            if i != len(commandNames) -1:
                toSend += ", "
        embedSend = discord.Embed(
            title="Custom Commands That Contain: {thing}".format(thing = arg1),
            description=toSend
        )
        await ctx.send(embed=embedSend)

    #gives a list of the custom commands whose command name start with a certain letter
    @commands.command(name="customStartsWith")
    async def customStartsWith(self, ctx, arg1):
        query = "select command_name from commands where command_name like '{commandName}%'".format(commandName = arg1)
        cursor = execute_query(connection, query)
        commandNames = cursor.fetchall()
        toSend = ""
        for i in range(len(commandNames)):
            toSend += commandNames[i][0]
            if i != len(commandNames) -1:
                toSend += ", "
        embedSend = discord.Embed(
            title="Custom Commands That Start With: {thing}".format(thing = arg1),
            description=toSend
        )
        await ctx.send(embed=embedSend)

def setup(bot):
    bot.add_cog(SqlCommands(bot))


    