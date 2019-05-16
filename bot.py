# Work with Python 3.6
import discord
import random
import asyncio
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------------')
    await client.change_presence(game=discord.Game(name='smiling :)'))

@client.event
async def on_message_delete(message):
    if message.author == client.user:
        await client.send_message(message.channel, "Why are you deleting my messages :(")
    else:
        await client.send_message(message.channel, "A message got deleted!  Here are its contents: \n" + message.content)


@client.event
async def on_message_edit(before, after):
    if before.author == client.user:
        return
    else:
        msg = "A message by " + str(before.author) + " has been edited. \nBefore: *" + before.content + "*\nAfter: *" + after.content + "*"
        await client.send_message(before.channel, msg)


@client.event
async def on_member_join(member):
    await client.send_message(member.server.default_channel, "Welcome, " + member.mention)


@client.event
async def on_message(message): #all commands
    simplecommands = {
        "!test": "Yep",
        "!ben": "goddamn ape",
        "!botinfo": "It's me, " + client.user.mention + "!\n" + str(client.user.id) + "\n" + str(client.user.discriminator),
        "!channelid": str(message.channel.id),
        "!connectioninfo": str(client.ws),
        "!elijah": "yurilord gigachad",
        "!hello": "Hi " + message.author.mention + "! How are you?",
        "!help": "```***COMMANDS***\n!hello\n!hi\n!kokoro\n!repeat\n!botinfo\n!selfie\n!connectioninfo\n!channelid\n!dm\n!roll\n!8ball\n!flip```",
        "!hi": "Hi " + message.author.mention + "! How are you?",
        "!kokoro": "That's me!",
        "!pregnant": "That's not true, look! https://i.ytimg.com/vi/psKUh0M4cW4/maxresdefault.jpg See?",
        "!roll": ":game_die: " + str(random.randint(1,6)) + " :game_die:",
        "!selfie": client.user.avatar_url
    }

    regularwords = {
        "owo": "owo what's this?",
       # "kokoro": "I heard my name?",
    }

    if message.author == client.user:
        return

    elif message.content.startswith("!8ball"):
        x = random.randint(1,10)
        ballresponses = {
            1: "Uhh, maybe?",
            2: "Definitely!",
            3: "You probably don't want to know...",
            4: "Not happening.",
            5: "Probably not.  Sorry.",
            6: "It's likely!",
            7: "100%!!!",
            8: "Uhh, nope.  Sorry.",
            9: "Yep!",
            10: "hell yea :joy: :ok_hand: :100:"
        }
        if len(message.content) > 7:
            await client.send_message(message.channel, ballresponses[x])
        else:
            await client.send_message(message.channel, "Huh? You didn't ask anything...")

    elif message.content.startswith("!dm"):
        await client.send_message(message.author, "Hey, " + message.author.name + ". Fuck you.")
        await client.send_message(message.author, "Also, look at this: https://www.youtube.com/watch?v=dzMq5_thk4o")

    elif message.content.startswith("!flip"):
        x = random.randint(1,2)
        if x == 1:
            await client.send_message(message.channel, "Heads")
        else:
            await client.send_message(message.channel, "Tails")

    elif message.content.startswith("!repeat"):
        try:
            x = message.content.index("pregnant")
            msg = "That's not true, look! https://i.ytimg.com/vi/psKUh0M4cW4/maxresdefault.jpg".format(message)
            await client.send_message(message.channel, msg)
            await client.send_message(message.channel, "See?")
        except ValueError:
            msg = message.content[8:].format(message)
            await client.send_message(message.channel, msg)

    elif message.content.startswith("!"):
        for x in simplecommands:
            if x in message.content.lower():
                msg = simplecommands[x]
                await client.send_message(message.channel, msg)
                break
        return

    elif client.user.mentioned_in(message):
        await client.send_message(message.channel, "Huh?")

    else:
        for x in regularwords:
            if x in message.content.lower():
                msg = regularwords[x]
                await client.send_message(message.channel, msg)
                break
        return

client.run('NTY0NjU4OTc0MTgwMjQ1NTIy.XKrKfg.8LctWjJNiUvHRnkWYtAmKyeZ8mY')
