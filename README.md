# Kokoro-Kode
A discord chatbot with a plethora of features: accesses multiple RESTful/RESTless APIs for a variety of information such as weather, stocks, Pokemon info, and more.

Has a web scraping function that checks whether or not some of my favorite YouTubers are live at the time the command is called.

Features MySQL connectivity to story custom commands from users.

Does all of this asynchronously, so no one is tripping over each other during command calls.

# Commands

### !addcommand

Adds a new custom command to be stored by the bot in a MySQL server.

Order: Send "!addcommand", wait for bot response, respond with command name, wait for bot response, respond with command content, command will be stored.

### !define

Asks the bot to connect to the PyDictionary API to define a given (english) word.  Done using the PyDictionary API on PyPi.

Order: Send "!define <word>", bot will respond.

### !eightball

Asks the bot a question, get a response back.

Order: Send "eightball <question>", get a response back.
  
### !hangman

Starts a game of hangman!  Bot will pick a random word from a list of 10000 words, then will send an ASCII image of the hangman board once ready.

Order: Send "!hangman", repeatedly send "!guess <word>" until either the users win or lose.

### !insult

Causes the bot to insult you!  Powered by evilinsult.com

Order: Send "!insult", get response.

### !roll

Roll a number between 1 and a given number.

Order: Send "!roll", wait for bot response, send a number n for the roll range cap, receive a random number from 1 to n.

### !stocks

Gets stock information for a certain company's ticker.  Done using the yfinance API on PyPi.

Order: Send "!stocks", wait for bot response, send the ticker of the company to analyze stock data for, receive either an error message (cannot be found) or the stock information of the company.

### !translate

Translates any given words or sentences into a different language using the Google Translate API, googletrans on PyPi.

Order: Send "!translate", wait for bot response, send the phrase to be translated, wait for bot response, send the language code for the phrase to be translated to.

### !vtuberLives

Checks who out of the dictionary of VTubers listed in definitions.py are live.  

Order: Send "!vtuberLives", get response (in a few moments).

### !weather

Gives the weather (temperature, pressure, humidity) in any place in the world using the OpenWeather API.

Order: Send "!weather", wait for bot response, send zip code, wait for bot response, send country's 2 letter ISO code (instructions given from bot), receive weather information.

### POKEDEX COMMANDS

## !pokeability

Gives the information for an ability.

Order: Send "!pokesprite <ability name>", get response.

## !pokedex

Gives the general pokedex info for a pokemon: name, sprite, typing, abilities, and description.

Order:  Send "!pokedex <pokemon name>

## !pokeitem

Gives the information for an item.

Order:  Send "!pokeitem <item name>", get response.

## !pokesprite

Gives the sprite for a pokemon, front, back, shiny, or normal colored.

Order: Send "!pokesprite <pokemon name> <front or back> <shiny or default>", get picture.

THANK YOU FOR THE TEAM AT https://pokeapi.co/ FOR POWERING THE POKEDEX!

### Other commands

Other commands may be stored from other users using the !addcommand function, so ask around and see what exists!
