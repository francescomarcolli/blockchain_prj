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
exchange = Contract.from_abi('Exchange', address="0xc9aaE2ADa5a5b650b48465B3C21FE584Bb55e18e", abi= exchange_abi)

print("Charging the prices on the exchange...")
prices = pd.read_csv(r'./pyscripts/challenge_scripts/price_history.csv', nrows=8759)
for j in range(0, 8760): 
    price = prices.iloc[j]['close']
    print("The price is: {}".format(Wei(f"{price} ether")))
    exchange.setHistory(Wei(f"{price} ether"), {'from' : local_account_admin})
    print("Price successfully updated.")
    time.sleep(2)

print("All done, bye bye and good luck!")