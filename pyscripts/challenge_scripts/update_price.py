import datetime
import pandas as pd
import numpy as np
from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import random

# Connecting to the network
network_selected = "ropsten"
network.connect(network_selected)

# Loading the metamask account
fss_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"
fss_account = web3.eth.account.from_key(private_key=fss_private_key)
local_account = LocalAccount(fss_account.address, fss_account, fss_account.privateKey)

tk_exchange = Contract.from_abi('', address=, abi=, owner= local_account) #TODO completa il campo!!!!!
df = pd.read_csv(r'./price_history.csv',  index_col=0, names= ['','delta'], skiprows=8758)

df = df.diff()
i = 1
while True:

    if (datetime.datetime.now() >= start && datetime.datetime.now() < start + datetime.timedelta(hours=9)):

        tk_exchange.setNewPrice(df.iloc[i]['delta'])

        time.sleep(random.randrange(300, 600))

        i += 1

    else:
        time.sleep(54000‬)


    if (datetime.datetime.now() > datetime.datetime(2020, 7, 1, 18)):
        break
