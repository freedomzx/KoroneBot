# Work with Python 3.6
import discord
import random
import asyncio
import sys
import time
import yfinance
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix="!")

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

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------------')
    statusText = discord.Game(name = "with code!")
    await client.change_presence(status = discord.Status.do_not_disturb, activity = statusText)
    print('set status as \"' + statusText.name + "\"\n------------------")

@client.event
async def on_message(message): #all commands triggered via message
    channel = message.channel
    messageStr = message.content

    if message.author == client.user:
        return

    #gives randomized responses after waiting for a string
    elif messageStr.startswith("!8ball"):
        await channel.send("What do you wanna know the answer to?")
        num = random.randint(1, 18)

        def check(m):
                if m.author != message.author:
                    print("not same ppl")
                    return False
                
                else:
                    return True

        msg = await client.wait_for('message', check=check)
        await channel.send(ballresponses[num])        

    #rolls a number from 1 to given range
    elif messageStr.startswith("!roll"):
        await channel.send("Please enter the cap for the roll range.")

        try:
            def check(m):
                if m.author != message.author:
                    print("not same ppl")
                    return False
                
                else:
                    return type(int(m.content)) is int and m.author != message.author

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

        msg = await client.wait_for('message', check=None)
        company = yfinance.Ticker(msg.content)
        dataframe = "```" + company.history(period="5d").to_string() + "```"

        if dataframe.startswith("```Empty DataFrame"):
            await channel.send("Cannot find ticker of " + msg.content)

        else: 
            await channel.send("Stock information over the last 5 days for: " + msg.content)
            await channel.send(dataframe)

    #simple text to text responses
    elif messageStr.startswith("!"):
        for x in simpleCommands:
            if x in messageStr.lower():
                toSend = simpleCommands[x]
                await channel.send(toSend)


client.run('NTY0NjU4OTc0MTgwMjQ1NTIy.XKrKfg.8LctWjJNiUvHRnkWYtAmKyeZ8mY')
