import pandas as pd

import datetime

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

prices_list_T1 = []
prices_list_T3 = []

for i in range(0, 8759): 
    prices_list_T1.append(T1_exchange.getHistory(i))
    prices_list_T3.append(T3_exchange.getHistory(i))

# data = {'TokenT1': prices_list_T1, 'TokenT3': prices_list_T3}
df_T1 = pd.DataFrame(prices_list_T1, columns=['TokenT1'])
df_T3 = pd.DataFrame(prices_list_T3, columns=['TokenT3'])

# Generate dates to append as index to df_T1,3
def datetime_range(start, end, delta):
    current = start
    if not isinstance(delta, datetime.timedelta):
        delta = datetime.timedelta(**delta)
    while current < end:
        yield current
        current += delta

start = datetime.datetime(2019,6,23)
end = datetime.datetime(2020,6,23)

dates = []
dates_refined = []

for dt in datetime_range(start, end, {'hours':1}):
    dates.append(dt)

for i in range(1, df_T1.shape[0]+1): 
    dates_refined.append(dates[-i])

dates_refined.reverse()
df_T1.index = dates_refined
df_T3.index = dates_refined

df_final = df_T1.join(df_T3)
df_final.to_csv('./token_prices.csv', sep='\t')