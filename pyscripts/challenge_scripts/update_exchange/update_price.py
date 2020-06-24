import datetime
import pandas as pd
import numpy as np
from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import random
import time
import json 
import requests

def telegram_bot_sendtext(bot_message):
    
    bot_token = '1262543569:AAEX0QVuvGpyooBG5R3Cztq1wwdaDAcZwQ4'
    bot_chatID = '-456518436'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

# Connecting to the network
network_selected = "ropsten"
network.connect(network_selected)

# Loading the metamask accounts
## Trading account
fss_trading_private_key = "faba88e53b6fac655f7e0b5cb900e0bc045e787eb850fdf17f458f0fb8607bde"
fss_trading_account = web3.eth.account.from_key(private_key=fss_trading_private_key)
local_account_trading = LocalAccount(fss_trading_account.address, fss_trading_account, fss_trading_account.privateKey)
## Admin account
fss_admin_private_key = "ede4dd8a3584fd7809a5e0bb299ff8f51983af5b1a9f1f506165b5c1f09e22b1"
fss_admin_account = web3.eth.account.from_key(private_key=fss_admin_private_key)
local_account_admin = LocalAccount(fss_admin_account.address, fss_admin_account, fss_admin_account.privateKey)

with open("./pyscripts/abi/token_exchange.json") as json_file:                                                                                                                                
    exchange_abi = json.load(json_file)
exchange = Contract.from_abi('Exchange', address="0x99d07b3fA4C2046a43e3911AC5a5bC3B0115b110", abi= exchange_abi, owner= local_account_admin) 

df = pd.read_csv(r'./pyscripts/challenge_scripts/price_history.csv',  index_col=0, names= ['','delta'], skiprows=8785)
#print(df)

df = df.diff()

i = 1
start = datetime.datetime(2020, 6, 24, 9)

while True:

    if (datetime.datetime.now() >= start and datetime.datetime.now() < start + datetime.timedelta(hours=9)):
        print("Changing price...")
        print("Delta price: {}".format(Wei(f"{df.iloc[i]['delta']} ether")))
        
        price = Wei(f"{df.iloc[i]['delta']} ether")
        try: 
            exchange.setNewPrice(price, {'from': local_account_admin, 'gas_price': Wei("2 gwei")})
        except: 
            telegram_bot_sendtext("Couldn't load price correctly, please check asap!")
            continue 

        time.sleep(random.randrange(300, 600))
        i = i + 1
    else:
        start = start + datetime.timedelta(hours=24)
        telegram_bot_sendtext("Script: update_price.py \nTrading day finished. \nGoing to sleep, goodnight <3")
        time.sleep(54000) 
        telegram_bot_sendtext("Script: update_price.py \nGoodmorning <3 \nRise and shine!. \nLet me drink my coffee and I will start updating.")
    
    if (datetime.datetime.now() > datetime.datetime(2020, 7, 1, 18)):
        break
