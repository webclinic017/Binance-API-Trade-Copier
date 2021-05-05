import binanceWork as b
from twisted.internet import reactor
import pprint
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


print(b.johnClient.get_account()["balances"])
   

#    On init, Create new balance price sheet with the ticker. Use ticker websocket to quickly parse and find balance. 
