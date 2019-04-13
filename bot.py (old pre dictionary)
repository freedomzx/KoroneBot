# Work with Python 3.6
import discord
import random
import asyncio
from discord.ext import commands

TOKEN = 'NTY0NjU4OTc0MTgwMjQ1NTIy.XKrKfg.8LctWjJNiUvHRnkWYtAmKyeZ8mY'

client = discord.Client()
bot = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print("Let's make the world smile!")
    print('------------------')

    await client.change_presence(game=discord.Game(name='smiling :)'))

@client.event
async def on_server_join(server):
    await client.send_message(server.default_channel, "It's me, " + client.user.mention + "!")

@client.event
async def on_message_delete(message):
    if message.author == client.user:
        await client.send_message(message.channel, "Why are you deleting my messages :(")
    else:
        await client.send_message(message.channel, "A message that said \"" + message.content + "\" got deleted!")

@client.event
async def on_member_join(member):
    await client.send_message(member.server.default_channel, "Welcome, " + member.mention)

@client.event
async def on_message(message): #all commands
    if message.author == client.user:
        return

    elif message.content.startswith("!test"):
        msg = "Yep"
        await client.send_typing(message.channel)
        await client.send_message(message.channel, msg)

    elif message.content.startswith("!ben"):
        msg = "retarded baboon monkey".format(message)
        await client.send_message(message.channel, msg)

    elif "ben" in message.content.lower():
        await client.send_message(message.channel, "did someone say ben fuck that guy")

    elif message.content.startswith("!botinfo"):
        await client.send_message(message.channel, "It's me,  " + client.user.mention + "!")
        await client.send_message(message.channel, client.user.id + "\n" + client.user.discriminator)
        await client.send_message(message.channel, client.user.created_at)

    elif message.content.startswith("!channelid"):
        await client.send_message(message.channel, message.channel.id + "")

    elif message.content.startswith("!connectioninfo"):
        await client.send_message(message.channel, client.is_logged_in)
        await client.send_message(message.channel, client.ws)
        await client.send_message(message.channel, client.is_closed)

    elif message.content.startswith("!dm"):
        await client.send_message(message.author, "Hey, " + message.author.name + ". Fuck you.")
        await client.send_message(message.author, "Also, look at this: https://www.youtube.com/watch?v=dzMq5_thk4o")

    elif message.content.startswith("!elijah"):
        msg = "big yurilord gigachad".format(message)
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!hello') or message.content.startswith('!hi'):
        msg = "Hi " + message.author.mention + "! How are you?".format(message)
        await client.send_message(message.channel, msg)

    elif message.content.startswith('!help'):
        msg = "```***COMMANDS***\n!hello\n!hi\n!kokoro\n!repeat\n!botinfo\n!selfie\n!connectioninfo\n!channelid\n!dm\n!roll```".format(message)
        await client.send_message(message.channel, msg)
        await client.send_message(message.channel, "And some stupid hidden shit")

    #elif message.content.startswith('!join'):
    #    await client.join_voice_channel(message.author.voice_channel)

    elif message.content.startswith("!kokoro"):
        msg = "That's me!".format(message)
        await client.send_message(message.channel, msg)

    #elif message.content.startswith("leave"):
    #    await client.disconnect()

    elif "owo" in message.content.lower():
        await client.send_message(message.channel, "what's this")

    elif message.content.startswith("!pregnant"):
        msg = "That's not true, look! https://i.ytimg.com/vi/psKUh0M4cW4/maxresdefault.jpg".format(message)
        await client.send_message(message.channel, msg)
        await client.send_message(message.channel, "See?")

    elif message.content.startswith("!repeat"):
        try:
            x = message.content.index("pregnant")
            msg = "That's not true, look! https://i.ytimg.com/vi/psKUh0M4cW4/maxresdefault.jpg".format(message)
            await client.send_message(message.channel, msg)
            await client.send_message(message.channel, "See?")
        except ValueError:
            msg = message.content[8:].format(message)
            await client.send_message(message.channel, msg)

    elif message.content.startswith("!roll"):
        x = ":game_die: " + str(random.randint(1, 6)) + " :game_die:"
        await client.send_message(message.channel, x)

    elif message.content.startswith("!selfie"):
        await client.send_message(message.channel, client.user.avatar_url + "")

    elif client.user.mentioned_in(message):
        await client.send_message(message.channel, "Huh?")

    elif message.content.startswith("!"):
        return

client.run(TOKEN)
