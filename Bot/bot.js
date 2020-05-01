var Discord = require('discord.io');
console.log("successfully connected discord.io");
var logger = require('winston');
// var auth = require('./auth.json');
//NOTE: Need to make sure this uses the token from .env 
require('dotenv').config()

// Configure logger settings
logger.remove(logger.transports.Console);
logger.add(new logger.transports.Console, {
    colorize: true
});
logger.level = 'debug';

// Initialize Discord Bot
var bot = new Discord.Client({
   token: auth.token,
   autorun: true
});

// Displays information about the connected bot
bot.on('ready', function (evt) {
    logger.info('Connected');
    logger.info('Logged in as: ' + bot.username + ' - (' + bot.id + ')');
});

var dict = {
    "deals": "none available"
};

bot.on('message', function (user, userID, channelID, message, evt) {
    // Our bot needs to know if it will execute a command
    // It will listen for messages that will start with `!`
    if (message.substring(0, 1) == '!') {

        // Get the command
        var args = message.substring(1).split(' ');
        var cmd = args[0];
       
        args = args.splice(1);

        switch(cmd) {
            // Response based on deals 
            case 'deals':
                bot.sendMessage({
                    to: channelID,
                    message: dict['deals']
                });
            break;
         }
     }
});