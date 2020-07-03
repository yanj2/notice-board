import discord
import os 
from deals_helper import search, retrieve, fn_mapping, call_fn, str_valid_queries, valid_query
from concurrent.futures import ThreadPoolExecutor
import asyncio 

OK = 1
FAIL = 0

class Bot(discord.Client):

    SHUTDOWN_COMMAND = ["sleep", "shutdown"]

    async def on_ready(self):
        # guild is a server 
        for guild in self.guilds:
            for channel in guild.text_channels:
                await channel.send(f"{bot.user} has entered the building.")

    async def on_message(self, message):
        if message.author == bot.user:
            return

        if message.content in self.SHUTDOWN_COMMAND:
            await bot.close()
            return 

        executor = ThreadPoolExecutor(max_workers=3)
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(executor, generate_response, message.channel, message.content)
        await message.channel.send(response)

def generate_response(channel, message):
    message = message.split()
    query, keyword = message[0], " ".join(message[1:])

    if not valid_query(query):
        return "Your query was invalid. Please try one of the following: " + str_valid_queries()
    
    status, results = call_fn(query, keyword)
    if status == OK:
        return create_message(results)
    else:
        return "Something went wrong while processing your request."

def create_message(results):
    return "\n".join(results)


bot = Bot()
bot.run(os.getenv("TOKEN"))
