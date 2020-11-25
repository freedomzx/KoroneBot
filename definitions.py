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

import definitions
from definitions import *
from PyDictionary import PyDictionary
from random_word import RandomWords
from googletrans import Translator
from bs4 import BeautifulSoup

wordsURL = "https://www.mit.edu/~ecprice/wordlist.10000"
wordsRequest = requests.get(wordsURL).content.splitlines()

ballresponses = {
    1: "Uhh, maybe?", 2: "Definitely!", 3: "You probably don't want to know...", 4: "Not happening.",
    5: "Probably not.  Sorry.", 6: "It's likely!", 7: "100%!!!", 8: "Uhh, nope.  Sorry.",
    9: "Yep!", 10: "hell yea :joy: :ok_hand: :100:", 11: "Hmm... there's a chance?", 12: "I wouldn't count on it.", 
    13: "Of course!  Why are you even asking?!", 14: "I don't know about that one...", 15: "Wouldn't dream of it.",
    16: "Yes.", 17: "No.", 18: "The answer will come to you.", 
}

hangmanLives = {
    7: "|---------\n|\n|\n|\n|\n|",
    6: "|---------\n|        |\n|\n|\n|\n|",
    5: "|---------\n|        |\n|        O\n|\n|\n|",
    4: "|---------\n|        |\n|        O\n|        |\n|\n|",
    3: "|---------\n|        |\n|        O\n|      / |\n|\n|",
    2: "|---------\n|        |\n|        O\n|      / | \\\n|\n|",
    1: "|---------\n|        |\n|        O\n|      / | \\\n|       /\n|",
    0: "|---------\n|        |\n|        O\n|      / | \\\n|       / \\\n|",
}

# pokemonTypePics = {
#     "normal": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Normal_Type_Icon.svg",
#     "fire": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Fire_Type_Icon.svg",
#     "water": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Water_Type_Icon.svg",
#     "fighting": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Fighting_Type_Icon.svg",
#     "flying": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Flying_Type_Icon.svg",
#     "grass": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Grass_Type_Icon.svg",
#     "poison": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Poison_Type_Icon.svg",
#     "electric": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Electric_Type_Icon.svg",
#     "ground": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Ground_Type_Icon.svg",
#     "psychic": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Psychic_Type_Icon.svg",
#     "rock": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Rock_Type_Icon.svg",
#     "ice": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Ice_Type_Icon.svg",
#     "bug": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Bug_Type_Icon.svg",
#     "dragon": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Dragon_Type_Icon.svg",
#     "ghost": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Ghost_Type_Icon.svg",
#     "dark": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Dark_Type_Icon.svg",
#     "steel": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Steel_Type_Icon.svg",
#     "fairy": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Fairy_Type_Icon.svg"
# }

r = RandomWords()
dictionary = PyDictionary()
translator = Translator()