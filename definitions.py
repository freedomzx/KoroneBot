import discord
import random
import asyncio
import sys
import time
import yfinance
import json
import requests
from discord.ext import commands

import tokendef
from tokendef import *
import definitions
from definitions import *
from PyDictionary import PyDictionary
from random_word import RandomWords

simpleCommands = {
    "!test" : "Working!",
    "!whoami" : "A discord bot that does random stuff.  Created by: \nhttps://github.com/freedomzx",
    "!help" : "List of commands are available in the source code at \nhttps://github.com/freedomzx/Kokoro-Kode",
}

ballresponses = {
    1: "Uhh, maybe?", 2: "Definitely!", 3: "You probably don't want to know...", 4: "Not happening.",
    5: "Probably not.  Sorry.", 6: "It's likely!", 7: "100%!!!", 8: "Uhh, nope.  Sorry.",
    9: "Yep!", 10: "hell yea :joy: :ok_hand: :100:", 11: "Hmm... there's a chance?", 12: "I wouldn't count on it.", 
    13: "Of course!  Why are you even asking?!", 14: "I don't know about that one...", 15: "Wouldn't dream of it.",
    16: "Yes.", 17: "No.", 18: "The answer will come to you.", 
}

hangmanLives = {
    7: "```|----------\n|         \n|\n|\n|\n|```" 
}

r = RandomWords()