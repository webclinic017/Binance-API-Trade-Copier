import binanceWork as b
from twisted.internet import reactor
from pprint import pprint
import time

def process_message(msg):
    # print("message type: {}".format(msg['e']))
    print(msg)
    # do something

# def test():
    
#     bm = b.BinanceSocketManager(b.client)

#     from datetime import datetime

#     now = datetime.now()

#     current_time = now.strftime("%H:%M:%S")
#     # while True:
#     conn_key = bm.start_symbol_ticker_socket('BNBBTC', process_message)
#     bm.start()
#     # pprint((conn_key))
#     time.sleep(10)


#     bm.stop_socket(conn_key)
#     print(f'Socket Reset: {current_time}')
#     bm.close()
#     reactor.stop()




# start = time.time()
# print(b.getTotalBalance())
# end = time.time()
# print(end - start)

# balance = b.johnClient.get_account()["balances"]
# pprint(balance)

def getTotalBalance():
    wallet = b.johnClient.get_account()["balances"]
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
            value = float(b.johnClient.get_avg_price(symbol=f"{asset}USDT")["price"])
        except:
            value = float(b.johnClient.get_avg_price(symbol=f"{asset}USD")["price"])
            
        print(f'Asset: {asset} Qty: {qty}  Value: {qty * value}')

        totalBalanceUSD += qty * value
        
        # print(f"{asset} Value: $" + str(qty * value))
    
    # print("Est. Total Balance: $" + str(totalBalanceUSD))
    return totalBalanceUSD
   
print(getTotalBalance())
#    On init, Create new balance price sheet with the ticker. Use ticker websocket to quickly parse and find balance. 
