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

vtuberChannelIDs = {
    "Tokino Sora": "UCp6993wxpyDPHUpavwDFqgg",
    "AZKi": "UC0TXe_LYZ4scaW2XMyi5_kw",
    "Roboco": "UCDqI2jOz0weumE8s7paEk6g",
    "Shirakami Fubuki": "UCdn5BQ06XqgXoAxIhbqw5Rg",
    "Sakura Miko": "UC-hM6YJuNYVAmUWxeIr9FeA",
    "Hoshimachi Suisei": "UC5CwaMl1eIgY8h02uZw7u8A",
    "Yozora Mel": "UCD8HOxPs4Xvsm8H0ZxXGiBw",
    "Natsuiro Matsuri": "UCQ0UDLQCjY0rmuxCDE38FGg",
    "Aki Rosenthal": "UCFTLzh12_nrtzqBPsTCqenA",
    "Akai Haato/Haachamachama": "UC1CfXB_kRs3C-zaeTG3oGyg",
    "Minato Aqua": "UC1opHUrw8rvnsadT-iGp7Cg",
    "Murasaki Shion": "UCXTpFs_3PqI41qX2d9tL2Rw",
    "Nakiri Ayame": "UC7fk0CB07ly8oSl0aqKkqFg",
    "Yuzuki Choco": "UC1suqwovbL1kzsoaZgFZLKg",
    "Oozora Subaru": "UCvzGlP9oQwU--Y0r9id_jnA",
    "Ookami Mio": "UCp-5t9SrOQwXMU7iIjQfARg",
    "Nekomata Okayu": "UCvaTdHTWBGv3MKj3KVqJVCw",
    "Inugami Korone": "UChAnqc_AY5_I3Px5dig3X1Q",
    "Usada Pekora": "UC1DCedRgGHBdm81E1llLhOQ",
    "Uruha Rushia": "UCl_gCybOJRIgOXw6Qb4qJzQ",
    "Shiranui Flare": "UCvInZx9h3jC2JzsIzoOebWg",
    "Shirogane Noel": "UCdyqAaZDKHXg4Ahi7VENThQ",
    "Houshou Marine": "UCCzUftO8KOVkV4wQG1vkUvg",
    "Amane Kanata": "UCZlDXzGoo7d44bwdNObFacg",
    "Kiryu Kazama Coco": "UCS9uQI-jC3DE0L4IpXyvr6w",
    "Tsunomaki Watame": "UCqm3BQLlJfvkTsX_hvm0UmA",
    "Tokoyami Towa": "UC1uv2Oq6kNxgATlCiez59hw",
    "Himemori Luna": "UCa9Y57gfeY0Zro_noHRVrnw",
    "Yukihana Lamy": "UCFKOVgVbGmX65RxO3EtH3iw",
    "Momosuzu Nene": "UCAWSyEs_Io8MtpY3m-zqILA",
    "Shishiro Botan": "UCUKD-uaobj9jiqB-VXt71mA",
    "Omaru Polka": "UCK9V2B22uJYu3N7eR_BT9QA",
    "Gawr Gura": "UCoSrY_IQQVpmIRZ9Xf-y93g",
    "Mori Calliope": "UCL_qhgtOy0dy1Agp8vkySQg",
    "Ninomae Ina'nis": "UCMwGHR0BTZuLsmjY_NT5Pwg",
    "Takanashi Kiara": "UCHsx4Hqa-1ORjQTh9TYDhww",
    "Amelia Watson": "UCyl1z3jo3XHR1riLFKG5UAg",
    "Artemis": "UCWImOidHDmm0KK20bkF-rSQ",
    "Airani Iofifteen": "UCAoy6rzhSf4ydcYjJw3WoVg",
    "Moona Hoshinova": "UCP0BspO_AMEe3aQqqpo89Dg",
    "Ayunda Risa": "UCOyYb1c43VlX9rc_lT6NKQw",
    "Amano Pikamee": "UCajhBT4nMrg3DLS-bLL2RCg",
    "Hikasa Tomoshika": "UC3vzVK_N_SUVKqbX69L_X4g",
    "Jitomi Monoe": "UCaFhsCKSSS821N-EcWmPkUQ"
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