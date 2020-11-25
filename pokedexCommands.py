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

    #general pokemon info: sprite, name, types, description, abilities
    @commands.command(name="pokedex")
    async def pokedex(self, ctx, arg1):
        pokemon = arg1.lower()
        url = start + "pokemon/" + pokemon
        request = requests.get(url)
        request = request.json()

        abilities = ""
        for i in range(len(request["abilities"])):
            abilities += request["abilities"][i]["ability"]["name"]
            if i != len(request["abilities"]) - 1:
                abilities += ", "

        types = ""
        for i in range(len(request["types"])):
            types += request["types"][i]["type"]["name"]
            if i != len(request["types"]) - 1:
                types += ", "

        sprite = request["sprites"]["front_default"]

        speciesURL = request["species"]["url"]
        speciesRequest = requests.get(speciesURL)
        speciesRequest = speciesRequest.json()
        speciesDesc = ""
        for i in range(len(speciesRequest["flavor_text_entries"])):
            if speciesRequest["flavor_text_entries"][i]["language"]["name"] == "en":
                speciesDesc += speciesRequest["flavor_text_entries"][i]["flavor_text"].replace("\n", " ").replace(".", ". ")
                break

        #print(abilities + "\n" + types + "\n" + sprite + "\n" + speciesDesc)
        embedSend = discord.Embed(
            title = "Pokedex entry for: " + arg1[0].upper() + arg1[1:],
        )
        embedSend.set_thumbnail(url=sprite)
        embedSend.add_field(name="Typing", value=types, inline=False)
        embedSend.add_field(name="Abilities", value=abilities, inline=False)
        embedSend.add_field(name="Description", value=speciesDesc, inline=False)
        await ctx.send(embed=embedSend)

    #get the back/front sprite for a pokemon
    @commands.command(name="pokesprite")
    async def pokesprite(self, ctx, arg1, arg2, arg3):
        pokemon = arg1.lower()
        position = arg2.lower()
        color = arg3.lower()

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

    #get the typing info of a pokemon: their type and their weaknesses and strengths
    @commands.command(name="pokeability")
    async def pokeability(self, ctx, *args):
        abilityName = ""
        for i in range(len(args)):
            abilityName += args[i]
            if i != len(args)-1:
                abilityName += '-'
        
        url = start + "ability/" + abilityName
        request = requests.get(url)
        request = request.json()

        abilityDesc = ""
        abilityDescShort = ""
        for i in range(len(request["effect_entries"])):
            if request["effect_entries"][i]["language"]["name"] == "en":
                abilityDesc += request["effect_entries"][i]["effect"]
                abilityDescShort += request["effect_entries"][i]["short_effect"]
                break

        embedSend = discord.Embed(
            title = "Ability description of: " + abilityName.replace('-', " ")
        )
        embedSend.add_field(name="Short Description", value=abilityDescShort, inline=False)
        embedSend.add_field(name="Description", value=abilityDesc, inline=False)
        await ctx.send(embed=embedSend)

    #get the info about a move
    @commands.command(name="pokemove")
    async def pokemove(self, ctx, *args):
        moveName = ""
        for i in range(len(args)):
            moveName += args[i]
            if i != len(args)-1:
                moveName += '-'

        url = start + "move/" + moveName
        request = requests.get(url)
        request = request.json()

        embedSend = discord.Embed(
            title = "Description of move: " + moveName.replace('-', " "),
        )
        flavorText = ""
        mostRecent = 0
        for i in range(len(request["flavor_text_entries"])):
            if request["flavor_text_entries"][i]["language"]["name"] == "en":
                mostRecent = i

        flavorText = request["flavor_text_entries"][mostRecent]["flavor_text"].replace("\n", " ")
        embedSend.add_field(name="Flavor text", value=flavorText, inline=False)

        effectText = ""
        shortEffectText = ""
        for i in range(len(request["effect_entries"])):
            if request["effect_entries"][i]["language"]["name"] == "en":
                effectText = request["effect_entries"][i]["effect"]
                shortEffectText = request["effect_entries"][i]["short_effect"]
                break
        embedSend.add_field(name="Effect Text (Short)", value=shortEffectText, inline=False)
        embedSend.add_field(name="Effect Text", value=effectText, inline=False)
        
        embedSend.add_field(name="Damage Class", value=request["damage_class"]["name"], inline=False)
        embedSend.add_field(name="Accuracy", value=request["accuracy"], inline=False)
        embedSend.add_field(name="Type", value=request["type"]["name"], inline=False)
        embedSend.add_field(name="Power", value=request["power"], inline=False)
        embedSend.add_field(name="PP", value=request["pp"], inline=False)
        embedSend.add_field(name="Priority", value=request["priority"], inline=False)

        await ctx.send(embed=embedSend)

def setup(bot):
    bot.add_cog(PokedexCommands(bot))