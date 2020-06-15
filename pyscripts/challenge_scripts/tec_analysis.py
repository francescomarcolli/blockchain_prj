import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
%matplotlib inline
import seaborn as sns
import ta
from ta.utils import dropna
from pandas_datareader import data as web

from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount

# Connecting to the network
network_selected = "ropsten"
network.connect(network_selected)

# Loading the metamask account
fss_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"
fss_account = web3.eth.account.from_key(private_key=fss_private_key)
local_account = LocalAccount(fss_account.address, fss_account, fss_account.privateKey)

# Init team1 (T1) and team3 (T3) tokens, exchanges and the PayCoin

payCoin = Contract.from_abi('', address=, abi=, owner= local_account)
T1_tk = Contract.from_abi('', address=, abi=, owner= local_account)
T1_exchange = Contract.from_abi('', address=, abi=, owner= local_account)
T3_tk = Contract.from_abi('', address=, abi=, owner= local_account)
T3_exchange = Contract.from_abi('', address=, abi=, owner= local_account)

for i in range(0, 8759): 
    prices_list_T1.append(T1_exchange.getHistory(i))
    prices_list_T3.append(T3_exchange.getHistory(i))

data = { 'TokenT1': prices_list_T1, 'TokenT2': prices_list_T3}
df = pd.DataFrame(data)