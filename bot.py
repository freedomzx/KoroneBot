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
import commandhelpers
from commandhelpers import *

from PyDictionary import PyDictionary
from random_word import RandomWords
from googletrans import Translator

client = discord.Client()
bot = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------------')
    statusText = discord.Game(name = "not yandere sim!")
    await client.change_presence(status = discord.Status.do_not_disturb, activity = statusText)
    print('set status as \"' + statusText.name + "\"\n------------------")

@client.event
async def on_message(message): #all commands triggered via message
    channel = message.channel
    messageStr = message.content
    hangmanOngoing = 0

    def basicCheck(m):
        if m.author != message.author:
            return False
        else:
            return True

    if message.author == client.user:
        return

    #gives randomized responses after waiting for a string
    elif messageStr.startswith("!8ball"):
        await channel.send("What do you wanna know the answer to?")
        num = random.randint(1, 18)
        msg = await client.wait_for('message', check=basicCheck)
        await channel.send(ballresponses[num])

    #define word, say if can't
    elif messageStr.startswith("!define"):
        toDefine = messageStr[8:len(messageStr)]
        definition = dictionary.meaning(toDefine)
        if definition is None:
            await channel.send("Hmm... Can't seem to find that word.")
        else:
            await channel.send(definition)

    #starts hangman
    elif messageStr.startswith("!hangman") and hangmanOngoing == 0:
        hangmanOngoing = 1
        await channel.send("Alright, new hangman game!  Say !guess <guess> to guess a letter or the entire word.  The word will be in all lowercase.  Please wait for the game to appear... (might take a little, the random words module isn't the best)")
        word = commandhelpers.getRandomWord().lower()
        length = len(word)
        guessSpaces = fillHMSpaces(word)

        def hangmanCheck(m):
            if m.content.startswith("!guess ") == False or len(m.content) <= 7:
                return False
            else: 
                return True

        lives = 7
        print(word)
        print(guessSpaces)

        #actual game 
        while(True):
            await channel.send(hangmanLives[lives])
            toSendSpaces = "```"
            for i in guessSpaces:
                toSendSpaces = toSendSpaces + i + " "
            toSendSpaces = toSendSpaces + "```"
            await channel.send(toSendSpaces)

            msg = await client.wait_for("message", check=hangmanCheck)
            guess = getGuess(msg.content).lower()

            if guess == word:
                await channel.send("You got it!  The word was: " + word + ".")
                hangmanOngoing = 0
                break
            elif len(guess) == 1 and guess in word:
                await channel.send("That's part of it!")
                #find all indices that the letter is in the word and replace it
                i = 0
                while i < len(word):
                    if word[i] == guess:
                        guessSpaces[i] = guess
                    i += 1
                #break if winning guess
                if "_" not in guessSpaces:
                    await channel.send("You win! The word was: " + word)
                    break

            else:
                await channel.send("Bad guess.\n")
                lives-=1
            #game over
            if lives == 0:
                await channel.send("Game over!\n" + hangmanLives[lives] + "The word was: " + word)
                break

    #fetches random word and its definition
    elif messageStr.startswith("!randomword"):
        word = commandhelpers.getRandomWord().lower()
        toSend = word## + ": " + json.dictionary.meaning(word)
        await channel.send(toSend)

    #rolls a number from 1 to given range
    elif messageStr.startswith("!roll"):
        await channel.send("Please enter the cap for the roll range.")
        try:
            def check(m):
                if m.author != message.author:
                    return False
                else:
                    return type(int(m.content)) is int and m.author == message.author
            msg = await client.wait_for('message', check=check)
            await channel.send(str(random.randint(1, int(msg.content))))
        except ValueError:
            await channel.send("Invalid input.")
        
    #rolls a number from 1-6
    elif messageStr.startswith("!rtd"):
        toSend = ":game_die: " + str(random.randint(1, 6)) + " :game_die:"
        await channel.send(toSend)

    #gets stcoks for thing
    elif messageStr.startswith("!stocks"):
        await channel.send("Stocks for who?  Please enter ticker symbol of company.")

        msg = await client.wait_for('message', check=basicCheck)
        company = yfinance.Ticker(msg.content)
        dataframe = "```" + company.history(period="5d").to_string() + "```"

        if dataframe.startswith("```Empty DataFrame"):
            await channel.send("Cannot find ticker of " + msg.content)
        else: 
            await channel.send("Stock information over the last 5 days for: " + msg.content)
            await channel.send(dataframe)

    #translate into a language!
    elif messageStr.startswith("!translate"):
        await channel.send("Please enter a sentence.")

        msg = await client.wait_for('message', check=basicCheck)
        sentence = msg.content

        await channel.send("Please enter the language code to translate to.  (consult https://sites.google.com/site/opti365/translate_codes)")
        msg = await client.wait_for('message', check=basicCheck)
        language = msg.content


        translated = translator.translate(sentence, dest=language)
        toSend = translated.text
        print(toSend)
        await channel.send(toSend)


    #get weather of a city/town using openweather api
    elif messageStr.startswith("!weather"):
        await channel.send("Please enter the zip code: ")

        msg = await client.wait_for('message', check=basicCheck)
        zipcode = msg.content
        await channel.send("Please enter the country code (check https://countrycode.org/ and use the 2-letter ISO code): ")
        msg = await client.wait_for("message", check=basicCheck)
        countrycode = msg.content
        url = "http://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + "," + countrycode + "&appid=" + weatherapitoken
        response = requests.get(url)
        x = response.json()

        if x["cod"] != "404":
            y = x["main"]
            tempK = y["temp"]
            tempF = tempK * (9/5) - 459.67
            tempC = tempK - 273.15
            pressure = y["pressure"]
            humidity = y["humidity"]
            z = x["weather"]
            weather = z[0]["description"]
            toSend = "```Weather in " + x["name"] + ":\nTemperature: " + str(tempK) + "K/" + str(tempF) + "F/" + str(tempC) + "C\nPressure: " + str(pressure) + "\nHumidity: " + str(humidity) + "\nWeather: " + str(weather) + "```"
            await channel.send(toSend)
        else:
            await channel.send("Cannot find " + zipcode + ", " + countrycode)

    # elif messageStr.startswith("!wordoftheday"): api is broken
    #     ##wordDic = json.loads(r.word_of_the_day().replace("definations", "definitions"))
    #     toSend = "Today's word of the day:\n```" + wordDic["word"] + ":\n"
    #     for i in wordDic["definitions"]:
    #         toSend = toSend + i["partOfSpeech"] + ": " + i["text"] + "\n"
    #     toSend = toSend + "```"
    #     await channel.send(toSend)

    #simple text to text responses
    elif messageStr.startswith("!"):
        for x in simpleCommands:
            if x in messageStr.lower():
                toSend = simpleCommands[x]
                await channel.send(toSend)
                break

client.run(token) #token is hidden from public repository