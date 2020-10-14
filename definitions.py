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

commandsList = "```!test, !whoami, !hangman, !weather, !stocks, !wordoftheday, !8ball, !roll, !rtd```"

simpleCommands = {
    "!test" : "Working!",
    "!whoami" : "A discord bot that does random stuff.  Created by: \nhttps://github.com/freedomzx",
    "!help" : commandsList,
    "!shutup" : "https://cdn.discordapp.com/attachments/622612389522702347/737068592423632937/20200726_112711.jpg",
}

ballresponses = {
    1: "Uhh, maybe?", 2: "Definitely!", 3: "You probably don't want to know...", 4: "Not happening.",
    5: "Probably not.  Sorry.", 6: "It's likely!", 7: "100%!!!", 8: "Uhh, nope.  Sorry.",
    9: "Yep!", 10: "hell yea :joy: :ok_hand: :100:", 11: "Hmm... there's a chance?", 12: "I wouldn't count on it.", 
    13: "Of course!  Why are you even asking?!", 14: "I don't know about that one...", 15: "Wouldn't dream of it.",
    16: "Yes.", 17: "No.", 18: "The answer will come to you.", 
}

hangmanLives = {
    7: "```|---------\n|\n|\n|\n|\n|```",
    6: "```|---------\n|        |\n|\n|\n|\n|```",
    5: "```|---------\n|        |\n|        O\n|\n|\n|```",
    4: "```|---------\n|        |\n|        O\n|        |\n|\n|```",
    3: "```|---------\n|        |\n|        O\n|      / |\n|\n|```",
    2: "```|---------\n|        |\n|        O\n|      / | \\\n|\n|```",
    1: "```|---------\n|        |\n|        O\n|      / | \\\n|       /\n|```",
    0: "```|---------\n|        |\n|        O\n|      / | \\\n|       / \\\n|```",
}

r = RandomWords()
dictionary = PyDictionary()