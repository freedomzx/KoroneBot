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

#dictionary of 8ball responses. didnt have to be a dictionary but hwatever
ballresponses = {
    1: "Uhh, maybe?", 2: "Definitely!", 3: "You probably don't want to know...", 4: "Not happening.",
    5: "Probably not.  Sorry.", 6: "It's likely!", 7: "100%!!!", 8: "Uhh, nope.  Sorry.",
    9: "Yep!", 10: "hell yea :joy: :ok_hand: :100:", 11: "Hmm... there's a chance?", 12: "I wouldn't count on it.", 
    13: "Of course!  Why are you even asking?!", 14: "I don't know about that one...", 15: "Wouldn't dream of it.",
    16: "Yes.", 17: "No.", 18: "The answer will come to you.", 19: "What are you thinking?"
}

#dictionary of ascii pictures for hangman lives
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

#list of discord statuses for the bot to change to every 30 seconds
activityList = [
    discord.Game(name="not yandere sim!"), discord.Activity(type=discord.ActivityType.listening, name="some weeb tunes!"),
    discord.Activity(type=discord.ActivityType.watching, name="some degenerate stuff!"), discord.Game(name="the system!"),
    discord.Game(name="Mogeko Castle!"), discord.Activity(type=discord.ActivityType.watching, name="Yakuza Shenanigans!"),
    discord.Activity(type=discord.ActivityType.listening, name="Baka Mitai!"), discord.Activity(type=discord.ActivityType.listening, name="Polkadot Stingray!"),
    discord.Game(name="Yakuza 0!"), discord.Game(name="Fire Emblem: Three Houses!"), discord.Game(name="Fighting Games!"), discord.Game("Half-Life 3!"),
]

#dictioanry of dictionaries containing vtuber channel IDs
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