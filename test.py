currentAsset = ''
currentTrader = ''
i = 0
currentMarket = "USDTUSD"
# How will I parse the market name?
if (currentMarket[-1] == 'T'):
    print(currentMarket.rsplit('USDT')[0])
    currentAsset = currentMarket.rsplit('USDT')[0]
    currentTrader = "USDT"
    i += 1
elif (currentMarket[-1] == 'C' and currentMarket[-3] == 'S'  ):
    currentAsset = currentMarket.rsplit('USDC')[0]
    currentTrader = "USDC"
    i += 1
elif (currentMarket[-1] == 'C' and currentMarket[-3] == 'B'  ):
    currentAsset = currentMarket.rsplit('BTC')[0]
    currentTrader = "BTC"
    i += 1
elif (currentMarket[-1] == 'D' and currentMarket[-4] == 'B'  ):
    currentAsset = currentMarket.rsplit('BUSD')[0]
    currentTrader = "BUSD"
    i += 1
else:
    print("DEBUG")
    print(currentMarket.rstrip('USD'))
    # currentAsset = currentMarket.lsplit('USD')[0]
    currentTrader = "USD"
    i += 1 