# Init values
from binance.client import Client
from binance.websockets import BinanceSocketManager
import binance.client as bc
from pprint import pprint
import tkinter
import time
import os
from twisted.internet import reactor
import json
import math

with open("key.json") as json_data_file:
    key = json.load(json_data_file)


APIKEY = key["aram"]["APIKEY"]
APISECRET = key["aram"]["APISECRET"]

JOHNAPIKEY = key["john"]["APIKEY"]
JOHNAPISECRET = key["john"]["APISECRET"]

LIMIT = 1


# Connect to Binance.us

client = Client(APIKEY, APISECRET)
johnClient = Client(JOHNAPIKEY, JOHNAPISECRET)

johnClient.order_market_buy(symbol="BANDUSDT", quantity=2.43)

pprint(johnClient.get_account()["balances"])
# pprint(client.get_symbol_info("USDTUSD"))["filters"]

# ticks = {}
# stepSize = 0
# for filt in client.get_symbol_info('ETHUSDT')['filters']:
#                 if filt['filterType'] == 'LOT_SIZE':
#                     stepSize = filt['stepSize']

# precision = int(round(-math.log(float(stepSize), 10), 0))

# print(ticks)
# print(stepSize)

# print(precision)