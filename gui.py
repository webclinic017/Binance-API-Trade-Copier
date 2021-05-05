# Imports
import tkinter as tk
import time
import threading
from random import randint

# Script Imports
import binanceWork as b
import discordManager


# Root Build
root = tk.Tk()
root.title("Binance.US Trade Copier")
root.geometry("500x400")

# Threaded Functions
def balanceLabel():
    while True:
        balance_label.config(text=f'Balance Estimate: {b.getTotalBalance()}')
        time.sleep(5)

def lastTrade():
    while True:
        if (b.checkForTrades()):
            lastTrade_label.config(text=f'Last Trade:  {b.lastTrade}')
        time.sleep(2)
def johnBalance():
    while True:
        johnBalance_label.config(text=f'johnBalance Estimate: {b.getJohnBalance()}')
        time.sleep(5)
# def discord():
    # import discordManager
    # while True:
    #     print('tes')
    #     time.sleep(5)




def socketTime():
    while True:
        # print("Socket reset")
        b.runClientSocket()
        time.sleep(1)



# Setup Widgets
balance_label = tk.Label(root, text="Balance Estimate: ")
balance_label.pack(pady=20)

lastTrade_label = tk.Label(root, text="Last Trade: ")
lastTrade_label.pack(pady=20)

johnBalance_label = tk.Label(root, text="johnBalance Estimate: ")
johnBalance_label.pack(pady=20)


# Start Threads
threading.Thread(target=socketTime).start()
threading.Thread(target=balanceLabel).start()
threading.Thread(target=lastTrade).start()
threading.Thread(target=johnBalance).start()
threading.Thread(target=discordManager.start).start()



root.mainloop()

