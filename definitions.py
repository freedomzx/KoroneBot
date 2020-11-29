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
    16: "Yes.", 17: "No.", 18: "The answer will come to you.", 19: "What are you thinking?"
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

defineHelp = """
    To use this command, send: \"!help <single english word to define>\".  
    The bot will then either define the word, or tell you that it cannot find a definition for the given word.
"""
defineHelpShort = "\"!define <word\""

eightBallHelp = """
    To use this command, send: \"!eightBall <a question>\".
    The bot will then give you a random response to that question.
"""
eightBallHelpShort = "\"!eightBall <question>\""

hangmanHelp = """
    To use this command, send \"!hangman\".
    The bot will then start a game of hangman, giving the slots for a word and sending an ASCII picture of a hangman board.
    To guess a letter or the entire word, send \"guess <guess>\".
    The game will proceed until the man is dead or the word is found.  You have 7 lives!
"""
hangmanHelpShort = "\"!hangman\", \"guess <guess>\""

insultHelp = """
    To use this command, send \"!insult\".
    The bot will then send a GET request to https://evilinsult.com/generate_insult.php?lang=en&type=json and give a random insult from there.
""" 
insultHelpShort = "\"!insult\""

rollHelp = """
    To use this command, send \"!roll\".
    Then, the bot will ask what the high bound of the roll should be.
    The bot will then generate a random number from 1-n, n being the number given from the previous question.
"""
rollHelpShort = "\"!roll\", then sending a number."

stocksHelp = """
    To use this command, send \"!stocks\".
    The bot will then ask for the company's ticker, which you should then enter.
    The bot will then send stock information over the last 5 days for the given company.
"""
stocksHelpShort = "\"!stocks\", then send ticker."

translateHelp = """
    To use this command, send \"!translate\".
    The bot will then ask for a phrase to translate, which you should then enter.
    The bot will then ask for the language code for the target language, which can be found at https://sites.google.com/site/opti365/translate_code.
    The bot will then try to translate the phrase then send it.
"""
translateHelpShort = "\"!translate\", then enter phrase, then enter language code."

weatherHelp = """
    To use this command, send \"!weather\".
    The bot will then ask for the zipcode of the place you want the weather for, which you should then enter.
    The bot will then ask for the country code of the place you want the weather for, which can be found at https://countrycode.org/.
    The bot will then send a GET request to http://api.openweathermap.org/data/2.5/weather?zip=, with the endpoints being filled in based on the given information.
    The weather from that area, if found, will then be send.
"""
weatherHelpShort = "\"!weather\", then send zipcode, then send country code."

whoamiHelp = """
    To use this command, send \"!whoami\".
    The bot will then send you your discord account's join date for the current server, discord account creation date, user ID, and username discriminator (the 4 numbers after your username.)
"""
whoamiHelpShort = "\"!whoami\""

addcommandHelp = """
    To use this command, send \"!addcommand\".
    The bot will then ask for the title of your command, which you should then send.  (No spaces or the ! prefix).
    The bot will then ask for the contents of your command, which you should then send.  (Less then the discord character limit).
    The bot will then inform you that the command has been added, if the title is not already in use.
"""
addcommandHelpShort = "\"!addcommand\", send command title, then send command description."

customHelp = """
    To use this command, send \"!custom <custom command name>\".
    The bot will then check through the SQL database and see if the command exists, then sends the contents if it does exist.
"""
customHelpShort = "\"!custom <custom command name>\""

vtuberlivesHelp = """
    To use this command, send \"!vtuberLives\".
    The bot will then check which of the vtubers on its list are live, then sends all the live vtubers, organized by affiliation.
    The bot will then ask if you want the links to the streams, which you should then answer "yes" or "no" to.
"""
vtuberlivesHelpShort = "\"!vtuberlives\", then say \"yes\" or \"no\"."

channelinfoHelp = """
    To use this command, send \"!channelinfo <youtube channel id>\".
    The bot will then send the channel's title, description, publish date, sub count, view count, and video count, if found.
"""
channelinfoHelpShort = "\"!channelinfo <youtube channel id>\""

pokeabilityHelp = """
    To use this command, send \"!pokeability <ability name>\".
    The bot will then send a GET request the pokiapi ability endpoint and attempt to search for the given ability.
"""
pokeabilityHelpShort = "\"!pokeability <ability name>\""

pokeberryHelp = """
    To use this command, send \"!pokeberry <berry name>\".
    The bot will then send a GET request to the pokeapi berry endpoint.
    If found, a berry's growth time, max harvest number, natural gift power + type, size, smoothness, soil dryness, and firmness will be sent.
"""
pokeberryHelpShort = "\"!pokeberry <berry name>\""

pokedexHelp = """
    To use this command, send \"!pokedex <pokemon name>\".
    The bot will then send a GET request to the pokeapi pokemon endpoint.
    If found, a pokemon's abilities, types, sprite, flavor text, and held items will be returned.
"""
pokedexHelpShort = "\"!pokedex <pokemon nmame>\""

pokeitemHelp = """
    To use this command, send \"!pokeitem <item name>\".
    The bot will then send a GET request to the pokeapi item endpoint.
    If found, an item's effect, flavor text, and pokemon who hold the item will be returned.
"""
pokeitemHelpShort = "\"!pokeitem <item name>\""

pokelocationHelp = """
    To use this command, send \"!pokelocation <pokemon name>\".
    The bot will then send a GET request to the pokeapi location endpoint.
    A pokemon's location will be found and returned.
"""
pokelocationHelpShort = "\"!pokelocation <pokemon name>\""

pokemoveHelp = """
    To use this command, send \"!pokemove <move name>\".
    The bot will then send a GET request to the pokeapi moves endpoint.
    A pokemon's move flavor text, PP, damage class, accuracy, type, power, priority, and effect will be returned.
"""
pokemoveHelpShort = "\"!pokemove <move name>\""

pokenatureHelp = """
    To use this command, send \"!pokenature <nature name>\".
    The bot will then send a GET request to the pokeapi nature endpoint.
    A nature's increased/decreased stats and flavor likes/dislikes will be returned, as well as its description.
"""
pokenatureHelpShort = "\"!pokenature <nature name>\""

pokespriteHelp = """
    To use this command, send \"!pokesprite <pokemon name> <back or front> <default or shiny>\".
    The bot will then send a GET request to the pokeapi pokemon endpoint.
    A pokemon's sprite will be returned based on front/back and default/shiny.
"""
pokespriteHelpShort = "\"!pokesprite <pokemon name> <front/back> <default/shiny>\""

vtuberChannelIDs = {
    "Hololive JP: Gen 0/1": {
        "Tokino Sora": "UCp6993wxpyDPHUpavwDFqgg",
        "AZKi": "UC0TXe_LYZ4scaW2XMyi5_kw",
        "Roboco": "UCDqI2jOz0weumE8s7paEk6g",
        "Shirakami Fubuki": "UCdn5BQ06XqgXoAxIhbqw5Rg",
        "Sakura Miko": "UC-hM6YJuNYVAmUWxeIr9FeA",
        "Hoshimachi Suisei": "UC5CwaMl1eIgY8h02uZw7u8A",
        "Yozora Mel": "UCD8HOxPs4Xvsm8H0ZxXGiBw",
        "Natsuiro Matsuri": "UCQ0UDLQCjY0rmuxCDE38FGg",
        "Aki Rosenthal": "UCFTLzh12_nrtzqBPsTCqenA",
        "Akai Haato/Haachamachama": "UC1CfXB_kRs3C-zaeTG3oGyg"
    },

    "Hololive JP: Gen 2": {
        "Minato Aqua": "UC1opHUrw8rvnsadT-iGp7Cg",
        "Murasaki Shion": "UCXTpFs_3PqI41qX2d9tL2Rw",
        "Nakiri Ayame": "UC7fk0CB07ly8oSl0aqKkqFg",
        "Yuzuki Choco": "UC1suqwovbL1kzsoaZgFZLKg",
        "Oozora Subaru": "UCvzGlP9oQwU--Y0r9id_jnA"
    },

    "Hololive Gamers": {
        "Ookami Mio": "UCp-5t9SrOQwXMU7iIjQfARg",
        "Nekomata Okayu": "UCvaTdHTWBGv3MKj3KVqJVCw",
        "Inugami Korone": "UChAnqc_AY5_I3Px5dig3X1Q"
    },

    "Hololive JP: Gen 3": {
        "Usada Pekora": "UC1DCedRgGHBdm81E1llLhOQ",
        "Uruha Rushia": "UCl_gCybOJRIgOXw6Qb4qJzQ",
        "Shiranui Flare": "UCvInZx9h3jC2JzsIzoOebWg",
        "Shirogane Noel": "UCdyqAaZDKHXg4Ahi7VENThQ",
        "Houshou Marine": "UCCzUftO8KOVkV4wQG1vkUvg"
    },

    "Hololive JP: Gen 4": {
        "Amane Kanata": "UCZlDXzGoo7d44bwdNObFacg",
        "Kiryu Kazama Coco": "UCS9uQI-jC3DE0L4IpXyvr6w",
        "Tsunomaki Watame": "UCqm3BQLlJfvkTsX_hvm0UmA",
        "Tokoyami Towa": "UC1uv2Oq6kNxgATlCiez59hw",
        "Himemori Luna": "UCa9Y57gfeY0Zro_noHRVrnw"
    },

    "Hololive JP: Gen 5": {
        "Yukihana Lamy": "UCFKOVgVbGmX65RxO3EtH3iw",
        "Momosuzu Nene": "UCAWSyEs_Io8MtpY3m-zqILA",
        "Shishiro Botan": "UCUKD-uaobj9jiqB-VXt71mA",
        "Omaru Polka": "UCK9V2B22uJYu3N7eR_BT9QA"
    },

    "Hololive EN": {
        "Gawr Gura": "UCoSrY_IQQVpmIRZ9Xf-y93g",
        "Mori Calliope": "UCL_qhgtOy0dy1Agp8vkySQg",
        "Ninomae Ina'nis": "UCMwGHR0BTZuLsmjY_NT5Pwg",
        "Takanashi Kiara": "UCHsx4Hqa-1ORjQTh9TYDhww",
        "Amelia Watson": "UCyl1z3jo3XHR1riLFKG5UAg"
    },

    "Hololive ID": {
        "Airani Iofifteen": "UCAoy6rzhSf4ydcYjJw3WoVg",
        "Moona Hoshinova": "UCP0BspO_AMEe3aQqqpo89Dg",
        "Ayunda Risa": "UCOyYb1c43VlX9rc_lT6NKQw"
    },

    "VOMS Project": {
        "Amano Pikamee": "UCajhBT4nMrg3DLS-bLL2RCg",
        "Hikasa Tomoshika": "UC3vzVK_N_SUVKqbX69L_X4g",
        "Jitomi Monoe": "UCaFhsCKSSS821N-EcWmPkUQ"
    },

    "Other": {
        "Kizuna Ai (Main)": "UC4YaOt1yT-ZeyB0OmxHgolA",
        "Kizuna Ai (Games)": "UCbFwe3COkDrbNsbMyGNCsDg",
        "Inuyama Tamaki": "UC8NZiqKx6fsDT3AVcMiVFyA",
        "Artemis": "UCWImOidHDmm0KK20bkF-rSQ"
    }
}

r = RandomWords()
dictionary = PyDictionary()
translator = Translator()