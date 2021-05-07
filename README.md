# Binance-API-Trade-Copier
Python-based program to copy trades from client to multiple copiers. 

** In Development

WARNING: This copier does not have a paper trade mode, and will copy active trades. This project is in development and is prone to errors, and may break upon untested use cases. If you find an error, please post on the github. This project is meant to be maintained and monitored by a developer who is comfortable altering the code base to

Requirements:
https://python-binance.readthedocs.io/en/latest/
(To work with the US version of Binance, go to *./python-binance/binance/client.py and change the domain to '.us')

Installation:
Create key.json in root with proper keys
install dependencies 
Configure desired settings
run gui.py to start program



{
    "client": {
        "APIKEY": "********************************",
        "APISECRET": "********************************"

    },
    "copier": {
        "APIKEY": "********************************",
        "APISECRET": "********************************"

    },

    "discord": {
        "TOKEN": "****************",
        "GUILD": "CHANNEL NAME",
        "TRADES_CHANNEL": MAIN CHANNEL,
        "JGTRADE_CHANNEL": PRIVATE CHANNEL
    }

}


Modularity not expanded upon, to operate this program in its current state user must modify code. Please email aram.devdocs@gmail.com with any questions in regard to this project.

TODO: 
Optimize balance with websockets
Replace redundant code
Integrate profiles for multiple copiers to be added.
Fix server time delay






Devlogs:

10:08 AM MST 5/7/2021: 
Alpha 1.0 Release: Current build runs without errors on current copy. The program watches the main account for any market trades, and then places those trades on the copier (placeholder == johnClient). It will place the same trade the main account does, unless the balance is not adequate to make trade. In that case the copier will place a percentage based trade. Sends updates to discord to notify copiers. 


12:10 AM MST 5/3/2021:
Uploading optmized code to run in persistence on server.

1:39 AM MST 4/24/2021:
Uploading initial commit to Github. Project still in early testing stages. By running gui.py, a terminal will show up with the primary client's estimated balance based off of average price from the last 5 minutes. A script will run via 'threading' in paralell with  one thread dedicated to the Websocket runtime, one socket dedicated to the balance, and one socket dedicated to monitoring for any new trades. Whenever a new trade is detected by the websocket, it will update a list with a new order to be checked. If a transaction["executed"] == false, the client will evaluate the trade to see the comperable percentage to be applied to the copier list, and upon verifcation of price minimum and available balance, the trade will be executed. Current issues are running into capping the websocket timer so that limits will not be exceeded. 


Questions? Email aram.devdocs@gmail.com