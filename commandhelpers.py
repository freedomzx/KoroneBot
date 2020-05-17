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
            reset = 0
            word = r.get_random_word(hasDictionaryDef = "true")
            for char in word: #check if each letter is part of alphabet or space or -
                if not char.isalpha() and char != "-" and char != " ": 
                    reset = 1
                    break
            if reset == 1:
                print("non alphabetical non - non space letter, getting new word")
                continue
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



