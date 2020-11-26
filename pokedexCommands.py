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

    #get the typing info of a pokemon: their type and their weaknesses and strengths
    @commands.command(name="pokeability")
    async def pokeability(self, ctx, *args):
        abilityName = ""
        for i in range(len(args)):
            abilityName += args[i]
            if i != len(args)-1:
                abilityName += '-'
        print("Request received for: " + abilityName)
        
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

    #get the specific information abotu a berry
    @commands.command(name="pokeberry")
    async def pokeberry(self, ctx, arg1):
        berry = arg1.lower()

        url = start + "berry/" + berry
        request = requests.get(url)
        request = request.json()

        embedSend = discord.Embed(
            title = "Description of berry: " + berry
        )
        embedSend.add_field(name="Growth time", value = request["growth_time"], inline=False)
        embedSend.add_field(name="Max harvest", value = request["max_harvest"], inline=False)
        embedSend.add_field(name="Natural Gift power", value = request["natural_gift_power"], inline=False)
        embedSend.add_field(name="Natural Gift type", value = request["natural_gift_type"]["name"], inline=False)
        embedSend.add_field(name="Size", value = request["size"], inline=False)
        embedSend.add_field(name="Smoothness", value = request["smoothness"], inline=False)
        embedSend.add_field(name="Soil dryness", value = request["soil_dryness"], inline=False)
        embedSend.add_field(name="Firmness", value = request["firmness"]["name"], inline=False)

        flavorList = ""
        for i in range(len(request["flavors"])):
            flavorList += request["flavors"][i]["flavor"]["name"]
            if i != len(request["flavors"]) -1:
                flavorList += ", "
        embedSend.add_field(name="Flavors", value=flavorList, inline=False)

        url = start + "item/" + berry + "-berry"
        request = requests.get(url)
        request = request.json()
        embedSend.set_thumbnail(url=request["sprites"]["default"])

        await ctx.send(embed=embedSend)


    #general pokemon info: sprite, name, types, description, abilities
    @commands.command(name="pokedex")
    async def pokedex(self, ctx, arg1):
        pokemon = arg1.lower()
        url = start + "pokemon/" + pokemon
        request = requests.get(url)
        request = request.json()

        print("Request received for: " + pokemon)
        #get list of pkmn abilites
        abilities = ""
        for i in range(len(request["abilities"])):
            abilities += request["abilities"][i]["ability"]["name"]
            if i != len(request["abilities"]) - 1:
                abilities += ", "
        #get list of pkmn types
        types = ""
        for i in range(len(request["types"])):
            types += request["types"][i]["type"]["name"]
            if i != len(request["types"]) - 1:
                types += ", "
        #get sprite url
        sprite = request["sprites"]["front_default"]
        #get species flavor text from new request
        speciesURL = request["species"]["url"]
        speciesRequest = requests.get(speciesURL)
        speciesRequest = speciesRequest.json()
        speciesDesc = ""
        for i in range(len(speciesRequest["flavor_text_entries"])):
            if speciesRequest["flavor_text_entries"][i]["language"]["name"] == "en":
                speciesDesc += speciesRequest["flavor_text_entries"][i]["flavor_text"]
                break

        #print(abilities + "\n" + types + "\n" + sprite + "\n" + speciesDesc)
        embedSend = discord.Embed(
            title = "Pokedex entry for: " + arg1[0].upper() + arg1[1:],
        )
        embedSend.set_thumbnail(url=sprite)
        embedSend.add_field(name="Typing", value=types, inline=False)
        embedSend.add_field(name="Abilities", value=abilities, inline=False)
        embedSend.add_field(name="Description", value=speciesDesc.replace("\n", " ").replace(".", ". "), inline=False)
        await ctx.send(embed=embedSend)

    #get the info about an item
    @commands.command(name="pokeitem")
    async def pokeitem(self, ctx, *args):
        itemName = ""
        for i in range(len(args)):
            itemName += args[i]
            if i != len(args)-1:
                itemName += '-'

        print("Request received for: " + itemName)

        url = start + "item/" + itemName
        request = requests.get(url)
        request = request.json()

        embedSend = discord.Embed(
            title="Description of item: " + itemName.replace("-", " ")
        )
        #get item effect entries
        effectEntry = ""
        effectEntryShort = ""
        for i in range(len(request["effect_entries"])):
            if request["effect_entries"][i]["language"]["name"] == "en":
                effectEntry = request["effect_entries"][i]["effect"]
                effectEntryShort = request["effect_entries"][i]["short_effect"]
                break
        if len(effectEntry) != 0:
            embedSend.add_field(name="Effect",value=effectEntry.replace("\n", " "), inline=False)
        if len(effectEntryShort) != 0:
            embedSend.add_field(name="Effect (Short)", value=effectEntryShort.replace("\n", " "), inline=False)
        #get item flavor text
        flavorText = ""
        for i in range(len(request["flavor_text_entries"])):
            if request["flavor_text_entries"][i]["language"]["name"] == "en":
                flavorText = request["flavor_text_entries"][i]["text"]
                break
        if len(flavorText) != 0:
            embedSend.add_field(name="Flavor Text", value=flavorText.replace("\n", " "), inline=False)
        
        heldBy = ""
        for i in range(len(request["held_by_pokemon"])):
            heldBy += request["held_by_pokemon"][i]["pokemon"]["name"]
            if i != len(request["held_by_pokemon"])-1:
                heldBy += ", "
        if len(heldBy) != 0:
            embedSend.add_field(name="Held by", value=heldBy, inline=False)

        embedSend.set_thumbnail(url=request["sprites"]["default"])

        await ctx.send(embed=embedSend)

    #get the info about a move
    @commands.command(name="pokemove")
    async def pokemove(self, ctx, *args):
        moveName = ""
        for i in range(len(args)):
            moveName += args[i]
            if i != len(args)-1:
                moveName += '-'

        print("Request received for: " + moveName)

        url = start + "move/" + moveName
        request = requests.get(url)
        request = request.json()

        embedSend = discord.Embed(
            title = "Description of move: " + moveName.replace('-', " "),
        )
        #get most recent flavor text
        flavorText = ""
        mostRecent = 0
        for i in range(len(request["flavor_text_entries"])):
            if request["flavor_text_entries"][i]["language"]["name"] == "en":
                mostRecent = i

        flavorText = request["flavor_text_entries"][mostRecent]["flavor_text"].replace("\n", " ")
        embedSend.add_field(name="Flavor text", value=flavorText, inline=False)
        #get effect text
        effectText = ""
        shortEffectText = ""
        for i in range(len(request["effect_entries"])):
            if request["effect_entries"][i]["language"]["name"] == "en":
                effectText = request["effect_entries"][i]["effect"]
                shortEffectText = request["effect_entries"][i]["short_effect"]
                break
        embedSend.add_field(name="Effect Text (Short)", value=shortEffectText.replace("\n", " "), inline=False)
        embedSend.add_field(name="Effect Text", value=effectText.replace("\n", " "), inline=False)

        embedSend.add_field(name="Damage Class", value=request["damage_class"]["name"], inline=False)
        embedSend.add_field(name="Accuracy", value=request["accuracy"], inline=False)
        embedSend.add_field(name="Type", value=request["type"]["name"], inline=False)
        embedSend.add_field(name="Power", value=request["power"], inline=False)
        embedSend.add_field(name="PP", value=request["pp"], inline=False)
        embedSend.add_field(name="Priority", value=request["priority"], inline=False)

        await ctx.send(embed=embedSend)

    #get characteristics about a nature
    @commands.command(name="pokenature")
    async def pokenature(self, ctx, arg1):
        nature = arg1.lower()

        url = start + "nature/" + nature
        request = requests.get(url)
        request = request.json()

        print("Request received for: " + nature)

        embedSend = discord.Embed(
            title="Description of nature: " + nature
        )
        embedSend.add_field(name="Increased stat", value=request["increased_stat"]["name"], inline=False)
        embedSend.add_field(name="Decreased stat", value=request["decreased_stat"]["name"], inline=False)
        embedSend.add_field(name="Flavor preference", value=request["likes_flavor"]["name"], inline=False)
        embedSend.add_field(name="Flavor dislike", value=request["hates_flavor"]["name"], inline=False)

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

        print("Request received for: " + pokemon + " sprite")

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

def setup(bot):
    bot.add_cog(PokedexCommands(bot))