# KoroneBot
A discord chatbot with a plethora of features: accesses multiple RESTful/RESTless APIs for a variety of information such as weather, stocks, Pokemon info, and more.

Current APIs powering the functions: Discord's API, PokeAPI, OpenWeatherAPI, Evilinsult.com's API, Youtube's Data API, Googletrans API, Yahoo Finance's API, Wordnik API.

Has a web scraping function that checks whether or not some of my favorite YouTubers are live at the time the command is called.

Features MySQL connectivity to store custom commands from users.

Does all of this asynchronously, so no one is tripping over each other during command calls.

All of the subsequent explanations for each command can be found by using "!help <command name>".  A brief overview of each command can also be found by saying "!help".

The explanations are grouped by the class found in each of their files.

The commands are CASE INSENSITIVE!

# General Commands (generalCommands.py)

## !eightBall

To use this command, send: "!eightBall <a question>".

The bot will then give you a random response to that question.

## !insult

To use this command, send "!insult".

The bot will then send a GET request to https://evilinsult.com/generate_insult.php?lang=en&type=json and give a random insult from there.

## !roll

To use this command, send "!roll".

Then, the bot will ask what the high bound of the roll should be.

The bot will then generate a random number from 1-n, n being the number given from the previous question.

## !stocks

To use this command, send "!stocks".

The bot will then ask for the company's ticker, which you should then enter.

The bot will then send stock information over the last 5 days for the given company.

## !weather

To use this command, send "!weather".

The bot will then ask for the zipcode of the place you want the weather for, which you should then enter.

The bot will then ask for the country code of the place you want the weather for, which can be found at https://countrycode.org/.

The bot will then send a GET request to http://api.openweathermap.org/data/2.5/weather?zip=, with the endpoints being filled in based on the given information.

The weather from that area, if found, will then be sent.

## !whoami

To use this command, send "!whoami".

The bot will then send you your discord account's join date for the current server, discord account creation date, user ID, and username discriminator (the 4 numbers after your username.)

# Word Commands (wordCommands.py)

## !define

To use this command, send: "!help <single english word to define>".  

The bot will then either define the word, or tell you that it cannot find a definition for the given word.

Thank you PyDictionary.

## !hangman

To use this command, send "!hangman".

The bot will then start a game of hangman, giving the slots for a word and sending an ASCII picture of a hangman board.

To guess a letter or the entire word, send "guess <guess>".

The game will proceed until the man is dead or the word is found.  You have 7 lives!

## !scrabblescore

To use this command, send: "!scrabblescore <single word>".

The bot will then send a get request to Wordnik API and retrieve the word's scrabble score.

## !wordoftheday

To use this command, send "!wordoftheday".

The bot will then give a word of the day and its definition, from a GET request to the Wordnik API.

Powered by Wordnik API.



# SQL Commands (sqlCommands.py)

## !addcommand

To use this command, send "!addcommand".

The bot will then ask for the title of your command, which you should then send.  (No spaces or the ! prefix).

The bot will then ask for the contents of your command, which you should then send.  (Less then the discord character limit).

The bot will then inform you that the command has been added, if the title is not already in use.

## !custom

To use this command, send "!custom <custom command name>".

The bot will then check through the SQL database and see if the command exists, then sends the contents if it does exist.

## !customContains

To use this command, send \"!customcontains <word or phrase>\".

The bot will then check through the SQL databaes and find the names of any commands whose contents contain the

specified word or phrase.

## !customEndsWith

To use this command, send \"!customendswith <letter or phrase>\".

The bot will then check the SQL database and retrieve a list of commands whose command

names end with the specified letter/phrase.

## !custominfo

To use this command, send "!custominfo <custom command name>".

The bot will check through the SQL database and see if the command exists.

If it does, the command's author and creation date will be sent.

## !customList

To use this command, send "!customList".

The bot will give a list of the names of all the custom commands it has.

## !customNameContains

 To use this command, send \"!customcontains <letter or phrase>\".

The bot will then check through the SQL database and retrieve a list of commands whose 

command names contain the desired letter or phrase.

## !customStartsWith

To use this command, send \"!customstartswith <letter or phrase>\".

The bot will then check through the SQL database and retrieve a list of commands

whose command names start the specified letter/phrase.

# Youtube Info Commands (youtubeScrapeCommands.py)

## !vtuberLives

To use this command, send "!vtuberLives".

The bot will then check which of the vtubers on its list are live, then sends all the live vtubers, organized by affiliation.

The bot will then ask if you want the links to the streams, which you should then answer "yes" or "no" to.

## !channelinfo

To use this command, send "!channelinfo <youtube channel id>".

The bot will then send the channel's title, description, publish date, sub count, view count, and video count, if found.

# NASA Commands (nasaCommands.py)

# Pokedex Commands (pokedexCommands.py)

## !pokeability

To use this command, send "!pokeability <ability name>".

The bot will then send a GET request the pokiapi ability endpoint and attempt to search for the given ability.

## !pokeberry

To use this command, send "!pokeberry <berry name>".

The bot will then send a GET request to the pokeapi berry endpoint.

If found, a berry's growth time, max harvest number, natural gift power + type, size, smoothness, soil dryness, and firmness will be sent.

## !pokedex

To use this command, send "!pokedex <pokemon name>".

The bot will then send a GET request to the pokeapi pokemon endpoint.

If found, a pokemon's abilities, types, sprite, flavor text, and held items will be returned.

## !pokeitem

To use this command, send "!pokeitem <item name>".

The bot will then send a GET request to the pokeapi item endpoint.

If found, an item's effect, flavor text, and pokemon who hold the item will be returned.

## !pokelocation

To use this command, send "!pokelocation <pokemon name>".

The bot will then send a GET request to the pokeapi location endpoint.

A pokemon's location will be found and returned.

## !pokemove

To use this command, send "!pokemove <move name>".

The bot will then send a GET request to the pokeapi moves endpoint.

A pokemon's move flavor text, PP, damage class, accuracy, type, power, priority, and effect will be returned.

## !pokenature

To use this command, send "!pokenature <nature name>".

The bot will then send a GET request to the pokeapi nature endpoint.

A nature's increased/decreased stats and flavor likes/dislikes will be returned, as well as its description.

## !pokesprite

To use this command, send "!pokesprite <pokemon name> <back or front> <default or shiny>".

The bot will then send a GET request to the pokeapi pokemon endpoint.

A pokemon's sprite will be returned based on front/back and default/shiny.
