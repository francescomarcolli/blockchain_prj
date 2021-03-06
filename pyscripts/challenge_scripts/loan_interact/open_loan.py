from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import json, time

network_selected = "ropsten"
network.connect(network_selected)

## Trading account
fss_trading_private_key = "faba88e53b6fac655f7e0b5cb900e0bc045e787eb850fdf17f458f0fb8607bde"
fss_trading_account = web3.eth.account.from_key(private_key=fss_trading_private_key)
local_account_trading = LocalAccount(fss_trading_account.address, fss_trading_account, fss_trading_account.privateKey)
## Admin account
fss_admin_private_key = "ede4dd8a3584fd7809a5e0bb299ff8f51983af5b1a9f1f506165b5c1f09e22b1"
fss_admin_account = web3.eth.account.from_key(private_key=fss_admin_private_key)
local_account_admin = LocalAccount(fss_admin_account.address, fss_admin_account, fss_admin_account.privateKey)


#payCoin = Contract.from_abi('', address=, abi=, owner= local_account)
with open("path_to_abi") as json_file:
    abi = json.load(json_file)
#lender = Contract.from_abi('Lender', address=, abi=, owner= local_account_trading)

#int loan = 0
#lender.openLoan(loan)

