# bot.py
import os
import discord
import json
import random
import time

import binanceWork as b
# Parse the stuff
with open("key.json") as json_data_file:
    key = json.load(json_data_file)

# Import encrypted keys
TOKEN = key["discord"]["TOKEN"]
GUILD = key["discord"]["GUILD"]
TRADECHANNEL = key["discord"]["TRADES_CHANNEL"]


# Global
# msg = b.DISCORD_MESSAGE_BOARD
# oldMsg = b.DISCORD_MESSAGE_BOARD


# Checked loop

    


client = discord.Client()

@client.event
async def on_ready():
    # global msg, oldMsg
    
    while True:
        # print(b.DISCORD_MESSAGE_BOARD == b.OLD_MESSAGE_BOARD)
        
        # await client.get_channel(TRADECHANNEL).send("bot is online")
        if (b.DISCORD_MESSAGE_BOARD != b.OLD_MESSAGE_BOARD):
            for i in b.DISCORD_MESSAGE_BOARD:
                if (i["executed"] == False):
                    await client.get_channel(i["channel"]).send(i["message"])
                    i["executed"] = True
            b.DISCORD_MESSAGE_BOARD = []
            print('ding')

        
        time.sleep(5)
#    await client.get_channel(TRADECHANNEL).send("bot is online")


def start():
    client.run(TOKEN)

# start()