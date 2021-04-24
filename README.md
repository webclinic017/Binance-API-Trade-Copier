# Binance-API-Trade-Copier
Python-based program to copy trades from client to multiple copiers. 

** In Development

Requirements:
https://python-binance.readthedocs.io/en/latest/
(To work with the US version of Binance, go to *./python-binance/binance/client.py and change the domain to '.us')

Installation:
Create key.json in root with keys

`
{
    "client": {
        "APIKEY": "********************************",
        "APISECRET": "********************************"

    },
    "copier": {
        "APIKEY": "********************************",
        "APISECRET": "********************************"

    }

}
`

Modularity not expanded upon, to operate this program in its current state user must modify code. Please email aram.devdocs@gmail.com with any questions in regard to this project.

TODO: 
Update GUI with accurate feedback regarding copier balances in stablecoin/USD, as well as a visual verification of trade being copied successfully. 
Logging system within the GUI.
Fix error with threading timing out and websocket not working after X amount of time. 
Ade modular copy purchasing system
Integrate profiles for multiple copiers to be added.





Devlogs:
1:39 AM MST 4/24/2021:
Uploading initial commit to Github. Project still in early testing stages. By running gui.py, a terminal will show up with the primary client's estimated balance based off of average price from the last 5 minutes. A script will run via 'threading' in paralell with  one thread dedicated to the Websocket runtime, one socket dedicated to the balance, and one socket dedicated to monitoring for any new trades. Whenever a new trade is detected by the websocket, it will update a list with a new order to be checked. If a transaction["executed"] == false, the client will evaluate the trade to see the comperable percentage to be applied to the copier list, and upon verifcation of price minimum and available balance, the trade will be executed. Current issues are running into capping the websocket timer so that limits will not be exceeded. 


