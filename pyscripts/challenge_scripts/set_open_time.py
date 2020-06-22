from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount

# Connecting to the network
network_selected = "ropsten"
network.connect(network_selected)

# Loading the metamask account
fss_private_key = "ede4dd8a3584fd7809a5e0bb299ff8f51983af5b1a9f1f506165b5c1f09e22b1"
fss_account = web3.eth.account.from_key(private_key=fss_private_key)
local_account = LocalAccount(fss_account.address, fss_account, fss_account.privateKey)

tk_exchange = Contract.from_abi('', address=, abi=, owner= local_account) #TODO completa il campo!!!!!

tk_exchange.setOpenTime()