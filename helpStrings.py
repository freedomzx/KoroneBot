#generalCommands

eightBallHelp = """
    To use this command, send: \"!eightBall <a question>\".
    The bot will then give you a random response to that question.
"""
eightBallHelpShort = "\"!eightBall <question>\""

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
    The weather from that area, if found, will then be sent.
"""
weatherHelpShort = "\"!weather\", then send zipcode, then send country code."

whoamiHelp = """
    To use this command, send \"!whoami\".
    The bot will then send you your discord account's join date for the current server, discord account creation date, user ID, and username discriminator (the 4 numbers after your username.)
"""
whoamiHelpShort = "\"!whoami\""

#sqlCommands

addcommandHelp = """
    To use this command, send \"!addcommand\".
    The bot will then ask for the title of your command, which you should then send.  (No spaces or the ! prefix).
    The bot will then ask for the contents of your command, which you should then send.  (Less then the discord character limit).
    The bot will then inform you that the command has been added, if the title is not already in use.
"""
addcommandHelpShort = "\"!addcommand\", send command title, then send command description."

customHelp = """
    To use this command, send \"!custom <custom command name>\".
    The bot will then check through the SQL database and see if the command exists, then sends the contents 
    if it does exist.
"""
customHelpShort = "\"!custom <custom command name>\""

customContainsHelp = """
    To use this command, send \"!customcontains <letter/phrase>\".
    The bot will then check through the SQL databaes and find the names of any commands whose contents contain the specified word or phrase.
"""
customContainsHelpShort = "\"!customcontains <letter/phrase>\""

customEndsWithHelp = """
    To use this command, send \"!customendswith <letter or phrase>\".
    The bot will then check the SQL database and retrieve a list of commands whose command names end with 
    the specified letter/phrase.
"""
customEndsWithHelpShort = "\"!customendswith <letter/phrase>\""

customInfoHelp = """
    To use this command, send \"!custominfo <custom command name>\".
    The bot will check through the SQL database and see if the command exists.
    If it does, the command's author and creation date will be sent.
"""
customInfoHelpShort = "\"!custominfo <custom command name>\""

customListHelp = """
    To use this command, send \"!customList\".
    The bot will give a list of the names of all the custom commands it has.
"""
customListHelpShort = "\"!customList\""

customNameContainsHelp = """
    To use this command, send \"!customcontains <letter or phrase>\".
    The bot will then check through the SQL database and retrieve a list of commands whose command names 
    contain the desired letter or phrase.
"""
customNameContainsHelpShort = "\"!customcontains <letter/phrase>\""

customStartsWithHelp = """
    To use this command, send \"!customstartswith <letter or phrase>\".
    The bot will then check through the SQL database and retrieve a list of commands whose command names start 
    the specified letter/phrase.
"""
customStartsWithHelpShort = "\"!customstartswith <letter/phrase>\""

#youtubeScrapeCommands

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

#nasaCommands

apodHelp = """
    To use this command, send \"!apod\".
    The bot will send a request to https://api.nasa.gov/, and retrieve an astronomy picture of the day and its details.
"""
apodHelpShort = "\"!apod\""

#wordCommands

defineHelp = """
    To use this command, send: \"!help <single english word to define>\".  
    The bot will then either define the word, or tell you that it cannot find a definition for the given word.
"""
defineHelpShort = "\"!define <word>\""

hangmanHelp = """
    To use this command, send \"!hangman\".
    The bot will then start a game of hangman, giving the slots for a word and sending an ASCII picture of a hangman board.
    To guess a letter or the entire word, send \"guess <guess>\".
    The game will proceed until the man is dead or the word is found.  You have 7 lives!
"""
hangmanHelpShort = "\"!hangman\", \"guess <guess>\""

scrabblescoreHelp = """
    To use this command, send: \"!scrabblescore <single word>\".
    The bot will then send a get request to Wordnik API and retrieve the word's scrabble score.
"""
scrabblescoreHelpShort = "\"!scrabblescore <single word>\""

wordofthedayHelp = """
    To use this command, send \"!wordoftheday\".
    The bot will then give a word of the day and its definition.
"""
wordofthedayHelpShort = "\"!wordoftheday\""


#pokedexCommands

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
pokedexHelpShort = "\"!pokedex <pokemon name>\""

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