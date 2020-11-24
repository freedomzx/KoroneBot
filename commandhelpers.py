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

import mysql.connector
from mysql.connector import Error
import pandas as pd

#for hangman
# def getRandomWord():
#     word = ""
#     while(True):
#         try:
#             reset = 0
#             word = r.get_random_word(hasDictionaryDef = "true")
#             for char in word: #check if each letter is part of alphabet or space or -
#                 if not char.isalpha() and char != "-" and char != " ": 
#                     reset = 1
#                     break
#             if reset == 1:
#                 print("non alphabetical non - non space letter, getting new word")
#                 continue
#             break
#         except:
#             print("Error in word retrieval, getting a new one")
#             continue
#     return word
def getRandomWord():
    word = random.choice(wordsRequest)
    word = word.decode("utf-8")
    return str(word)
    

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

#for custom commands via sql
#connect to server
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#connect to specific db in server
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#regular query function, but print statements are specifically for db creation
def create_database(connection, query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}''")

    return cursor

#execute regular query function
def execute_query(connection, query):
    cursor = connection.cursor(buffered=True)
    try:
        cursor.execute(query)
        connection.commit()
        print(f"Query '{query}' successful")
    except Error as err:
        print(f"Error: '{err}'")

    return cursor


