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

TRADECHANNEL = key["discord"]["TRADES_CHANNEL"]
JGTRADE_CHANNEL = key["discord"]["JGTRADE_CHANNEL"]

LIMIT = 1

DISCORD_MESSAGE_BOARD = []
OLD_MESSAGE_BOARD = []

# Connect to Binance.us

client = Client(APIKEY, APISECRET, {"verify": True, "timeout": 10000})
johnClient = Client(JOHNAPIKEY, JOHNAPISECRET, {"verify": True, "timeout": 10000})


# Init Globals
tradingMarkets = ["USDTUSD", "DOGEUSDT", "VTHOUSDT", "ONEUSDT", "BANDUSDT", "ETCUSDT", "EGLDUSDT", "HNTUSDT", "ATOMUSDT", "ZRXUSDT", "MANAUSD", "KNCUSDT", "QTUMUSDT", "HBARUSD", "ENJUSD", "BATUSDT", "XLMUSDT", "BNBUSDT", "ETHUSDT", "BTCUSDT"]
initMarketTrade = []
lastTrade = ""
liveSocket = True
minTrade = float(15.00)
# Socket global
clientSocketList = []
newClientSocketList = []
makeTrade = False

# Global Cache
# precision = 6


# Populate initMarketTrade[]
# for market in tradingMarkets:
#     # print(market)
#     currentAsset, currentTrader = os.path.splitext(market)
#     currentTrader = currentTrader.lstrip(".")
#     currentMarket = currentAsset + currentTrader
#     # print(client.get_my_trades(symbol=currentMarket, limit=LIMIT)[0])
#     initMarketTrade.append(client.get_my_trades(symbol=currentMarket, limit=LIMIT)[0])

# Web Socket
messageTimer = 0
# This is our callback function. For now, it just prints messages as they come.
def process_message(msg):
    global messageTimer
    global clientSocketList
    global liveSocket
    global makeTrade

    if msg['e'] == "error":
        # Handle Error
        print("Error: ")
        pprint(msg)
        liveSocket = False
    else:
        print(f'Message Number: {messageTimer}')
        print("message type: {}".format(msg['e']))
        # pprint(msg)

        if (msg['e'] == "executionReport" and msg['X'] == "FILLED"):
            msg['executed'] = False
            clientSocketList.append(msg)
            makeTrade = True
            print("Added order to list")
            messageTimer += 1
    


def passToDiscord(msg, chnl):
  
    print("Info passed to discord")
    appy = {
        "message": msg,
        "executed": False,
        "channel": chnl
    }
    DISCORD_MESSAGE_BOARD.append(appy)
    





def runClientSocket():
    global liveSocket
    bm = BinanceSocketManager(client)

    from datetime import datetime

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    # while True:
    conn_key = bm.start_user_socket(process_message)
    bm.start()
    # pprint((conn_key))
    time.sleep(180)
    bm.stop_socket(conn_key)
    print(f'Socket Reset: {current_time}')
    bm.close()
    # reactor.stop()

    # Kill
    # bm.close()
    # reactor.stop()

# runClientSocket()

def checkForTrades():
    i = 0
    newTradeMade = False
    global lastTrade, minTrade
    global clientSocketList, newClientSocketList
    global makeTrade
    
    # print("DEBUG:")
    # pprint(newClientSocketList)
    # pprint(clientSocketList)
    # if (newClientSocketList != clientSocketList):
    if (makeTrade):
        for transaction in clientSocketList:
            if (transaction["executed"] == False):

                currentAsset = ''
                currentTrader = ''

                currentMarket = transaction['s']
                
                # Manual fixes
                if (currentMarket == 'BANDUSDT'):
                    currentAsset = 'BAND'
                    currentTrader = 'USDT'
                else:

                    # How will I parse the market name?
                    if (currentMarket[-1] == 'T'):
                        # print(currentMarket.rstrip('USDT')[0])
                        currentAsset = currentMarket.rstrip('USDT')
                        currentTrader = "USDT"
                        i += 1
                    elif (currentMarket[-1] == 'C' and currentMarket[-3] == 'S'  ):
                        currentAsset = currentMarket.rstrip('USDC')
                        currentTrader = "USDC"
                        i += 1
                    elif (currentMarket[-1] == 'C' and currentMarket[-3] == 'B'  ):
                        currentAsset = currentMarket.rstrip('BTC')
                        currentTrader = "BTC"
                        i += 1
                    elif (currentMarket[-1] == 'D' and currentMarket[-4] == 'B'  ):
                        currentAsset = currentMarket.rstrip('BUSD')
                        currentTrader = "BUSD"
                        i += 1
                    else:
                        # print("DEBUG")
                        # print(currentMarket.rstrip('USD'))
                        currentAsset = currentMarket.rstrip('USD')
                        currentTrader = "USD"
                        i += 1 
                    
                # newTrade = client.get_my_trades(symbol=currentMarket, limit=LIMIT)[0]

                
                

                # print("Eval: " + currentMarket)
                # print("Current Asset: " + currentAsset)
                # print("Current Trader: " + currentTrader)

            
                


                

                print(f'{currentMarket} transaction detected')

                # Init variables as Float
                orderQuantity = float(transaction['q'])
                orderPrice = float(client.get_avg_price(symbol = currentMarket)["price"])
                minAssetOrder = minTrade / orderPrice 
                orderCost = orderQuantity * orderPrice

                assetQuantity = 0

                try:
                    freeBalance = float(client.get_asset_balance(asset=currentAsset)["free"])
                    lockedBalance = float(client.get_asset_balance(asset=currentAsset)["locked"])
                    assetQuantity =  freeBalance + lockedBalance 
                except:
                    assetQuantity = 0

                traderQuantity = float(client.get_asset_balance(asset=currentTrader)["free"]) + float(client.get_asset_balance(asset=currentTrader)["locked"])

                assetPercentage = orderQuantity / (assetQuantity + orderQuantity)
                traderPercentage = orderQuantity / (traderQuantity + orderQuantity)

                try:
                    johnAssetQuantity = float(johnClient.get_asset_balance(asset=currentAsset)["free"])
                except:
                    johnAssetQuantity = 0

                johnTraderQuantity = float(johnClient.get_asset_balance(asset=currentTrader)["free"])
                

                # Copier's wallets
                # blankAssetWallet = float(blankClient.get_asset_balance(asset=currentTrader)["free"])
                # blankTraderWallet = float(blankClient.get_asset_balance(asset=currentTrader)["free"])

                from datetime import datetime

                now = datetime.now()

                current_time = now.strftime("%H:%M:%S")
                # print("Current Time =", current_time)


                # Create precision
                ticks = {}
                stepSize = 0
                for filt in client.get_symbol_info(currentMarket)['filters']:
                    if filt['filterType'] == 'LOT_SIZE':
                        stepSize = filt['stepSize']

                precision = int(round(-math.log(float(stepSize), 10), 0))  

                buy_or_sell = str(transaction['S'])
                
                # Gui
                # Add balance to last trade when getBalance is optimized 
                lastTrade = f'{buy_or_sell} -- Market: {currentMarket} Qty: {orderQuantity} Cost: {round(orderCost, 2)} Time: {current_time}'
                passToDiscord(lastTrade, TRADECHANNEL) 
                messFail = "Trade failed, contact admin for details"
            
                # Buy
                if (transaction['S'] == "BUY"):
                    print(f'{currentAsset} was bought')
                    print("New order quantity: " + str(orderQuantity))
                    print("New order cost: " + str(orderCost))

                    
                    johnPurchaseQuantity = traderPercentage * johnTraderQuantity
                    if (johnPurchaseQuantity > orderQuantity):
                        johnPurchaseQuantity = orderQuantity
                    
                

                    johnPurchasePrice = float(johnClient.get_avg_price(symbol= currentMarket)["price"])  * johnPurchaseQuantity

                    if (johnPurchasePrice < minTrade):
                        if (johnTraderQuantity >= (minTrade + 0.1)):
                            print('min trade made')
                            johnPurchaseQuantity = minTrade + 0.1
                            print(f'new purchase qty {johnPurchaseQuantity}')
                            johnPurchasePrice = johnPurchaseQuantity
                            print(f'new purchase price {johnPurchasePrice}')
                    
                    
                    if (johnPurchasePrice < minTrade):
                        print("John's balance too low")
                        messLow = f'{johnPurchasePrice} is too low to make trade'
                        print(messLow)
                        passToDiscord(messLow, JGTRADE_CHANNEL)
                    else:
                        print("Trade made")
                        messBuy = f'John buys {str(johnPurchaseQuantity)} {currentAsset}, which is worth ${str(round(johnPurchasePrice, 2))}'
                        print(messBuy)
                        passToDiscord(messBuy, JGTRADE_CHANNEL)

                        # Copy Buys
                        try:
                            johnClient.order_market_buy(symbol=currentMarket, quantity=(round(johnPurchaseQuantity, precision)))
                        except:
                            print("Buy failed")
                            passToDiscord(messFail, JGTRADE_CHANNEL)


                        # transaction["executed"] = True
                        newTradeMade = True
                        new = clientSocketList
                        newClientSocketList = new
                        makeTrade = False
                # Sell
                else:
                    print(f'{currentAsset} was sold')
                    print("New order quantity: " + str(orderQuantity))
                    print("New order cost: " + str(orderCost))


                    johnPurchaseQuantity = assetPercentage * johnAssetQuantity
                    if (johnPurchaseQuantity > orderQuantity):
                        johnPurchaseQuantity = orderQuantity
                    
                    johnPurchasePrice = float(johnClient.get_avg_price(symbol= currentMarket)["price"])  * johnPurchaseQuantity

                    if (johnPurchasePrice < minTrade):
                        if (johnAssetQuantity >= (minAssetOrder + 0.1)):
                            johnPurchaseQuantity = minAssetOrder + 0.1
                            johnPurchasePrice = johnPurchaseQuantity * orderPrice
                    
                    
                    if (johnPurchasePrice < minTrade):
                        print("John's balance too low")
                        messLow = f'{johnPurchasePrice} is too low to make trade'
                        print(messLow)
                        passToDiscord(messLow, JGTRADE_CHANNEL)

                    else:
                        print("Trade made")
                        messSell = f'John sells {str(johnPurchaseQuantity)} {currentAsset}, which is worth ${str(round(johnPurchasePrice, 2))}'
                        print(messSell)
                        passToDiscord(messSell, JGTRADE_CHANNEL)

                        
                        try:
                            johnClient.order_market_sell(symbol=currentMarket, quantity=(round(johnPurchaseQuantity, precision)))
                        except:
                            print('Sell Failed')
                            passToDiscord(messFail, JGTRADE_CHANNEL)



                        # Copy Sells
                        # johnClient.order_market_buy(symbol=currentMarket, quantity=(assetPercentage * johnAssetQuantity))
                        # client.order_market_sell(symbol=currentMarket, quantity=orderQuantity)
                        # transaction["executed"] = True
                        newTradeMade = True
                        new = clientSocketList
                        newClientSocketList = new
                        makeTrade = False

                
                transaction["executed"] = True
                i += 1

    return newTradeMade





    

def balanceWebSocket(wlt):
    balance = 0.00



    return balance

    
def getTotalBalance():
    wallet = client.get_account()["balances"]
    totalBalanceUSD = 0.00

    # print(wallet[0]["asset"])
    for entry in wallet:
        
        asset = entry["asset"]
        qty = float(entry["free"]) + float(entry["locked"])
        value = 0
        if (asset == "USD"):
            totalBalanceUSD += qty
            continue
        try:
            value = float(client.get_avg_price(symbol=f"{asset}USDT")["price"])
        except:
            value = float(client.get_avg_price(symbol=f"{asset}USD")["price"])

        totalBalanceUSD += qty * value
        
        # print(f"{asset} Value: $" + str(qty * value))
    
    # print("Est. Total Balance: $" + str(totalBalanceUSD))
    return totalBalanceUSD


def getJohnBalance():
    wallet = johnClient.get_account()["balances"]
    balance = {}
    balance["total"] = 0.00

    # pprint(wallet)

    for entry in wallet:
        qty = float(entry["free"]) + float(entry["locked"])
        asset = entry["asset"]

        if (asset == "USD"):
            balance["USD"] = qty
            balance["total"] += qty
        if (asset == "BUSD"):
            balance["BUSD"] = qty
            balance["total"] += qty

        if (asset == "USDT"):
            balance["USDT"] = qty
            balance["total"] += qty

        if (asset == "USDC"):
            balance["USDC"] = qty
            balance["total"] += qty

        if (asset == "BTC"):
            value = float(client.get_avg_price(symbol="BTCUSD")["price"])
            balance["BTC"] = qty * value
            balance["total"] += qty * value

    return balance


# pprint(client.get_account())
# pprint(float(client.get_asset_balance(asset=currentAsset)["free"]))

# print("before")    
# pprint(johnClient.get_account()["balances"])
# johnClient.order_limit_sell(
#     symbol='BTCUSDT',
#     quantity=0.0016,
#     price='64000')
# print("after")
# pprint(johnClient.get_all_orders(symbol='BTCUSDT'))


# DEBUG

# pprint(johnClient.get_account())

# while True:
#     checkForTrades()
#     time.sleep(2)


# global liveSocket
# def test_message(msg):
#     pprint(msg)

# bm = BinanceSocketManager(client)


# conn_key = bm.start_ticker_socket(test_message)
# bm.start()
# time.sleep(10)
# bm.stop_socket(conn_key)
# print('Socket Reset')

# # Kill
# bm.close()
# reactor.stop()

