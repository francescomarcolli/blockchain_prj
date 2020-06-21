import datetime
import pandas as pd
import numpy as np
from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import random
import time
import json 

# Connecting to the network
network_selected = "ropsten"
network.connect(network_selected)

# Loading the metamask account
fss_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"
fss_account = web3.eth.account.from_key(private_key=fss_private_key)
local_account = LocalAccount(fss_account.address, fss_account, fss_account.privateKey)

with open("./pyscripts/token_exchange.json") as json_file:                                                                                                                                
    exchange_abi = json.load(json_file)
tk_exchange = Contract.from_abi('Exchange', address="0xA0E802c3582C59bdD1050E3a38b4D2eaCa2F7790", abi= exchange_abi, owner= local_account) 

df = pd.read_csv(r'./pyscripts/challenge_scripts/price_history.csv',  index_col=0, names= ['','delta'], skiprows=1)
print(df)

df = df.diff()
print(df)
i = 1

start = datetime.datetime.now()

while True:

    if (datetime.datetime.now() >= start and datetime.datetime.now() < start + datetime.timedelta(hours=9)):
        print("Changing price...")
        print("Delta price: {}".format(Wei(f"{df.iloc[i]['delta']} ether")))
        
        price = Wei(f"{df.iloc[i]['delta']} ether")
        tk_exchange.setNewPrice(price)
        time.sleep(random.randrange(300, 600))

        i = i + 1
    else:
        time.sleep(54000)

    if(i >= 8759): 
        break
    if (datetime.datetime.now() > datetime.datetime(2020, 7, 1, 18)):
        break
