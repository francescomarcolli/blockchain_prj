from brownie import web3, network, Wei, Contract, project
from brownie.network.account import LocalAccount
import json, time

network_selected = "ropsten"
network.connect(network_selected)

# Loading the metamask account
fss_private_key = "E45161BD0BACE1E6F28B28BF49A96A5F4D81D133D09A6E3E18674422D9FD47C4"
fss_account = web3.eth.account.from_key(private_key=fss_private_key)
local_account = LocalAccount(fss_account.address, fss_account, fss_account.privateKey)


#payCoin = Contract.from_abi('', address=, abi=, owner= local_account)
with open("path_to_abi") as json_file:
    abi = json.load(json_file)
lender = Contract.from_abi('Lender', address=, abi=, owner= local_account)

int loan = 0


lender.openLoan(loan)

