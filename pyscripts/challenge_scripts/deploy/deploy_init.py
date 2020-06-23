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

# Deploing and initializing prices
_payCoinAddress = "0xa501cA3B72d8D90235BD8ADb2c67aCc062F451FA"
with open('../blockchain_course_unimi/challenge/teamCST/abi/PayCoin.json') as json_file: 
    pc_abi = json.load(json_file)
pc = Contract.from_abi('PayCoin', address= _payCoinAddress, abi= pc_abi)

print("Deploying our token...")
token = local_account_admin.deploy(token_prj.token_erc20)
print("Token successfully deployed.")
print('\n')
print("Deploying the exchange...")
exchange = local_account_admin.deploy(token_prj.token_exchange, token.address, _payCoinAddress)
print("Exchange succesfully deployed.")
print('\n')
print("Setting exchange priviligies...")
pc.addMinter(exchange.address, {'from': local_account_admin})
time.sleep(2)
pc.addBurner(exchange.address, {'from': local_account_admin})
time.sleep(2)
token.addMinter(exchange.address, {'from': local_account_admin})
time.sleep(2)
token.addBurner(exchange.address, {'from': local_account_admin})
time.sleep(2)

print("Deploying the challenge...")
challenge = local_account_admin.deploy(token_prj.token_challenge, exchange.address, pc.address)
print("Challenge succesfully deployed.")
print('\n')
print("Setting challenge priviligies...")
exchange.addBroker(challenge.address, {'from': local_account_admin})
time.sleep(2)
pc.addMinter(challenge.address, {'from': local_account_admin})
time.sleep(2)
pc.addBurner(challenge.address, {'from': local_account_admin})
time.sleep(2)

print("Deploying the lender...")
lender = local_account_admin.deploy(token_prj.Lender, pc.address)
print("Lender succesfully deployed.")
print('\n')
print("Setting lender priviligies...")
pc.addMinter(lender.address, {'from': local_account_admin})
time.sleep(2)
pc.addBurner(lender.address, {'from': local_account_admin})

print("All done, bye bye and good luck!")

