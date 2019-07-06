//initialization
const Discord = require("discord.js");
const client = new Discord.Client();
const config = require("./config.json");

//on ready
client.on("ready", () => {
  const connectMessage = require("./testModule.js");
  const message = connectMessage("Kokoro");
  console.log(message);
  client.user.setActivity("hentai", { type: "WATCHING"});
});

//commands
client.on("message", (message) => {
  //preliminary
  if(message.author.bot) return;
  if(message.content.indexOf(config.prefix) !== 0) return;
  const args = message.content.slice(config.prefix.length).trim().split(/ +/g);
  const command = args.shift().toLowerCase();
  //everything else
  if(command === 'ping'){
    message.channel.send('Pinging, just gimme a second...')
    .then((msg) => {
      msg.edit("Ping: " + (Date.now() - msg.createdTimestamp) + " ms")
    });
  }

  if(command === 'test'){
    var george = client.users.get(121711133554900996);
    console.log(george);
  }

  if(command === 'avatar'){
    if(args.length === 1){
      if(message.mentions.users.array().length === 0) message.channel.send("Invalid argument, mention a user please");
      else{
        var person = message.mentions.users.first();
        if(person.avatarURL == null) message.channel.send("this dude dont even have an avatar");
        else message.channel.send(person.avatarURL)
      }
    }
    else message.channel.send(message.author.avatarURL);
  }

  if(command === 'dm'){
    message.author.send("https://www.youtube.com/watch?v=YJgvrQXlRaw");
  }

});

//run client
client.login(config.token);
