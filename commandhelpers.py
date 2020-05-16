import discord
import random
import asyncio
import sys
import time
import yfinance
import json
import requests
from discord.ext import commands

import definitions
from definitions import *
from PyDictionary import PyDictionary
from random_word import RandomWords

def getRandomWord():
    word = ""
    while(True):
        try:
            word = r.get_random_word(hasDictionaryDef = "true")
            break
        except:
            print("Error in word retrieval, getting a new one")
            continue
    return word

def getGuess(msgContent):
    guess = msgContent[7:len(msgContent)]
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



