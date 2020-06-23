from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import pandas as pd
import json, time

# Connecting to the network
network_selected = "ropsten"
network.connect(network_selected)

# Loading the current project and importing metamask account
token_prj = project.load("./", name="TokenPrj")

## Trading account
fss_trading_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"
fss_trading_account = web3.eth.account.from_key(private_key=fss_trading_private_key)
local_account_trading = LocalAccount(fss_trading_account.address, fss_trading_account, fss_trading_account.privateKey)
## Admin account
fss_admin_private_key = "ede4dd8a3584fd7809a5e0bb299ff8f51983af5b1a9f1f506165b5c1f09e22b1"
fss_admin_account = web3.eth.account.from_key(private_key=fss_admin_private_key)
local_account_admin = LocalAccount(fss_admin_account.address, fss_admin_account, fss_admin_account.privateKey)

with open('./pyscripts/abi/token_exchange.json') as json_file: 
    exchange_abi = json.load(json_file)
exchange = Contract.from_abi('Exchange', address="0x99d07b3fA4C2046a43e3911AC5a5bC3B0115b110", abi= exchange_abi)

print("Charging the prices on the exchange...")
prices = pd.read_csv(r'./pyscripts/challenge_scripts/price_history.csv', skiprows=3459, nrows=8759, names=['', 'close'])
for j in range(3460, 8760, 10): 
    price1 = prices.iloc[j]['close']
    price2 = prices.iloc[j + 1]['close']
    price3 = prices.iloc[j + 2]['close']
    price4 = prices.iloc[j + 3]['close']
    price5 = prices.iloc[j + 4]['close']
    price6 = prices.iloc[j + 5]['close']
    price7 = prices.iloc[j + 6]['close']
    price8 = prices.iloc[j + 7]['close']
    price9 = prices.iloc[j + 8]['close']
    price10 = prices.iloc[j + 9]['close']
    print("The first price is: {} \nThe last price is {}".format(Wei(f"{price1} ether"), Wei(f"{price10} ether")))
    try:
        exchange.massiveLoad(Wei(f"{price1} ether"),
                             Wei(f"{price2} ether"),
                             Wei(f"{price3} ether"),
                             Wei(f"{price4} ether"),
                             Wei(f"{price5} ether"),
                             Wei(f"{price6} ether"),
                             Wei(f"{price7} ether"),
                             Wei(f"{price8} ether"),
                             Wei(f"{price9} ether"),
                             Wei(f"{price10} ether"),
                            {'from' : local_account_admin, 'gas_price': Wei("10 gwei")})
    except Exception as e: 
        print(e)
        continue
    print("Price successfully updated.")
    time.sleep(2)

print("All done, bye bye and good luck!")