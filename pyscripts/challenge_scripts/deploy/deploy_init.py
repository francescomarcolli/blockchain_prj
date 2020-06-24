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
fss_trading_private_key = "faba88e53b6fac655f7e0b5cb900e0bc045e787eb850fdf17f458f0fb8607bde"
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

with open('./pyscripts/abi/token_exchange.json') as json_file: 
    exchange_FSS_abi = json.load(json_file)
exchange_FSS = Contract.from_abi('ExchangeFSS', address="0xc9aaE2ADa5a5b650b48465B3C21FE584Bb55e18e", abi= exchange_FSS_abi)
#print("Deploying our token...")
#token = local_account_admin.deploy(token_prj.token_erc20)
#print("Token successfully deployed.")
#print('\n')
#print("Deploying the exchange...")
#exchange = local_account_admin.deploy(token_prj.token_exchange, token.address, _payCoinAddress)
#print("Exchange succesfully deployed.")
#print('\n')
#print("Setting exchange priviligies...")
#pc.addMinter(exchange.address, {'from': local_account_admin})
#time.sleep(2)
#pc.addBurner(exchange.address, {'from': local_account_admin})
#time.sleep(2)
#token.addMinter(exchange.address, {'from': local_account_admin})
#time.sleep(2)
#token.addBurner(exchange.address, {'from': local_account_admin})
#time.sleep(2)

print("Deploying the challenge...")
challenge = local_account_admin.deploy(token_prj.token_challenge, exchange_FSS.address, pc.address)
print("Challenge succesfully deployed.")
print('\n')
print("Setting challenge priviligies...")
exchange_FSS.addBroker(challenge.address, {'from': local_account_admin})
time.sleep(2)
pc.addMinter(challenge.address, {'from': local_account_admin})
time.sleep(2)
pc.addBurner(challenge.address, {'from': local_account_admin})
time.sleep(2)

print("Minting on trading account...")
pc.mint(local_account_trading.address, 50000e18, {'from': local_account_admin})
#print("Deploying the lender...")
#lender = local_account_admin.deploy(token_prj.Lender, pc.address)
#print("Lender succesfully deployed.")
#print('\n')
#print("Setting lender priviligies...")
#pc.addMinter(lender.address, {'from': local_account_admin})
#time.sleep(2)
#pc.addBurner(lender.address, {'from': local_account_admin})

print("All done, bye bye and good luck!")

